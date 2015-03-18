# -*- coding: utf-8 -*-
"""
This is a set of tools originally designed to grab QC Qexactive
data from multiple directories/plates. -Luke Marney 8/3/2014

Navigate to the parent directory containing the folders you want to pull
files out of. Then call the following:

python FNC_mzXML.py QC plate /home/luke/python/data/ /home/luke/python/data/qc

details: 
reFiles = sys.argv[1]
reFolders = sys.argv[2]
path = sys.argv[3]
dest = sys.argv[4]
"""

import os
import re
import shutil
import sys

def main():
    reFiles = sys.argv[1]
    reFolders = sys.argv[2]
    path = sys.argv[3]
    dest = sys.argv[4]
    os.chdir(path)
    Move(reFiles,reFolders,dest,path)
    #mzXML_conv(dest)

# copy all files in all folders to destination, 
# path is a directory containing the folders
def Move(reFiles,reFolders,dest,path):
    folders = pygrep(reFolders, path)
    home = os.getcwd()
    for folder in folders:
        files = pygrep(reFiles, folder)
        os.chdir(folder)
        cp_all(files,dest)
        os.chdir(home)
    
    os.chdir(home)

# kinda like ls | grep in Unix
def pygrep(regex,path):
    home = os.getcwd()
    os.chdir(path) # cd
    filenames = os.listdir(os.getcwd()) # ls
    matches = list()
    for file in filenames:
        if re.search(regex,file):
            matches.append(file)
            
    os.chdir(home)            
    return matches

#copy all files to destination directory
def cp_all(files,dest):
    for file in files:
        shutil.copy(file,dest)
    
#convert files in destination directory using msconvert
def mzXML_conv(dest):
    home = os.getcwd()
    os.chdir(dest)
    files = pygrep("raw",home)
    for file in files:
        os.system("msconvert " + file + " --mzXML")
    os.chdir(home)

#main()    
