#!/usr/bin/python3
# Usage: python3 $0 -i InversionUniquebed -br bam_dir -o outputfile
#2022.9.14 fixed 130M20S matching situation

import glob, os,  argparse,re

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', dest='InversionUniquebed_file',required=True) #
my_parser.add_argument('-br', dest='bam_dir',default='bam_dir',required=True)
my_parser.add_argument('-bpf', dest='bam_postfix',default='.mapQ20.bam')
my_parser.add_argument('-o', dest='outputFile',default='InversionGenotype.txt',required=True)
args = my_parser.parse_args()

outputfile1 = open(args.outputFile,'w')
InversionbedFile=args.InversionUniquebed_file
InversionsortedBedUnique =  open(InversionbedFile,'r').readlines()

bamfilelist = glob.glob(args.bam_dir+'/*'+args.bam_postfix)
sample_prefix1 = [re.findall(r'(\S+?)%s'%args.bam_postfix, os.path.basename(sample))[0] for sample in bamfilelist]
print('Chr','posF','\t'.join(sample_prefix1),sep='\t',file=outputfile1)
#############
# input: bam and breakpoint position
# output: the ReadsCoverage of the breakpoint region (40 bp)
breakpointregion = 20
def readabsolutecoverage(bam, breakpointChr, breakpointPos):
    beforebreakpointregion = int(breakpointPos)-breakpointregion
    afterbreakpointregion = int(breakpointPos)+breakpointregion
    sam = os.popen('samtools view %s %s:%d-%d'% (bam,breakpointChr,beforebreakpointregion,afterbreakpointregion),'r')
    ReadsCoverage = 0
    while 1:
        line1 = sam.readline()
        if not line1:
            break
        readpos = line1.rstrip().split()
        if readpos[2] == breakpointChr and int(readpos[3]) < int(breakpointPos)-breakpointregion+1:
            matchbases = re.findall('(\d+)M', readpos[5])
            #print(matchbases)
            if matchbases:
                matchbase = sum([int(m) for m in matchbases])
                if int(breakpointPos)+breakpointregion-1 < int(readpos[3]) + matchbase:
                    ReadsCoverage += 1
    return ReadsCoverage

###############

for line in InversionsortedBedUnique:
    lineList = line.rstrip().split()
    Chr = lineList[0]
    posF = lineList[1]
    posR = lineList[2]
    oneInversionLeftEndInfo = []
    oneInversionRightEndInfo = []    
    for bamfile in bamfilelist:
        InversionLeftDepth = readabsolutecoverage(bamfile, Chr, posF)
        if InversionLeftDepth >=5:
            LeftInversionOrNot = "C"   # "C" represent Normal
        else:
            LeftInversionOrNot = "A" # "A" represent Inversion
        InversionRightDepth = readabsolutecoverage(bamfile, Chr, posR)
        if InversionRightDepth >=5:
            RightInversionOrNot = "C"   # "C" represent Normal
        else:
            RightInversionOrNot = "A" # "A" represent Inversion
        oneInversionLeftEndInfo.append(LeftInversionOrNot)
        oneInversionRightEndInfo.append(RightInversionOrNot)
    print(Chr,posF,'\t'.join(oneInversionLeftEndInfo),sep='\t',file=outputfile1)
    print(Chr,posR,'\t'.join(oneInversionRightEndInfo),sep='\t',file=outputfile1)

outputfile1.close()

