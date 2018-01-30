#try to test the start-up.py

from startUpSifter import *
import datetime
import sys,os
lib_path = os.path.abspath('../util')
sys.path.append(lib_path)
from dataCenterUtil import *
from sshcontroller import *
from tpcwParser import *

ntfIP = ""
ntfPath = ""
userName = ""
pwd = ""
top_path = "" #path to java
        
def test1(configFile):
    userNumList, blueToken, expiredTime, bluequietTime, dataCenterList= getDCs(configFile)
    #rubis = getRubis(rubisConfigFile)
    dcNum = len(dataCenterList)
    wpNum = getProxyNum(dataCenterList)
    sshimNum = getSshimNum(dataCenterList)
    userNum = getUserNum(dataCenterList)
    
    print "\n ===> start create result folders"
    ssc = SSHController(Node(ntfIP , "chengli" , pwd, "/home/chengli/.ssh/id_rsa"))
    ssc.open()

    exp = experi_handler(testName,dataCenterList, dbFile, userName, pwd,top_path, debug, isAmazon, nodeFile)
    if deployConfig == "Deploy":
        print "You want to deploy the experiment since you haven't done yet or code has been changed!"
        exp.deploy_experiment()
        sys.exit(-1)
    elif deployConfig == "Config":
        print "You already deployed your code, now you want to config all of them"
        exp.configure_experiment()
        sys.exit(-1)
    else:
        print "You already deployed and configured your code, now you want to launch experiments, Good luck!"
        exp.prepare_experiment()
        
    #mkdir top directory
    command = "mkdir " + ntfPath
    ssc.run_command(command)
    prefix = str(dcNum) + "dc" + str(wpNum) + "proxy" + str(sshimNum) + "storage"+str(userNum) +"user" + "-" + "as" + str(appThdCount) + "-" + "p" + str(proxyThdCount) + "-" + "c" + str(coorThdCount) + "-ss" + str(sshimThdCount)
    folderName = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-"
    folderName += str(now.hour) + "-" + str(now.minute) +"-" + testName + "-"+ prefix
    folderPath = ntfPath+ "/" + folderName
    command = "rm -rf "+folderPath + "; mkdir " + folderPath
    ssc.run_command(command)
    
    #for each emulate user, we run experiment TODO://fix it
    for userNum in userNumList:
        subfolderPath = folderPath + "/simulateUser"+str(userNum)
        ssc.run_command("mkdir " + subfolderPath)
        exp.run_test(subfolderPath, appThdCount, proxyThdCount, coorThdCount, sshimThdCount, userNum, blueToken, expiredTime,bluequietTime)
    exp.logOut()
    #mv config.txt to that directory
    command= "scp " + configFile + " " + folderPath
    ssc.put(folderPath +"/"+configFile,configFile);

if __name__ == '__main__':
    '''
    option[0] => ntf IP
    option[1] => ntf path
    option[2] => userName
    option[3] => password
    option[4] => maxUserNum
    shareFolder => ntf folder to store the raw data
    path => the path to java
    userName => root in Amazon
    '''
    if len(sys.argv) != 17:
        print "Usage: python rubisSifterExpeRun.py ntfIP ntfPath userName pwd dbFile testName configFile tpcwConfigFile appThdCount proxyThdCount coorThdCount sshimThdCount debug isAmazon nodes.db DeployOrConfigOrRun"
        sys.exit()
    option = sys.argv[1:]
    now = datetime.datetime.now()
    ntfIP = option[0]
    ntfPath = option[1]
    userName = option[2]
    pwd = option[3]
    dbFile = option[4]
    testName = option[5]
    configFile = option[6]
    rubisConfigFile = option[7]
    appThdCount = int(option[8])
    proxyThdCount = int(option[9])
    coorThdCount = int(option[10])
    sshimThdCount = int(option[11])
    debug = option[12]
    if option[13] == "Amazon":
        isAmazon = True
    else:
        isAmazon = False
    nodeFile = option[14]
    deployConfig = option[15]
    assert (deployConfig == "Deploy" or deployConfig == "Config" or deployConfig == "Run")
    top_path = "/var/tmp/"+userName+"/"
    test1(configFile)
    sys.exit()
