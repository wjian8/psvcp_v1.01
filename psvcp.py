#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Author: Jian Wang
# Email: wjian@gdaas.cn
helpInfo = """
# Usage: python3  $0 availableCommand otherParameter
#
AvaliableCommand:
  RefGenomeUpdateByQuest ref.fa quest.fa	# Whole genome comparison between refGenome and questGenome, update refGenome by PAV
  GenomeConstructPangenome genome_dir genome_list	# Whole genome comparison between genomes and the reference genome, pan-genome construction
  MapFqToPan -t 4 -fqd fq_dir -r ReferenceFile -br bam_dir	# Map short read resequencing data to the pan-genome and detect the PAVs
  CallSVtoGenotype -br bam_dir -o hmp_prefix	# Calling population PAV genotype based on all samples’ PAVs
  GWASgapit phonetype.txt genotype.txt	
  ConstructPanAndCallPAV genome_dir genome_list -fqd fq_dir -o out_postfix	# One step for Pan-genome Construction and Population Structure Variation Calling
  CheckGff pan.pep.fa quest.pep.fa	# Check the pan gene annotation by protein sequence
  CheckPAV refN.fa questM.fa refN.pav.gff	# Check the pan gene annotation by PAV sequence
"""
# 
import os, sys
script_dir = os.path.dirname(sys.argv[0])
if len(sys.argv)<=2:
    print("Error, No enough Parameter input")
    print(helpInfo)
    sys.exit(0)
functionCommand = sys.argv[1]
otherParameter = sys.argv[2:]
if (functionCommand == 'ConstructPanAndCallPAV'):
    os.system('python3 %s/Construct_pan_and_Call_sv.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'RefGenomeUpdateByQuest'):
    os.system('bash {0}/Refgenome_update_by_quest.sh {1} > jobRefQuest.sh  && bash jobRefQuest.sh '.format(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'GenomeConstructPangenome'):
    os.system('python3 %s/1Genome_construct_Pangenome.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'MapFqToPan'):
    os.system('python3 %s/2Map_fq_to_Pan.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'CallSVtoGenotype'):
    os.system('python3 %s/3Call_sv_to_genotype.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'GWASgapit'):
    os.system('python3 %s/4GWAS_gapit.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'CheckGff'):
    os.system('python3 %s/Check_gff.py %s'%(script_dir, ' '.join(otherParameter)))
elif (functionCommand == 'CheckPAV'):
    os.system('python3 %s/Check_pav.py %s'%(script_dir, ' '.join(otherParameter)))
else:
    os.system("Error, Wrong availableCommand")
