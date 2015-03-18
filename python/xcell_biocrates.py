# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:09:55 2014

@author: marneyl
"""
import xlrd
import os
import sys
import numpy
import pandas

def main():
    filename = sys.argv[1] #include full pathname
    sheetname = 'Data Export'
    wb=xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(sheetname)
    data = get_subset(filename,sheetname,[7,17],[sheet.ncols,sheet.nrows],False)
    metabolites = get_subset(filename,sheetname,[2,17],[2,sheet.ncols],True)
    samples = get_subset(filename,sheetname,[7,4],[sheet.nrows,4],True)
    biocrates = pandas.DataFrame(data,index=samples,columns=metabolites)
    biocrates.to_csv(os.path.splitext(filename)[0]+'.csv')
    
    return biocrates # returning dataframe for possible future use in python

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