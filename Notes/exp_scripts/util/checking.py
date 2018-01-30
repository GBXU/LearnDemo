import os, sys
from time import time, sleep

def checkProxyReady(sshHandler, top_path, dcId, proxyId):
    command = "tail -n 1 " + top_path + "/webproxy" + str(dcId) +"-"+str(proxyId)+".txt"
    returnStr= sshHandler.run_command(command)
    if returnStr.find("Listening to ") <> -1:
        print "proxy ", dcId, proxyId, " ready"
        return True
    else:
        print "proxy ", dcId, proxyId, " not ready"
        return False
    
def checkTomcatProxyReady(sshHandler, tomcatLogPath, dcId, proxyId, backend='txmud'):
    #if backend == 'txmud':
        #command = "grep \"creating new connection\" "+tomcatLogPath + "/catalina.out | wc -l "
    #else:
    command = "grep \"Initializing database pool\" "+tomcatLogPath + "/catalina.out | wc -l "
    returnStr = sshHandler.run_command(command)
    connNum = int(returnStr)
    if connNum <> 101:
        print "proxy ", dcId, proxyId, " not ready"
        return False
    command = "tail -n 2 " + tomcatLogPath + "/catalina.out"
    returnStr = sshHandler.run_command(command)
    if returnStr.find("Server startup") <> -1:
        print "proxy ", dcId, proxyId, " ready"
        return True
    else:
        print "proxy ", dcId, proxyId, " not ready"
        return False
            
def checkStorageshimReady(sshHandler, top_path, dcId, sshimId):
    while True:
        command = "tail -n 10 " + top_path + "/sshim" + str(dcId) +"-"+str(sshimId)+".txt"
        returnStr= sshHandler.run_command(command)
        if returnStr.find("Listening to ") <> -1:
            return True
        else:
            print "waiting for storageshim "
            sleep(10)
            
def checkUserFinished(sshHandler, userName):
    count = 0
    while True:
        command = "ps aux | grep "+userName+" | grep java | grep ClientEmulator | grep -v grep "
        returnStr= sshHandler.run_command(command)
        if len(returnStr) == 0:
            return True
        else:
            print "wait for user to finish"
            if count == 50:
                print "something wrong"
                return False
            sleep(100)
            count = count + 1
    
