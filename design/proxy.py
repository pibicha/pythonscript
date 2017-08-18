# -*- coding: utf-8 -*-
# 参考 https://github.com/faif/python-patterns/blob/master/structural/proxy.py
"""
代理模式和装饰模式的区别：装饰者是将被装饰对象在自身构造器中注入，
而代理模式则是在属性中持有被代理的实例！！
不过python中可以通过注解方式实习装饰器模式
"""
import time


class SalesManager:
    def talk(self):
        print("Sales Manager ready to talk")


class Proxy:
    def __init__(self):
        self.busy = 'No'
        self.sales = None

    def talk(self):
        print("Proxy checking for Sales Manager availability")
        if self.busy == 'No':
            self.sales = SalesManager()
            time.sleep(2)
            self.sales.talk()
            time.sleep(2)
        else:
            time.sleep(2)
            print("Sales Manager is busy")
            time.sleep(2)


if __name__ == '__main__':
    p = Proxy()
    p.talk()
    p.busy = 'Yes'
    p.talk()
