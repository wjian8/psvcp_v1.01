#!/usr/local/bin/python3  
# -*- coding: utf-8 -*-  
# Usage: python3  $0 -t 9 -fqd fq_dir -r ReferenceFile -br bam_dir
# Author: Jian Wang
# Email: wjian@gdaas.cn

import os,  glob, time, argparse, threading, re

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-t', dest='thread',type=int,default='4') 
my_parser.add_argument('-fqd', dest='input_dir',required=True,help='fq.gz files are in the directory') #
my_parser.add_argument('-r', dest='reference',required=True) #
my_parser.add_argument('-fpf', dest='fq_postfix',default='_1.fq.gz',help="Only fq1 file postfix, like _1.fq.gz or .R1.fastq.gz") #
my_parser.add_argument('-br', dest='bam_dir',default='bam_dir',required=True)
my_parser.add_argument('-bpf', dest='bam_postfix',default='.mapQ20.bam')
args = my_parser.parse_args()
TimeTable = open(args.input_dir+'TimeTable.txt','w')

ref=args.reference
if not os.path.exists(re.sub('fa','fa.sa',ref)):
    os.system('bwa index %s'%(ref))
if not os.path.exists(re.sub('fa','fa.fai',ref)):
    os.system('samtools faidx %s'%(ref))
if not os.path.exists(re.sub('fa','dict',ref)):
    os.system('picard CreateSequenceDictionary -R %s -O %s'%(ref,re.sub('fa','dict',ref)))

output_bam_dir =args.bam_dir
if os.path.exists(output_bam_dir):
    sys.exit(output_bam_dir+' exist!!!')
else:
    os.makedirs(output_bam_dir)

def mult(funct, ls, n=3):
    pool = []  
    length = len(ls)
    step = int(length / n) + 1
    for i in range(0, length, step):
        p = threading.Thread(target=funct, args=(ls[i: i + step],)) 
        pool.append(p)
    for p in pool: 
        p.start() 
    for p in pool:
        p.join() 
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'_Main thread STAR exiting', file=TimeTable)
    TimeTable.flush()

fq1_postfix = args.fq_postfix
fq2_postfix = args.fq_postfix.replace('1','2')
sample_name1 = glob.glob(args.input_dir+'/*'+fq1_postfix)
sample_name2 = glob.glob(args.input_dir+'/*'+fq2_postfix)
sample_prefix1 = [re.findall(r'(\S+?)%s'%fq1_postfix, os.path.basename(sample))[0] for sample in sample_name1]  # all the sample name
sample_prefix2 = [re.findall(r'(\S+?)%s'%fq2_postfix, os.path.basename(sample))[0] for sample in sample_name2]  # all the sample name
sample_prefixs = [i for i in sample_prefix1 if i in sample_prefix2]

bam_list = []
all_sample_fq = {} 

def bwa(part_sample_prefixectory): 
    for sample_prefix in part_sample_prefixectory:
        if not (os.path.exists(args.input_dir+"/"+sample_prefix+fq1_postfix) and args.input_dir+"/"+sample_prefix+fq2_postfix):
            sys.exit(args.input_dir+"/"+sample_prefix+fq2_postfix + ' or '+args.input_dir+"/"+sample_prefix+fq2_postfix + " don't exist!!!")
        os.system('bwa mem -M -t 16 -R  "@RG\\tID:{0}\\tSM:{0}\\tPL:illumina\\tLB:lib1\\tPU:unit1" {1} {2}/{0}{4} {2}/{0}{5} | samtools view -bhS -o {3}/{0}.bam'.format(sample_prefix, ref, args.input_dir, output_bam_dir,fq1_postfix,fq2_postfix))
        time.sleep(0.2)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'bwa_programming finished***In threading***'+sample_prefix, file=TimeTable)
        TimeTable.flush()
        os.system('picard SortSam INPUT={0}/{1}.bam OUTPUT={0}/{1}_sorted.bam SORT_ORDER=coordinate TMP_DIR=./tmp'.format(output_bam_dir,sample_prefix))
        time.sleep(0.2)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'picard_SortSam programming finished***In threading***'+sample_prefix, file=TimeTable)
        TimeTable.flush()
        os.system('rm {0}/{1}.bam'.format(output_bam_dir,sample_prefix))
        os.system('picard AddOrReplaceReadGroups I={0}/{1}_sorted.bam O={0}/{1}_sorted_add.bam RGLB=lib1 RGPL=illumina RGPU=unit1 RGSM={1} TMP_DIR=./tmp'.format(output_bam_dir,sample_prefix))
        time.sleep(0.2)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'picard_AddOrReplaceReadGroups programming finished***In threading***'+sample_prefix, file=TimeTable)
        TimeTable.flush()
        os.system('rm {0}/{1}_sorted.bam'.format(output_bam_dir,sample_prefix))
        os.system('picard MarkDuplicates I={0}/{1}_sorted_add.bam O={0}/{1}_sorted_add_dedup.bam M={0}/{1}_sorted_add_dedup.metrics MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=4000 TMP_DIR=./tmp'.format(output_bam_dir,sample_prefix))
        time.sleep(0.2)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'picard_MarkDuplicates programming finished***In threading***'+sample_prefix, file=TimeTable)
        TimeTable.flush()
        os.system('rm {0}/{1}_sorted_add.bam'.format(output_bam_dir,sample_prefix))
        os.system('samtools view -h -q 20 -F 4 -F 256 -Sb  {0}/{1}_sorted_add_dedup.bam >{0}/{1}{2}'.format(output_bam_dir,sample_prefix,args.bam_postfix))
        os.system('samtools index {0}/{1}{2} '.format(output_bam_dir,sample_prefix,args.bam_postfix))
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'samtools_BuildBamIndex programming finished***In threading***'+sample_prefix, file=TimeTable)
        TimeTable.flush()
        #os.system('rm {0}/{1}_sorted_add_dedup.bam'.format(output_bam_dir,sample_prefix))
        #os.system('rm {0}/{1}_sorted_add_dedup.metrics'.format(output_bam_dir,sample_prefix))

mult(bwa, sample_prefixs, n=args.thread)
TimeTable.close()
