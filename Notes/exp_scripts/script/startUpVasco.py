import MySQLdb
from time import time, sleep
import datetime
import os, sys
lib_path = os.path.abspath('../util')
sys.path.append(lib_path)
from sshcontroller import *
from createXmls import *
from datacenter import *
from dataCenterUtil import *
from InitDB import *
from nodeParser import *
from checking import *
from vascoConfigParser import *


class experi_handler():
    def __init__(self, testName, dcList, dbFile, userName, password, path, debug, isAmazon, nodeFile,
                 vascoConfigFile, bftSmartSysConfigFile, bftSmartHostConfigFile, sqlFile, wpFile):
        print "experiment handler initialization"
        self.nodeDict = dict()
        self.userNodeList = list()
        self.shareFolder = ""
        self.userName = userName
        self.pwd = password
        self.top_path = path
        self.isAmazon = isAmazon
        self.nodeFile = nodeFile
        self.txmud_src_path = "/home/chengli/newJava"
        self.txmud_top_path = path + "txmud"
        self.tomcat_top_path = self.txmud_top_path + "/tomcat6"
        self.tomcat_lib_path = self.tomcat_top_path + "/lib"
        self.tomcat_log_path = self.tomcat_top_path + "/logs"
        self.dcs = dcList
        self.port = 60000
        self.dcFile = ""
        self.dbFile = dbFile
        self.sshList = dict() #id => ssc
        self.time = 0.0
        self.testName = testName
        self.zookeeper = None
        self.appThdCount = 0
        self.proxyThdCount = 0
        self.sshimThdCount = 0
        self.coorThdCount = 0
        self.debug = debug
        self.blueToken = 0
        self.proxyScratchpadNum = 0
        self.datawriterScratchpadNum = 0
        self.dcNum = 0
        self.wpNum = 0
        self.ssNum = 0
        self.uNum = 0
        self.timeout = 0
        self.simulateUserNum = 0
        
        self.coordinatorJar = ""
        self.storageshimJar = ""
        self.proxyJar = ""
        self.userJar = ""
        
        #some parameters for tpcw 
        self.logicalClock = "0-0"
        self.backend = "vasco"
        self.jdbcTxMudJar = ""
        self.jsqlparserJar = ""
        self.nettyJar = ""
        self.logJar = ""
        self.rubis_root_path = self.txmud_src_path+"/src/applications/RUBiStxmud"
        self.proxy_root_path = self.rubis_root_path + "/Servlets"
        self.client_root_path = self.rubis_root_path + "/Client"
        self.txmud_outputdir = self.tomcat_lib_path + "/output/txmud"
        self.txmud_binary = self.txmud_outputdir + "/dist"
        self.client_deploy_path = self.top_path
        self.user_log_path = self.client_deploy_path + "/bench"
        
        self.vasco_root_path = "/home/chengli/git/Vasco/vasco/"
        self.sifter_root_path = "/var/tmp/workspace/georeplication/"
        
        #tomcat
        self.tomcatMem = "4G"
        self.websiteCode = dict()
        self.proxydbFile = "rubis_txmud_db.xml"
        self.proxydcFile = "rubis_txmud.xml"
        
        self.vasco_jar_name = "vasco-1.0-SNAPSHOT.jar"
        
        #define jar file
        jarFilePath = self.vasco_root_path + "/target/"
        self.jsqlparserJar = self.vasco_root_path + "/lib/jsqlparser.jar"
        self.nettyJar = self.vasco_root_path + "/lib/netty-3.3.1.Final.jar"#used by the proxy
        self.logJar = self.vasco_root_path + "/lib/log4j-1.2.15.jar"
        self.vascoJar = jarFilePath + self.vasco_jar_name
        
        
        self.warmUpTime = 300000
        self.measureTime = 300000   
        self.tearDownTime = 60000
        
        #files required by vasco
        self.vasco_config_xml = vascoConfigFile
        self.bftHostConfig = bftSmartHostConfigFile
        self.bftSystemConfig = bftSmartSysConfigFile
        self.bftSmartLib = "/home/chengli/git/Vasco/vasco/lib/BFT-SMaRt.jar"
        self.lockServerClients = None
        
        self.clientJar = self.rubis_root_path + "/Client/rubis_client.jar"
        self.clientPropertiesFile = self.rubis_root_path + "/Client/rubis.properties.vasco"
        self.clientTransitionTableFile = self.rubis_root_path + "/workload/vasco_transitions_3.txt"
        
        #self.clientPropertiesFile = self.rubis_root_path + "/Client/rubis.properties"
        #self.clientTransitionTableFile = self.rubis_root_path + "/workload/transitions.txt"
        self.clientDeployedPropertiesFile = self.top_path + "/rubis.properties"
        self.clientDeployedTransitionTableFile = self.top_path + "/transitions.dat"
        
        self.webappDeployDir = self.tomcat_top_path+"/webapps"
        
        ##files for vasco
        self.annotatedSqlFile = sqlFile
        self.wpFile = wpFile
        
    def getLockServerClients(self):
        self.lockServerClients = parseFileAndGetLockServerClients(self.vasco_config_xml)
        
    def getNodeDict(self):
        self.nodeDict = getNodeDict(self.nodeFile,self.pwd)
    
    def initiateDatacenters(self):
        print "initiate datacenters"
        self.getNodeDict()
        
        if len(self.nodeDict) < len(self.dcs):
            print "No enough nodes"
            sys.exit(-1)
        
        keys = self.nodeDict.keys()
        count = 0
        for x in self.dcs:
            self.initiateDatacenter(x)
            count = count + 1
        self.ssNum = getSshimNum(self.dcs)
        self.dcNum = getDcNum(self.dcs)
        self.wpNum = getProxyNum(self.dcs)
        self.uNum = getUserNum(self.dcs)
        print "all dc"
        self.printOut()
        print "set logical clock"
        self.logicalClock = getLogical_clock(self.dcNum, self.backend)
            
    def printOut(self):
        for x in range(0,self.dcNum):
            print "dc ", x
            dc = self.dcs[x]
            dc.printOut()
        
    def initiateDatacenter(self, dc):
        if dc.coorNum == 1: 
            self.assignCoordinator(dc)
        if dc.dbNum > 0:
            self.assignDatabases(dc)
        if dc.sshimNum > 0:
            self.assignStorageshims(dc)
        if dc.proxyNum > 0:
            self.assignWebProxies(dc)
        if dc.userNum > 0:
            self.assginUsers(dc)
        
    def assignCoordinator(self, dcObj):
        nodeList = self.nodeDict["coordinator-"+str(dcObj.dcId)]
        node = nodeList.pop(0)
        dcObj.coor = (node, self.port, self.port+1)
        self.port += 2
        
    def assignStorageshims(self, dcObj):
        nodeList = self.nodeDict["sshim-"+str(dcObj.dcId)]
        for x in range(0, dcObj.sshimNum):
            node = nodeList.pop(0)
            dcObj.storageshims[x] = (node, self.port)
            self.port += 1
    
    def assignWebProxies(self,dcObj):
        nodeList = self.nodeDict["proxy-"+str(dcObj.dcId)]
        for x in range(0, dcObj.proxyNum):
            node = nodeList.pop(0)
            dcObj.webproxies[x] = (node, self.port)
            self.port += 1
            
    def assginUsers(self, dcObj):
        nodeList = self.nodeDict["user-"+str(dcObj.dcId)]
        print dcObj.userNum, len(nodeList)
        count = 0
        while True:
            if count == dcObj.userNum:
                break
            for x in range(0,len(nodeList)):
                if count == dcObj.userNum:
                    break
                dcObj.users[count] = (nodeList[x], self.port)
                print "assign user", count
                self.port +=1
                count = count + 1
                        
    def prepareCode(self):
        #check sifter file exist or not
        if not os.path.exists(self.vasco_root_path):
            print "Vasco code doesn't exist, please download"
            sys.exit()
        
        #compile the code here
        #command = "cd " + self.vasco_root_path + " && mvn clean && mvn compile && mvn install"
        #print command
        #os.system(command)
        
        command = "cd " + self.txmud_src_path + " && ant clean && ant"
        print command
        os.system(command)
        
        #compile the client code
        command = "cd " + self.client_root_path + " && ant clean && ant"
        print command 
        os.system(command)
                
    def assignDatabases(self, dcObj):
        nodeList = self.nodeDict["database-"+str(dcObj.dcId)]
        for x in range(0, dcObj.dbNum):
            node = nodeList.pop(0)
            dcObj.databases[x] = (node, 50000)
            #change the ip address of dbConn.xml
            pattern = "dcId=\'"+str(dcObj.dcId)+"\' dbId=\'" +str(x)+"\'"
            print pattern
            command = "sed -i \"/"+pattern+"/s/dbHost=\'.*\' dbPort/dbHost=\'"+dcObj.databases[x][0].hostname+"\' dbPort/g\" " + self.dbFile
            print command
            os.system(command)     
            os.system("cat " + self.dbFile)
                 
    def writeXmls(self):
        self.dcFile = makeDcConfigXml(self.dcs, self.dcNum, self.wpNum, self.ssNum, self.uNum)
        command = "cat " + self.dcFile
        os.system(command)
        
    def createConnections(self):
        print "create connections"
        command = "mkdir " + self.top_path + "; rm " + self.top_path + "/*.log; rm " + self.top_path + "/*.txt" 

        for dc in self.dcs:
            #coordinator
            if dc.coorNum > 0:
                coorPrefix = "coor-"+str(dc.dcId)
                print dc.coor[0].hostname
                self.sshList[coorPrefix] = SSHController(dc.coor[0])
                self.sshList[coorPrefix].open()
                self.sshList[coorPrefix].run_command(command)
            #storage
            storagePrefix = "sshim-"+str(dc.dcId)
            for k, v in dc.storageshims.items():
                print v[0].hostname
                self.sshList[storagePrefix+"-"+str(k)] = SSHController(v[0])
                self.sshList[storagePrefix+"-"+str(k)].open()
                self.sshList[storagePrefix+"-"+str(k)].run_command(command)
            dbPrefix = "db-"+str(dc.dcId)
            for k, v in dc.databases.items():
                print v[0].hostname
                self.sshList[dbPrefix+"-"+str(k)] = SSHController(v[0])
                self.sshList[dbPrefix+"-"+str(k)].open()
            proxyPrefix = "proxy-"+str(dc.dcId)
            for k,v in dc.webproxies.items():
                print v[0].hostname
                self.sshList[proxyPrefix+"-"+str(k)] = SSHController(v[0])
                self.sshList[proxyPrefix+"-"+str(k)].open()
                self.sshList[proxyPrefix+"-"+str(k)].run_command(command)
            userPrefix = "user-"+str(dc.dcId)
            for k,v in dc.users.items():
                print v[0].hostname
                self.sshList[userPrefix+"-"+str(k)] = SSHController(v[0])
                self.sshList[userPrefix+"-"+str(k)].open()
                self.sshList[userPrefix+"-"+str(k)].run_command(command)
                #command = "mv /var/tmp/root/txmud/tomcat6/webapps/tpcw/Images /var/tmp/"
                #self.sshList[userPrefix+"-"+str(k)].run_command(command)
        
        print "create connects to all lock servers and clients"
        for lsId in range(0, self.lockServerClients.getLockServerCount()):
            lsServer = self.lockServerClients.getLockServer(lsId)
            sshInfoNode = self.nodeDict["lockserver-"+str(lsId)][0]
            print sshInfoNode.hostname
            self.sshList["lockserver-"+str(lsId)] = SSHController(sshInfoNode)
            self.sshList["lockserver-"+str(lsId)].open()
            self.sshList["lockserver-"+str(lsId)].run_command(command)
            
        for lcId in range(0, self.lockServerClients.getLockClientCount()):
            lcClient = self.lockServerClients.getLockClient(lcId)
            sshInfoNode = self.nodeDict["lockclient-"+str(lcId)][0]
            print sshInfoNode.hostname
            self.sshList["lockclient-"+str(lcId)] = SSHController(sshInfoNode)
            self.sshList["lockclient-"+str(lcId)].open()
            self.sshList["lockclient-"+str(lcId)].run_command(command)
            
    def setUpNetwork(self):
        command = "set enforce 0; iptables -F"
        for k,v in self.sshList.items():
            v.run_command(command)
        
    def clean_database(self):
        #clean database here
        for s in self.dcs:
            for x in range(0, s.dbNum):
                print "clean database here", s.dcId, x
                dbPrefix = "db-"+str(s.dcId)+"-"+str(x)
                ssc = self.sshList[dbPrefix]
                stopMySQLServer(ssc)
                resetDatabase(ssc, self.isAmazon, self.backend, self.dcNum)
                startMySQLServer(ssc)
                
    def refresh_databases(self):
        #get a timestamp
        utc_datetime = datetime.datetime.utcnow()
        utc_datetime_str = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print "utc timestamp we get now is ", utc_datetime_str
        for s in self.dcs:
            if s.dbNum>0:
                print "refresh database here", s.dcId, 0
                dbPrefix = "db-"+str(s.dcId)+"-"+str(0)
                ssc = self.sshList[dbPrefix]
                refreshDatabase(ssc, self.isAmazon, 33000, utc_datetime_str, 1, 7)
        print "Finishing refresh all database"
        
    def preload_databases(self):
        for s in self.dcs:
            if s.dbNum > 0:
                print "preload database here", s.dcId, 0
                dbPrefix = "db-"+str(s.dcId)+"-"+str(0)
                ssc = self.sshList[dbPrefix]
                command = " cd " + self.top_path + " && nohup java -jar preloadDB-big.jar rubis &> preloadDB.log"
                ssc.run_command(command)
        
        numOfDBReady = 0
        while numOfDBReady < len(self.dcs):
            print numOfDBReady, "size of dcs ", len(self.dcs)
            numOfDBReady = 0
            sleep(10)
            for s in self.dcs:
                if s.dbNum > 0:
                    print "checking database is ready or not", s.dcId, 0
                    dbPrefix = "db-"+str(s.dcId)+"-"+str(0)
                    ssc = self.sshList[dbPrefix]
                    returnVar = removeNewLine(ssc.remoteTailFile(self.top_path+"/preloadDB.log", 1))
                    if returnVar == "Successfully preloaded":
                        numOfDBReady = numOfDBReady + 1
                    elif returnVar == "Failed to preload":
                        print "you have problems to preload, please check"
                        sys.exit()
                    else:
                        break
                else:
                    numOfDBReady = numOfDBReady + 1
        print "Finishing preload all database"
                
    def checkAllDatabase(self):
        for s in self.dcs:
            for x in range(0, s.dbNum):
                print "check database here", s.dcId, x
                dbPrefix = "db-"+str(s.dcId)+"-"+str(x)
                ssc = self.sshList[dbPrefix]
                if checkDatabase(ssc, self.isAmazon) == True:
                    continue
                else:
                    return False
        return True
    
    def checkDatabases(self):
        while(True):
            if self.checkAllDatabase() == True:
                break
            sleep(20)
        print "all databases are started"
    
    def stop_database(self,dcId, dbId):
        dbPrefix = "db-"+str(dcId)+"-"+str(dbId)
        ssc = self.sshList[dbPrefix]
        stopMySQLServer(ssc)
                
                
    ##need to fix it
    def copyCodeToRemote(self):
        print "copy codes to remote machines"
        for dc in self.dcs:
            #coordinator
            if dc.coorNum > 0:
                coorPrefix = "coor-"+str(dc.dcId)
                command = "rm -rf " + self.top_path + "/" + self.vasco_jar_name
                self.sshList[coorPrefix].run_command(command)
                self.sshList[coorPrefix].put(self.top_path+"/"+self.vasco_jar_name, self.vascoJar)
                self.sshList[coorPrefix].put(self.top_path+"/lib/"+self.bftSmartLib.split("/")[-1], self.bftSmartLib)

            #storage
            storagePrefix = "sshim-"+str(dc.dcId)
            for k, v in dc.storageshims.items():
                command = "rm -rf " + self.top_path + "/" + self.vasco_jar_name
                self.sshList[storagePrefix+"-"+str(k)].run_command(command)
                print "copy jar file  to storage node", dc.dcId, k
                self.sshList[storagePrefix+"-"+str(k)].put(self.top_path+"/"+self.vasco_jar_name, self.vascoJar)
                self.sshList[storagePrefix+"-"+str(k)].put(self.top_path+"/lib/"+self.bftSmartLib.split("/")[-1], self.bftSmartLib)
        
        print "copy the central vasco server code to remote"
        command = "rm -rf " + self.top_path + "/" + self.vasco_jar_name
        for lsId in range(0, self.lockServerClients.getLockServerCount()):
            self.sshList["lockserver-"+str(lsId)].run_command(command);
            print "copy jar file to vasco central lock server ", lsId
            self.sshList["lockserver-"+str(lsId)].put(self.top_path+"/"+self.vasco_jar_name, self.vascoJar)
            self.sshList["lockserver-"+str(lsId)].put(self.top_path+"/lib/"+self.bftSmartLib.split("/")[-1], self.bftSmartLib)
 
    ##need to fix it  
    def copyFilesToRemote(self):
        print "copy Files to remote machines"
        for dc in self.dcs:
            #coordinator
            if dc.coorNum > 0:
                coorPrefix = "coor-"+str(dc.dcId)
                self.sshList[coorPrefix].put(self.top_path+"/"+self.dcFile,self.dcFile)
            #storage
            storagePrefix = "sshim-"+str(dc.dcId)
            for k, v in dc.storageshims.items():
                print "copy file  to storage node", dc.dcId, k
                self.sshList[storagePrefix+"-"+str(k)].put(self.top_path+"/"+self.dcFile,self.dcFile)
                self.sshList[storagePrefix+"-"+str(k)].put(self.top_path+"/"+self.dbFile.split("/")[-1],self.dbFile)
        
        print "copy vasco config and raft config file to remote servers and clients (coordinators)"
        
        print "copy the central vasco server files to remote"
        for lsId in range(0, self.lockServerClients.getLockServerCount()):
            print "copy config file to vasco central lock server ", lsId
            self.sshList["lockserver-"+str(lsId)].put(self.top_path+"/config/"+self.bftSystemConfig.split("/")[-1], self.bftSystemConfig)
            self.sshList["lockserver-"+str(lsId)].put(self.top_path+"/config/"+self.bftHostConfig.split("/")[-1], self.bftHostConfig)
            self.sshList["lockserver-"+str(lsId)].put(self.top_path+"/"+self.vasco_config_xml.split("/")[-1],self.vasco_config_xml)
            
        for lcId in range(0, self.lockServerClients.getLockClientCount()):
            print "copy config file to vasco client/coordinator ", lcId 
            self.sshList["lockclient-"+str(lcId)].put(self.top_path+"/config/"+self.bftSystemConfig.split("/")[-1], self.bftSystemConfig)
            self.sshList["lockclient-"+str(lcId)].put(self.top_path+"/config/"+self.bftHostConfig.split("/")[-1], self.bftHostConfig)
            self.sshList["lockclient-"+str(lcId)].put(self.top_path+"/"+self.vasco_config_xml.split("/")[-1],self.vasco_config_xml)
    
    def start_coordinator(self, dcObj):
        #get hostname and username
        dcId = dcObj.dcId
        coorPrefix = "coor-" + str(dcId)
        #connect to coordinator
        ssc = self.sshList[coorPrefix]
        #if int(self.dcNum) == 1 or float(self.ratio) == 0.0:
            #blueTokenNum = int(self.blueToken)
        #else:
            #blueTokenNum = int(int(self.blueToken)*int(self.outstandingOps)*int(dcObj.userNum)*int(self.dcNum)*float(self.ratio)*0.5) + 1
        command = "cd "+self.top_path + " && " + "nohup java -Xms4000m -Xmx8000m -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseConcMarkSweepGC "
        command += "-cp " + self.vasco_jar_name + ":./lib/*  org.mpi.vasco.txstore.coordinator.NewCoordinator "
        command += self.dcFile+ " " + str(dcId)+ " " + str(dcId) + " " + str(self.coorThdCount) + " " + str(0.5) + " " + self.vasco_config_xml.split("/")[-1]
        command += " &> coor"+str(dcId)+".txt &"
        ssc.run_command(command, True)
        sleep(1)
        isDone = ssc.checkProcessAlive("java")
        if isDone:
           print "set up coordinator", dcId
           return True
        else:
           print "failed to set up coordinator", dcId
           return False
       
    def start_all_coordinator(self):
        for s in self.dcs:
            if s.coorNum > 0:
                if self.start_coordinator(s) == False:
                    return False
        return True
            
    def stop_coordinator(self, dcId):
        coorPrefix = "coor-" + str(dcId)
        ssc = self.sshList[coorPrefix]
        ssc.killAllProcessesBySpecifiedPattern("java")
        
        
    def start_storageshim(self, dcObj, ssId): #start command needs to be modified
        #compute scratchpad number here
        scratchpadNum = int(25)
        #if self.dcNum > 1:
            #scratchpadNum = int(int(self.simulateUserNum) + (((int(self.simulateUserNum)*int(self.uNum))/3 + 1)*(int(self.dcNum) - 1)*0.2))
            #if scratchpadNum < 20:
                #scratchpadNum = 20
        print "scratchpad num :" , scratchpadNum
            
        dcId = dcObj.dcId
        sshimPrefix = "sshim-" + str(dcId)+"-" + str(ssId)
        ssc = self.sshList[sshimPrefix]
        command = "cd "+self.top_path + " && " + "nohup java -Xms4000m -Xmx8000m -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseConcMarkSweepGC -cp " 
        command += self.vasco_jar_name + ":./lib/* org.mpi.vasco.txstore.appextend.MicroStorage "
        command += " "+ self.dcFile + " "+self.dbFile.split("/")[-1] +" " + str(dcId) + " " + str(ssId) + " " + str(self.sshimThdCount) + " true " + str(scratchpadNum)
        command += " &>sshim"+str(dcId)+"-"+str(ssId)+".txt &"  
        ssc.run_command(command, True)
        sleep(1)
        isDone = ssc.checkProcessAlive("java")
        if isDone:
           print "set up storageshim", dcId, ssId
           return True
        else:
           print "failed to set up storageshim", dcId, ssId
           return False
            
    def start_all_storageshim(self):
        print "try to start all storageshims"
        for s in self.dcs:
            for x in range(0,s.sshimNum):
                isDone = self.start_storageshim(s, x)
                if isDone == False:
                    return False
        return True
    
    def wait_for_storageshims(self):
        print "waiting for storageshims "
        for s in self.dcs:
            for x in range(0,s.sshimNum):
                ssc = self.sshList["sshim-"+str(s.dcId) + "-" + str(x)]
                checkStorageshimReady(ssc, self.top_path, s.dcId, x)
       
    def stop_storageshim(self, dcId, ssId):
        sshimPrefix = "sshim-" + str(dcId)+"-" + str(ssId)
        ssc = self.sshList[sshimPrefix]
        ssc.killAllProcessesBySpecifiedPattern("java")
            
    def compile_txmud(self, ssc):
        if self.isAmazon == False:
            command = "mkdir " + self.top_path + "; mkdir " + self.txmud_top_path
            ssc.run_command(command)
            
            print "\n ===> compile txmud"
            command = "cd " + self.txmud_src_path + " && ant clean && ant"
            ssc.run_command(command)
        else:
            print "check out code here"
            #command = "cd " + self.txmud_src_path + " && svn up --username osdi2012 --password=oej5Deec "
            #ssc.run_command(command)
            command = "cd " + self.txmud_src_path + " && ant clean && ant"
            ssc.run_command(command)
            
    def deploy_tomcat(self, ssc):
        
        print "\n ===> Downloading Tomcat6"
        
        if ssc.rexists(self.tomcat_top_path) == False:
            command = "wget -P "+self.top_path+" -c https://myming.googlecode.com/files/apache-tomcat-6.0.35.tar.gz"
            ssc.run_command(command)
        
            print "\n ===> Installing Tomcat6"
            command = "tar xzvf "+self.top_path+"apache-tomcat-6.0.35.tar.gz -C "+self.txmud_top_path+"  > /dev/null"
            ssc.run_command(command)
        
            command = "mv "+self.txmud_top_path+"/apache-tomcat-6.0.35 " + self.txmud_top_path+"/tomcat6"
            ssc.run_command(command)
            self.tune_tomcat(ssc)
        else:
            print "tomcat directory already exists"
        
    def deploy_mysql_driver(self, ssc):
        print "\n ===> downloading mysql driver"
        
        if ssc.rexists(self.tomcat_lib_path+"/mysql-connector-java-5.1.17-bin.jar") == False:
            command = "wget -P "+self.top_path+" -c http://crocket-slackbuilds.googlecode.com/files/mysql-connector-java-5.1.17.zip"
            ssc.run_command(command)
        
            print "Deploying mysql driver on tomcat lib dir "
            command = "mkdir -p " + self.tomcat_lib_path
            ssc.run_command(command)
        
            command = "cd "+self.top_path+" && unzip mysql-connector-java-5.1.17.zip "
            ssc.run_command(command)
        
            command = "cp "+self.top_path+"mysql-connector-java-5.1.17/mysql-connector-java-5.1.17-bin.jar " + self.tomcat_lib_path
            ssc.run_command(command)
        
            command = "cp "+self.top_path+"mysql-connector-java-5.1.17/mysql-connector-java-5.1.17-bin.jar /tmp"
            ssc.run_command(command)
        
            command = "rm -rf "+self.top_path+"mysql-connector-java-5.1.17"
            ssc.run_command(command)
        else:
            print "mysql driver already installed"
        
        
    def deploy_txmud_components(self, ssc):
        print "\n ===> deploy txmud components"
        command = "rm -f " + self.tomcat_lib_path + "/jsqlparser.jar " + self.tomcat_lib_path + "/netty-3.2.1.Final.jar "
        command += self.tomcat_lib_path + "/log4j-1.2.15.jar " + self.tomcat_lib_path + "/jdbctxmud.jar " + self.tomcat_lib_path + "/georeplication.jar"
        ssc.run_command(command)
        
        #command = "cp " + self.jdbcTxMudJar + " " + self.tomcat_lib_path
        #ssc.run_command(command)
        command = "cp " + self.logJar + " " + self.tomcat_lib_path
        ssc.run_command(command)
        
        #remote copy
        ssc.put(self.tomcat_lib_path + "/jsqlparser.jar", self.jsqlparserJar)
        ssc.put(self.tomcat_lib_path + "/netty-3.2.1.Final.jar", self.nettyJar)
        #ssc.put(self.tomcat_lib_path + "/georeplication.jar", self.sifterJar)
        ssc.put(self.tomcat_lib_path + "/" + self.vascoJar.split("/")[-1], self.vascoJar)
        
    def tune_tomcat(self, ssc):
        print "\n ===> Tuning tomcat server"
        command = "sed  -i \'2s/^/JAVA_OPTS=\"\$JAVA_OPTS -Xms"+self.tomcatMem+"\"/\' "+self.tomcat_top_path+"/bin/catalina.sh"
        ssc.run_command(command)
        
        command = "sed -i  \'/<Connector port=\"8080\" protocol=\"HTTP\/1\.1\"/{p;s/.*/maxThreads=\"10000\" minSpareThreads=\"200\"/;}\'  "+self.tomcat_top_path+"/conf/server.xml"
        ssc.run_command(command)
        
    def deploy_website(self, ssc):
        print "\n ===> deploy website"
        self.compile_txmud(ssc)
        self.deploy_tomcat(ssc)
        self.deploy_mysql_driver(ssc)
        self.deploy_txmud_components(ssc)
       
    def configure_proxy(self, ssc, dcId, proxyId): 
        print "change db access url"
        s = self.dcs[dcId]
        databaseHost = s.databases[0][0].hostname
        databasePort = s.databases[0][1]
        print "change proxy to connect to database ", databaseHost, databasePort
        command = "sed -i '/datasource.url/c  \datasource.url    jdbc:mysql://"+str(databaseHost)+":"+str(databasePort)+"/rubis? \'  "+self.proxy_root_path+"/mysql.properties" 
        ssc.run_command(command)
        
        print "install website"
        command = "cd "+self.proxy_root_path + " && ant clean undeploy dist deploy -Dbackend="+self.backend+" -Dtotalproxy="+str(self.wpNum) +" -DdcCount="+str(self.dcNum)
        command += " -DdcId="+str(dcId) + " -DproxyId="+str(proxyId) + " -Ddbpool=100"
        command += " -DschemaPath=" + self.top_path+"/"+self.annotatedSqlFile.split('/')[-1] + " -DwpFilePath=" + self.top_path + "/"+self.wpFile.split('/')[-1]
        ssc.run_command_long(command)
    
    def configure_all_proxy_websites(self):
        print "install proxy all websites"
        for s in self.dcs:
            for x in range(0,s.proxyNum):
                wpPrefix = "proxy-"+str(s.dcId) + "-" + str(x)
                ssc = self.sshList[wpPrefix]
                self.configure_proxy(ssc, s.dcId,x)
   
    def configure_all_user_websites(self):
        print "install all user websites"
        for s in self.dcs:
            for x in range(0,s.userNum):
                userPrefix = "user-"+str(s.dcId) + "-" + str(x)
                ssc = self.sshList[userPrefix]
                command = "sed -i '/workload_up_ramp_time_in_ms/c  \workload_up_ramp_time_in_ms  ="+str(self.warmUpTime) + "\' " + self.clientDeployedPropertiesFile
                command += " && " + "sed -i '/workload_session_run_time_in_ms/c  \workload_session_run_time_in_ms  ="+str(self.measureTime) + "\' " + self.clientDeployedPropertiesFile
                command += " && " + "sed -i '/workload_down_ramp_time_in_ms/c  \workload_down_ramp_time_in_ms  ="+str(self.tearDownTime) + "\' " + self.clientDeployedPropertiesFile
                #change the proxy ip
                connectDcId = int(s.userProxy[x][0])
                connectProxyId = int(s.userProxy[x][1])
                print "try to configure user ", s.dcId, x
                print "connect to ", connectDcId, connectProxyId
                wpIP = self.dcs[connectDcId].webproxies[connectProxyId][0].hostname
                command += " && sed -i '/httpd_hostname/c \httpd_hostname ="+wpIP+"\' "+self.clientDeployedPropertiesFile
                ssc.run_command(command)
                
                print "try to configure user to use the transition table " + self.clientDeployedTransitionTableFile
                command = "sed -i '/workload_transition_table/c \workload_transition_table =" + self.clientDeployedTransitionTableFile + "\' " + self.clientDeployedPropertiesFile
                ssc.run_command(command)
                
    def remove_other_webapp_deployment(self, ssc):
        print "remove all other deployment to avoid inteference"
        prefix = "tpcw"
        command = "rm -rf " + self.webappDeployDir + "/"+prefix +"*"
        ssc.run_command(command)
    
    def deploy_remote_proxies(self):
        print "\n ===> deploy proxies to remote nodes"
        for s in self.dcs:
            for x in range(0,s.proxyNum):
                wpPrefix = "proxy-"+str(s.dcId) + "-" + str(x)
                ssc = self.sshList[wpPrefix]
                self.copy_files_rubis(ssc)
                self.remove_other_webapp_deployment(ssc)
                self.deploy_website(ssc)
                
    def copy_files_rubis(self, ssc):
        print "\n ===> copy files to rubis"   
        ssc.put(self.proxy_root_path+"/rubis_txmud_db.xml", self.dbFile)
        ssc.put(self.proxy_root_path + "/rubis_txmud.xml", self.dcFile)
        
        ssc.put(self.top_path + "/" + self.annotatedSqlFile.split('/')[-1], self.annotatedSqlFile)
        ssc.put(self.top_path + "/" + self.wpFile.split('/')[-1], self.wpFile)
                
    def deploy_remote_users(self):
        print "\n ===> deploy users to remote nodes"
        for s in self.dcs:
            for x in range(0,s.userNum):
                userPrefix = "user-"+str(s.dcId) + "-" + str(x)
                ssc = self.sshList[userPrefix]
                command = "rm -rf " + self.top_path + "/"+self.clientJar.split("/")[-1]
                ssc.run_command(command)
                #self.deploy_website(ssc)
                #cp two things, a rubis.properties
                #cp client jar file
                print "copy jar file  to client node", s.dcId, x
                ssc.put(self.top_path+"/"+self.clientJar.split("/")[-1],self.clientJar)
                print "copy client properties to client node", s.dcId, x
                ssc.put(self.clientDeployedPropertiesFile, self.clientPropertiesFile)
                
                print "copy client transition table to client node", s.dcId, x
                ssc.put(self.clientDeployedTransitionTableFile, self.clientTransitionTableFile)
                
                command = "mkdir " + self.top_path + "/bench"
                ssc.run_command(command)
                
    def start_lockserver(self, lsId):
        lockServerPrefix = "lockserver-" + str(lsId)
        ssc = self.sshList[lockServerPrefix]
        command = "cd " + self.top_path + " && "
        command += "nohup java -Xms4000m -Xmx8000m -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseConcMarkSweepGC -cp " 
        command += self.vasco_jar_name + ":./lib/* org.mpi.vasco.coordination.protocols.centr.ReplicatedLockService "
        command += self.top_path + "/" + self.vasco_config_xml.split("/")[-1] + " " + str(lsId) 
        command += " &> lockserver-"+str(lsId)+".txt &"
        ssc.run_command(command, True)
        sleep(10)
        isDone = ssc.checkProcessAlive("java")
        if isDone:
            print "set up lockserver", lsId
            return True
        else:
            print "failed to set up lockserver", lsId
            return False
        
    def start_all_lockservers(self):
        print "try to start all lockservers"
        for lsId in range(0, self.lockServerClients.getLockServerCount()):
            isDone = self.start_lockserver(lsId)
            if isDone == False:
                return False
        return True
        
    def stop_lockserver(self, lsId):
        lockServerPrefix = "lockserver-" + str(lsId)
        ssc = self.sshList[lockServerPrefix]
        command = "rm -rf /tmp/*.log && rm -rf " + self.top_path + "/config/currentView"
        ssc.run_command(command)
        ssc.killAllProcessesBySpecifiedPattern("java")
        
    def start_rubisproxy(self, dcObj, wpId):
        dcId = dcObj.dcId
        wpPrefix = "proxy-" + str(dcId) +"-" +str(wpId)
        ssc = self.sshList[wpPrefix]
        command = "cd "+self.proxy_root_path + " && ant start"
        ssc.run_command(command, True)
        sleep(1)
        isDone = ssc.checkProcessAlive("java")
        if isDone:
            print "set up webproxy", dcId, wpId
            return True
        else:
            print "failed to set up webproxy", dcId, wpId
            return False
        
    def start_all_rubisproxy(self):
        print "try to start all proxies"
        for s in self.dcs:
            for x in range(0,s.proxyNum):
                isDone = self.start_rubisproxy(s, x)
                if isDone == False:
                    return False
        return True
        
    def stop_rubisproxy(self, dcId, wpId):
        proxyPrefix = "proxy-" + str(dcId)+"-" + str(wpId)
        ssc = self.sshList[proxyPrefix]
        ssc.killAllProcessesBySpecifiedPattern("tomcat")
            
    def start_user(self, dcObj, userId):
        dcId = dcObj.dcId
        ssc = self.sshList["user-"+str(dcObj.dcId)+"-"+str(userId)]
        connectDcId = int(self.dcs[dcObj.dcId].userProxy[userId][0])
        connectProxyId = int(self.dcs[dcObj.dcId].userProxy[userId][1])
        print "try to start user ", dcObj.dcId, userId
        print "connect to ", connectDcId, connectProxyId
        
        #change the user number
        command = "cd " + self.client_deploy_path + " && sed -i '/workload_number_of_clients_per_node/c \workload_number_of_clients_per_node ="+str(self.simulateUserNum)+"\' rubis.properties"
        command += " && nohup java -cp \"rubis_client.jar:./\" edu.rice.rubis.client.ClientEmulator "+ str(dcId) + " " + str(userId) + " &> user"+str(dcId)+"-"+str(userId)+".log &"
        ssc.run_command(command, True)
        
        sleep(1)
        isDone = ssc.checkProcessAlive("java")
        if isDone:
            print "set up user", dcId, userId
            return True
        else:
            print "failed to set up user", dcId, userId
            return False
        
    def start_all_users(self):
        print "try to start all users"
        for dcObj in self.dcs:
            if self.start_all_users_one_dc(dcObj) == False:
                return False
        return True
    
    def start_all_users_one_dc(self, dcObj):
        for userId in range(0, dcObj.userNum):
            if self.start_user(dcObj, userId) == False:
                return False
        return True
        
    def stop_user(self, dcId, userId):
        print "killall user ", dcId, userId
        ssc = self.sshList["user-"+str(dcId)+"-"+str(userId)]
        ssc.killAllProcessesBySpecifiedPattern("java")
        
    def check_user_ready(self): 
        for s in self.dcs:
            for x in range(0,s.userNum):
                ssc = self.sshList["user-"+str(s.dcId)+"-"+str(x)]
                checkUserFinished(ssc, self.userName)
        
    def kill_remote_process(self):
        
        print "\n ==> kill all remote process"    
        for dc in self.dcs:
            dcId = dc.dcId
            if dc.coorNum > 0:
                self.stop_coordinator(dcId)
            for x in range(0,dc.sshimNum):
                self.stop_storageshim(dcId, x)
            for x in range(0,dc.dbNum):
                self.stop_database(dcId, x)
            for x in range(0,dc.proxyNum):
                self.stop_rubisproxy(dcId, x)
            for x in range(0, dc.userNum):
                self.stop_user(dcId, x)
            
                
                
    def move_logfiles(self):
        
        print "copy coordinator and data writer log"
        for k,v in self.sshList.items():
            #first get file list
            if k.find("user") == -1 and k.find("proxy") == -1 and k.find("db") == -1:
                logFileList = v.getLogFileList(self.top_path)
                if logFileList <> None:
                    for x in logFileList:
                        v.get(self.top_path+"/"+x, self.shareFolder+"/"+x)
                else:
                    print  k, "doesn't produce any files" 
                
        print "copy webproxy file"
        for dcObj in self.dcs:
            for x in range(0,dcObj.proxyNum):
                ssc = self.sshList["proxy-"+str(dcObj.dcId) + "-" + str(x)]
                logFileList = ssc.getFileList(self.tomcat_log_path)
                if logFileList<> None:
                    for logFile in logFileList:
                        ssc.get(self.tomcat_log_path+"/" + logFile, self.shareFolder +  "/"+logFile+".dcid"+str(dcObj.dcId) +".proxyid" +str(x) )
                else:
                    print "catalina.out dosen't exist ", dcObj.dcId, x
        
        print "copy user file"
        for dcObj in self.dcs:
            for x in range(0,dcObj.userNum):
                ssc = self.sshList["user-"+str(dcObj.dcId) + "-" + str(x)]
                logFileList = ssc.getUserLogFileList(self.user_log_path)
                if logFileList <>None:
                    #first compress the file and then download this file, and then uncompress
                    command = "cd "+self.user_log_path+" && tar -cvf rubis_dcId"+str(dcObj.dcId)+"_userId"+str(x)+".tar --exclude='*.jar'  --exclude='.properties' ./"
                    ssc.run_command(command)
                    tarFile = "rubis_dcId"+str(dcObj.dcId)+"_userId"+str(x)+".tar"
                    ssc.get(self.user_log_path+"/"+tarFile, self.shareFolder + "/"+tarFile)
                else:
                    print "user ", dcObj.dcId, x , "doesn't generate log files"
                        
    def check_proxies_ready(self):
        for dcObj in self.dcs:
            for x in range(0,dcObj.proxyNum):
                if checkTomcatProxyReady(self.sshList["proxy-" + str(dcObj.dcId) +"-" +str(x)], self.tomcat_log_path, dcObj.dcId, x) == False:
                    return False
                else:
                    continue
        return True
                
    def check_all_proxies_ready(self):
        while True:
            if self.check_proxies_ready() == True:
                return
            else:
                sleep(20)  
                
    '''
    The deploy experiment is to deploy the code to all machines
    '''
    def deploy_experiment(self):
        print "\n ===> deploy experiment"
        self.initiateDatacenters()
        self.getLockServerClients()
        self.writeXmls()
        self.createConnections()
        print "\n ===> prepare local code and jars"
        self.prepareCode()
        
        #deploy coordinator and storageshim
        print "\n ===> deploy coordinator and storageshim remotely"
       #if self.isAmazon == False:
        self.copyCodeToRemote()
            
        #copy website//TODO: here
        self.deploy_remote_proxies()
        self.deploy_remote_users()
        
        print "\n ===> experiment is deployed!"
    
    def configure_experiment(self):
        print "\n ===> configure experiment"
        self.initiateDatacenters()
        self.getLockServerClients()
        self.writeXmls()
        self.createConnections()
        self.copyFilesToRemote()
        
        self.configure_all_proxy_websites()
        self.configure_all_user_websites()
    
    def prepare_experiment(self):
        print "prepare connections"
        self.initiateDatacenters()
        self.getLockServerClients()
        self.writeXmls()
        self.createConnections()
 
    def cleanFiles(self):
        print "clean files"
        coorCommand = " rm " + self.top_path + "/*.log; rm " + self.top_path + "/*.txt"  + "; rm " + self.top_path + "/config/currentView"
        sshimCommand = " rm " + self.top_path + "/*.log; rm " + self.top_path + "/*.txt" 
        proxyCommand = "rm " + self.tomcat_log_path + "/* "
        userCommand = "rm -rf " + self.client_deploy_path+"/*.log && rm -rf " + self.user_log_path + "/rubis_dcId*"
        for dc in self.dcs:
            #coordinator
            if dc.coorNum > 0:
                coorPrefix = "coor-"+str(dc.dcId)
                ssc = self.sshList[coorPrefix]
                ssc.run_command(coorCommand)
            #data writer
            storagePrefix = "sshim-"+str(dc.dcId)
            for k, v in dc.storageshims.items():
                ssc = self.sshList[storagePrefix+"-"+str(k)]
                ssc.run_command(sshimCommand)
            proxyPrefix = "proxy-"+str(dc.dcId)
            for k,v in dc.webproxies.items():
                ssc = self.sshList[proxyPrefix+"-"+str(k)]
                ssc.run_command(proxyCommand)
            userPrefix = "user-"+str(dc.dcId)
            for k,v in dc.users.items():
                ssc = self.sshList[userPrefix+"-"+str(k)]
                ssc.run_command(userCommand)
        
        print "\n ===> additionally clean all currentview on all lockservers"
        for lsId in range(0, self.lockServerClients.getLockServerCount()):
            self.stop_lockserver(lsId)
        
    def logOut(self):
        for k,v in self.sshList.items():
            v.close()
            
    def finish_experiment(self):
        print "\n ===> finish experiment"
        self.kill_remote_process()
        self.move_logfiles()
        print "finish to copy data and clean systems"
        
    def run_test(self, folderPath,appThdCount, proxyThdCount, coorThdCount, sshimThdCount, userNum, blueToken, timeout, bluequietTime):
        print "\n ===>run test now"
        self.kill_remote_process()
        self.setUpNetwork()
        self.cleanFiles()
        self.shareFolder = folderPath
        self.appThdCount = appThdCount
        self.proxyThdCount = proxyThdCount
        self.coorThdCount = coorThdCount
        self.sshimThdCount = sshimThdCount
        self.blueToken = blueToken
        self.timeout = timeout
        self.bluequietTime = bluequietTime
        self.simulateUserNum = userNum
        
        self.clean_database()
        self.checkDatabases()
        sleep(10)
        self.preload_databases()
        self.refresh_databases()
        sleep(20)
        if self.start_all_lockservers():
            if self.start_all_coordinator():
                if self.start_all_storageshim():
                    self.wait_for_storageshims()
                    if self.start_all_rubisproxy():
                        self.check_all_proxies_ready()
                        if self.start_all_users():
                            self.check_user_ready()
                            self.finish_experiment()
                            print "already finished the test"
                            return True
        else:
            self.finish_experiment()
            print "some webproxies failed to connected to zookeeper or failed to set up, please check"
            return False
    
            
    
        
    
    
    
