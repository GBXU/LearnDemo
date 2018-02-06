'''
Created on 2011-3-22

@author: chengli
'''
import os,sys
 
import xml.dom.minidom
from xml.dom.minidom import Node

class DataCenter(object):


    def __init__(self):
        self.cdConnInfo = "",0
        self.dbConnInfoList = list()
        self.storageShimConnInfoList = list() #(IP, Port)
        self.webproxyConnInfoList = list() #(IP, Port)
        self.tableList = {}
        self.tableLWWList = {} #(tableId,database Id)
        self.tableColor = {}
        self.colorTableList = {} #color => table_list
        
    def setCdConnInfo(self, cdIP, cdPort):
        self.cdConnInfo = str(cdIP), int(cdPort)
        print 'cdConnInfo', self.cdConnInfo
        
    def addToStorageShimConnInfoList(self, ssIP, ssPort):
        tmp_tuple = str(ssIP), int(ssPort)
        self.storageShimConnInfoList.append(tmp_tuple)
        print 'storage shim conn tuple', tmp_tuple
        print 'current storage shim conn info list', self.storageShimConnInfoList
        
    def addToWebProxyConnInfoList(self, wpIP, wpPort):
        tmp_tuple = str(wpIP), int(wpPort)
        self.webproxyConnInfoList.append(tmp_tuple)
        print 'web proxy conn tuple',tmp_tuple
        print 'current web proxy conn info list', self.webproxyConnInfoList
    
    def addToDbConnInfoList(self, dbHost, dbPort, dbUser, dbPwd, dbName):
        tmp_tuple = str(dbHost), int(dbPort), str(dbUser), str(dbPwd), str(dbName)
        self.dbConnInfoList.append(tmp_tuple)
        print 'db connection tuple',tmp_tuple
        print 'current db connection list', self.dbConnInfoList    
    
    def addToTableList(self,tableName, dbId):
        self.tableList[str(tableName)] = int(dbId)
        
    def addToTableLWWList(self, tableName, dbId):
        self.tableLWWList[str(tableName)] = int(dbId)
        
    def addToTableColorList(self, tableName, color):
        self.tableColor[str(tableName)] = color
        if self.colorTableList.has_key(color) == False:
            table_list = list()
            self.colorTableList[color] = table_list
        self.colorTableList[color].append(str(tableName))
    
    def getCdConnInfo(self):
        return self.cdConnInfo
    
    def getDbConnInfoList(self):
        return self.dbConnInfoList
    
    def getDbConnInfo(self, storageId):
        return self.dbConnInfoList[storageId]
    
    def getStorageShimConnInfoList(self):
        return self.storageShimConnInfoList
    
    def getStorageShimConnInfo(self, ssId):
        return self.storageShimConnInfoList[ssId]
    
    def getWebProxyConnInfoList(self):
        return self.webproxyConnInfoList
    
    def getWebProxyConnInfo(self,wpId):
        return self.webproxyConnInfoList[wpId]
    
    def getTableList(self):
        return self.tableList
    
    def getTableLWWList(self):
        return self.tableLWWList
    
    def getTableColorList(self):
        return self.tableColor
    
    def getColorTableList(self):
        return self.colorTableList
    

class DataCenters(object):
    
    def __init__(self):
        self.dcNum = 0
        self.dataCenterList = list()

    def getDataCenterCount(self):
        return self.dcNum
        
    def getDataCenter(self, dcId):
        return self.dataCenterList[dcId]
    
    def getRemoteDataCenterList(self, dcId):
        tmp_list = self.dataCenterList[:]
        del tmp_list[dcId]
        return tmp_list
    
    def parseStorageShim(self, node, dcElement):
        print 'parse storage shim list here'
        for ssNode in node[0].getElementsByTagName("storageShim"): #get all storage shims
            dcElement.addToStorageShimConnInfoList(ssNode.getAttribute("ssIP"),ssNode.getAttribute("ssPort"))
        
    def parseWebProxy(self, node, dcElement):
        print 'parse web proxy list here'    
        for wpNode in node[0].getElementsByTagName("webproxy"): #get all storage shims
            dcElement.addToWebProxyConnInfoList(wpNode.getAttribute("wpIP"),wpNode.getAttribute("wpPort"))
    
    def parseDcConnXml(self, xmlFileName):
        print 'parse dc Conn file here'
        doc = xml.dom.minidom.parse(xmlFileName)
        node = doc.getElementsByTagName("dataCenters")
        self.dcNum = int(node[0].getAttribute("dcNum"))
        print 'dcNum', self.dcNum
        dcNodeList = node[0].getElementsByTagName("dataCenter")
        for dcNode in dcNodeList:
            dcElement = DataCenter()
            dcElement.setCdConnInfo(dcNode.getAttribute("cdIP"), dcNode.getAttribute("cdPort"))
            self.parseStorageShim(dcNode.getElementsByTagName("storageShims"), dcElement)
            self.parseWebProxy(dcNode.getElementsByTagName("webProxies"), dcElement)
            self.dataCenterList.append(dcElement)
        
    def parseDbConnXml(self, xmlFileName):
        print 'parse db Conn file here'
        doc = xml.dom.minidom.parse(xmlFileName)
        node = doc.getElementsByTagName("databases")
        for dcElement in self.dataCenterList:
            id = 0
            for dbNode in node[0].getElementsByTagName("database"):
                tuple = dbNode.getAttribute("dbHost"), dbNode.getAttribute("dbPort"), dbNode.getAttribute("dbUser"), dbNode.getAttribute("dbPwd"), dbNode.getAttribute("dbName")
                dcElement.addToDbConnInfoList(tuple[0], tuple[1],tuple[2], tuple[3], tuple[4])
                tableStr = dbNode.getAttribute("tableList")
                tmpList = tableStr.split(',')
                for x in tmpList:
                    dcElement.addToTableList(x,id)
                tmpList = dbNode.getAttribute("tableLWW").split(',')
                for x in tmpList:
                    dcElement.addToTableLWWList(x,id)
                tmpList = dbNode.getAttribute("redTable").split(',')
                for x in tmpList:
                    dcElement.addToTableColorList(x,0)
                tmpList = dbNode.getAttribute("blueTable").split(',')
                for x in tmpList:
                    dcElement.addToTableColorList(x,1)
                id = id + 1
        
