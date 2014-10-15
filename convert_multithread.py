#!/usr/bin/env python

import os
import re
import shutil
import threading
import time
home = os.getcwd()
os.chdir('/home/marneyl/LCMS_highthroughput/')
from lcms import *
os.chdir(home)
rawfiles = pygrep('mzXML','.')
maxnumthreads = 4

for f in rawfiles:
  t = mzXML_conv(f)
  t.start()
  while threading.activeCount() > maxnumthreads:
    time.sleep(0)

