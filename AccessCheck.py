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

import os, sys
import time, datetime

from common import LogSetup, write_list
from networks import IpProcess, CheckAccess
    
#----------------------------------------------------------    
# global define

LogFileName   = "AccessCheck.log"

SSH_LOGIN_NAME = "upl1-tester"
SSH_LOGIN_PWD  = "btstest"

check_path = "/home/" + SSH_LOGIN_NAME + "/shufan"
#--------------------------------------------------------      

def ip_accessCheck(argv):
    
    global SSH_LOGIN_NAME
    global SSH_LOGIN_PWD	
    global check_path 
    
    global logger
    logger = LogSetup(LogFileName)
    
    if len(argv) == 2:
	start = time.clock()
	fileEndStr = argv[1]
	
	if os.path.isfile(argv[1]):
	    fileEndStr = os.path.basename(argv[1])
	    fileEndStr = fileEndStr[0:fileEndStr.rfind('.')]
		
	ip_obj = IpProcess(argv[1])
	validList = ip_obj.ping_ipList()

	access_obj = CheckAccess(SSH_LOGIN_NAME, SSH_LOGIN_PWD, check_path)
	
	(access_ipList, check_pass_ip) = access_obj.ipList_accessCheck(validList)
	
	logger.info(" * Access ip List writing... \n")
	accessIpFile = "accessIpList_%s.txt"% fileEndStr
	
	printList = ["[access pass: %d]\n"% len(access_ipList)]
	printList.extend(access_ipList)
	printList.append("\ncheck pass ip: \n")
	printList.extend(check_pass_ip)
	 
	write_list(accessIpFile, printList) 
	
	logger.info(" * Duration: %.2f seconds."% (float(time.clock()) - float(start))) 

    
if __name__ == '__main__':
    
    ip_accessCheck(sys.argv) 
