from inspect import getgeneratorstate


def nm(func):
    def inner(*args):
        print(f"The result is {func(*args)}")
    return inner


@nm
def add_a(a, b):
    return (a * b) ** b


def get_avarager():
    total = 0
    count = 0
    avarager = None
    while True:
        term = yield avarager
        total += term
        count += 1
        avarager = total / count


if __name__ == '__main__':
    add_a(6, 21)
    target = get_avarager()
    next(target)
    print(target.send(10))
    print(target.send(11))
    print(target.send(100))
    target.close()
    print(getgeneratorstate(target))