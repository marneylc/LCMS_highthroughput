# -*- coding: utf-8 -*-
"""
When converting files to mzML be sure to not compress the files!!!
If using the gui, be sure to unselect zlib compression.

Currently this is designed for absciex mrm data. No other spectral files have
been analyzed as of yet.

Created on Wed Jun 04 11:39:29 2014

@author: marneyl
"""

import pymzml
import os
import pandas
import matplotlib
os.chdir('C:/github/LCMS_highthroughput/')
from lcms import *

os.chdir('C:/Users/marneyl/Downloads/testconvert/')
files = pygrep('.mzML', '.')

data = getMRM(files[2])

# plot a single transition
plotMRM('225.2-44.2', data['transitions'])

# plot all of them
for cid in data['masses']:
    plotMRM(cid, data['transitions'])
    
# make a table of transitions to look at if you want
TT = pandas.DataFrame(transitions.keys(), index=numtransition, columns = {'Transitions'})
TT.to_html('transitions.html')

def getMRM(filename):
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

def plotMRM(cid, transitions):
    plot(transitions[cid][0],transitions[cid][1])



