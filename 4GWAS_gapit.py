#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Usage: python3  $0 phonetype.txt genotype.text
# Author: Jian Wang
# Email: wjian@gdaas.cn

import os, sys

Work_Position1=os.path.abspath(os.path.dirname(sys.argv[1]))
Work_Position2=os.path.abspath(os.path.dirname(sys.argv[2]))
Result_Position=os.path.join(Work_Position1,'Gapit_Result')
script_Position=os.path.dirname(sys.argv[0])
Rpackage_Position=os.path.join(script_Position,'Gapit_Rpackage')
if os.path.exists(Result_Position):
    sys.exit(Result_Position+' exist!!!')
else:
    os.makedirs(Result_Position)

Rscript_mix_model=os.path.join(Rpackage_Position,'mix_model.r')
phenotype=os.path.join(Work_Position1,os.path.basename(sys.argv[1]))
genotype=os.path.join(Work_Position2,os.path.basename(sys.argv[2]))
os.system("Rscript {0} {1} {2} {3} {4}".format(Rscript_mix_model,Rpackage_Position, Result_Position, phenotype, genotype))

