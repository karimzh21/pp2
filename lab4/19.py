def генерировать_числа(n):
    for число in range(n + 1):
        if число % 3 == 0 and число % 4 == 0:
            yield число

n = int(input("Введите число n: "))
for число in генерировать_числа(n):
    print(число)

