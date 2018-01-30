import MySQLdb
import string
import os,sys
import math
from time import time, sleep
import random
random.seed()
from sshcontroller import *
from util import *

#random string
char_set = string.ascii_lowercase

databaseTopDir = "/var/tmp/chengli/"
databaseDir = "/var/tmp/chengli/mysql-5.5.18"

def getDatabaseFile(dcNum, expName):
    if expName == "sifter" or expName == "txmud":
        if dcNum == 1:
            return "/var/tmp/chengli/mysql-5.5.18.1dc.lc0-0.rubis.tar.bz2"
        elif dcNum == 2:
            return "/var/tmp/chengli/mysql-5.5.18.2dc.lc0-0-0.rubis.tar.bz2"
        elif dcNum == 3:
            return "/var/tmp/chengli/mysql-5.5.18.3dc.lc0-0-0-0.rubis.tar.bz2"
        else:
            print "no available database"
            sys.exit()
    elif expName == "vasco" or expName == "mysql":
        if dcNum == 1:
            return "/var/tmp/chengli/mysql-5.5.18.1dc.lc0.rubis.vasco.tar.bz2"
        elif dcNum == 2:
            return "/var/tmp/chengli/mysql-5.5.18.2dc.lc0-0.rubis.vasco.tar.bz2"
        elif dcNum == 3:
            return "/var/tmp/chengli/mysql-5.5.18.3dc.lc0-0-0.rubis.vasco.tar.bz2"
        else:
            print "no available database"
            sys.exit()


def getLogical_clock(dcNum, expName):
    lc = ""
    if expName == "sifter" or expName == "txmud":
        for x in range(0,dcNum):
            lc += "0-"
        lc += "0"
    elif expName == "vasco":
        lc = "0"
        for x in range(1,dcNum):
            lc += "-0"
    else:
        print "invalid exp name"
        sys.exit()
    return lc

def getRandomString(length):
    rStr = ''.join(['a' for i in range(length)]) 
    return rStr

def stopMySQLServer(ssc):
    print "stop mysql server here"
    while True:
        command = "kill -9 $(pidof mysqld)"
        ssc.run_command(command)
        isAlive = ssc.checkProcessAlive("mysqld")
        if isAlive:
            print "not killed, try again"
        else:
            print "already kill mysqld"
            break
    
    command = "rm /tmp/mysql.sock"
    ssc.run_command(command)
        
def clearBinLog(sshHandler): #try to release space for database
    print "clear bin log"
    command = "cd " + databaseDir+"/data; rm mysqld-bin*;"
    sshHandler.run_command(command)
    command = "cd " + databaseDir+"/data; rm ib_logfile*;"
    sshHandler.run_command(command)
        
def startMySQLServer(ssc):
    print "start mysql server here"
    clearBinLog(ssc)
    while True:
        command = "cd "+databaseDir+"/bin;"
        command += "nohup ./mysqld_safe --defaults-file=../mysql-test/include/default_mysqld.cnf --port=50000 --innodb_lock_wait_timeout=1 --max_connections=5000 --innodb_buffer_pool_size=8G --innodb_flush_method=O_DIRECT --skip-innodb_doublewrite --innodb_flush_log_at_trx_commit=0 --innodb_log_file_size=128M --disable-log-bin --innodb_log_buffer_size=8M --open-files-limit=5000 --table_open_cache=5000 --transaction-isolation=REPEATABLE-READ --query_cache_size=512M> mysqld.log &"
        ssc.run_command(command, True)
        isAlive = ssc.checkProcessAlive("mysqld")
        if isAlive:
            print "ok you started mysqld"
            break
        else:
            print "failed to start mysqld"

def executeQuery(cur, sqlStr):
    try:
        cur.execute(sqlStr)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        if e.args[1].find("Duplicate") == -1:
            sys.exit (1)
            
def executeSelect(cur, selectStr):
    
    try:
        cur.execute(selectStr)
    except MySQLdb.Error, e:
        sys.exit(1)
    rows = cur.fetchall()
    for row in rows:
        print "%s, %s" % (row[0], row[1])
    print "Number of rows returned: %d" % cur.rowcount

def creatDB(cur):
    ## drop db and create a new db
    sqlStr = "drop database if exists micro;"
    executeQuery(cur, sqlStr)
    sqlStr = "create database micro;"
    executeQuery(cur, sqlStr)
    
def selectDB(cur):
    sqlStr = "use micro;"
    executeQuery(cur, sqlStr)
    
def createScratchpadTables(cur):
    
    sqlStr = "CREATE TABLE IF NOT EXISTS SCRATCHPAD_ID ( k int NOT NULL primary key, id int);"
    executeQuery(cur, sqlStr)
    sqlStr = "INSERT INTO SCRATCHPAD_ID VALUES ( 1, 1);"
    executeQuery(cur, sqlStr)
    sqlStr = "CREATE TABLE IF NOT EXISTS SCRATCHPAD_TRX ( k int NOT NULL primary key, id int);"
    executeQuery(cur, sqlStr)
    sqlStr = "INSERT INTO SCRATCHPAD_TRX VALUES ( 1, 1);"
    executeQuery(cur, sqlStr)
    

def createMicroSmallTables(cur):
    sqlStr = "create table t1 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(50)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
        
    sqlStr = "create table t2 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(50)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
    
    sqlStr = "create table t3 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(50)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
    
    sqlStr = "create table t4 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(50)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
        
        
def createMicroTables(cur):
    
    sqlStr = "create table t1 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(250),"
    sqlStr += "f char(250),"
    sqlStr += "g char(250),"
    sqlStr += "h char(250)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
        
    sqlStr = "create table t2 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(250),"
    sqlStr += "f char(250),"
    sqlStr += "g char(250),"
    sqlStr += "h char(250)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
    
    sqlStr = "create table t3 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(250),"
    sqlStr += "f char(250),"
    sqlStr += "g char(250),"
    sqlStr += "h char(250)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
    
    sqlStr = "create table t4 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e char(250),"
    sqlStr += "f char(250),"
    sqlStr += "g char(250),"
    sqlStr += "h char(250)," 
    sqlStr += "_SP_del BIT(1) DEFAULT FALSE," 
    sqlStr += "_SP_ts int default 0,"
    sqlStr += "_SP_clock varchar(100));"
    executeQuery(cur, sqlStr)
        
def insertRequestToMicroTables(cur, requestNum, dcNum):
    for x in range(requestNum):
        sqlStr = "insert into t1 values("
        a = x
        b = 1
        c = 1
        d = 1
        e = getRandomString(250)
        f = getRandomString(250)
        g = getRandomString(250)
        h = getRandomString(250)
        i = 0
        j = 1
        k = getLogical_clock(dcNum)
        sqlStr += str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e +"'" + ",'" + f +"'" +",'" + g +"'" +",'" + h +"'," +str(i) + "," +str(j) + ",'" +k + "');"
        #print sqlStr
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t2 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e +"'" + ",'" + f +"'" +",'" + g +"'" +",'" + h +"'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t3 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e +"'" + ",'" + f +"'" +",'" + g +"'" +",'" + h +"'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t4 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e +"'" + ",'" + f +"'" +",'" + g +"'" +",'" + h +"'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
    
def insertRequestToMicroSmallTables(cur, requestNum, dcNum):
    for x in range(requestNum):
        sqlStr = "insert into t1 values("
        a = x
        b = 1
        c = 1
        d = 1
        e = getRandomString(50)
        i = 0
        j = 1
        k = getLogical_clock(dcNum)
        sqlStr += str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "'," +str(i) + "," +str(j) + ",'" +k + "');"
        #print sqlStr
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t2 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t3 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t4 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "'," +str(i) + "," +str(j) + ",'" +k + "');"
        executeQuery(cur, sqlStr)
        
        
def createTables(cur):
    
    sqlStr = "create table t1 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e varchar(50));" 
    executeQuery(cur, sqlStr)
    
    #print "create table", sqlStr
        
    sqlStr = "create table t2 (a int NOT NULL primary key, "
    sqlStr += "b int unsigned,"
    sqlStr += "c int unsigned,"
    sqlStr += "d int unsigned," 
    sqlStr += "e varchar(50));" 
    executeQuery(cur, sqlStr)
    
def insertRequestToTables(cur, requestNum):
    max_primary_key = 10000
    sqlStr = "insert into t1 values("
    a = 1
    b = random.randint(0, max_primary_key)
    c = random.randint(0, max_primary_key)
    d = random.randint(0, max_primary_key)
    e = "abcde"
    sqlStr += str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "');"
    executeQuery(cur, sqlStr)
    sqlStr = "insert into t2 values("
    a = 1
    b = random.randint(0, max_primary_key)
    c = random.randint(0, max_primary_key)
    d = random.randint(0, max_primary_key)
    e = "abcde" 
    sqlStr += str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "');"
    executeQuery(cur, sqlStr)
    ratio = 0
    if requestNum < max_primary_key:
        tmp = 0.0
        tmp = float(max_primary_key/requestNum)
        ratio = int(round(tmp))
    else:
        ratio = 1
        requestNum = max_primary_key
    for x in range(requestNum):
        sqlStr = "insert into t1 values("
        a = (x*ratio) % max_primary_key
        b = random.randint(0, max_primary_key)
        c = random.randint(0, max_primary_key)
        d = random.randint(0, max_primary_key)
        #e = ''.join([random.choice(char_set) for i in range(random.randint(1,50))]) 
        e = "abcde"
        sqlStr += str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "');"
        #print sqlStr
        executeQuery(cur, sqlStr)
        
        sqlStr = "insert into t2 values("+str(a) + "," + str(b) + "," + str(c) + "," + str(d) + ",'" + e + "');"
        executeQuery(cur, sqlStr)
        
def initiateMicroDatabases(dbHost, dbPort, recordNum, dcNum):
    print "initiate database now"
    dbUser, dbPwd= "root","123456"
    try:
        dbconn = MySQLdb.connect (host=dbHost, port=dbPort, user=dbUser, passwd=dbPwd)
        cur = dbconn.cursor()
        
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        print 'Has Troubles to connect with Database'
        sys.exit (1)

    creatDB(cur)
    dbconn.commit()
    selectDB(cur)
    createScratchpadTables(cur)
    createMicroTables(cur)
    #insertRequestToMicroTables(cur, 300*self.uNum)
    insertRequestToMicroTables(cur, recordNum, dcNum)
    cur.close()
    dbconn.commit() 
    dbconn.close()
        
def backUpDatabase(sshHandler):
    #cp the data dir to initial
    print "back Up database"
    '''
    command = "rm -rf " + databaseDir + "/initial-micro"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    command = "cp -r " + databaseDir + "/data/micro " + databaseDir + "/initial-micro"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    
    command = "rm -rf " + databaseDir + "/initial-ib*"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    
    command = "cp " + databaseDir + "/data/ib_logfile0 " + databaseDir + "/initial-ib_logfile0"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    command = "cp " + databaseDir + "/data/ib_logfile1 " + databaseDir + "/initial-ib_logfile1"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    command = "cp " + databaseDir + "/data/ibdata1 " + databaseDir + "/initial-ibdata1"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    '''
    command = "rm -rf " + databaseDir + "/initial-data"
    sshHandler.run_command(command)
    
    command = "cp -r " + databaseDir + "/data " + databaseDir + "/initial-data"
    sshHandler.run_command(command)
    
def restoreDatabase(sshHandler):
    #cp the initial data dir to data dir
    print "restore Database"
    '''
    command = "rm -rf " + databaseDir + "/data/micro"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    
    command = "cp -r " + databaseDir +"/initial-micro " + databaseDir + "/data/micro"
    sshHandler.login()
    sshHandler.run_command(command)
    sshHandler.logout()
    
    '''
    command = "rm -rf " + databaseDir + "/data"
    sshHandler.run_command(command)
    
    command = "cp -r " + databaseDir +"/initial-data " + databaseDir + "/data"
    sshHandler.run_command(command)
    
def resetDatabase(sshHandler, isAmazon, expName, dcNum=1):
    command = "rm -rf " + databaseDir + "/data"
    sshHandler.run_command(command)
    
    databaseFile = getDatabaseFile(dcNum, expName)
    command = "tar -xf " + databaseFile + " -C " + databaseTopDir
    sshHandler.run_command(command)
    if isAmazon == False:
        command = "cd " + databaseDir 
    else:
        command = "cd " + databaseDir + " && chown -R mysql . && chgrp -R root ."
    sshHandler.run_command(command)
    
def checkDatabase(sshHandler, isAmazon):
    if isAmazon == True:
        command = "ps -u admin -o pid,state,command |grep -v PID | grep mysqld | grep -v safe | grep -v grep | awk '{print $2}'"
    else:
        command = "ps -u chengli -o pid,state,command |grep -v PID | grep mysqld | grep -v safe | grep -v grep | awk '{print $2}'"
    returnStr = sshHandler.run_command(command)
    if len(returnStr) == 0:
        print "database is not ready"
        return False
    returnStr = removeNewLine(returnStr) 
    print returnStr
    length = len(returnStr)
    if returnStr[length-1] == 'S':
        print "database already start up"
        return True
    else:
        print "database is not ready"
        return False
    
def refreshDatabase(sshHandler, isAmazon, activeItems, currentTs, minT, maxT):
    command = "cd " +databaseDir+"/bin && ./mysql --defaults-file=../mysql-test/include/default_mysqld.cnf --user=root --password=101010 --port=50000 rubis -e  \"update items set end_date  = \'"+currentTs+"\' + interval FLOOR("+str(minT)+"+(RAND(13)*"+str(maxT)+")) day where id <= "+str(activeItems)+"\""
    
    #command = "cd " +databaseDir+"/bin && ./mysql --defaults-file=../mysql-test/include/default_mysqld.cnf --user=root --password=101010 --port=50000 rubis -e  \"update items set end_date  = \'"+currentTs+"\' + interval FLOOR("+str(minT)+"+(RAND(13)*"+str(maxT)+")) day where id > "+str(olditems)+"\""
    sshHandler.run_command(command)
    

