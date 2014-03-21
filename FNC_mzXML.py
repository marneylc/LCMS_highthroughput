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
convert = sys.argv[5]
"""

import os
import re
import shutil
import sys
import thread

# main function takes boolean for whether you want to convert all files in 
# destination directory after all files have been moved
def main():
    reFiles = sys.argv[1]
    reFolders = sys.argv[2]
    path = sys.argv[3]
    dest = sys.argv[4]
    convert = sys.argv[5]
    os.chdir(path)
    Move(reFiles,reFolders,dest,path)
    if convert:
        mzXML_conv(dest)

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
    for filename in filenames:
        if re.search(regex,filename):
            matches.append(filename)
            
    os.chdir(home)            
    return matches

#copy all files to destination directory in multiple threads
def cp_all(files,dest):
    i = range(0,len(files),4)
    for filenum in i:
        try:
            thread.start_new_thread(shutil.copy,(files[filenum], dest, ))
            thread.start_new_thread(shutil.copy,(files[filenum+1], dest, ))
            thread.start_new_thread(shutil.copy,(files[filenum+2], dest, ))
            thread.start_new_thread(shutil.copy,(files[filenum+3], dest, ))
            
        except:
            print "Error: unable to start thread for file copy"
        
def exe_conv(thread_name, filename):
    print "Converting " + filename
    os.system("msconvert " + filename + " --mzXML")
    
#convert files in destination directory using msconvert in multiple threads
def mzXML_conv(dest):
    home = os.getcwd()
    os.chdir(dest)
    files = pygrep("raw",home)
    i = range(0,len(files),4)
    for filenum in i:
        try:
            thread.start_new_thread(exe_conv,("Thread 1:", files[filenum], ))
            thread.start_new_thread(exe_conv,("Thread 2:", files[filenum+1], ))
            thread.start_new_thread(exe_conv,("Thread 3:", files[filenum+2], ))
            thread.start_new_thread(exe_conv,("Thread 4:", files[filenum+3], ))
            
        except:
           print "Error: unable to start thread for msconvert"

    os.chdir(home)

main()
