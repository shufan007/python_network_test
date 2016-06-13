# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2015-7-7 
#*      description:    
#           - Input:    
#           - DstFile:      ip list
# ##############################################################################
#!/usr/bin/python

import os, sys, platform
import time, datetime
import re, socket
from multiprocessing.dummy import Pool as ThreadPool
#from multiprocessing import Pool
#from functools import partial
#----------------------------------------------------------

sysStr = platform.system()
#print "* System: %s"% sysStr

if sysStr.upper() == "WINDOWS":
    import paramiko as ssh
elif sysStr.upper() == "LINUX":
    import ssh
    
#----------------------------------------------------------    
# global define
global SSH_LOGIN_PORT
global SSH_TIME_OUT

global PROCESS_NUM

global PING_PACKET_NUM
global PING_WAIT_TIME

SSH_LOGIN_PORT = 22
SSH_TIME_OUT = 2 

PROCESS_NUM = 12

PING_PACKET_NUM = 1
PING_WAIT_TIME = 1
#--------------------------------------------------------------
	
# #############################################################################
# function:  class for Ip Process
# * input:
#   - argv: can be a list, file with ip string or ip_segment
#
# #############################################################################
class IpProcess():
    
    def __init__(self, argv):
	
	self.ipList = []
	
	if os.path.isfile(argv):
	    self.get_ipListFromFile(argv)
	elif isinstance(argv, str):
	    self.get_ipListBySegment(argv)
	else:
	    self.ipList = argv
	    
	self.sort_ipList()
	    		    
	    
    def get_ipListBySegment(self, ip_segment):
        point = '.'
	line1 = '_'
        seg_num = len(ip_segment.split(point))
        
        if seg_num == 2:
            for i in range(0, 256):
                for j in range(1, 256):
                    self.ipList.append(ip_segment + point + str(i) + point + str(j)) 
        if seg_num == 3:
            header = ip_segment[0: ip_segment.rfind(point)]
            if ip_segment.rfind(line1)>0:
                start = int(ip_segment.split(point)[-1].split(line1)[0])
                end = int(ip_segment.split(point)[-1].split(line1)[1])
            else:
                start = int(ip_segment.split(point)[-1])
                end = start
            for i in range(start, end+1):  
                for j in range(1, 256):
                    self.ipList.append(header + point + str(i) + point + str(j))
        elif seg_num == 4:
            self.ipList.append(ip_segment)  
	    
		
    def get_ipListFromFile(self, IpListFileName):	
	fp = open(IpListFileName, 'r')
	lines = fp.readlines()
	ip_pattern = re.compile('(\d{1,3}\.){3}\d{1,3}$')
	
	for line in lines:
	    line = line.strip()
	    if ip_pattern.match(line) != None:
		self.ipList.append(line)
		
	self.ipList = list(set(self.ipList))
	
	    
    def sort_ipList(self):
	point = '.'
	
	for i in range(0, len(self.ipList)):
	    self.ipList[i] = map(int, self.ipList[i].split(point))
	    self.ipList[i] = "%03d.%03d.%03d.%03d"% tuple(self.ipList[i])
	    
	self.ipList.sort()
	for i in range(0, len(self.ipList)):
	    self.ipList[i] = map(str, map(int, self.ipList[i].split(point)))
	    self.ipList[i] = point.join(self.ipList[i])
    
      
    def ping_ipList(self, packet_num = PING_PACKET_NUM, wait_time = PING_WAIT_TIME):
	if sysStr.upper() == "WINDOWS":
	    pingStr = "ping -n %d -w %d "% (packet_num, wait_time)
	elif sysStr.upper() == "LINUX":
	    pingStr = "ping -c %d -i %d "% (packet_num, wait_time)	
		
	ping_pool = ThreadPool(processes = PROCESS_NUM)
	pingStrList = map(lambda ip: pingStr + ip, self.ipList)
	ping_status = ping_pool.map(os.system, pingStrList)  
	ping_pool.close()
	ping_pool.join()
	
	valid_ipList = []
	for i in range(0, len(ping_status)):           
	    if ping_status[i] == 0:
		valid_ipList.append(self.ipList[i])	
	
	return valid_ipList
		

# #############################################################################
# function:  class for ssh access check Process
# * input:
#   - 
# #############################################################################    
class CheckAccess():
    
    def __init__(self, access_name, passwd, check_path = None):
        
	self.access_name = access_name
	self.passwd = passwd

        self.check_pass_ip = []
	if check_path != None:
	    self.check_cmd = "ls %s |grep %s"%(os.path.dirname(check_path), os.path.basename(check_path))
	else:
	    self.check_cmd = None

    def ssh_connect(self, ip, ssh_timeout = SSH_TIME_OUT, port = SSH_LOGIN_PORT):    
	ssh_obj = ssh.SSHClient()
	ssh_obj.set_missing_host_key_policy(ssh.AutoAddPolicy())   
	try:                
	    ssh_obj.connect(ip, port, self.access_name, self.passwd, timeout = ssh_timeout)
	    #self.id = self.ssh.get_transport().getpeername()[0] 
	    print " * SSH Connect to " + ip + " success!\n" 
	except Exception, ssh_e:
	    ssh_obj = None
	    print ssh_e	
	    
	return ssh_obj
    
    
    def access_check(self, ip):
	return_value = False
	try:
	    ssh = self.ssh_connect(ip)
	    if ssh != None:
		if self.check_cmd != None:		
		    (stdin, stdout, stderr) = ssh.exec_command(self.check_cmd)
		    status = stdout.channel.recv_exit_status() 		    
		    if status == 0:
			self.check_pass_ip.append(ip)		    
		ssh.close()
		return_value = True
	except Exception, ssh_e:
	    print ssh_e
	
	return return_value

    
    def ipList_accessCheck(self, ipList): 
        access_pool = ThreadPool(processes = PROCESS_NUM)
        access_status = access_pool.map(self.access_check, ipList)  
        access_pool.close()
        access_pool.join()
	
	access_ipList = []
	for i in range(0, len(ipList)):
	    if access_status[i] == True:
		access_ipList.append(ipList[i])	
	
	return (access_ipList, self.check_pass_ip)
    

