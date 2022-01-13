#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Usage: python3 $0 genome_dir genome_list
# Author: Jian Wang
# Email: wjian@gdaas.cn

import os, sys, glob, time, argparse, threading, re

my_parser = argparse.ArgumentParser()
my_parser.add_argument('genome_dir', help='genome_dir contains genome.fa and genome.gff')
my_parser.add_argument('genome_list', help='genome_list is a text file, First line is ref.fa, second or else line is query.fa')
my_parser.add_argument('-t', dest='thread',type=int,default='12')
args = my_parser.parse_args()

script_dir = os.path.dirname(sys.argv[0])
genome_dir = args.genome_dir
genome_list = open(args.genome_list,'r') # MSU.fa DHX2.fa
if os.path.exists('pan_dir_result'):
    sys.exit('pan_dir_result exist!!!')
else:
    os.makedirs('pan_dir_result')
    os.makedirs('pan_dir_result/temp')

for num,value in enumerate(genome_list):
    if num==0:
        ref = 'ref'+str(num)
        os.system('ln %s/%s pan_dir_result/ref0.fa'% (genome_dir,value.strip()))
        os.system('ln %s/%s pan_dir_result/ref0.gff'% (genome_dir,re.sub(re.escape('.fa'),'.gff',value.strip())))
    else:
        round=num
        os.system("bash {5}/{0} pan_dir_result/{1} {4}/{2} > job{3}.sh && bash job{3}.sh && rm -f job{3}.sh".format("Refgenome_update_by_quest.sh",ref+'.fa',value.strip(),num,genome_dir,script_dir))
        os.system('ln pan_dir_result/%s pan_dir_result/ref%s.fa'%(ref+value.strip(),num))  #ref0DHX2.fa ref1.fa
        os.system('ln pan_dir_result/%s pan_dir_result/ref%s.gff'%(re.sub(re.escape('.fa'),'.gff',ref+value.strip()),num))
        os.system('ln pan_dir_result/%s pan_dir_result/ref%s.pav.gff'%(re.sub(re.escape('.fa'),'.pav.gff',ref+value.strip()),num))
        ref = 'ref'+str(num)
genome_list.close()
os.system('ln pan_dir_result/ref%s.gff pan.gff'%(num))
os.system('ln pan_dir_result/ref%s.fa pan.fa'%(num))