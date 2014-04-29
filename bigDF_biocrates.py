#!/usr/bin/env python
"""
Created on Tue Apr 29 11:57:59 2014

@author: luke
"""

import os
import pandas
import re

def main():
    dframes = bigDF("/home/luke/Dropbox/biocrates/metIDQ_results/afterCurtainExp/",'lodAdj')

def bigDF(path2files,refiles):
    home = os.getcwd()
    os.chdir(path2files)
    files = pygrep(refiles,'.')
    dframes = dict()
    for filename in files:
        df = pandas.read_csv(filename, index_col=0)
        df['Plate#'] = [filename[0:6]] * df.shape[0]
        dframes[filename[0:6]] = df
    
    fulldf = pandas.concat(dframes.values())
    fulldf.to_csv('fulldf.csv')
    os.chdir(home)
    return dframes

def pygrep(regex,path):
    home = os.getcwd()
    os.chdir(path) # cd
    filenames = os.listdir(os.getcwd()) # ls
    matches = list()
    for filename in filenames:
        if re.search(regex,filename):
            matches.append(filename)
            
    os.chdir(home)
    return matches
    
main()