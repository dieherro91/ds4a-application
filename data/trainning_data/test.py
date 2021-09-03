import gzip
import os






DATA_DIR = os.getcwd()
sav_path = os.path.join(os.path.join(os.path.join(DATA_DIR, "data"), "trainning_data"),'GF512'+'.json')


import gzip
import shutil
from contextlib import ExitStack
with ExitStack() as stack:
    f_in = stack.enter_context(open(sav_path, 'rb'))
    f_out = stack.enter_context(gzip.open(sav_path+'.gz', 'wb'))
    shutil.copyfileobj(f_in, f_out)