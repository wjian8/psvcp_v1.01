#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 bed3.file pav.gff

import sys, re

bed3 = open(sys.argv[1],'r')
gffout = open(sys.argv[2], 'w')
for line in bed3:
    line = line.rstrip()
    line_list = line.split()
    if line_list:
        Insertion_name = 'ID='+'_'.join(line_list[5:])+";Name="+'_'.join(line_list[5:])
        print(line_list[0],line_list[5],"Insertion",line_list[1],line_list[2],".","+",".",Insertion_name,sep='\t',file=gffout)
bed3.close()
gffout.close()
