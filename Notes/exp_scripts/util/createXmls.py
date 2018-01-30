
from datacenter import Datacenter
import xml.dom.ext
from xml.dom.minidom import Document
from nodeParser import *

def writeToFile(doc, filename):
    xml.dom.ext.PrettyPrint(doc, open(filename,"w"))


def makeDcConfigXml(dcs, dcNum, proxyNum, sshimNum, userNum):
    #dcs is a list of Datacenter
    print "we make DcConfigXml here"
    fileName = str(dcNum) + "dc" + str(proxyNum) + "proxy" + str(sshimNum) + "storage" + str(userNum) + "user1.xml"
    doc = Document()
    node = doc.createElement('dataCenters')
    node.setAttribute('dcNum',str(dcNum))
    doc.appendChild(node)
    
    #each data center
    for s in dcs:
        if s.coorNum > 0:
            #s is a dataCenter instance
            dcNode = doc.createElement('dataCenter')
            if s.coor == None:
                dcNode.setAttribute('cdIP',"")
                dcNode.setAttribute('cdPort',str(0))
            else:
                dcNode.setAttribute('cdIP',s.coor[0].hostname)
                dcNode.setAttribute('cdPort',str(s.coor[1]))
                dcNode.setAttribute('RemotecdIP',s.coor[0].hostname)
                dcNode.setAttribute('RemotecdPort',str(s.coor[2]))
            node.appendChild(dcNode)
            
            ##storageshims
            if s.sshimNum > 0:
                sshimsNode = doc.createElement('storageShims')
                sshimsNode.setAttribute('ssNum',str(s.sshimNum))
                dcNode.appendChild(sshimsNode)
                
                ##each storageshim
                for key in sorted(s.storageshims.iterkeys()):
                    ssNode = doc.createElement('storageShim')
                    ssNode.setAttribute('ssIP', s.storageshims[key][0].hostname)
                    ssNode.setAttribute('ssPort', str(s.storageshims[key][1]))
                    sshimsNode.appendChild(ssNode)
            
            ##webproxies
            if s.proxyNum >0 :
                wproxiesNode = doc.createElement('webProxies')
                wproxiesNode.setAttribute('wpNum',str(s.proxyNum))
                dcNode.appendChild(wproxiesNode)
                
                for key in sorted(s.webproxies.iterkeys()):
                    wpNode = doc.createElement('webproxy')
                    wpNode.setAttribute('wpIP',s.webproxies[key][0].hostname)
                    wpNode.setAttribute('wpPort',str(s.webproxies[key][1]))
                    wproxiesNode.appendChild(wpNode)
        
    #print doc.toprettyxml(indent="  ")    
    writeToFile(doc, fileName)
        
    return fileName

def getDCNumFromApplication(dcs):
    count = 0;
    for s in dcs:
        if s.proxyNum > 0 or s.userNum > 0:
            count = count + 1
    return count

def makeUserDcConfigXml(dcs, zookeeper, dcNum, proxyNum, sshimNum, userNum):
    print "we make UserDcConfigXml here"
    fileName = str(dcNum) + "dc" + str(proxyNum) + "proxy" + str(sshimNum) + "storage" + str(userNum) + "user2.xml"
    doc = Document()
    node = doc.createElement('dataCenters')
    count = getDCNumFromApplication(dcs)
    node.setAttribute('dcNum',str(count))
    doc.appendChild(node)
    
    #each data center
    for s in dcs:
        #s is a dataCenter instance
        if s.proxyNum > 0 or s.userNum > 0:
            zooNode = doc.createElement('zooKeeper')
            zooNode.setAttribute('zooIP', zookeeper.hostname)
            zooNode.setAttribute('zooPort','10000')
            node.appendChild(zooNode)
            
            dcNode = doc.createElement('dataCenter')
            node.appendChild(dcNode)
            
            if s.proxyNum > 0:
                ##appServers
                assNode = doc.createElement('appServers')
                assNode.setAttribute('asNum',str(s.proxyNum))
                dcNode.appendChild(assNode)
                
                ##each appServer
                
                for key in sorted(s.webproxies.iterkeys()):
                    asNode = doc.createElement('appServer') 
                    asNode.setAttribute('asIP',s.webproxies[key][0].hostname)
                    asNode.setAttribute('asPort',str(s.webproxies[key][2]))
                    assNode.appendChild(asNode)
                
            if s.userNum > 0:
                ##users
                usNode = doc.createElement('users')
                usNode.setAttribute('uNum',str(s.userNum))
                dcNode.appendChild(usNode)
                
                ##each user
                
                for key in sorted(s.users.iterkeys()):
                    uNode = doc.createElement('user')
                    uNode.setAttribute('uIP',s.users[key][0].hostname)
                    uNode.setAttribute('uPort',str(s.users[key][1]))
                    usNode.appendChild(uNode)
    
    #print doc.toprettyxml(indent="\t")
    writeToFile(doc, fileName)
    
    return fileName


def makeDbConfigXml(dcs, dcNum, proxyNum, sshimNUm, userNum):
    
    print "we make DbConfigXml here"
    fileName = str(dcNum) + "dc" + str(proxyNum) + "proxy" + str(sshimNum) + "storage" + str(userNum) + "userDb.xml"
    
    
    return fileName
    
    
    