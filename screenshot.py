import config

from PIL import ImageGrab

import os
import time
from datetime import datetime

def screenshot_timely_saver(interval, dirpath):
    '''
    interval - seconds between captures
    '''
    while True:
        im = ImageGrab.grab()
        ts = datetime.strftime(datetime.now(), config.FNAME_TIMESTAMP_FORMAT)
        fpath = os.path.join(dirpath, ts + '.png')
        im.save(fpath, 'png')
        time.sleep(interval)
