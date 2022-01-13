#!/usr/bin/python3

# Usage: python3 $0 hmp.txt maf
import sys

hmp = open(sys.argv[1],'r')
maf = float(sys.argv[2])
genotype_maf = open(sys.argv[1]+sys.argv[2]+'.maf.txt','w')
for num,line in enumerate(hmp):
    if num == 0:
        print(line,file=genotype_maf,end='')
    elif (len(line.rstrip().split('\t')[11:])*maf<line.rstrip().split('\t')[11:].count('A') & line.rstrip().split('\t')[11:].count('A') <len(line.rstrip().split('\t')[11:])*(1-maf) ):
        print(line,file=genotype_maf,end='')
genotype_maf.close()

