from functools import reduce

def f(x):
    return 3*x**2+1

a = -10  # Нижний предел интегрирования
b = 10  # Верхний предел интегрирования
dx = 0.5
n = int((b - a)/dx)  # Количество разбиений

x = [a + i*dx + dx/2 for i in range(n+1)]  # Массив значений x на интервале [a, b]

# Метод прямоугольников для вычисления интеграла
integral = reduce(lambda s, i: s + f(x[i])*dx, range(n), 0)

print(integral)