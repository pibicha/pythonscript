# -*- coding: utf-8 -*-
"""
实现懒加载，方式一不太好看 ，参考 https://github.com/faif/python-patterns/blob/master/creational/lazy_evaluation.py

该方式实现懒加载的原理，主要是通过python的动态性质；在对象创建后，为其绑定一个属性~！从而实现懒加载


"""
from __future__ import print_function


def lazy_property(fn):
    attr = '_lazy__' + fn.__name__

    @property  # 属性装饰器
    def _lazy_property(self):  # 此处的self为什么是Person的实例？？？ 个人猜测是因为lazy_property作为注解被Person实例调用，所以self会一路传入到这
        if not hasattr(self, attr):
            setattr(self, attr, fn(self))
        return getattr(self, attr)

    return _lazy_property


class Person(object):
    def __init__(self, name, occupation):
        self.name = name
        self.occupation = occupation
        self.call_count2 = 0

    @lazy_property
    def relatives(self):
        # Get all relatives, let's assume that it costs much time.
        relatives = "Many relatives."
        return relatives


def lazy_property2(fn):
    methodname = '_lazy__' + fn.__name__

    @property
    def say(self):
        if not hasattr(self, methodname):
            setattr(self, methodname, fn(self))
        return getattr(self, methodname)

    return say


class Animal(object):
    def __init__(self, sort):
        self.sort = sort

    @lazy_property2
    def say(self):
        return 'kkkkkk'


if __name__ == '__main__':
    Jhon = Person('Jhon', 'Coder')
    print(u"Name: {0}    Occupation: {1}".format(Jhon.name, Jhon.occupation))
    print(u"Before we access `relatives`:")
    print(Jhon.__dict__)
    print(u"Jhon's relatives: {0}".format(Jhon.relatives))
    print(u"After we've accessed `relatives`:")
    print(Jhon.__dict__)

    print("===============================================================================================")
    DaloDuck = Animal('duck')
    print("Name : {0}".format(DaloDuck.sort))
    print(u"Before we access `say`:")
    print(DaloDuck.__dict__)
    print(u"DaloDuck say: {0}".format(DaloDuck.say))
    print(u"After we've accessed `say`:")
    print(DaloDuck.__dict__)
