#!/usr/bin/env python2
# -*- coding: utf-8 -*-
############################################
'''
Created on 2017年3月20日

@author: xgb99
'''
#functional programming
#
#函数式编程 抽象 数学意义上的计算
#汇编 低级语言 
#如：
#def add(x, y, f):
#    return f(x) + f(y)
#
#add(-5, 6, abs)

def f(x):
    # 高阶函数
    # 
    # map()函数接收两个参数，一个是函数，一个是Iterable
    # 把结果作为新的Iterator返回
    return x * x
    #r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    #print(list(r))

from functools import reduce
def f_1(x, y):
    # 高阶函数
    #reduce()函数接收两个参数，一个是函数，一个是Iterable
    #reduce把结果继续和序列的下一个元素做累积计算
    return x * 10 + y
    #reduce(f_1, [1, 3, 5, 7])
    #等价于
    #f(f(f(1, 3), 5), 7)

def is_odd(n):
    # 高阶函数
    ##filter()函数用于过滤序列
    #filter()也接收一个函数和一个序列 返回Iterator
    #筛选函数 返回boolean
    return n % 2 == 1
    #r = filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])
    #list(r)

def tosorted():
    # 高阶函数
    #sort 传入序列 和 key=函数
    sorted([36, 5, -12, 9, -21], key=abs)
    sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)


def lazy_sum(*args):
    #返回函数,函数并没有立即执行
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
    #f = lazy_sum(1, 3, 5, 7, 9)
    #f
    #print(f())

#函数并没有立即执行的结果
def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i*i #使用的局部变量，在最后i=3才真正被执行
        fs.append(f)
    return fs
    #f1, f2, f3 = count()
    #f1();f2();f3()

def lam():
    f = lambda x: x * x#匿名函数
    print(f(5))
    
#装饰器
#假设我们要增强 函数的功能,
#但又不希望修改 函数的定义，
#这种在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）。
#定义Decorator
#方式一
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log   #借助Python的@语法，把decorator置于函数的定义处：    
def now():
    print('2015-3-25')
    #now()#执行
###########

#方式二
def log_1(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

def now_1():
    print('2015-3-25')
    #now_1 = log_1(now_1)#传入函数
    #now_1()
########

#####带参数 方式一
def log_2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now_2():
    print('2015-3-25')
    #now_2() 
###########
    
####带参数 方式二
def log_3(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper

def now_3():
    print('2015-3-25')
    #now_3 = log_3('execute')(now_3)#此处第一层传入参数 第二层传入函数参数
###########

#偏函数  用decorator也能实现， 起到的是不修改定义而增加一种默认参数的作用 类似override重载
import functools
def parfunc():
    int2 = functools.partial(int, base=2)#base=不能省略
    print(int2('1000000'))
    
    
if __name__ == '__main__':
    pass

