from time import time, sleep
import os, sys
lib_path = os.path.abspath('../util')
sys.path.append(lib_path)
from datacenter import *
from dataCenterUtil import *
from tpcwParser import *
from nodeParser import *
from checking import *
from svn_compile import *


class experi_handler():
    def __init__(self, userName, path, debug):
        print "experiment handler initialization"
        self.userName = userName
        self.top_path = path
        self.txmud_src_path = "/home/"+self.userName+"/java"
        self.txmud_top_path = path + "txmud"
        self.tomcat_top_path = self.txmud_top_path + "/tomcat6"
        self.tomcat_lib_path = self.tomcat_top_path + "/lib"
        self.tomcat_log_path = self.tomcat_top_path + "/logs"
        
        self.debug = debug
        
        self.coordinatorJar = ""
        self.storageshimJar = ""
        self.proxyJar = ""
        self.userJar = ""
        
        #some parameters for tpcw 
        self.jdbcTxMudJar = ""
        self.jsqlparserJar = ""
        self.nettyJar = ""
        self.logJar = ""
        self.rubis_root_path = "/home/"+self.userName+"/java/src/applications/RUBiStxmud/"
        self.proxy_root_path = self.rubis_root_path + "Servlets"
        self.client_root_path = self.rubis_root_path + "Client"
        self.txmud_outputdir = self.tomcat_lib_path + "/output/txmud"
        
        self.txmud_binary = self.txmud_outputdir + "/dist"
        #tomcat
        self.tomcatMem = "4G"
                        
    def prepareCode(self):
        #create jar files
        print "create jar files"
        jarFilePath = svn_checkout_compile(self.debug,"/home/"+userName)
        jarFilePath = "/var/tmp/"+userName+"/output/txmud/dist/"
        #command = "cd " + self.txmud_src_path + " && ant clean && ant "
        #os.system(command)
        jarFilePath = "/var/tmp/"+self.userName+"/output/txmud/dist/"
        self.coordinatorJar = jarFilePath+"coordinator-big.jar"
        self.storageshimJar = jarFilePath+"storageshim-big.jar"
        
        libJarFilePath = "/home/"+self.userName+"/java/lib/"
        
        #rubis jars
        self.jdbcTxMudJar = jarFilePath + "jars/jdbctxmud.jar"
        self.jsqlparserJar = libJarFilePath + "jsqlparser.jar"
        self.nettyJar = libJarFilePath + "netty-3.2.1.Final.jar"
        self.logJar = libJarFilePath + "log4j-1.2.15.jar"
            
    def compile_txmud(self):
        self.prepareCode()
        command = "mkdir " + self.top_path + "; mkdir " + self.txmud_top_path
        print command
        os.system(command)
        
        print "\n ===> compile txmud"
        command = "cd " + self.txmud_src_path + " && ant clean && ant"
        print command
        os.system(command)
            
    def deploy_tomcat(self):
        
        print "\n ===> Downloading Tomcat6"
        
        if os.path.exists(self.tomcat_top_path) == False:
            command = "wget -P "+self.top_path+" -c http://www.bitlib.net/mirror/apache.org/tomcat/tomcat-6/v6.0.35/bin/apache-tomcat-6.0.35.tar.gz"
            print command
            os.system(command)
        
            print "\n ===> Installing Tomcat6"
            command = "tar xzvf "+self.top_path+"apache-tomcat-6.0.35.tar.gz -C "+self.txmud_top_path+"  > /dev/null"
            print command
            os.system(command)
        
            command = "mv "+self.txmud_top_path+"/apache-tomcat-6.0.35 " + self.txmud_top_path+"/tomcat6"
            print command
            os.system(command)
            self.tune_tomcat()
        else:
            print "tomcat directory already exists"
        
    def deploy_mysql_driver(self):
        print "\n ===> downloading mysql driver"
        
        if os.path.exists(self.tomcat_lib_path+"/mysql-connector-java-5.1.17-bin.jar") == False:
            command = "wget -P "+self.top_path+" -c http://ftp.gwdg.de/pub/misc/mysql/Downloads/Connector-J/mysql-connector-java-5.1.17.zip"
            os.system(command)
        
            print "Deploying mysql driver on tomcat lib dir "
            command = "mkdir -p " + self.tomcat_lib_path
            print command
            os.system(command)
        
            command = "cd "+self.top_path+" && unzip mysql-connector-java-5.1.17.zip "
            print command
            os.system(command)
        
            command = "cp "+self.top_path+"mysql-connector-java-5.1.17/mysql-connector-java-5.1.17-bin.jar " + self.tomcat_lib_path
            print command
            os.system(command)
        
            command = "cp "+self.top_path+"mysql-connector-java-5.1.17/mysql-connector-java-5.1.17-bin.jar /tmp"
            print command
            os.system(command)
        
            command = "rm -rf "+self.top_path+"mysql-connector-java-5.1.17"
            print command
            os.system(command)
        else:
            print "mysql driver already installed"
        
        
    def deploy_txmud_components(self):
        print "\n ===> deploy txmud components"
        command = "rm -f " + self.tomcat_lib_path + "/jsqlparser.jar " + self.tomcat_lib_path + "/netty-3.2.1.Final.jar "
        command += self.tomcat_lib_path + "/log4j-1.2.15.jar " + self.tomcat_lib_path + "/jdbctxmud.jar"
        print command
        os.system(command)
        
        command = "cp " + self.jsqlparserJar + " " + self.tomcat_lib_path
        print command
        os.system(command)
        command = "cp " + self.jdbcTxMudJar + " " + self.tomcat_lib_path
        print command
        os.system(command)
        command = "cp " + self.nettyJar + " " + self.tomcat_lib_path
        print command
        os.system(command)
        command = "cp " + self.logJar + " " + self.tomcat_lib_path
        print command
        os.system(command)
        
    def tune_tomcat(self):
        print "\n ===> Tuning tomcat server"
        command = "sed  -i \'2s/^/JAVA_OPTS=\"\$JAVA_OPTS -Xms"+self.tomcatMem+"\"/\' "+self.tomcat_top_path+"/bin/catalina.sh"
        print command
        os.system(command)
        
        command = "sed -i  \'/<Connector port=\"8080\" protocol=\"HTTP\/1\.1\"/{p;s/.*/maxThreads=\"10000\" minSpareThreads=\"200\"/;}\'  "+self.tomcat_top_path+"/conf/server.xml"
        print command
        os.system(command)
        
    def deploy_website(self):
        print "\n ===> deploy website"
        self.compile_txmud()
        self.deploy_tomcat()
        self.deploy_mysql_driver()
        self.deploy_txmud_components()
        
        print "install website"
        command = "cd "+self.proxy_root_path+" && ant clean undeploy dist "
        print command
        os.system(command)
        
        print "compile client"
        command = "cd " + self.client_root_path + " && sed -i '/workload_remote_client_command/c  \workload_remote_client_command  =/home/"+self.userName+"/java/src/applications/RUBiStxmud/Client edu.rice.rubis.client.ClientEmulator\' rubis.properties"
        command += " && sed -i '/workload_transition_table/c  \workload_transition_table  =/home/"+self.userName+"/java/src/applications/RUBiStxmud/workload/transitions.txt\' rubis.properties"
        command += " && sed -i '/database_regions_file/c  \database_regions_file  =/home/"+self.userName+"/java/src/applications/RUBiStxmud/database/ebay_regions.txt\' rubis.properties"
        command += " && sed -i '/database_categories_file/c  \database_categories_file  =/home/"+self.userName+"/java/src/applications/RUBiStxmud/database/ebay_simple_categories.txt\' rubis.properties"
        os.system(command)
        
        #need to change here
        command = "cd " + self.client_root_path + " && ant clean && ant"
        os.system(command)
        
        
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "python rubisDeployment.py username"
        sys.exit()
        
    option = sys.argv[1:]
    userName = option[0]
    path = "/var/tmp/"+userName+"/"
        
    exp = experi_handler(userName, path, "nondebug")
    exp.deploy_website()

                
    
            
    
        
    
    
    