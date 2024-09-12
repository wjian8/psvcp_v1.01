#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# Usage: python3 $0 i.gff.in_pv i.gff_gene_absolutly.in_pv

import pandas as pd
import re, sys
df = pd.read_csv(sys.argv[1],sep='\t',header=None)
genes_info = [gene_info for gene_info in list(df[df.iloc[:,2]=='gene'].iloc[:,8])]
if genes_info:  # if the pav include gene
    gene_name = re.findall('ID=(.+?);',genes_info[0]) # most gff file have geneinfo like:  ID=gene:Osmh63.08G000180;biotype=protein_coding;logic_name=oryza_cshl
    if gene_name:
        genes = set([re.findall('ID=(.+?);', gene)[0] for gene in list(df[df.iloc[:, 2] == 'gene'].iloc[:, 8])])  # from a14.tab extract all geneID
        gene_in_pv = [any([gene in gff for gene in genes]) for gff in
                      df.iloc[:, 8]]  # each line which contain mRNA, exon or cds have the geneID info.
        df[gene_in_pv].to_csv(sys.argv[2], sep='\t', index=False, header=False, float_format=None)
    else:
        gene_name = re.findall('ID=(.+)',genes_info[0]) # some gff file have geneinfo like:  ID=OsHZ_03g0355400
        if gene_name:
            genes = set([re.findall('ID=(.+)', gene)[0] for gene in list(df[df.iloc[:, 2] == 'gene'].iloc[:, 8])])
            gene_in_pv = [any([gene in gff for gene in genes]) for gff in
                          df.iloc[:, 8]]  # each line which contain mRNA, exon or cds have the geneID info.
            df[gene_in_pv].to_csv(sys.argv[2], sep='\t', index=False, header=False, float_format=None)

