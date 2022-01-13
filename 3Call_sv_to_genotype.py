#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 -br bam_dir -o hmp_prefix
# Author: Jian Wang
# Email: wjian@gdaas.cn

import os, sys, glob, sys, re, argparse

script_dir = os.path.dirname(sys.argv[0])
my_parser = argparse.ArgumentParser(description="Genome Structure Variation Calling Pipeline. The bam_dir should contain bam files and bai files, This pipeline will generate a hapmap file based on the reads depth information in each bam file")
my_parser.add_argument('-t', dest='mosdepth_thread',default='12')
my_parser.add_argument('-br', dest='bam_dir',required=True)
my_parser.add_argument('-bpf', dest='bam_postfix',default='.bam')
my_parser.add_argument('-d', dest='depth_threshold',default='5')
my_parser.add_argument('-g', dest='min_gap_threshold',default='50')
my_parser.add_argument('-w', dest='mosdepth_window',default='20')
my_parser.add_argument('-m', dest='maf',default='0.05')
my_parser.add_argument('-o', dest='output_prefix',required=True)
args = my_parser.parse_args()
bam_sample_names = glob.glob(args.bam_dir+"/*%s"%args.bam_postfix)
mosdepth_output_dir=args.bam_dir+'_mosdepth_dir'
if os.path.exists(mosdepth_output_dir):
    os.system('rm -rf '+mosdepth_output_dir)
    os.makedirs(mosdepth_output_dir)
else:
    os.makedirs(mosdepth_output_dir)

bam_sample_prefixs = [re.findall(r'(\S+?)%s'%args.bam_postfix, os.path.basename(sample))[0] for sample in bam_sample_names]
for bam_sample in bam_sample_prefixs:
    os.system("mosdepth -t {4} -b {3} -x {2}/{1}  {0}/{1}{5}".format(args.bam_dir, bam_sample, mosdepth_output_dir, args.mosdepth_window, args.mosdepth_thread, args.bam_postfix))
    os.system("python3 {4}/structure_variation_calling_script/1depth_call_pav.py {0}/{1}.regions.bed.gz {0}/{1}{2}depth_{3}bp.txt {2} {3}".format(mosdepth_output_dir,bam_sample,args.depth_threshold,args.min_gap_threshold,script_dir))

os.system('Rscript {5}/structure_variation_calling_script/2merge_samples_pav_to_population.r {0} {1}depth_{2}bp.txt {3} {4}'.format(mosdepth_output_dir,args.depth_threshold,args.min_gap_threshold,args.output_prefix,args.mosdepth_thread,script_dir))
os.system('python3 {1}/structure_variation_calling_script/3.1pav_genotype_to_hmp.py {0}'.format(args.output_prefix,script_dir))
os.system('python3 {2}/structure_variation_calling_script/3.2hapmap_screen_maf.py {0}.hmp {1}'.format(args.output_prefix,args.maf,script_dir))
#os.system('rm -f {0} {0}.maf'.format(args.output_prefix))
