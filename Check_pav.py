#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 refN.fa questM.fa refN.pav.gff
# M < N (they are number)
# example: python3 $path/psvcp/Check_pav.py pan_dir_result/ref2.fa genome_example_dir/CN1_0-2M.fa pan_dir_result/ref2.pav.gff
from Bio import SeqIO
import sys, os, re
import pandas as pd


refN = open(sys.argv[1],'r')
refN_dict ={}
for record in SeqIO.parse(refN,'fasta'):
    refN_dict[record.id] = record.seq  #The dic have chr and sequences
refN.close()

questM = open(sys.argv[2],'r')
questM_dict ={}
for record in SeqIO.parse(questM,'fasta'):
    questM_dict[record.id] = record.seq  #The dic have chr and sequences
questM.close()


questM_basename = os.path.basename(sys.argv[2])
questM_basename_no_postfix = os.path.splitext(questM_basename)[0]

fout = open(sys.argv[3], 'r')

df = pd.read_csv(sys.argv[3],sep="\s+",header=None)
questM_pav = df.loc[df.iloc[:,1]==questM_basename_no_postfix,:]
#print(df)
#print(questM_pav)
#print(questM_pav.iloc[:,1])
refN_pav_equal_quest_seq=[]
for i,row in questM_pav.iterrows():
    chr = row[0]
    pos_start = row[3]
    pos_end = row[4]
    print("########################################################")
    print("The pav seq in %s"%(sys.argv[1]),chr,pos_start,pos_end)
    print(refN_dict[chr][int(pos_start):int(pos_end)])
    length_seq = int(pos_end) - int(pos_start)
    quest = re.findall('ID=(\S+?)_(Chr\d+)_(\d+);',str(row[8]))
    if quest:
        quest_name = quest[0][0]
        quest_chr=quest[0][1]
        quest_pos=quest[0][2]
        print(questM_dict[quest_chr][int(quest_pos):(int(quest_pos)+length_seq)])
        print("The pav seq from %s"%(sys.argv[2]),quest_name,quest_chr,quest_pos,str((int(quest_pos)+length_seq)))
        print("#####################################################")
        if refN_dict[chr][int(pos_start):int(pos_end)] == questM_dict[quest_chr][int(quest_pos):(int(quest_pos)+length_seq)]:
            refN_pav_equal_quest_seq.append(1)
        else:
            refN_pav_equal_quest_seq.append(0)
print(refN_pav_equal_quest_seq)
print('The pav number in %s being same with %s is %d' % (sys.argv[1],sys.argv[2],sum(refN_pav_equal_quest_seq)))
print('The pav number from %s is %d' % (sys.argv[2],questM_pav.shape[0]))
