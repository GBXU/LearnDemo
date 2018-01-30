'''
Created on 2015-10-14

@author: chengli
'''
import os,sys
 
import xml.dom.minidom
from xml.dom.minidom import Node

class LockServer(object):
    
    def __init__(self):
        self.lsId = -1;
        self.ipAddress = ""
    
    def setInfo(self, lsId, ipAddress):
        self.lsId = lsId;
        self.ipAddress = ipAddress
    
    def getLsId(self):
        return self.lsId    
    
    def getIpAddress(self):
        return self.ipAddress
    
    def printOut(self):
        print "Lock Server ", self.lsId, " ipAddress ", self.ipAddress
        
class LockClient(object):
    def __init__(self):
        self.lcId = -1;
        self.ipAddress = ""
    
    def setInfo(self, lcId, ipAddress):
        self.lcId = lcId;
        self.ipAddress = ipAddress
    
    def getLcId(self):
        return self.lcId    
    
    def getIpAddress(self):
        return self.ipAddress
    
    def printOut(self):
        print "Lock Client ", self.lcId, " ipAddress ", self.ipAddress

class LockServersAndClients(object):
    
    def __init__(self):
        self.lsNum = 0
        self.lcNum = 0
        self.lServers = list()
        self.lClients = list()

    def getLockServerCount(self):
        return self.lsNum
    
    def getLockClientCount(self):
        return self.lcNum
        
    def getLockServer(self, lsId):
        assert(lsId >= 0 and lsId < self.getLockServerCount())
        return self.lServers[lsId]
    
    def getLockClient(self, lcId):
        assert(lcId >= 0 and lcId < self.getLockClientCount())
        return self.lClients[lcId]
    
    def addLockServer(self, lsId, ipAddress):
        ls = LockServer()
        ls.setInfo(lsId, ipAddress)
        self.lServers.append(ls)
        
    def addLockClient(self, lcId, ipAddress):
        lc = LockClient()
        lc.setInfo(lcId, ipAddress)
        self.lClients.append(lc)
    
    def parseLockServer(self, node):
        print 'parse vasco lock server list here'
        for lsNode in node[0].getElementsByTagName("lockServer"): 
            self.addLockServer(lsNode.getAttribute("lsId"),lsNode.getAttribute("lsIP"))
        assert(self.lsNum == len(self.lServers))
        
    def parseLockClient(self, node):
        print 'parse vasco lock client list here'
        for lsNode in node[0].getElementsByTagName("lockClient"): 
            self.addLockClient(lsNode.getAttribute("lcId"),lsNode.getAttribute("lcIP"))
        assert(self.lcNum == len(self.lClients))
            
    def parseVascoConnXml(self, xmlFileName):
        print 'parse vasco Conn file here'
        doc = xml.dom.minidom.parse(xmlFileName)
        node = doc.getElementsByTagName("lockServerCluster")
        self.lsNum = int(node[0].getAttribute("lsNum"))
        print 'lsNum', self.lsNum
        self.parseLockServer(node)
            
        node = doc.getElementsByTagName("lockClientGroup")
        self.lcNum = int(node[0].getAttribute("lcNum"))
        print 'lcNum', self.lcNum
        self.parseLockClient(node);
    
    def printOut(self):
        print "Vasco Config File"
        for lsId in range(0, self.getLockServerCount()):
            self.getLockServer(lsId).printOut()
        for lcId in range(0, self.getLockClientCount()):
            self.getLockClient(lcId).printOut()
    
def parseFileAndGetLockServerClients(configFile):
    lockServerClients = LockServersAndClients()
    lockServerClients.parseVascoConnXml(configFile)
    lockServerClients.printOut()
    return lockServerClients

if __name__ == '__main__':
    '''
    option[0] => config File
    '''
    if len(sys.argv) != 2:
        print "Usage: python vascoConfigFileParser.py configFile"
        sys.exit()
    option = sys.argv[1:]
    configFile = option[0]
    #lockServerClients = LockServersAndClients()
    #lockServerClients.parseVascoConnXml(configFile)
    #lockServerClients.printOut()
    parseFileAndGetLockServerClients(configFile)
        
        
