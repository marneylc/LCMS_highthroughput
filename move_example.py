#!/usr/bin/env python
import os
import re
import shutil
import threading
import time
home = os.getcwd()
os.chdir("C:/github/LCMS_highthroughput")
from lcms import *
os.chdir(home)


def main():
	path2folders = "Z:/MS-Exactive/Data/PROMIS"
	os.chdir(path2folders)
	dest = "H:/data/PROMIS/blanks"
	FF_dict = filesNfolders("BLANK", "PROMIS", path2folders)
	for folder in FF_dict:
		for f in FF_dict[folder]:
			mthread = Move(f,folder,path2folders,dest)
			mthread.start()
			while threading.activeCount() > 4:
				time.sleep(0)

main()