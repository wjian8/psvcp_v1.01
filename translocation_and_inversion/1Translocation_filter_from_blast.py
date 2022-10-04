#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# python $0 blast.out.file  
# the blast out file is format 6

import sys
file1 = open(sys.argv[1],'r')
outfile1 = open(sys.argv[1]+'_NotTranslocation','w')
outfile2 = open(sys.argv[1]+'_Translocation','w')

InfoLine = file1.readline()
pav_pos1 = InfoLine.rstrip().split('\t')[0]
last_lineoutputWhere = 0
while 1:
    InfoLine2 = file1.readline()
    if not InfoLine2:
        if last_lineoutputWhere == 0:
            print(InfoLine,end='',file=outfile1)
        else:
            print(InfoLine,end='',file=outfile2)
        break
    pav_pos2 = InfoLine2.rstrip().split('\t')[0]
    if pav_pos1!=pav_pos2:
        #print(pav_pos1+'\t'+pav_pos2)
        if last_lineoutputWhere == 0:
            print(InfoLine,end='',file=outfile1)
        else:
            print(InfoLine,end='',file=outfile2)
        pav_pos1=pav_pos2
        InfoLine=InfoLine2
        last_lineoutputWhere = 0
    else:
        print(InfoLine,end='',file=outfile2)
        InfoLine=InfoLine2
        last_lineoutputWhere = 1
outfile1.close()
outfile2.close()