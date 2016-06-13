# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       Memory dump for codec RunTimeLog
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-12-31 
#*      description:    auto Memory dump for codec RunTimeLog
# ##############################################################################
#!/usr/bin/python

import os, sys
import time, datetime
import telnetlib, socket
from thread import *
#import subprocess, traceback, shutil



# ################################################################################
# function:  class for TcpServer
# * 
# * 
# ################################################################################
class TcpServer():
    
    def __init__(self):
        
        pass
        
                
    # ###############################################
      
    def TcpServerStart(self):

        HostName = socket.gethostname()
        HOST = socket.gethostbyname(HostName)
        
        print "HostName %s: HOST %s"% (HostName, HOST)

        
        #HOST = 'hzling27.china.nsn-net.net'
        #HOST = '10.159.194.138'
        
        #HOST = 'hzling27'
        HOST = '127.0.0.1'
        PORT = 8081
        #PORT = 50000
        BUFFER = 1024
        Timeout = 3    
        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        
        print('tcpServer listen at: %s:%s\n\r'% (HOST, PORT))
        

        (client_sock, client_addr) = sock.accept()
        print('%s:%s connect' % client_addr)
        
        while True:
            recv = client_sock.recv(BUFFER)
            
            if not recv:
                client_sock.close()
                break
            else:
                
                print('[Client %s:%s Said]: %s'% (client_addr[0], client_addr[1], recv))
                
                #client_sock.close()
            
            client_sock.send('tcpServer has received your message.') 

            
        sock.close()


            
# ########**** main ****#######***** main *****#######
if __name__ == '__main__':
    
    # ****************************************
    # TODO:
    #  1. set interaction
    # ****************************************
    
    
    if len(sys.argv) == 1:
        ts = TcpServer()
        ts.TcpServerStart()
        
        
    else:
        print'''

   *************************** Usage: ***************************
    -input: No input       
           
   @example:
        MemoryDump_CodecRtl.py
        
   - output:
        - Out put Location: the dumped .bin files in "D:\memoryDump"
            
   **************************************************************
        '''
        exit(0)  
    
        

