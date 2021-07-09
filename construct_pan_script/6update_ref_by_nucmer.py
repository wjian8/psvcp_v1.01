#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 ref.fa bed2.file new_ref.fa

from Bio import SeqIO
import sys
import pandas as pd

############
#read the ref.fa into a dictionary, the ref.fa sequence cann't have \s or \n
fin = open(sys.argv[1],'r')
record_dict ={}
for record in SeqIO.parse(fin,'fasta'):
    record_dict[record.id] = record.seq  #The dic have chr and sequences
fin.close()
fout = open(sys.argv[3], 'w')
###########
#read bed.file
df = pd.read_csv(sys.argv[2],sep="\s+",header=None)

###########
for chr in record_dict:
    pos = list(df.loc[df.iloc[:,0]==chr,1])   #the bed.file must have been sorted, pos have the position of one chr. eg chr01 include 3, 6, 8. pos turn the position info into a list
    ins_seq = list(df.loc[df.iloc[:,0]==chr,4]) # the seq of one chr correspond with the pos list
    if len(pos) >= 1:
        for i in range(len(pos)+1):
            if i == 0:
                print(">"+chr,file=fout)
                print(record_dict[chr][:int(pos[i])-1]+ins_seq[i],file=fout,end='')
            elif i == len(pos):
                print(record_dict[chr][int(pos[i-1]):],file=fout)
            else:
                print(record_dict[chr][int(pos[i-1]):int(pos[i])-1]+ins_seq[i],file=fout,end='')
    else:
        print(">"+chr,file=fout)
        print(record_dict[chr],file=fout)