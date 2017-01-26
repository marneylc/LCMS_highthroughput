# -*- coding: utf-8 -*-
"""
When converting files to mzML be sure to not compress the files!!!
If using the gui, be sure to unselect zlib compression.

Currently this is designed for masshunter data. No other spectral files have
been analyzed as of yet.

Created on Wed Jan 18 2017

@author: marneyl
"""

import pymzml
import os
import pandas
import matplotlib
import webbrowser
os.chdir('C:/Users/marne/github/LCMS_highthroughput/python/')
from lcms import *
from pylab import *

os.chdir("C:/Users/marne/Google Drive/virtual_server/data/lcms/Luke/") # directory where data is
files = pygrep('.mzML', '.')

# load a spectrum
filename = files[0]
msrun = pymzml.run.Reader(filename)

# plot tic
t = msrun['TIC']
plot(t.mz,t.i)
for f in files:
    msrun = pymzml.run.Reader(f)
    t = msrun['TIC']
    plot(t.mz,t.i)

ax=gca() # set axis object to ax
ax.set_xticklabels(ax.get_xticks(), fontsize=20)
sci_yticks = list()
for t in ax.get_yticks():
    sci_yticks.append("%.1E" % t)

ax.set_yticklabels(sci_yticks, fontsize=20)
show()



#--------------------------- other stuff ----------------------------#
# will error because the last scan stores the TIC
scans = list()
for spec in msrun:
    scans.append(spec['scan time'])

# find scans for time window
window = [2.07,2.20]
indx=list()
for i in range(1,len(scans)):
    s = scans[i]
    if s >= window[0] and s <= window[1]:    
        indx.append(i)

# plot one of the spectra
plot(msrun[indx[4]].mz,msrun[indx[4]].i)

# sum spectral data from indx, takes a bit depending on size of window
# still doesn't work, need to revisit
spec = pymzml.spec.Spectrum( measuredPrecision = 1e-4 )
for scan_num in indx:
    spec += msrun[scan_num]
    
# plot spectrum in s variable
plot(s.mz,s.i)

# find a peak
# PC(17:0/17:0) = 761.593
# would love to make a class called EIC with plot cammands and EIC.rt EIC.signal and EIC.mzs
# but this is pretty slow

target = 761.593
rt,signal,mzs = getEIC(filename,target)
plot(rt,signal)

def getEIC(filename,target):
    msrun = pymzml.run.Reader(filename)
    rt = list()
    signal = list()
    mzs = list()
    for spectrum in msrun:
        finder = spectrum.hasPeak(761.593)
        if finder != []:
            for mz,I in finder:
                rt.append(spectrum['scan time'])
                signal.append(I)
                mzs.append(mz)
            
    return rt,signal,mzs


        

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
fig2.suptitle(filename)
for cid in data['masses']:
    plotSRM(cid, data['transitions'])

# set some parameters for the chromatogram
ax=gca() # set axis object to ax
ax.set_xticklabels(ax.get_xticks(), fontsize=20)
sci_yticks = list()
for t in ax.get_yticks():
    sci_yticks.append("%.1E" % t)

ax.set_yticklabels(sci_yticks, fontsize=20)
# use show() to plot the chromatograms in a new plotting window
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



