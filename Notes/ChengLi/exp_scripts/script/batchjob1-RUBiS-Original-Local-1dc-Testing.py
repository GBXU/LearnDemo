import os,sys
from time import time,sleep
import datetime

if __name__ == '__main__':
    
    if len(sys.argv) != 1:
        print "python batchjob.py password"
        sys.exit()
        
    #option = sys.argv[1:]
    #password = option[0]
    password = "aa"
        
    now = datetime.datetime.now()
    dpsDir = "/DPS/TxMud/archive00/1dc-LocalUser-Local-RUBiS-Orig-bidding-mix-new-output"
    
    command = "python rubisOrigExpeRun.py 139.19.131.115 " + dpsDir + " chengli " +password+ " rubis_txmud_db1dc.xml rubis rubis1dc1proxyOrigConfig.txt tpcw1dc1proxyRUBiSOrigConfig.txt  nondebug Local nodes.db"
    print command, "is running"
    os.system(command)
    print command, "finished"
    
    sys.exit(-1)
    
   
