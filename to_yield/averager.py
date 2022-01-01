from inspect import getgeneratorstate
from decorate import decoration


def nm(func):
    def inner(*args):
        print(f"The result is {func(*args)}")
    return inner


@nm
def add_value(a, b):
    """

    :type b: object
    """
    return (a * b) ** b


@decoration
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
    add_value(6, 10)
    target = get_avarager()
    print(target.send(10))
    print(target.send(11))
    print(target.send(100))
    target.close()
    print(getgeneratorstate(target))