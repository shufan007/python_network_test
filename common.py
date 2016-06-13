
import os, sys
import logging

#--------------------------------------------------------------

def LogSetup(logFileName):
    os.chdir(sys.path[0])
    logging.basicConfig(filename = os.path.join(os.getcwd(), logFileName),
                        level = logging.WARN, 
                        filemode = 'w', 
                        format =  '%(asctime)s - %(levelname)s: [line:%(lineno)d]: %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)   
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info('* Logging start...')
    
    return logger
#-------------------------------------------------------------------------
        
def write_list(file_name, items_list, access_mode = 'w'):

    fp = open(file_name, access_mode)
    for item in items_list:
	fp.write(item + '\n')
    fp.close()
    
    