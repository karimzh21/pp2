def числа_делящиеся_на_3_и_4(n):
    for число in range(n + 1):
        if число % 3 == 0 and число % 4 == 0:
            yield число

n = int(input("Введите число n: "))

for число in числа_делящиеся_на_3_и_4(n):
    print(число)
