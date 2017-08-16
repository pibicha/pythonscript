# -*- coding: utf-8 -*-
# 参考 http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

"""Implementation of the abstract factory pattern"""
import six
import abc
import random


@six.add_metaclass(abc.ABCMeta)  # 申明如java中的抽闲类一般，同时可以被子类以minIn的形式继承
class People(object):
    @classmethod  # 类似java中的静态方法，只属于当前类，子类不可继承；且所属类可直接调用
    def from_name(cls, name):
        for sub_cls in cls.__subclasses__():
            if name == sub_cls.__name__.lower():
                return sub_cls()

    @abc.abstractmethod  # 同java中的抽象方法
    def speak(self):
        """"""


class Farmer(People):
    def speak(self):  # 重写父类的speak方法
        return "I'm a farmer"


class Fisher(People):
    def speak(self):
        return "I'm a fisher"


if __name__ == '__main__':
    for name in ['farmer', 'fisher']:
        people = People.from_name(name)
        print "{} say: {}".format(name, people.speak())
