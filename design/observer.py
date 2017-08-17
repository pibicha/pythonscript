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
        Dashboard.__init__(self)
        self.name = name
        self._content = ''

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content
        # 当内容有变时，需要调用notify
        self.notify()


class Storm:
    def update(self, dashboard):
        print("{0}今天雷转{1}".format(dashboard.name, dashboard.content))  # 在这一步，如果是在java中，会找不到content属性，但由于


class Sunny:
    def update(self, dashboard):
        print("{0}今天晴转{0}".format(dashboard.name, dashboard.content))


if __name__ == '__main__':
    c1 = Province('北京')
    c2 = Province('上海')

    storm = Storm()
    sunny = Sunny()

    c1.attach(storm)
    c2.attach(sunny)

    c1.content = '多云'
    c2.content = '阵雨'
