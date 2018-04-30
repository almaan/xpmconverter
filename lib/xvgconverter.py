#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 08:34:32 2018

@author: almaan
"""


import numpy as np

def xvg_convert(path,output):
    with open(path,'r+') as fopen:
        frames,rmsd = [],[]
        for line in fopen:
            if not (line.startswith('@') or line.startswith('#')):
                sp = [float(rr) for rr in line.split(' ') if rr != '']
                frames.append(sp[0]), rmsd.append(sp[-1])
                
    fopen.close()
    joint = np.array(zip(frames,rmsd))
    frames = np.array(frames)
    rmsd = np.array(rmsd)
    joint = np.array(zip(frames,rmsd))
    with open(output + '.csv','w+') as fopen:
        for r,f in zip(rmsd,frames):
            fopen.write(','.join([str(f),str(r)]) + '\n')
    fopen.close()
    
    np.save(output + '.npy',joint)