# -*- coding: utf-8 -*-
"""
多个实例，使用同一个状态
python类中的__dict__，是类属性， 同时是保存了所有实例信息的变量，
通过在基类中设置私有属性__shared_state；并在构造器中将其赋值给
类变量__dict__；
所以每次创建Borg的实例时，其__init__类属性都会被置为空，而在新的
实例和以前的实例，都会共享新的属性
"""
# 参考 http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

class Borg(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = 'Init'

    def __str__(self):
        return self.state


class YourBorg(Borg):
    pass


if __name__ == '__main__':
    rm1 = Borg()
    rm2 = Borg()

    rm1.state = 'Idle'
    rm2.state = 'Running'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    rm2.state = 'Zombie'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    print('rm1 id: {0}'.format(id(rm1)))
    print('rm2 id: {0}'.format(id(rm2)))

    rm3 = YourBorg()  # 子类由于继承不到父类的私有属性，但是会调用父类的构造器，所以输出“Init”

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))
    print('rm3: {0}'.format(rm3))
