#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 19:38:13 2018

@author: almaan
"""

import sys, os
sys.path.append('../lib')
import convertxpm as xpm
import xvgconverter as xvg
import correlation as corr
import shutil
import tempfile as tmp
import subprocess as sub

#-------Variables------#
start_res_number = 83

path = '/data/PepBind/scripts/motion/xpmconverter/workflow'
trj = '/data/PepBind/4rjd/4rjd_TFP2/sims/center_1.xtc'
tpr = '/data/PepBind/4rjd/4rjd_TFP2/sims/s3_prod.tpr'

tdir = tmp.mkdtemp(dir=path)
#--------gmx commands------#
gmx1 = 'gmx rmsf -f ' + trj + ' -s ' + tpr + ' -o ' + tdir + '/rmsf.xvg' + ' -ox  ' + tdir + '/aver.pdb<<EOF\n1\nEOF' 
gmx2 = 'gmx rms -f ' + trj + ' -s ' + tdir + '/aver.pdb' + ' -o ' + tdir + '/rmsd.xvg' + '<<EOF\n1\nEOF'  
gmx3 = 'gmx rms -f ' + trj + ' -s ' + tdir + '/aver.pdb' + ' -mean ' + tdir + '/mdmat.dm' + ' -frames ' + tdir + '/mdmat.dmf' + '<<EOF\n1\nEOF<<EOF\n1\nEOF'  

result1 = sub.check_output(gmx1, shell=True)
result2 = sub.check_output(gmx2, shell=True)
result3 = sub.check_output(gmx3, shell=True)

rmsf = xvg.xvg_convert(tdir+'/rmsf.xvg',tdir+'/rmsf.npy')
rmsd = xvg.xvg_convert(tdir+'/rmsd.xvg',tdir+'/rmsd.npy')
dmat = xpm.generate_frame_matrix(tdir + '/mdmat.dmf')
shutil.rmtree(tdir)

values = corr.quick_correlate(rmsd,dmat,rmsf,100)
values[:,1:2] = values[:,1:2] + start_res_number
