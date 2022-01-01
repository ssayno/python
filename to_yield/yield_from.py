from collections import namedtuple
from decorate import decoration
from random import randint, uniform
from inspect import getgeneratorstate

Result = namedtuple("Result", ['count', 'average'])


def averages():
    total = 0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


# 委派生成器
@decoration
def grouper(results, key):
    while True:
        results[key] = yield from averages()


# 客户端代码
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        for value in values:
            group.send(value)
        group.send(None)
        print(getgeneratorstate(group))
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        sex, unit = key.split(';')
        print(f"{result.count} {sex}, average {result.average:.2f}{unit}")


data = {
    'girls;kg':
        [randint(40, 52) for i in range(10)],
    'girls;m':
    [uniform(1.5, 1.6) for i in range(9)],
    'boys;kg':
        [randint(50, 62) for i in range(10)],
    'boys;m':
    [uniform(1.6, 1.7) for i in range(9)],
}


if __name__ == '__main__':
    main(data)