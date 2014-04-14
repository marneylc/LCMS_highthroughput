"""
Created on Tue Apr 01 20:23:54 2014

@author: marneyl


"""

import os
import re
import shutil
import threading

def filesNfolders(reFiles,reFolders,path):
    FF_dict = dict()
    folders = pygrep(reFolders, path)
    home = os.getcwd()
    os.chdir(path)
    for folder in folders:
        files = pygrep(reFiles, folder)
        FF_dict[folder] = files
    os.chdir(home)
    return FF_dict
    
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
        
class mzXML_conv(threading.Thread):
    def __init__(self,filename):
        self.filename = filename
        threading.Thread.__init__(self)
    def run(self):
        os.system("msconvert " + self.filename + " --mzXML")
        
class Move(threading.Thread):
    def __init__(self,filename,folder,dest):
        self.filename = filename
        self.folder = folder
        self.dest = dest
        threading.Thread.__init__(self)
    def run(self):
        home = os.getcwd()
        os.chdir(self.folder)
        shutil.copy(self.filename, self.dest)
        os.chdir(home)

# only works in unix environments        
class R_hrms(threading.Thread):
    def __init__(self,filename):
        self.filename = filename
        threading.Thread.__init__(self)
    def run(self):
        os.system("./hrms.R " + self.filename)
