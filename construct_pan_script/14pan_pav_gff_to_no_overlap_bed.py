# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:31:51 2023
@author: wjian        wjian@gdaas.cn
Delete the redundancy pav, gff -> bed
Usage: python3 $0 pan.pav.gff
"""

import sys
gff_file = open(sys.argv[1], 'r')
bed_file = open(sys.argv[1]+'.no_overlap.bed', 'w')
line1 = gff_file.readline()
if line1:
    chromosome1 = line1.strip().split()[0]
    pos_start1 = line1.strip().split()[3]
    pos_end1 = line1.strip().split()[4]
line2 = True


def overlap_two_seq(start1,end1,start2,end2):
    return(min(start1,end1,start2,end2), max(start1,end1,start2,end2))


while line2:
    line2 = gff_file.readline()
    if line2:
        chromosome2 = line2.strip().split()[0]
        pos_start2 = line2.strip().split()[3]
        pos_end2 = line2.strip().split()[4]
        if chromosome1 != chromosome2 or int(pos_end1) < int(pos_start2):
            print("{}\t{}\t{}".format(chromosome1, pos_start1, pos_end1), file=bed_file)
            chromosome1 = chromosome2
            pos_start1 = pos_start2
            pos_end1 = pos_end2
        else:
            pos_start1, pos_end1 = overlap_two_seq(pos_start1,pos_end1,pos_start2,pos_end2)

    else:
        print("{}\t{}\t{}".format(chromosome1, pos_start1, pos_end1), file=bed_file)
        break
gff_file.close()
bed_file.close()