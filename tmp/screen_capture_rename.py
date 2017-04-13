import os
import re
from datetime import datetime

#SRC_FMT = '%Y%m%d%H%M%S'
#SRC_FMT = '%Y-%m-%d %H-%M-%S %f'
#DST_FMT = '%Y-%m-%d %H-%M-%S-%f'
SRC_FMT = '%Y-%m-%d %H-%M-%S'
DST_FMT = '%Y-%m-%d %H-%M-%S-%f'

for fname in os.listdir('.'):
    if os.path.isdir(fname):
        continue
    if fname in ('t.py'):
        continue
    name, ext = os.path.splitext(fname)
    m = 14 + 4 + 1
    ts_str = name[:m]
    suffix = ts_str[m:]
    r = re.match('\d+( .*)', suffix)
    if r:
        print r.group(1)
        exit()
    try:
        new_name = datetime.strptime(ts_str, SRC_FMT).strftime(DST_FMT)
    except Exception as e:
        print e
        print 'ignore', fname
        raw_input()
        continue
    print (name, new_name, suffix, ext)
    #raw_input()
    try:
        os.rename(fname, new_name + suffix + ext)
    except Exception:
        print fname
