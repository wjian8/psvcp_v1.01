#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# Usage: python3 $0 in_pv.gff

import pandas as pd
import re, sys
df = pd.read_csv(sys.argv[1],sep='\t',header=None)
genes=set([re.findall('ID=(.+?);',gene)[0] for gene in list(df[df.iloc[:,2]=='gene'].iloc[:,8])]) # from a14.tab extract all geneID
gene_in_pv = [any([gene in gff for gene in genes])  for gff in df.iloc[:,8]] # each line which contain mRNA, exon or cds have the geneID info.
df[gene_in_pv].to_csv(sys.argv[2],sep='\t', index=False, header=False,float_format=None)
