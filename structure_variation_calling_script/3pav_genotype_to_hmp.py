#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 pav_genotype.file maf

import sys
import pandas as pd

hmp = open(sys.argv[1],'r')
maf = float(sys.argv[2])
genotype_maf = open(sys.argv[1]+'.maf','w')
for num,line in enumerate(hmp):
    if num == 0:
        print(line,file=genotype_maf,end='')
    elif (len(line.rstrip().split('\t')[2:])*maf<line.rstrip().split('\t')[2:].count('A') & line.rstrip().split('\t')[2:].count('A') <len(line.rstrip().split('\t')[2:])*(1-maf) ):
        print(line,file=genotype_maf,end='')
genotype_maf.close()

df = pd.read_csv(sys.argv[1]+'.maf',sep='\t')
df.insert(2,'QCcode','NA')
df.insert(2,'panelLSID','NA')
df.insert(2,'assayLSID','NA')
df.insert(2,'protLSID','NA')
df.insert(2,'center','NA')
df.insert(2,'assembly','NA')
df.insert(2,'strand','+')
df.rename(columns={'chr':'chrom'},inplace=True)
df.insert(0,'alleles','A/C')
df['pos'] = df['pos'].map(lambda x:str(x))
df.insert(0,'rs',df['chrom']+"_"+df['pos'])
df.to_csv(sys.argv[1]+'.maf.hmp.txt',sep='\t',na_rep='NA',index=0) 

