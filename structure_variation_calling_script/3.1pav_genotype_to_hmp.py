#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 pav_genotype.file

import sys
import pandas as pd

df = pd.read_csv(sys.argv[1],sep='\t')
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
df.to_csv(sys.argv[1]+'.hmp',sep='\t',na_rep='NA',index=0)
