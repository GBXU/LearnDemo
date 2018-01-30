import os,sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from util import *

class Node():
                
    def __init__(self, hostname, username, password,keyfile=None):
        print "create a node for ssh connection"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.keyfile = keyfile
        #strfilename=hostname +".log"
        #self.log_handler = Log(filename=strfilename)
    
    def __str__(self):
        if self.keyfile == None:
            return "<"+self.hostname+","+self.username+","+self.password +">"
        else:
            return "<"+self.hostname+","+self.username+","+self.password + "," + self.keyfile+">"
    
    def printOut(self):
        print self.__str__()
        

#dict zoneId => [<node,userName,password,key>]
def getNodeDict(nodeFile,pwd=None):
    f = open(nodeFile,"r+")
    s = f.readlines()
    nodeDict = dict()
    for x in s:
        #print x
        if x[0] <> '#' and x <> "\n":
            tmpList = x.split(" ")
            tmpList[4] = removeNewLine(tmpList[4])
            if nodeDict.has_key(tmpList[0]) == False:
                nodeDict[tmpList[0]] = list()
            if str(tmpList[4]) == "\"\"":
                if pwd <> None:
                    nodeDict[tmpList[0]].append(Node(tmpList[1],tmpList[2],pwd,None))
                else:
                    nodeDict[tmpList[0]].append(Node(tmpList[1],tmpList[2],tmpList[3],None))
            else:
                if pwd <> None:
                    nodeDict[tmpList[0]].append(Node(tmpList[1],tmpList[2],pwd,tmpList[4]))
                else:
                   nodeDict[tmpList[0]].append(Node(tmpList[1],tmpList[2],tmpList[3],tmpList[4])) 
        
    for k, v in nodeDict.items():
        for item in v:
            print k, item.__str__()
    return nodeDict
    
    