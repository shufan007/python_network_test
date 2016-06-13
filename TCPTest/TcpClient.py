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
#from thread import *
import threading
#import subprocess, traceback, shutil



# ################################################################################
# function:  class for TcpServer
# * 
# * 
# ################################################################################
class TcpClient():
    
    def __init__(self):
        
        self.HostName = socket.gethostname()
        self.MyIp = socket.gethostbyname(self.HostName)
        
        print "HostName %s: HOST %s"% (self.HostName, self.MyIp)   
        
        #HOST = '10.159.194.138'
        #HOST = 'hzling27.china.nsn-net.net'
        
        #HOST = '10.140.90.165'
        #HOST = '127.0.0.1'
        
        self.HOST = '10.141.149.122'
        self.PORT = 50000
        self.BUFFER = 1024
        self.Timeout = 3
        self.joinTimeOut = 60
        
        #self.sendThreadStop__Flag = 0
        

    # ###############################################
    # Function for handling connections
    # be used to create threads
    # ###############################################         
    def SockThread_recv(self, sock):
              
        while True:            
            recv = sock.recv(1024)
            print('[Server Said]: %s'% (recv))
               

    # ###############################################
    # Function for handling connections
    # be used to create threads
    # ###############################################         
    def SockThread_send(self, sock):
        
        while True:

            msg = raw_input(" @_@ [Input]: ")           
            msg += "\n\r" 
            
            if msg.find('exit')>=0:
                sock.close()
                #thread.exit_thread()
                self.sendThreadStop__Flag = 1
                break
                                       
            sock.sendall(msg)  
                        

    # ###############################################
    # Function for handling connections
    # be used to create threads
    # ###############################################         
    def SockThread(self, sock):
        
        while True:            
            recv = sock.recv(1024)
            print('[Server Said]: %s'% (recv))

            msg = raw_input(" @_@ [Input]: ")           
            msg += "\n\r" 
            
            if msg.find('exit')>=0:
                sock.close()
                #thread.exit_thread()
                #self.sendThreadStop__Flag = 1
                break
                                       
            sock.sendall(msg)             

    # ###############################################
      
    def TcpClientStart(self):

        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))
        sock.send('Hello, tcpServer! here is: %s'% self.MyIp)
        
        sock_thread = threading.Thread(target=self.SockThread, args=( sock, ))
        sock_thread.setDaemon(True)
        sock_thread.start()                    
        sock_thread.join(self.joinTimeOut)
        
        sock.close()

            
# ########**** main ****#######***** main *****#######
if __name__ == '__main__':
    
    # ****************************************
    # TODO:
    #  1. set interaction
    # ****************************************
    
    
    if len(sys.argv) == 1:
        ts = TcpClient()
        ts.TcpClientStart()
        
        
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
    
        

