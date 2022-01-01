from collections import namedtuple


Result = namedtuple('Result', 'count average')
a = Result(1, 2)
for i in a:
    print(i)
print(a.count, a.average)