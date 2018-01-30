import os,sys
from util import *

def getTPCW(file):
    
    print "\n ==> parse TPCW file"
    f = open(file, "r+")
    s = f.readlines()
    tpcw = TPCW()
    for x in s:
        x = removeNewLine(x)
        tmpList = x.split(" ")
        tmpList = removeNoneFromList(tmpList)
        if tmpList[0] == "eb":
            tpcw.eb = tmpList[1]
        elif tmpList[0] == "item":
            tpcw.item = tmpList[1]
        elif tmpList[0] == "tpcwMix":
            tpcw.tpcwMix = tmpList[1]
        elif tmpList[0] == "tpcwWarmUpTime":
            tpcw.tpcwWarmUpTime = tmpList[1]
        elif tmpList[0] == "tpcwMeasureTime":
            tpcw.tpcwMeasureTime = tmpList[1]
        elif tmpList[0] == "tpcwTearDownTime":
            tpcw.tpcwTearDownTime = tmpList[1] 
        elif tmpList[0] == "tpcwThinkingTime":
            tpcw.tpcwThinkingTime = tmpList[1]
        elif tmpList[0] == "backend":
            tpcw.backend = tmpList[1]
        else:
            print "unknow parameters"
            sys.exit(-1)
            
    tpcw.experimentTag = tpcw.backend
    tpcw.printOut()     
    return tpcw

class TPCW(object):
    
    def __init__(self):
        print "\n ===>here is the initialization function of TPCW"
        self.eb = 0
        self.item = 0
        self.tpcwMix = 0
        self.tpcwWarmUpTime = 0
        self.tpcwTearDownTime = 0
        self.tpcwMeasureTime = 0
        self.tpcwThinkingTime = 0.0
        
        self.backend = ""
        self.experimentTag = ""
        
    def setTag(self, str):
        self.experimentTag = str
        
    def printOut(self):
        print "eb ", self.eb
        print "item ", self.item
        print "tpcwMix ", self.tpcwMix
        print "tpcwWarmUpTime ", self.tpcwWarmUpTime
        print "tpcwTearDownTime ", self.tpcwTearDownTime
        print "tpcwMeasureTime ", self.tpcwMeasureTime
        print "tpcwThinkingTime ", self.tpcwThinkingTime
        print "backend ", self.backend
        print "experimentTag ", self.experimentTag