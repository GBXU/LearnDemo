'''
Created on 2017年3月20日

@author: xgb99
'''
def slicefunc():
    #切片操作
    L = list(range(100))
    print(L)
    #前10
    print(L[ :10])
    #后10
    print(L[-10: ])
    #到第19
    print(L[10:20])
    #前10中 每隔2 去选
    print(L[:10:2])
    #全部 每隔5
    print(L[::5])
    #前3
    print('ABCDEFG'[ :3 ])
    #全部 每隔2
    print('ABCDEFG'[ : :2])
    

from collections import Iterable
from collections import Iterator
def isIterable():
    #迭代器
    #迭代器惰性序列
    #任何可迭代对象都可以作用于for循环
    #判断可迭代
    print(isinstance({}, Iterable)) #dict
    print(isinstance((x for x in range(10)), Iterable)) #generator可迭代
    print(isinstance('abc', Iterable))# str是否可迭代 True
    print(isinstance([1,2,3], Iterable)) # list是否可迭代 True
    print(isinstance(123, Iterable))# 整数是否可迭代  False
    # str list 等 是 iterable 但不是 iterator
    # iterable可用于for 
    # iterator可用于for 并且 next()
    #可迭代 变成迭代器 iter()
    print(isinstance(iter('abc'), Iterator))
    for ch in 'ABC':
        print(ch)
        
    d = {'a': 1, 'b': 2, 'c': 3}
    for key in d:
        print(key)

    for i, value in enumerate(['A', 'B', 'C']):
        print(i, value)
    
    for x, y in [(1, 1), (2, 4), (3, 9)]:
        print(x, y)

def listGenerator():
    #列表生成式
    print(list(range(1, 11)))
    print([x * x for x in range(1, 11)])
    #if 
    print([x * x for x in range(1, 11) if x % 2 == 0])
    # two layers for
    print([m + n for m in 'ABC' for n in 'XYZ'])
    #dict
    d = {'x': 'A', 'y': 'B', 'z': 'C' }
    for k, v in d.items():
        print(k, '=', v)

def generatorfunc():
    #generator
    # 定义一
    g=(x * x for x in range(10))
    print(g)
    next(g) #计算下一个值
    for n in g:  #for in 自动调用next()
        print(n)

def fib(max):
    # 定义二 
    n, a, b = 0, 0, 1#此处相当于tuple
    while n < max:
        yield b #generator 遇到yield就返回
        a, b = b, a + b
        n = n + 1
    return 'done'
    #f = fib(6)
    #f
    #for n in fib(6):
    #   print(n)





if __name__ == '__main__':
    pass
