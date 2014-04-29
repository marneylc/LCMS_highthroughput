#!/usr/bin/env python

"""
Created on Wed April 23 17:09:55 2014

@author: marneyl
"""

import xlrd
import os
import sys
import numpy
import pandas
import re

os.chdir("/home/luke/python/data/biocrates/")

def main():
    filename = sys.argv[1] #include full pathname
    sheetname = 'Data Export'
    wb=xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(sheetname)
    lods_biocrates = get_lods(sheet,filename,sheetname)
    biocrates = get_data(sheet,filename,sheetname)
    biocrates = remove_cals(biocrates)
    biocrates.to_csv(os.path.splitext(filename)[0]+'.csv')
    biocrates_lodAdj = lod_set2value(lods_biocrates,biocrates,0)
    biocrates_lodAdj.to_csv(os.path.splitext(filename)[0]+'lodAdj.csv')

"""
# starting some code to combine multiple plates of data into a single data 
# frame
from lcms import pygrep
filelist = pygrep('lodAdj','.')
def combine_plates(filelist):
    dataframes = list()
    for filename in filelist:
        dataframes.append(pandas.read_csv(filename))
    
    
    
"""
def remove_cals(biocrates):
    calibrants = list()
    for name in biocrates.index:
        if re.search('Cal', name):
            calibrants.append(name)            
    biocrates = biocrates.drop(calibrants,axis=0)
    return biocrates
    
def lod_set2value(lods_biocrates,biocrates,value):
    # set values below LOD to zero for each lc metabolite
    for lc_metabolite in lods_biocrates.index:
        for i in range(0,len(biocrates[lc_metabolite])):
            if (biocrates[lc_metabolite][i] < float(lods_biocrates[lc_metabolite])):
                biocrates[lc_metabolite][i] == value
    return biocrates


def get_data(sheet,filename,sheetname):
    data = get_subset(filename,sheetname,[7,17],[sheet.ncols,sheet.nrows],False)
    metabolites = get_subset(filename,sheetname,[2,17],[2,sheet.ncols],True)
    samples = get_subset(filename,sheetname,[7,4],[sheet.nrows,4],True)
    biocrates = pandas.DataFrame(data,index=samples,columns=metabolites)
    return biocrates

    
def get_lods(sheet,filename,sheetname):
    lods = get_subset(filename,sheetname,[5,57],[5,98],True)
    lods_metabolites = get_subset(filename,sheetname,[2,57],[2,98],True)
    lods_biocrates = pandas.Series(lods, index=lods_metabolites)
    return lods_biocrates


def get_subset(filename, sheetname, topleft, bottomright, string):
    left = topleft[0]; right = bottomright[1]
    top = topleft[1]; bottom = bottomright[0]
    left = left - 1; top = top - 1 # python indexing starts with zero
    # we don't need to adjust the right and bottom because the function 'range'
    # includes all values upto the second arg value but not including it
    wb=xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(sheetname)    
    if top+1==right:
        if string==True:
            data = list()
            for row_index in range(left,bottom):
                data.append(str(sheet.cell(row_index,top).value))            
        else:
            data = numpy.zeros((numpy.size(range(left,bottom)),1))
            for row_index in range(left,bottom):
                data[row_index-(left), top] = sheet.cell(row_index,top).value
    elif string==True:
        data = list()
        for col_index in range(top,right):
            data.append(str(sheet.cell(left,col_index).value))
    else:
        data = numpy.zeros((numpy.size(range(left,right)),numpy.size(range(top,bottom))))
        for row_index in range(left,right):
            for col_index in range(top,bottom):
                try:
                    data[row_index-(left), col_index-(top)] = sheet.cell(row_index,col_index).value
                except ValueError:
                    data[row_index-(left), col_index-(top)] = float('nan')
    return data
    
main()