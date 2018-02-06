import os,sys
from time import time,sleep

if __name__ == '__main__':
    
    if len(sys.argv) != 1:
        print "python batchjob.py"
        sys.exit()
    
    print "we run the sieve experiments of RUBiS all together"
    command = "python batchjob176-RUBiS-Sifter-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob172-RUBiS-Sifter-Local-2dc-2Proxies-Replication.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob172-RUBiS-Sifter-Local-2dc-2Proxies-Replication.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    sys.exit(-1)
    
   
