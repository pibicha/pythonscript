# -*-coding:utf-8-*-
"""
free variable capture 问题：当在闭包中使用包外的变量时，该变量的值只会是最终值
参考：https://www.v2ex.com/t/380331#reply10
"""


def count():
    fs = []
    for i in range(0, 4):
        def f(x):
            return x * i  # 闭包中使用了外部的局部变量

        fs.append(f)
    return fs


def mul():  # 该方法同count方法，lambda中使用了包外变量，而不是立即执行！ 执行顺序，i的赋值早于lambda，而lambda不会立刻执行(参考count方法)，所以造成free variable capture
    return [lambda x: x * i for i in range(4)]


def mul_ex():
    return (lambda x: x * i for i in range(4))


if __name__ == "__main__":
    print [m(2) for m in count()]
    print [m(2) for m in mul()]

    print [m(2) for m in mul_ex()]
