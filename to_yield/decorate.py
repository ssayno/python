from functools import wraps


def decoration(func):
    @wraps(func)
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        # 激活协程函数
        next(gen)
        return gen
    return inner