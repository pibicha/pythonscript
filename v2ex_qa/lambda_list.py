# -*-coding:utf-8-*-
"""
free variable capture 问题：当在闭包中使用包外的变量时，该变量的值只会是最终值
参考：https://www.v2ex.com/t/380331#reply10
"""


def count():
    fs = []
    for i in range(0, 4):
        def f(x):
            return x * i  # 闭包中使用了外部的局部变量，并且这一步只有count实例调用f方法时才会执行！

        fs.append(f)
    return fs


# 该方法同count方法，lambda中使用了包外变量，并且匿名对象的方法不是立即执行！
# 执行顺序：
# for 右边先执行，
# for 左右创建匿名对象，注意只是创建匿名对象！并没有调用！也就是还没有执行x*i!!!

def mul():
    return [lambda x: x * i for i in range(4)]


def mul_ex():
    return (lambda x: x * i for i in range(4))


if __name__ == "__main__":
    print [m(2) for m in count()]
    print [m(2) for m in mul()]

    print [m(2) for m in mul_ex()]
