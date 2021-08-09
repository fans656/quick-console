import datetime
import subprocess
import traceback

from logger import logger


def main():
    logger.info('foo')
    try:
        #with open('C:/Windows/System32/Drivers/etc/hosts', 'a') as f:
        #    f.write('\n#test {}\n'.format(datetime.datetime.now()))
        out = subprocess.check_output('wsl hostname -I', stderr = subprocess.STDOUT, shell = True)
        logger.info('output:')
        logger.info(out.encode())
    except:
        logger.info(traceback.format_exc())
