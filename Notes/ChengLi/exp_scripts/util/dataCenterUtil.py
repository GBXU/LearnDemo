from datacenter import *
import os,sys
from util import *

def getDCs(file):
    
    print "\n ==> parse configure file"
    f = open(file, "r+")
    s = f.readlines()
    dcs = list()
    userNumList = list()
    blueToken = 0
    expiredTime = 0
    bluequietTime = 0
    for x in s:
        x = removeNewLine(x)
        tmpList = x.split(" ")
        tmpList = removeNoneFromList(tmpList)
        if tmpList[0] == "userNumList":
            userNumList = tmpList[1:]
            userNumList = removeNoneFromList(userNumList)
        elif tmpList[0] == "blueToken":
            blueToken = int(tmpList[1])
        elif tmpList[0] == "expiredTime":
            expiredTime = long(tmpList[1])
        elif tmpList[0] == "bluequietTime":
            bluequietTime = long(tmpList[1])
        elif tmpList[0] == "dcId":
            dc = Datacenter()
            dc.dcId = int(tmpList[1])
            dcs.append(dc)            
        else:
            dc = dcs[-1]
            if tmpList[0] == "coor":
                dc.setCoorNum()
            if tmpList[0] == "proxy":
                dc.proxyNum = int(tmpList[1])
            if tmpList[0] == "sshim":
                dc.sshimNum = int(tmpList[1])
            if tmpList[0] == "dbNum":
                dc.dbNum = int(tmpList[1])
            if tmpList[0] == "user":
                dc.userNum = int(tmpList[1])
            if tmpList[0] == "userProxy":
                proxyList = tmpList[1:]
                dc.setUserProxy(int(proxyList[0]), int(proxyList[1]), int(proxyList[2]))
     
    print "datacenters:"
    for dc in dcs:
        dc.printOut()               
    print "userNumList", userNumList
    print "blueToken ", blueToken
    print "expiredTime ", expiredTime
    print "bluequietTime", bluequietTime
    return userNumList, blueToken, expiredTime, bluequietTime, dcs

def getProxyNum(dcList):
    proxyNum = 0
    for x in dcList:
        proxyNum += x.proxyNum
    print "totalProxyNum:", proxyNum
    return proxyNum

def getSshimNum(dcList):
    sshimNum = 0
    for x in dcList:
        sshimNum += x.sshimNum
    print "total sshimNum", sshimNum
    return sshimNum  

def getUserNum(dcList):
    userNum = 0
    for x in dcList:
        userNum += x.userNum
    print "total userNum", userNum
    return userNum

def getDcNum(dcList):
    dcNum = 0
    for x in dcList:
        if x.coorNum > 0 or x.dbNum > 0:
            dcNum += 1
    return dcNum