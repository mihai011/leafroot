# pylint: disable-all
def star(*args_start, **kargs_start):
    def wrapper(func):
        def inner(*args, **kwargs):
            print(args_start * 1)
            func(*args, **kwargs)
            print(args_start * 1)

        return inner

    return wrapper


def percent(*args_percent, **kargs_percent):
    def wrapper(func):
        def inner(*args, **kwargs):
            print(args_percent * 1)
            func(*args, **kwargs)
            print(args_percent * 1)

        return inner

    return wrapper


@star("test1")
@percent("test2")
def printer(msg):
    print(msg)


printer("Hello")


# this translates too
def printer(msg):
    print(msg)


star("test1")(percent("test2")(lambda x: print(x)))(100)
