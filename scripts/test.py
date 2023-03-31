# pylint: disable-all
class Foo:
    def __init__(self, x):
        self.x = x

    def test(self):
        return "Foo: {}".format(self.x)


class Bar:
    def __init__(self, x):
        self.x = x

    def test(self):
        return "Bar: {}".format(self.x)


class Foobar(Foo, Bar):
    pass


obj = Foobar(10)
print(obj.test())


def test(n, x=[]):
    x.extend(range(n))
    return x


a = test(2)
b = test(3)
print(b)
