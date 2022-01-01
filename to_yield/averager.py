from inspect import getgeneratorstate


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
    target = get_avarager()
    next(target)
    print(target.send(10))
    print(target.send(11))
    print(target.send(100))
    target.close()
    print(getgeneratorstate(target))