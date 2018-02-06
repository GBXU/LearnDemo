import paramiko
import sys,os,select,socket

paramiko.util.log_to_file('/var/tmp/chengli/paramiko.log') 

class SSHController:
    """Connect to remote host with SSH and issue commands.
    
    This is a facade/wrapper that uses Paraminko to spawn and control an SSH client. 
    You must have paraminko library installed. 
        
    @ivar node: Host name or IP address, User name, Password
    @ivar port: Ssh port
    @ivar ssh: instance of ssh client
    """
        
    def __init__(self, node): 
        """
            
        @ivar node connection parameters
        
        """
        print "create a connection controller"
        self.node = node    
        self.port = 22  #default SSH port
        self.ssh = None
        #str=self.node.log_handler.logname+".ssh"
        #paramiko.util.log_to_file(str)
        #self.logger = paramiko.util.logging.getLogger()
        self.sftp = None

    def __del__(self):
        """Close the socket in case it was left opened
        
            
        """
        if self.ssh != None:
            self.ssh.close()
   
   
    def agent_auth(self,transport, username):
        """
        Attempt to authenticate to the given transport using any of the private
        keys available from an SSH agent.
        """
        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        if len(agent_keys) == 0:
            return
    
        for key in agent_keys:
#            print 'Trying ssh-agent key %s' % hexlify(key.get_fingerprint()),
            try:
                transport.auth_publickey(username, key)
#                print '... success!'
                return
            except paramiko.SSHException:
 #               print '... nope.'
                return
   
    def open(self):
        username = self.node.username
        hostname = self.node.hostname
        port = self.port

        # now connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((hostname, port))
        except Exception, e:
            print '*** Connect failed: ' + str(e) +" check your network connection"
            sys.exit(1)

        t = paramiko.Transport(sock)

        try:
            t.start_client()
        except paramiko.SSHException:
            print '*** SSH negotiation failed. first attempt'
            print sys.exc_info()
            sys.exit(1)
 
        
        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print '*** Unable to open host keys file'
                keys = {}
        # check server's host key -- this is important.
#            key = t.get_remote_server_key()
#            if not keys.has_key(hostname):
#                print '*** WARNING: Unknown host key!'
#            elif not keys[hostname].has_key(key.get_name()):
#                print '*** WARNING: Unknown host key!'
#            elif keys[hostname][key.get_name()] != key:
#                print '*** WARNING: Host key has changed!!!'
#                sys.exit(1)
#            else:
#                print '*** Host key OK.'
        # get username
        self.agent_auth(t, username)
        self.ssh=t
        if not t.is_authenticated():
            t.close()
            self.open_old()
        
    

    def open_old(self):
        """Connect to a remote host and login.
        
        """
       
        # get host key, if we know one
        hostkeytype = None
        hostkey = None
        host_keys = None
        try:
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
                host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print '*** Unable to open host keys file'
                host_keys = {}
        
        print "type of host_keys", type(host_keys)
        #if host_keys.has_key(self.node.hostname):
        if self.node.hostname in host_keys:
            hostkeytype = host_keys[self.node.hostname].keys()[0]
            hostkey = host_keys[self.node.hostname][hostkeytype]
            #print 'Using host key of type %s' % hostkeytype
        
        
        # now, connect and use paramiko Transport to negotiate SSH2 across the connection
        #print self.node
        #it might use password or an RSA key file
        #print " parameters",self.node.hostname, self.port
   
        try:
            self.ssh = paramiko.Transport((self.node.hostname, self.port))
            key=None
            if self.node.keyfile!= None:
                try:
                    key = paramiko.RSAKey.from_private_key_file(self.node.keyfile)
                except paramiko.PasswordRequiredException:
                    key = paramiko.RSAKey.from_private_key_file(self.node.keyfile, self.node.password)
                    
                self.ssh.connect(username=self.node.username, pkey=key)
            else:
                self.ssh.connect(username=self.node.username, password=self.node.password, hostkey=hostkey)
        except socket.gaierror, e:
            print 'Error: hostname %s is unreacheable, check your connection trying to ping to it ' % (self.node.hostname)
            sys.exit(1)

        except paramiko.AuthenticationException, e:
            print 'Error: Autentication Failed for hostname %s , check in node.db file whether the credentials for connection to this node are correct' % (self.node.hostname)
            sys.exit(1)
        except IOError, e:
            print "\tFile not found!"
            print "Error: keyfile not found, check the node.db file again!"
            sys.exit(1)
        except Exception, e:
            print '*** Caught exception: %s --> %s: %s' % (self.node.hostname,e.__class__, e)
            traceback.print_exc()
            try:
                self.ssh.close()
            except:
                pass
            sys.exit(1)
    
    
    
    def close(self):
        """Close the connection to the remote host.
            
        """
        self.ssh.close()
    
        
                
    def run_command(self, str_command, background=False):
        """Run a command on the remote host.
            
        @param command: Unix command
        @return: Command output
        @rtype: String
        """ 
        print "node ", self.node.hostname
        print "execute cmd ", str_command
        chan = self.ssh.open_session()

        chan.exec_command(command=str_command)
        str = ""
        if not background:
            #wait for the output
            while(True):
                strbuff = chan.recv(1024)
                if len(strbuff) == 0:
                    break
                str = str + strbuff
        chan.close()
        return str
    
    def run_command_long(self, str_command):
        print "node ", self.node.hostname
        print "execute cmd ", str_command
        chan = self.ssh.open_session()

        chan.exec_command(command=str_command)
        str = ""
        #wait for the output
        while(True):
            strbuff = chan.recv(1024)
            #print strbuff
            if strbuff.find("BUILD SUCCESSFUL") <> -1:
                break
            str = str + strbuff
        chan.close()
        print str
        return str
    
    def get(self,remote_path,local_path):
        print "Downloading file from source ",remote_path," to destination",local_path
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            self.sftp.get(remote_path,local_path)
        except IOError, e:
            print "\tFile not found!"
    
    def getFileList(self, path, pattern=None):
        print "get a list of files from ", self.node.hostname, path
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            
            fileList = self.sftp.listdir(path)
            returnFileList = list()
            if pattern <> None:
                for x in fileList:
                    if x.find(pattern) <> -1:
                        returnFileList.append(x)
            else:
                returnFileList.extend(fileList)
            print returnFileList
            return returnFileList
        except IOError, e:
            print "\tFile not found!"
            return None
        
    def getLogFileList(self,path):
        print "get a list of files from ", self.node.hostname, path
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            
            fileList = self.sftp.listdir(path)
            returnFileList = list()
            for x in fileList:
                if x.endswith("log") or x.endswith("txt"):
                    returnFileList.append(x)
            print returnFileList
            return returnFileList
        except IOError, e:
            print "\tFile not found!"
            return None
        
    def getUserLogFileList(self,path):
        print "get a list of files from ", self.node.hostname, path
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            
            fileList = self.sftp.listdir(path)
            print fileList
            return fileList
        except IOError, e:
            print "\tFile not found!"
            return None 
    
    def put(self,remote_path, local_path):
        print "Copying file from source ",local_path," to destination",remote_path
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            self.sftp.put(local_path, remote_path)
        except IOError, e:
            print "\File not found!"
    
    def checkProcessAlive(self, pattern):
        command = "ps aux | grep " + self.node.username+ "  | grep " + pattern + " | grep -v grep"
        returnStr = self.run_command(command)
        #print returnStr
        if len(returnStr) == 0:
            return False
        else:
            return True 
        
    def remoteTailFile(self, filePath, numOfTailLine):
        command = "tail -n " + str(numOfTailLine) + " "+ filePath
        returnStr = self.run_command(command)
        return returnStr
    
    def returnContentOfDir(self, dir):
        command = "ls -l " + dir
        returnStr = self.run_command(command)
        return returnStr
        
    def killAllProcessesBySpecifiedPattern(self, pattern):
        command = "kill -9 $(ps aux | grep " + self.node.username + " | grep "+pattern+" | grep -v grep | awk '{print $2}')"
        print command
        while self.checkProcessAlive(pattern):
            print "Trying to kill all processes by the specified pattern " + pattern
            self.run_command(command)
        print "All such processes are killed!"
        
    def rexists(self, path):
        """os.path.exists for paramiko's SCP object
        """
        try:
            if self.sftp == None:
                self.sftp = paramiko.SFTPClient.from_transport(self.ssh)
            self.sftp.stat(path)
        except IOError, e:
            if e[0] == 2:
                return False
            else:
                return True
