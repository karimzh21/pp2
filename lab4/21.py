def countdown(n):
    for число in range(n, -1, -1):
        yield число

n = int(input("Введите число n: "))

for число in countdown(n):
    print(число)
