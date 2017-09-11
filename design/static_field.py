# -*- coding: utf-8 -*-
"""
属性单例：
1，__dict__属性：同一个类的所有实例都会有该字典属性，它记录了
属性名和属性值；同时它是一个类属性；
2，在类的构造器中，将__dict__属性设置为实例属性，每次在创建
Borg实例时，Borg的__dict__的都被变成实例的__shared_state，使得
所有实例可以共享同一个dict
"""


# 参考 http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

class Borg(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = 'Init'

    def __str__(self):
        return self.state  # 这一步的隐含操作是 __dict__.get('state')


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
