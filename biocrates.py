#!/usr/bin/env python

"""
Execute by shell prompt in active directory of xlsx files: python biocrates.py


Pulls out all the necessary information from biocrates xlsx export file,
parses it to a csv file, then turns all values bellow their LOD to zero, and 
finally normalizes the relative quantification values to the QC1 sample signal.

Created on Wed April 23 17:09:55 2014

@author: marneyl
"""

import xlrd
import os
import sys
import numpy
import pandas
import re

def main():
    #filename = sys.argv[1] #include full pathname
    files = pygrep('.xlsx','.')
    for filename in files:
		sheetname = 'Data Export'
		wb=xlrd.open_workbook(filename)
		sheet = wb.sheet_by_name(sheetname)
		lods_biocrates = get_lods(sheet,filename,sheetname)
		wellpos = get_subset(filename,sheetname,[7,12],[sheet.nrows,12],True) # get well positions
		dates = get_dates(sheet,filename,sheetname)  # get sample run date
		biocrates = get_data(sheet,filename,sheetname)
		biocrates['Well_Position'] = wellpos # add in well positions to data frame
		biocrates['Date'] = dates
		biocrates = remove_cals(biocrates)
		biocrates.to_csv(os.path.splitext(filename)[0]+'.csv')
		biocrates_lodAdj = lod_set2value(lods_biocrates,biocrates,0)
		biocrates_lodAdj.to_csv(os.path.splitext(filename)[0]+'lodAdj.csv')
		# split absolute quantification?
		biocrates_lodAdj_norm = normalize(biocrates_lodAdj, 'MetaDis QC1')
		biocrates_lodAdj_norm.to_csv(os.path.splitext(filename)[0]+'lodAdj_norm.csv')


def normalize(biocrates, reQCsample):
    # normalizes each value for relative quant metabolites (columns 40 - 81)
    # uses a regular expression to pull out normalization sample name
    # will fail if there are multiple matches
    reQC = list()
    for name in biocrates.index:
        if re.search(reQCsample, name):
            reQC.append(name)
    if len(reQC) > 1:
        print("Multiple matches for norm sample regular expression")
        return False
    else:
        biocrates_lodAdj_norm = pandas.DataFrame(index = biocrates.index)
        reQCdata = biocrates.ix[reQC]
        absoluteCol = pandas.Series(biocrates.columns[40:82])
        for column in biocrates.columns:
            if (absoluteCol.str.contains(column).any() or column == 'Well_Position' or column == 'Date'):
                biocrates_lodAdj_norm[column] = biocrates[column]
            else:
                biocrates_lodAdj_norm[column] = biocrates[column]/reQCdata[column].values
    return biocrates_lodAdj_norm
                
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
    
def get_dates(sheet,filename,sheetname):
    long_dates = get_subset(filename,sheetname,[7,16],[sheet.nrows,16],True)
    dates=list()    
    for i in range(len(long_dates)):
        dates.append(long_dates[i][0:10])
    return dates

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

main()
