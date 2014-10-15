#!/usr/bin/env python
import os
import re
import shutil
import threading
import time
import sys
home = os.getcwd()
os.chdir('C:/github/LCMS_highthroughput/')
from lcms import *
os.chdir(home)
path = sys.argv[1] # path to folder of files to convert to mzXML

def main():
	maxnumthreads = 4
	os.chdir(path)
	rawfiles = pygrep('raw','.')
	for f in rawfiles:
		t = mzXML_conv(f)
		t.start()
		while threading.activeCount() > maxnumthreads:
			time.sleep(0)

main()