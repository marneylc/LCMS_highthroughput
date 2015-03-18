# -*- coding: utf-8 -*-
"""

python mrm2csv.py filename.wiff

Created on Wed Jun 04 11:39:29 2014

@author: marneyl
"""

import sys
import threading
import time
import pymzml
import os
import pandas

def main():
	filename = sys.argv[1]
	data = getSRM(filename)
	data['transitions'].to_csv(os.path.splitext(filename)[0]+'.csv')
		
class mzML_conv(threading.Thread):
    def __init__(self,filename):
        self.filename = filename
        threading.Thread.__init__(self)
    def run(self):
        os.system("msconvert " + self.filename + " --mzML" + ' -o ' + filename + '.mzML')
	
def getSRM(filename):
    data = dict()
    transitions = dict()
    numtransition = list()
    masses = list()
    msrun = pymzml.run.Reader(filename)
    for spectra in msrun:
        if spectra['id'] != 'TIC':
            x = str.split(spectra['id'])
            transition = x[2].split('=')[1] + '-' + x[3].split('=')[1]
            numtransition.append(x[-1].split('=')[1])
            masses.append(transition)
            transitions[transition] = (spectra.mz, spectra.i)
    data['transitions'] = transitions
    data['numtransition'] = numtransition
    data['masses'] = masses
    return data

main()