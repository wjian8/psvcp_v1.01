#!/usr/local/bin/python3  
# -*- coding: utf-8 -*-
# Usage: python3 $0 IRGSP.L032_RAGOO2.ins.bed
import re, sys
nucmer2bed = open(sys.argv[1],'r')
nucmer2bed2 = open(sys.argv[1]+'2','w')
for line in nucmer2bed:
    one_line_list = line.rstrip().split()
    qstart = re.findall('(.+?)_(C.+?):(\S+?)-',one_line_list[8])
    if qstart:
        print(one_line_list[0],one_line_list[1],one_line_list[2],one_line_list[5],one_line_list[6],qstart[0][0],qstart[0][1],qstart[0][2],sep='\t',file=nucmer2bed2)
nucmer2bed.close()
nucmer2bed2.close()
