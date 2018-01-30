import os,sys
from time import time,sleep

if __name__ == '__main__':
    
    if len(sys.argv) != 1:
        print "python batchjob.py"
        sys.exit()
    
    print "we run the gemini and sieve experiments of RUBiS all together"
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Deploy"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Config"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob183-RUBiS-Gemini-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    print "switching to another one, please"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Deploy"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Config"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    command = "python batchjob171-RUBiS-Sifter-Local-1dc-1Proxy-AvgLatency.py Run"
    print command, "is running"
    
    os.system(command)
    print command, "finished"
    
    sys.exit(-1)
    
   
