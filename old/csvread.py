#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 23:06:25 2018

@author: almz
"""
#import csv
filename = 'csvtest3.csv'

with open(filename,'r+') as fopen:
    smat = []
    for line in fopen: 
        smat.append(line.replace('\n',''))
    fopen.close()

dmat = [[]]
for mat in smat[0:-1]:
    if '%' in mat:
        dmat.append([])
    else:
        dmat[-1].append(mat.split(','))
del smat