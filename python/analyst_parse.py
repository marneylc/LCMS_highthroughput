# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:14:26 2014

@author: marneyl

This piece of code parses the default text file output into a tab delimited
csv file that is easily loaded into a dataframe object. The code takes one 
system argument: the file name. Place this file in the directory with the 
files you wish to convert and run the following in cmd or cygwin:

python analyst_parse.py <filename>

Some additional code at the bottom has been commented out for converting 
the file from tab delimited to comma delimited, but is buggy and unessesary.

Additional Note: to import into R make sure to set the delimiter to tab,
such as: DF <- read.csv("<filename>", sep="\t")

requires python packages:
os
sys

"""

import os
import sys
#import csv

def main():
    filename = sys.argv[1]
    output_csv(filename)

def output_csv(filename):
    #outputs the tab delimited file into a .csv file
    colnames = linefind("Sample Name", filename)
    data = linefind(".dam", filename)
    csv_filename = os.path.splitext(filename)[0]+'.csv'
    with open(csv_filename,"a") as f:
        #temp = open("temp.csv", "a")
        f.write(colnames[0])
        f.writelines(data)
        #temp.close()
        
    #csv_outfobj = open(csv_filename, 'wb')
    #change from tab to comma delimited
#    with open("temp.csv","r") as temp:
#        tab_data = csv.reader(temp, delimiter = '\t')
#        out_csv = csv.writer(csv_outfobj)
#        out_csv.writerows(tab_data)
#    
#    csv_outfobj.close()
    return

def linefind(search_string,filename):
    f = open(filename, 'r')    
    match = list()
    for line in f:
        if search_string in line:
            match.append(line)
    f.close()
    
    return match
    
main()