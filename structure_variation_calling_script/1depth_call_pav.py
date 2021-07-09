#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 depth.infor.gz.file out.file depth_threshold gap_threshold
# The input file is the depth information file from mosdepth output, it can be per-base.bed.gz or regions.bed.gz
# The output file show the present/absent situation in one sample. This file have 8 columns. On every line, the 2 column means the begining of the absence region and the 6 column means the ending of the absence region. The 2 column also means the ending of a presence region of last line and he 6 column means the begining of a presence region of next line. the 4 and 8 columns contain the depth information.
import gzip
import sys
depths = gzip.open(sys.argv[1],'r').readlines()
outputfile = open(sys.argv[2], 'w')
depth_threshold=sys.argv[3]
gap_threshold=sys.argv[4]
av_or_not = True
chromosome = depths[0]
for line in depths:
    line = line.decode('utf-8')
    if chromosome.split()[0] == line.split()[0]:
        if float(line.split()[3]) <= float(depth_threshold):
            if av_or_not:
                absence_present_line=line.rstrip()
                av_or_not = False
                chromosome = line
            else:
                chromosome = line
        else:
            if av_or_not:
                chromosome = line
            else:
                absence_present_line=absence_present_line+'\t'+line.rstrip()
                if float(absence_present_line.split()[5])-float(absence_present_line.split()[1])>float(gap_threshold):
                    print(absence_present_line,file=outputfile)
                av_or_not = True
                chromosome = line
    else:
        if not av_or_not:
            absence_present_line=absence_present_line+'\t'+chromosome.rstrip()
            if float(absence_present_line.split()[5])-float(absence_present_line.split()[1])>float(gap_threshold):
                print(absence_present_line,file=outputfile)
        chromosome = line
        if float(line.split()[3]) <= float(depth_threshold):
            absence_present_line=line.rstrip()
            av_or_not = False
        else:
            av_or_not = True
if not av_or_not:
        absence_present_line=absence_present_line+'\t'+chromosome.rstrip()
        if float(absence_present_line.split()[5])-float(absence_present_line.split()[1])>float(gap_threshold):
            print(absence_present_line,file=outputfile)
outputfile.close()
