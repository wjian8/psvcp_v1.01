#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# python $0 mergedInversionsorted.bed
# 

import sys
file1 = open(sys.argv[1],'r')
outfile1 = open(sys.argv[1]+'_unique','w')

InfoLine = file1.readline()
pav_pos1 = InfoLine.rstrip().split('\t')[0:3]
print(InfoLine,end='',file=outfile1)
while 1:
    InfoLine2 = file1.readline()
    if not InfoLine2:
        break
    pav_pos2 = InfoLine2.rstrip().split('\t')[0:3]
    if pav_pos1==pav_pos2:
        pass
    else:
        print(InfoLine2,end='',file=outfile1)
        pav_pos1=pav_pos2
outfile1.close()
