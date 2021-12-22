#!/usr/bin/env python3
from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=" ")
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    display("Script starting")
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, [10, 1, 2, 4])
    display("the type of results", type(results))
    display("Waiting for individual results：")
    for i, result in enumerate(results):
        display(f"result {i}: {result}")


if __name__ == '__main__':
    main()
