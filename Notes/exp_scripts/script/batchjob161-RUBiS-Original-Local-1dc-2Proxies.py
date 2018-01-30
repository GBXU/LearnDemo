import os,sys
from time import time,sleep

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "python batchjob.py wantToDeploy[Deploy|Config|Run]"
        sys.exit()
        
    option = sys.argv[1:]
    wantToDeploy = option[0]
    password = "aa"
        
    dpsDir = "/DPS/TxMud/archive00/SIEVE/DATA/RUNTIME/RUBiS/Original/LATENTHPUT"
    command = "python rubisOrigExpeRun.py 139.19.131.115 " + dpsDir + " chengli " +password+ " rubis_txmud_db1dc.xml rubis rubis1dc2proxiesLocalConfigOrig.txt notused  nondebug Local nodesRUBiSOrig1dc2Proxies.db " + wantToDeploy
    print command, "is running"
    os.system(command)
    print command, "finished"
    
    sys.exit(-1)
    
   
