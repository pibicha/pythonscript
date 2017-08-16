# -*- coding: utf-8 -*-
# https://github.com/faif/python-patterns/blob/master/structural/adapter.py
"""
python的适配器模式实现，主要是依靠类变量__dict__；
1， Adapter的构造器中，传入待适配对象及其待适配方法；
2， 将适配器的类属性__dict__更新为带适配方法即可
"""
class Dog(object):
    def __init__(self):
        self.name = "Dog"

    def bark(self):
        return "woof!"


class Cat(object):
    def __init__(self):
        self.name = "Cat"

    def meow(self):
        return "meow!"


class Human(object):
    def __init__(self):
        self.name = "Human"

    def speak(self):
        return "'hello'"


class Car(object):
    def __init__(self):
        self.name = "Car"

    def make_noise(self, octane_level):
        return "vroom{0}".format("!" * octane_level)


class Adapter(object):
    def __init__(self, obj, **adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)  # 将传入的实例属性作为适配器实例的属性

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

    def original_dict(self):
        """Print original object dict"""
        return self.obj.__dict__


def main():
    objects = []
    dog = Dog()
    print(dog.__dict__)
    objects.append(Adapter(dog, say=dog.bark))
    print(objects[0].__dict__)
    print(objects[0].original_dict())
    cat = Cat()
    objects.append(Adapter(cat, say=cat.meow))
    human = Human()
    objects.append(Adapter(human, say=human.speak))
    car = Car()
    objects.append(Adapter(car, say=lambda: car.make_noise(3)))

    for obj in objects:
        print("A {0} goes {1}".format(obj.name, obj.say()))


if __name__ == "__main__":
    main()
