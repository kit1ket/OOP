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


#--------------------------------------------------------------------------------------------

on = 1 # 1 - АБС включён, 0 - выкл.

# Конфигуация АБС
min_speed = 1 # Ниже этой скорости АБС не работает
Tb_max = 2000

# Функция-генератор
def anti_lock_braking_system(get_v, get_ww, calc_vw, calc_slip, controller):
    Tb = 0 # Tb - крутящий момент торможения, Н*м

    v = get_v()

    while (v > 0):
        s = 0 if not on or v < min_speed else calc_slip(get_ww(), calc_vw(v))
        Tb = controller(s, lambda dTb: Tb + dTb)
        yield Tb
        v = get_v()

def get_calc(calc_slip, calc_mu, calc_Ff, calc_v, calc_ww):
    def calc(prev_v, prev_ww, Tb, dt):
        s = calc_slip(prev_ww, prev_v / radius_wheel)
        mu = calc_mu(s)
        Ff = calc_Ff(mu)
        v = calc_v(Ff, lambda dv: prev_v + dv * dt)
        ww = calc_ww(Tb, Ff, lambda dw: prev_ww + dw * dt)
        return v, ww
    return calc

# Характеристики автомобиля
weight = 1000
radius_wheel = 0.28
inertia_wheel = 0.01

# Коэффициенты дорожных покрытий
road_cfs = ((0.9, 1.07, 0.2773, 0.0026), (0.7, 1.07, 0.5, 0.003), (0.7, 1.07, 0.1773, 0.006), (0.1, 1.07, 0.38, 0.007))

def calc_mu(road_type, slip):
    cfs = road_cfs[road_type]
    slip *= 100
    return norm(cfs[0] * (cfs[1] * (1 - math.exp(-cfs[2] * slip)) - cfs[3] * slip), (0, 1))


def calc_v(Ff, apply_dv):
    return norm(apply_dv(-Ff / weight), (0, 1000))

#сила трения
def calc_Ff(mu):
    return mu * weight / 4 * 9.81

def calc_ww(Tb, Ff, apply_dw):
    return norm(apply_dw(-(Tb - Ff * radius_wheel) * inertia_wheel), (0, 1000))

def calc_slip(ww, vw):
     return norm(1 - (ww / (vw + (vw == 0) * 1e-12)), (0, 1))

def controller(s, k, calc_final_Tb, dt):
    s_sign = sign(0.2 - s)
    dTb = (s_sign * k) / (1 + s * dt)
    return norm(calc_final_Tb(dTb * dt), (0, Tb_max))
    
# Сила нажатия водитель на педаль тормоза теперь зависит от времени
def k(t):
    return 1000 + norm(t, (0, 5)) / 5 * 1000

# Тип дороги меняется от дистанции
def get_road_type(distance):
    return 3 if distance in range(20, 40) else 2

dt = 0.1

time = 0
distance = 0

v = 14
ww = v / radius_wheel #угловая скорость колеса

calc_mu_for_road = lambda s: calc_mu(get_road_type(distance), s)
calc = get_calc(calc_slip, calc_mu_for_road, calc_Ff, calc_v, calc_ww)

abs_generator = anti_lock_braking_system(
    lambda: v, 
    lambda: ww, 
    lambda v: v / radius_wheel,
    calc_slip,
    lambda s, calc_final_Tb: controller(s, k(time), calc_final_Tb, dt))

print('{:>7}{:>16}{:>16}{:>16}{:>16}{:>16}{:>16}'.format("time, s", "distance, m", "velocity, m/s", "vw, rad/s", "ww, rad/s", "slip", "Tb, N*m"))
print(f"{time:>7.2f}{distance:>16.2f}{v:>16.4f}{v / radius_wheel:>16.2f}{ww:>16.2f}{calc_slip(ww, v / radius_wheel):>16.2f}{0:>16.2f}")

for Tb in abs_generator:
    v, ww = calc(v, ww, Tb, dt)
    distance += v * dt
    time += dt
    print(f"{time:>7.2f}{distance:>16.2f}{v:>16.4f}{v / radius_wheel:>16.2f}{ww:>16.2f}{calc_slip(ww, v / radius_wheel):>16.2f}{Tb:>16.2f}")