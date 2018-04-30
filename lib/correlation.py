#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:26:21 2018

@author: almaan
"""

import numpy as np
import matplotlib.pyplot as plt


#pth_rmsd = '/data/PepBind/4rjd/4rjd_noligand_temp/438/sims/rmsd/avermsd.npy'
#pth_dmat = '/data/PepBind/4rjd/4rjd_noligand_temp/438/sims/mat/temp438.npy'
#pth_out = '/data/PepBind/4rjd/4rjd_noligand_temp/438/sims/mat/distances.dat'
path = '/data/PepBind/4rjd/4rjd_noligand/sims/rmsd/rmsd.xvg'
output = '/data/PepBind/4rjd/4rjd_noligand/sims/rmsd/avermsd'

pth_rmsd = '/data/PepBind/4rjd/4rjd_noligand/sims/rmsd/avermsd.npy'
pth_dmat = '/data/PepBind/4rjd/4rjd_noligand/sims/mat/dmat.npy'
pth_out = '/data/PepBind/4rjd/4rjd_noligand/analysis/distances.dat'

def backmap(idx,sz):
    r = np.floor(idx/sz)
    c = (idx + 1)-sz*r 
    return r, c - 1

def normalize(rmsd):
    m = np.mean(rmsd)
    std = np.std(rmsd)
    return (rmsd-m)/std

def correlate(rm,dm):
    corr_mat = np.zeros((dm.shape[1],dmat.shape[2]))
    mrm = (rm-np.mean(rm))**2
    for ii in xrange(dmat.shape[1]):
        for jj in xrange(dmat.shape[2]):
                if ii <= jj:
                    mdm = (dm[:,ii,jj]-np.mean(dm[:,ii,jj]))**2
                    corr_mat[ii,jj] = np.sum(np.sqrt(mdm*mrm))
                    corr_mat[jj,ii] = corr_mat[ii,jj]
    return corr_mat
#%%    
rmsd = np.load(pth_rmsd)
dmat = np.load(pth_dmat)
nres = dmat.shape[1]

corr = (1./nres)**2*correlate(rmsd[:,1],dmat)

plt.imshow(corr)
plt.colorbar()
lower_triangular = np.tril(corr)
lower_triangular_rav = np.ravel(lower_triangular)
idx  = (-lower_triangular_rav).argsort()[:10]
row, col =  backmap(idx,nres)

pinpoint = np.zeros((nres,nres))
for r,c in zip(row,col):
    pinpoint[int(r),int(c)] = 1.

plt.imshow(pinpoint)

with open(pth_out,'w+') as fopen:
    fopen.write('Residue1\t\tResidue2\n')
    for r,c in zip(row,col):
        fopen.write(str(int(r+83)) + '\t\t\t' + str(int(c+83))+'\n')