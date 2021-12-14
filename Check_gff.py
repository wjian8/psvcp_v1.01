#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 pan.pep.fa quest.pep.fa
# example: python3 $path/psvcp/Check_gff.py pan.pep.fa genome_example_dir/MSU_0-2M.fa 
from Bio import SeqIO
import sys, os, re
import pandas as pd

pan=open(sys.argv[1],'r')
pan_pep = {}
for record in SeqIO.parse(pan,'fasta'):
   pan_pep[record.id] = record.seq
pan.close()

quest = open(sys.argv[2],'r')
quest_pep = {}
for record in SeqIO.parse(quest ,'fasta'):
   quest_pep[record.id] = record.seq
quest.close()

print('The number of proteins in %s is %s'%(sys.argv[2],str(len(quest_pep))))


i=0
j=0
for key in quest_pep:
    if key in pan_pep:
        j=j+1
        if (quest_pep[key] == pan_pep[key]):
            i=i+1

print('The number of proteins ID in %s and in %s is %d'%(sys.argv[2], sys.argv[1],j))
print('The number of proteins sequence in %s which are the same in %s is %d'%(sys.argv[2], sys.argv[1],i))

