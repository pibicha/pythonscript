# -*- coding: utf-8 -*-
from __future__ import print_function

"""
参考 http://code.activestate.com/recipes/131499-observer-pattern/
观察者模式：
需要三个角色：主题、内容、观察者
1，主题：绑定观察者，通知观察者
2，内容：主题的延伸/子类，当内容改变时，调用主题的通知方法
3，观察者：当主题的内容变化时，实现自身的监听策略；
在spring自身提供的观察者模式中，往往只需要实现观察者的监听策略即可
"""


class Dashboard(object):
    def __init__(self):
        self.__obsersers = []

    def attach(self, observer):
        if observer not in self.__obsersers:
            self.__obsersers.append(observer)

    def detach(self, observer):
        self.__obsersers.remove(observer)

    def notify(self, modifier=None):
        for observer in self.__obsersers:
            if observer != modifier:
                observer.update(self)  # 观察者需要根据主题中的内容变化时，做出自己的调整


class Province(Dashboard):
    def __init__(self, name=''):
        Dashboard.__init__(self)  # 这里得显示调用父类构造器，和java还不一样
        self.name = name
        # self._content = ''python属性定义很灵活，不一定要在init方法中申明，不过在这申明比较规范

    @property
    def content(self):
        # return self.content
        return self._content

    @content.setter
    def content(self, content):
        # self.content = content 属性名一定不要和方法名一样，，否则会认为将方法引用赋值属性，，同时这里又会调用方法，形成递归
        self._content = content
        # 当内容有变时，需要调用notify
        self.notify()


class Storm:
    def update(self, dashboard):
        print("{0}今天雷转{1}".format(dashboard.name, dashboard.content))


class Sunny:
    def update(self, dashboard):
        print("{0}今天晴转{1}".format(dashboard.name, dashboard.content))


if __name__ == '__main__':
    c1 = Province('北京')
    c2 = Province('上海')

    storm = Storm()
    sunny = Sunny()

    c1.attach(storm)
    c2.attach(sunny)

    c1.content = '多云'
    c2.content = '阵雨'
