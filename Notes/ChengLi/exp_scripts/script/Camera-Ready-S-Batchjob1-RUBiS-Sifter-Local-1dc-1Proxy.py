import os,sys
from time import time,sleep

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "python batchjob.py wantToDeploy[Deploy|Config|Run]"
        sys.exit()
        
    option = sys.argv[1:]
    wantToDeploy = option[0]
    password = "aa"
        
    dpsDir = "/DPS/TxMud/archive00/SIEVE/DATA/RUNTIME/CameraReady/RUBiS/SIEVE/NoReplication"
    command = "python rubisSifterExpeRun.py 139.19.168.56 " + dpsDir + " chengli " +password+ " rubis_txmud_db1dc.xml rubis Camera-Ready-Rubis1dc1proxyLocalConfigSifter.txt notused  20 10 20 20 nondebug Local Camera-ReadyNodesRUBiSSifter1dc1Proxy.db " + wantToDeploy
    print command, "is running"
    os.system(command)
    print command, "finished"
    
    sys.exit(-1)
    
   
