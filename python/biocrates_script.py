#!/usr/bin/env python

import os
import sys
import time
import threading
from lcms import *

github = 'C:/github/'
os.chdir('H:\Biocrates_fenland\FenBiocrates_Results_Tables\Processed Biocrates Data\intensityExp\IS_signals')

def main():
    reFiles = sys.argv[1]
    maxnumthreads = sys.argv[2]
    xlfiles = pygrep(reFiles,'.')
    multitask_files(xlfiles,biocrates_thread,maxnumthreads)

def multitask_files(filelist,threadclass,maxnumthreads):
    for f in filelist:
        t = threadclass(f)
        t.start()
        while threading.activeCount() > maxnumthreads:
            time.sleep(1)

class biocrates_thread(threading.Thread):
    def __init__(self,filename):
        self.filename = filename
        threading.Thread.__init__(self)
    def run(self):
        os.system("python " + github + "/LCMS_highthroughput/biocrates.py " + 
self.filename)

main()
