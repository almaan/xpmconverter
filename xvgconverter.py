#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 08:34:32 2018

@author: almaan
"""
def normalize(rmsd):
    m = np.mean(rmsd)
    std = np.std(rmsd)
    return (rmsd-m)/std

import numpy as np
path = '/data/PepBind/4rjd/4rjd_noligand_temp/438/sims/rmsd/avermsd.xvg'
output = '/data/PepBind/4rjd/4rjd_noligand_temp/438/sims/rmsd/adjrmsd'
with open(path,'r+') as fopen:
    frames,rmsd = [],[]
    lines = []
    for line in fopen:
        if not (line.startswith('@') or line.startswith('#')):
            sp = [float(rr) for rr in line.split(' ') if rr != '']
            frames.append(sp[0]), rmsd.append(sp[-1])
#            lines.append(sp)
            
fopen.close()
joint = np.array(zip(frames,rmsd))
frames = np.array(frames)
rmsd = np.array(rmsd)
rmsd_av = normalize(rmsd)
joint = np.array(zip(frames,rmsd_av))

#import matplotlib.pyplot as plt
#plt.plot(frames,rmsd_av)
#plt.plot(frames,rmsd)

with open(output + '.csv','w+') as fopen:
    for r,f in zip(rmsd_av,frames):
        fopen.write(','.join([str(f),str(r)]) + '\n')
fopen.close()

np.save(output + '.npy',joint)