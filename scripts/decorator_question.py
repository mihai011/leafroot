from functools import wraps


def log(*largs, **lkwargs):
    def wrapper(func):
        def inner(*args, **kwargs):
            print("log")
            return func(*args, **kwargs)

        return inner

    return wrapper


def dec(*dargs, **dkwargs):
    def wrapper(func):
        def inner(*args, **kwargs):
            print("dec")
            return func(*args, **kwargs)

        return inner

    return wrapper


@log()
@dec()
def test():
    print("test")


test()
