#!/usr/bin/env python2
# -*- coding: utf-8 -*-
############################################
'''
Created on 2017年3月20日

@author: xgb99
'''
#函数 
#官方文档  https://docs.python.org/3/library/functions.html#
def func1():
    #函数名赋给变量
    #定义函数 如果没有return语句 返回None 
    a = abs
    print(a(-1))

def my_abs(x):
    #包含参数类型检查
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
    

def enroll(name, gender, age=6, city='Beijing'):
    #默认参数
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

def add_end(L=[]):
    #定义默认参数要牢记一点：默认参数必须指向不变对象！ 否则会出错
    L.append('END')
    return L

def calc(numbers):
    #参数
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
    #calc([1, 2, 3]) #数组
    #calc((1, 3, 5, 7)) #tuple

def calc_1(*numbers):
    #定义可变参数 则可以不用组成list 或者 tuple
    #在函数调用时候自动组装成tuple
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
    #calc_1(1, 2)
    #calc_1()
    #nums = [1, 2, 3]
    #calc_1(nums[0], nums[1], nums[2])
    #print(calc_1(*nums))

def person(name, age, **kw):
    #关键字参数
    #关键字参数在函数内部自动组装为一个dict
    if 'city' in kw:
        # 假如有city参数
        pass#空函数
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)
    #person('Michael', 30)#只传入必选参数
    #person('Bob', 35, city='Beijing')#传入一个关键字参数
    #person('Adam', 45, gender='M', job='Engineer')#两个
    #extra = {'city': 'Beijing', 'job': 'Engineer'}
    #person('Jack', 24, **extra)
    #person('Jack', 24, city=extra['city'], job=extra['job'])#一个dict
    

#python3
#def person_1(name, age, * , city='Beijing', job):
    #print(name, age, city, job)
    #命名关键字参数
    #命名关键字参数必须传入参数名
    #*后面的参数被视为命名关键字参数
    #person_1('Jack', 24, city='Beijing', job='Engineer') #指定dict的key

#python3
#def person_2(name, age, *args, city, job):
    #print(name, age, args, city, job)
    #如果函数定义中已经有了一个可变参数，
    #后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
    #person_2('Jack', 24, 'sth', city='Beijing', job='Engineer')

#python3
#def f2(a, b, c=0, *, d, **kw):
    #print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)
    #f2(1, 2, d=99, ext=None)
    #args = (1, 2, 3)
    #kw = {'d': 88, 'x': '#'}
    #f2(*args, **kw)
    
    
def f1(a, b, c=0, *args, **kw):
    #必选参数、默认参数、可变参数、命名关键字参数和关键字参数
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
    #f1(1, 2)
    #f1(1, 2, c=3)
    #f1(1, 2, 3, 'a', 'b')
    #f1(1, 2, 3, 'a', 'b', x=99)
    #args = (1, 2, 3, 4)
    #kw = {'d': 99, 'x': '#'}
    #f1(*args, **kw)
    
    #对于任意函数，
    #都可以通过类似func(*args, **kw)的形式调用它
    #
    #要注意定义可变参数和关键字参数的语法：
    #*args是可变参数，args接收的是一个tuple；
    #**kw是关键字参数，kw接收的是一个dict。

#返回多个值
import math

def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
    #x, y = move(100, 100, 60, math.pi / 6)
    #print(x, y)
  
    #返回的其实是tuple
    #r = move(100, 100, 60, math.pi / 6)
    #print(r)
    #如果你已经把my_abs()的函数定义保存为abstest.py文件了，
    #那么，可以在该文件的当前目录下启动Python解释器，
    #用from abstest import my_abs来导入my_abs()函数，
    #注意abstest是文件名（不含.py扩展名）

def fact(n):
    #递归
    if n==1:
        return 1
    return n * fact(n - 1)

def fact_1(n):
    #当时栈溢出，改成尾递归。但是大多数编译语言还是没有对尾递归进行优化，还是会溢出
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)


if __name__ == '__main__':
    pass
