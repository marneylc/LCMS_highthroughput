# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:56:05 2014

@author: marneyl
"""
import sys
import os
import pandas


filename = sys.argv[1]
os.system(("python xcell_biocrates.py " + filename)) # use xcell_biocrates.py to convert analyst .txt files to usable .csv files
data = pandas.read_table((os.path.splitext(filename)[0]+'.csv'), sep=',', header = )
# import analyst concentrations of QC's and Pool Samples from current plate

# change QC names to include the plate number
# append concentration data for all metabolites to a .csv file