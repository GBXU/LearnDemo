
import os,sys

def getNum(dcList):
    proxyNum = 0
    sshimNum = 0
    userNum = 0
    for x in dcList:
        proxyNum += x.proxyNum
        sshimNum += x.sshimNum
        userNum += x.userNum
    return proxyNum, sshimNum, userNum

def setDCsUserNum(dcList, userNum):
    for x in dcList:
        x.userNum = int(userNum)
    

class Datacenter(object):
    
    def __init__(self):
        print "\n ===>here is the initialization function"
        self.dcId = 0
        self.coorNum = 0
        self.sshimNum = 0
        self.proxyNum = 0
        self.userNum = 0
        self.dbNum = 0
        self.coor = None
        self.webproxies = dict() #id = > ip + port
        self.storageshims = dict() #id => ip + port
        self.databases = dict() #id => ip + port
        self.users = dict() #id => ip + port
        self.userProxy = dict() #id => dcId + proxyId
        
    def setCoorNum(self):
        self.coorNum = 1
        
    
    def setUserNum(self, userNum):
        self.userNum = userNum
    
    def setProxyNum(self, proxyNum):
        self.proxyNum = proxyNum
        
    def setDcId(self, dcId):
        self.dcId = dcId
    
    def setCoordinator(self, ip, port1, port2):
        self.coor = (ip, port1, port2)
        
    def setWebProxy(self,proxyId, ip, port1):
        if self.webproxies.has_key(proxyId):
            print "that proxy id already seen", proxyId
            sys.exit(-1)
        self.webproxies[proxyId] = (ip, port1)

    def setUserProxy(self, userId, dcId, proxyId):
        if self.userProxy.has_key(userId):
            print "that user id already seen", userId
            sys.exit(-1)
        self.userProxy[userId] = (dcId, proxyId)
        
    def setStorageShim(self, ssId, ip, port):
        
        if self.storageshims.has_key(ssId):
            print "storageshim already assigned", ssId
            sys.exit(-1)
        self.storageshims[ssId] = (ip, port)
        
    def setdatabase(self,dbId, ip, port):
        if self.databases.has_key(dbId):
            print "that database is already assigned",dbId
            sys.exit(-1)
        self.databases[dbId] = (ip, port)
        
    def setUser(self, uId, ip, port):
        if self.users.has_key(uId):
            print "that user is already assigned", uId
            sys.exit(-1)
        self.users[uId] = (ip, port)
        
    def proxyPrintOut(self):
        for k,v in self.webproxies.items():
            print "proxy ", k, v[0].hostname, v[1]
            
    def sshimPrintOut(self):
        for k, v in self.storageshims.items():
            print "sshim ", k, v[0].hostname, v[1]
    
    def dbPrintOut(self):
        for k, v in self.databases.items():
            print "database ", k, v[0].hostname, v[1]
            
    def userPrintOut(self):
        for k, v in self.users.items():
            print "user ", k, v[0].hostname, v[1]
        
    def userProxyPrintOut(self):
        for k, v in self.userProxy.items():
            print "user ", k, " proxy ", v
        
    def printOut(self):
        print "coorNum", self.coorNum
        self.proxyPrintOut()
        self.sshimPrintOut()
        self.dbPrintOut()
        self.userPrintOut()
        self.userProxyPrintOut()
        
        
            
    