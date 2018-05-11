#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:26:21 2018

@author: almaan
"""

import numpy as np

def normalize(rmsd):
    m = np.mean(rmsd)
    std = np.std(rmsd)
    return (rmsd-m)/std

def correlate(rm,dm,rf):
    corr_mat = np.zeros((dm.shape[1],dm.shape[2]))
    mrm = (rm-np.mean(rm))**2
    for ii in xrange(dm.shape[1]):
        for jj in xrange(dm.shape[2]):
                if ii < jj:
                    mdm = (dm[:,ii,jj]-np.mean(dm[:,ii,jj]))**2
                    corr_mat[ii,jj] = np.sum(np.sqrt(mdm*mrm)/rf[ii]/rf[jj])
                    corr_mat[jj,ii] = corr_mat[ii,jj]
    return corr_mat

def quick_correlate(rm,dm,rf,N):
    top_val = np.zeros((N,3))
    mrm = (rm-np.mean(rm))**2
    for ii in xrange(dm.shape[1]):
        for jj in xrange(dm.shape[2]):
                if ii < jj:
                    srt = np.argsort(top_val[:,0])
                    top_val = top_val[srt,:]
                    mdm = (dm[:,ii,jj]-np.mean(dm[:,ii,jj]))**2
                    sig = np.sum(np.sqrt(mdm*mrm)/rf[ii]/rf[jj])            
                    if sig >= top_val[0,0]:
                        top_val[0,:] = sig,ii,jj
                        
    srt = np.argsort(top_val[:,0])
    top_val = top_val[srt,:]
    return top_val

def save_corr_top(pth_out,res1,res2):
    with open(pth_out,'w+') as fopen:
        fopen.write('Residue1\t\tResidue2\n')
        for r1,r2 in zip(res1,res2):
            fopen.write(str(int(r1)) + '\t\t\t' + str(int(r2))+'\n')
