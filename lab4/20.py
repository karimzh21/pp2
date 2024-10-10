def squares(a, b):
    for число in range(a, b + 1):
        yield число ** 2

a = int(input("Введите число a: "))
b = int(input("Введите число b: "))

for квадрат in squares(a, b):
    print(квадрат)





