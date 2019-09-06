from functools import wraps


class father:
    x = 1
    def __init__(self, y, z):
        self.y = y
        self.z = z


class child(father):
    x = 1
    def __init__(self, y, z):
        super().__init__(y, z)
        self.w = self.y + self.z


# print(dir(father(1, 2)))
# print(dir(child(1, 2)))


class meta(type):
    xx = 1
    def __new__(cls, name, base, attri):
        print('call __new__ when write a new class created')
        print(cls)  # <class '__main__.meta'>
        attri['xx'] = 1
        _cls = super().__new__(cls, name, base, attri)
        print(_cls)  # <class '__main__.child2'>

        print(dir(cls))
        setattr(_cls, '__init__', meta.__new__init__(getattr(_cls, '__init__', None)))
        print(dir(_cls))
        return _cls

    def __call__(cls, *args, **kwargs):
        print('call __call__ when creating the instance')
        print(dir(cls))  # 这里和33行执行完__new__方法一样
        print(*args)  #  这里是 1， 2
        kwargs['xyz'] = 2
        return super().__call__(cls, *args, **kwargs)


    @staticmethod
    def __new__init__(func):
        @wraps(func)
        def new_func(self, *args, **kwargs):
            self.any = 'any'
            f = func(self, *args, **kwargs)
            return f
        return new_func


# metaclass可以理解成构造类的时候讲x=1，"__init__": 作为参数传到meta类中进行构造
# 因此下面这个类__init__真实的代码应该是
# self.any = 'any'
# self.x = x
# self.y = y
class child2(metaclass=meta):
    x = 1
    def __init__(self, x, y, *args, **kwargs):
        self.x = x
        self.y = y
        self.kwargs = kwargs


print(dir(child2(1, 2)))
