from inspect import getgeneratorstate


def simple_corout():
    print('-> started')
    x = yield
    print(f'-> ended and value of x is {x}')


if __name__ == '__main__':
    target = simple_corout()
    print(target)
    print(getgeneratorstate(target))
    # 激活协程，必须得先激活协程
    next(target)
    print(getgeneratorstate(target))
    try:
        target.send("Hello, to yield")
    except StopIteration:
        print('Get an error')
    finally:
        print(getgeneratorstate(target))