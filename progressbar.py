import sys
import os
import time

hashlist=[]

for i in range(1,10):
    hashlist.append('#')

for r in range(1,len(hashlist)):
    sys.stdout.write(hashlist[r])
    time.sleep(2)    
    sys.stdout.flush()

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
sys.stdout.flush()
