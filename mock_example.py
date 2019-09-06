import unittest
from unittest import mock


tp = 'test passed'
tf = 'test failed'
def func1(x):
    return x**2


def func2(x):
    return func1(x) + x*5

# 原来的unittest
# 假设我们想测试func2的功能，但是func2依赖func1


class ExampleTest(unittest.TestCase):
    """Test example
    """
    def test_func2(self):
        self.assertEqual(func2(5), 50)
        self.assertEqual(func2(-5), 1)


# 使用mock就可以让func1的更改不影响func2
# 甚至可以在func1改好之前就测试func2，只需要知道func1的返回结果

class ExampleTest2(unittest.TestCase):
    """Test example for mocking
    """
    @mock.patch('__main__.func1')
    def test_func2(self, mock_func1):
        mock_func1.return_value = 25
        self.assertEqual(func2(5), 50)
        mock_func1.return_value = 26
        self.assertEqual(func2(-5), 1)


t = ExampleTest()
t2 = ExampleTest2()
try:
    t.test_func2()
except AssertionError as e:
    print(e, tf)

try:
    t2.test_func2()
except AssertionError as e:
    print(e, tf)


# mock一些__call__属性，包括return value，多次return不同结果， return Exception
fake_class = mock.MagicMock()
fake_class.return_value = 1
print(fake_class, fake_class())
fake_class.side_effect = [1, 2, 3, Exception('Haha')]
print([fake_class() for _ in range(3)])
try:
    fake_class()
except Exception as e:
    print(e)


# mock一些方法和类属性
fake_class.fake_method.return_value = 1
print(fake_class.fake_method,
      fake_class.fake_method(1),
      fake_class.fake_method('string'),
      fake_class.fake_method(1, 2, 3))
fake_class.fake_attr = 'test attri'
print(fake_class.fake_attr,
      fake_class.fake_method(fake_class.fake_attr))

# 被mock的方法的自带属性和关键字： called, call_count,
#                             assert_called_with, 
#                             call_args, call_args_list
print('fake_class.fake_method called: {}\n'.format(fake_class.fake_method.called),
      'this method has been called {} times\n'.format(fake_class.fake_method.call_count))

try:
    fake_class.fake_method.assert_called_with(1)
except Exception as e:
    print(e)

fake_class.fake_method.assert_called_with('test attri')
print(fake_class.fake_method.call_args_list)
print(fake_class.call_args_list)

fake_class.fake_method.reset_mock()
print(fake_class.fake_method.call_args_list)
print(fake_class.call_args_list)

fake_func = lambda x: len(x)
fake_class.fake_func = fake_func
print(fake_class.fake_func([1, 3, 4]))

# patch的具体用法
'''
@mock.patch('module_name.SomeClassName.some_method_name')

用假的方法或者类来代替需要代替的类
class test_whatever():
    def __init__(self):
        pass

    @mock.patch('example.func2')
    @mock.patch('example.func1')
        def test_func3(self, mock_func1, mock_func2):
'''
