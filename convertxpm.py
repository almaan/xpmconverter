#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 22:13:37 2018

@author: Alma Andersson

xpm converter is a tool to convert the generated output from gromacs mdmat\n
this tool is to some extent based on the script given by Tsjerk A. Wassenaar, Ph.D.
in the gromacs mailing list. Several modifications in order to support generation 
of time-series and saving the data in different formats have been done.
"""

import argparse as arp


def mat_series(filename):
    split = '/* XPM */'
    lines = []
    with open(filename,'r+') as fopen:
        for line in fopen:
            if split in line:
                lines.append([])
                lines[-1].append(line)
            else:
                lines[-1].append(line)
    return lines

def extract_dmat(xpm):
    def unquote(s):
        return s[1+s.find('"'):s.rfind('"')]
    
    def uncomment(s):
        return s[2+s.find('/*'):s.rfind('*/')]
    
    def col(c):
        color = c.split('/*')
        value = unquote(color[1])
        color = unquote(color[0]).split()
        return color[0], value
    
    xpm_iter = (x for x in xpm)
    meta = [next(xpm_iter)]
    while not meta[-1].startswith("static char *gromacs_xpm[]"):
        meta.append(next(xpm_iter))
    
    dim = next(xpm_iter)
    nx, ny, nc, nb = [int(i) for i in unquote(dim).split()]
    colors = dict([col(next(xpm_iter)) for i in range(nc)])
    dmat = list([])
    for i in xpm_iter:
        if i.startswith("/*"):
            continue
        j = unquote(i)
        z = [float(colors[j[k:k+nb]]) for k in range(0,nx,nb)]
        dmat.append(z)
    return dmat

def generate_frame_matrix(filename):
    frames = mat_series(filename)
    dframes = []
    for frame in frames:
        dframes.append(extract_dmat(frame))
    return dframes


def save_matrix_csv(mat,output):
    ext = output.split('.')[-1]
    if ext != 'csv':
        output = '.'.join(output.split('.')[0::-1]) + '.csv'
    with open(output,'w+') as fopen:
        for frame in mat:
            for line in frame:
                fopen.write(','.join([str(s).replace(']','').replace('[','') for s in line]) + '\n')
            fopen.write('%\n')
    fopen.close()
    
def print_mat(mat):
    for line in mat:
        print ','.join([str(s) for s in line])
    
def save_matrix_npy(mat,output):
    import numpy as np
    ext = output.split('.')[-1]
    if ext != 'npy':
        output = '.'.join(output.split('.')[0::-1]) + '.npy'
    nmat = np.array(mat)
    np.save(output,nmat)

if __name__ == '__main__':

	prs = arp.ArgumentParser()
	prs.add_argument('-f','--filename',help='Name of xpm-file',required=True)
	prs.add_argument('-c','--csvname',help='Name of output csv-file',default='',type=str)
	prs.add_argument('-n','--npyname',help='Name of output numpy-file',default='',type=str)
	prs.add_argument('-v','--verbose',help='Verbose',action='store_true', default=False)
	arg = prs.parse_args()


    dmat = generate_frame_matrix(arg.filename)
    if arg.csvname:
        save_matrix_csv(dmat,arg.csvname)
    if arg.npyname:
        save_matrix_npy(dmat,arg.npyname)
    if (bool(arg.npyname)+bool(arg.csvname)) == 0 or arg.verbose:
        print_mat(dmat)

    
