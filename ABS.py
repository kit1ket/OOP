import math

def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def norm(x, bounds):
    if x < bounds[0]:
        return bounds[0]
    elif x > bounds[1]:
        return bounds[1]
    else:
        return x

dt = 0.5
on = 1

# Контроллер АБС
# s - коэффициент скольжения
# v - скорость автомобиля, м/с
# next_k - возвращает коэффициент гидравлики тормозов
# is_active - возвращает True, если АБС функционирует
# Возвращает тормозной момент, Н*м
#максимальное значение кэф трения достигается только при проскальзывании в 20% поэтому 0.2 
def controller(prev_Tb, s, v, next_k, is_active, Tb_max, dt = dt):
    if not is_active(v):
        s = 0
    s_sign = sign(0.2 - s)
    Tb = prev_Tb + s_sign * next_k() / (1 + dt * s)
    return norm(Tb, (0, Tb_max))

# Считает коэффициент скольжения
# vw - предполагаемая угловая скорость колеса автомобиля, рад/с
# next_ww - считает фактическую угловую скорость колеса, рад/с
# eps - какое-то маленькое число, чтобы случайно не поделить на ноль
def slip(vw, next_ww, eps):
    return norm((1 - (next_ww() / (vw + (vw == 0) * eps))), (0, 1))

# Считает угловую скорость колеса, рад/с
# Ff - сила трения, Н
# Tb - крутящий момент торможения, Н*м
# dt - время моделирования, c
def wheel(prev_ww, Tb, Ff, rw, Jw):
    return norm(prev_ww - (Tb - rw * Ff) * Jw, (0, 1000))

# Считает 
# - силу трения, Н
# - скорость автомобиля, м/с
# next_mu - возвращает текущий коэффициент трения с дорогой
# mv - масса автомобиля, кг
# dt - время моделирования, с
# wheel_count - количество колёс
# g - ускорение свободного падения, м/с^2
def vehicle(prev_v, next_mu, mv, dt = dt, wheel_count = 4, g = 9.81):
    mpw = mv / wheel_count # масса на одно колесо
    mu = next_mu()
    Ff = mu * mpw * g
    return Ff, norm(prev_v - Ff * (1 / mpw) * dt, (0, 1000))

# Считает коэффициент трения с дорогой
# s - коэффициент скольжения
# cfs - список из 4 коэффицентов определения силы трения, которые зависят от покрытия дороги
def friction(s, cfs):
    s *= 100
    mu = cfs[0] * (cfs[1] * (1 - math.exp(-cfs[2] * s)) - cfs[3] * s)
    return norm(mu, (0, 1))

# Характеристики автомобиля
weight = 1200 # кг - масса автомобиля
radius_wheel = 0.28 # м - радиус колеса
inertia_wheel = 0.01 # кг*м^2 - инерция колес

# Конфигуация АБС
min_speed = 1.4 # м/с - минимальная скорость работы АБС

# init_s - начальный коэффициент скольжения
# init_v - начальная скорость, м/с
# controller - контроллер АБС
# next_s_and_v - возвращает следующие коэффициенты скольжения и скорость
# next_k - возвращает коэффициент усиления тормозной системы
# Tb_max - максимальный крутящий момент торможения
# v_min - скорость, ниже которой АБС не будет работать, м/с
# dt - время цикла моделирования, с
def anti_lock_braking_system(init_s, init_v, controller, next_s_and_v, next_k, Tb_max, dt = dt):
    time = 0
    s = init_s
    v = init_v
    Tb = Tb_max
    while (v > 0):
        time += dt
        Tb = controller(Tb, s, v, next_k, lambda v: on and v > min_speed, Tb_max, dt)
        print("t=", time, "s")
        print("v=", v, " m/s")
        print("s=", s)
        print("Tb=", Tb)
        s, v = next_s_and_v(s, v, Tb)
        print("-------------")

eps = 1e-12 # Малое значение, чтобы избежать деления на ноль
Tb_max = 2000
init_v = 28
w0 = init_v / radius_wheel

cfs_for_beton = (0.7, 1.07, 0.5, 0.003)
cfs_for_ice = (0.1, 1.07, 0.38, 0.007)

def next_s_and_v(prev_s, prev_v, Tb):
    Ff, v = vehicle(prev_v, lambda: friction(prev_s, cfs_for_ice), weight, dt, 4)

    prev_ww = (1 - prev_s) * (prev_v / radius_wheel)
    ww = wheel(prev_ww, Tb, Ff, radius_wheel, inertia_wheel)
    print("ww=", ww)
    print("vw=", v / radius_wheel)
    s = slip(v / radius_wheel, lambda: ww, eps)
    return s, v

anti_lock_braking_system(slip(w0, lambda: w0, eps), init_v, controller, next_s_and_v, lambda: 1000, Tb_max, dt)