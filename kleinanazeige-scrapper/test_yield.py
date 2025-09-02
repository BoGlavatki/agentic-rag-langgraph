def my_generator(x=1):
    while True:
        yield x
        x += 1


gen = my_generator()
print(next(gen))
print(next(gen))
print(next(gen))
