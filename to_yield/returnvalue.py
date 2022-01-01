from collections import namedtuple
from decorate import decoration


Result = namedtuple("result", ['count', 'average'])


@decoration
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


if __name__ == '__main__':
    target = averages()
    print(target.send(10))
    target.send(20)
    try:
        target.send(None)
    except StopIteration as e:
        print(e.value.average, e.args)
