#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 19:38:13 2018

@author: almaan
"""

import sys, os
sys.path.append('../lib')  
import xvgconverter as xvg
import shutil
import tempfile as tmp
import subprocess as sub


path = '/data/PepBind/scripts/motion/xpmconverter/workflow'
trj = '/data/PepBind/4rjd/4rjd_TFP2/sims/center_1.xtc'
tpr = '/data/PepBind/4rjd/4rjd_TFP2/sims/s3_prod.tpr'

tdir = tmp.mkdtemp(dir=path)
#tname = tdir()
print tdir
#--------gmx commands------#
gmx1 = 'gmx rmsf -f ' + trj + ' -s ' + tpr + ' -o ' + tdir + '/rmsf.xvg' + ' -ox  ' + tdir + '/aver.pdb<<EOF\n1\nEOF' 
#gmx2
#os.system(gmx1)
result = sub.check_output(gmx1, shell=True)
xvg.xvg_convert(tdir+'/rmsf.xvg',tdir+'/rmsf')

#result2 = sub.check_output('')
#shutil.rmtree(tdir)
#