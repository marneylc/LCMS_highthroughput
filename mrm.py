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
import webbrowser
os.chdir('C:/github/LCMS_highthroughput/')
from lcms import *
from pylab import *

os.chdir('C:/Users/marneyl/Downloads/testconvert/')
files = pygrep('.mzML', '.')

filename = files[2]
data = getSRM(filename)

''' 
Below is how to show all SRM transitions and plot them.
In the future, data['transitions'] could be restructured to only include the wanted transitions.
First you make an html table and display it in a webrowser
'''
# make a table of transitions to look at
TT = pandas.DataFrame(data['transitions'].keys(), index=data['numtransition'], columns = {'Transitions'})
TT.to_html('transitions.html')
url = "file://" + os.getcwd() + '\\transitions.html'
webbrowser.open_new_tab(url)

# to plot a single transition
fig1 = figure()
plotSRM('758.6-184', data['transitions'])
# use >>> show() to display figure if not in an IDE

# plot all SRMs
fig2 = figure()
fig.suptitle(filename)
for cid in data['masses']:
    plotSRM(cid, data['transitions'])

# set some parameters for the chromatogram
ax=gca() # set axis object to ax
ax.set_xticklabels(ax.get_xticks(), fontsize=20)
sci_yticks = list()
for t in ax.get_yticks():
    sci_yticks.append("%.1E" % t)

ax.set_yticklabels(sci_yticks, fontsize=20)
show()

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

def plotSRM(cid, transitions):
    plot(transitions[cid][0],transitions[cid][1],)



