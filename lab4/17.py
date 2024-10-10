def generation(N):
    for число in range(N):
        yield число ** 2

for квадрат in generation(10):
    print(квадрат)

