#!/usr/bin/env python2
# -*- coding: utf-8 -*-
############################################
'''
Created on 2017年3月20日

@author: xgb99
'''
import math
def func():
    print(abs(-20))
    
def data():
    #数据类型转换
    print(float('12.34'))
    print(bool(1))
    #十六进制 
    print(0x0001)
    #科学计数法 
    print(1.2e-5)
    #字符串
    tmp = 'abc'
    print(tmp)
    # 含有'的
    tmp = "I'm OK"
    print(tmp)
    # 用转义\
    tmp = 'I\'m \"OK\"!'
    print(tmp)
    #r'\\\t\\' 忽视转义
    tmp = r'\\\t\\'
    print(tmp)
    tmp = '\\\t\\'
    print(tmp)
    #'''...''' 多行内容
    print('''1
    2
    3''' )
    #/ 除法 //地板除 % 模
    print(4/3,4//3,4%3)
    #输出
    print('Age: %s. Gender: %s' % (25, True))
    print('growth rate: %d %%' % 7)
    print('%.2f' % 3.1415926)
    #编码
    print(ord('A'))
    print(chr(66))
    print('ABC'.encode('ascii'))
    #print('中文'.encode('utf-8'))
    #字符数
    print(len('中文'))
    #字节数
    print(len(b'\xe4\xb8\xad\xe6\x96\x87'))
    #print(len('中文'.encode('utf-8')))
    
def booleanfunc():
    #and、or和not 布尔运算
    print((True and False or True) and (not False))
    #None
    print(None)

def listfunc():
    #list
    #初始化
    classmates = ['Michael', 'Bob', 'Tracy']
    print(classmates)
    #查找 长度 后查找
    print(classmates[0],len(classmates),classmates[-1])
    #添加
    classmates.append('Adam')
    print(classmates)
    #插入
    classmates.insert(1, 'Jack')
    print(classmates)
    #删除
    classmates.pop()
    print(classmates)
    #定点删除
    classmates.pop(1)
    print(classmates)
    #list里面的元素的数据类型多样
    L = ['Apple', 123, True]
    print(L)
    #list元素也可以是另一个list
    s = ['python', 'java', ['asp', 'php'], 'scheme']
    print(s[2][1])
   
def tuplefunc():
    #tuple
    #初始化 空
    t = ()
    print(t)
    #一个
    t = (1,)
    print(t)
    # 初始化 
    t = ('Michael', 'Bob', 'Tracy')
    print(t)
    #初始化 除了 数字 字符串 还能有list，使得tuple可变
    t = ('a', 'b', ['A', 'B'])
    print(t)
    
def dictfunc():    
    #dict key和value
    #初始化
    d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
    print(d)
    #增加
    d['Adam'] = 67
    print(d)
    #判断是否在
    print('Thomas' in d)
    #查找，不再就返回None或者自己定义如-1
    print(d.get('Thomas', -1))
    #删除
    d.pop('Bob')
    print(d)
    
def setfunc():
    #set  key的集合
    #初始化
    s = set([1, 4, 3])
    print(s)
    #增加
    s.add(4)
    print(s)
    #删除
    s.remove(4)
    print(s)
    #集合运算
    s1 = set([1, 2, 3])
    s2 = set([2, 3, 4])
    print(s1 & s2)
    print(s1 | s2)
    
def forfunc():
    #for 
    L = ['Bart', 'Lisa', 'Adam']
    print('for:')
    for str in L:
        print('    %s' % str)
    
    sum = 0
    for x in range(101):
        sum = sum + x
    print(sum) 

def whilefunc():
    #while
    L = ['Bart', 'Lisa', 'Adam']
    n = 0
    print('while:')
    while n < len(L):
        print('    %s' % L[n])
        n= n+1

def iffunc():
    # if
    weight = float(input('please enter your weight (kg):'))
    height = float(input('please enter your height (m):'))
    bmi = weight/(height*height)
    print('%.2f' % bmi)
    if bmi<18.5:
        print('过轻')
    elif bmi<25:
        print('正常')
    elif bmi<28:
        print('过重')
    elif bmi<32:
        print('肥胖')
    else:
        print('严重肥胖')

if __name__ == "__main__":
    print ('This is main of module',__name__)
    #func()
    #data()
    #booleanfunc()
    #listfunc()
    #tuplefunc()
    #dictfunc()
    #setfunc()
    #forfunc()
    #whilefunc()
    #iffunc()