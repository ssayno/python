from inspect import getgeneratorstate


def simple_mul(a):
    print(f'-> value of a is {a}')
    b = yield a
    print(f'-> the value of b is {b}')
    c = yield a + b
    print(f'-> the value of c is {c}')


if __name__ == '__main__':
    target = simple_mul(10)
    print(getgeneratorstate(target))
    print(next(target))
    print(target.send(22))
    try:
        print(target.send(30))
    except StopIteration:
        print('Get an error')
    print(None)
    print(Ellipsis)