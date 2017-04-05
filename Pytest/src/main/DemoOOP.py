#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
__doc__
Created on 2017年3月20日
@author: xgb99
private:
_xxx
__xxx
'''
__author__ = 'XuGB'
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))

if __name__ == '__main__':
    pass

