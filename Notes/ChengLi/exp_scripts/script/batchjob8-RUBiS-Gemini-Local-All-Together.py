import os,sys
from time import time,sleep

if __name__ == '__main__':
    
    if len(sys.argv) != 1:
        print "python batchjob.py"
        sys.exit()
    
    print "we run the gemini experiments of RUBiS all together"
    command = "python batchjob186-RUBiS-Gemini-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob186-RUBiS-Gemini-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob186-RUBiS-Gemini-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob186-RUBiS-Gemini-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob186-RUBiS-Gemini-Local-1dc-1Proxy-BreakLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    sys.exit(-1)
    
   
