#!/usr/bin/python3
# Usage: python3 $0 -i TranslocationUniquebed -br bam_dir -o outputfile
#2022.9.14 fixed 130M20S matching situation

import glob, os,  argparse,re

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', dest='TranslocationUniquebed_file',required=True) #
my_parser.add_argument('-br', dest='bam_dir',default='bam_dir',required=True)
my_parser.add_argument('-bpf', dest='bam_postfix',default='.mapQ20.bam')
my_parser.add_argument('-o', dest='outputFile',required=True)
args = my_parser.parse_args()

outputfile1 = open(args.outputFile,'w')
TranslocationbedFile=args.TranslocationUniquebed_file
TranslocationsortedBedUnique =  open(TranslocationbedFile,'r').readlines()

bamfilelist = glob.glob(args.bam_dir+'/*'+args.bam_postfix)
sample_prefix1 = [re.findall(r'(\S+?)%s'%args.bam_postfix, os.path.basename(sample))[0] for sample in bamfilelist]
print('TransID','identity','Chr','posF','\t'.join(sample_prefix1),sep='\t',file=outputfile1)
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
        #print(readpos)
        #print(breakpointChr, breakpointPos)
        if readpos[2] == breakpointChr and int(readpos[3]) < int(breakpointPos)-breakpointregion+1:
            matchbases = re.findall('(\d+)M', readpos[5])
            #print(matchbases)
            if matchbases:
                matchbase = sum([int(m) for m in matchbases])
                if int(breakpointPos)+breakpointregion-1 < int(readpos[3]) + matchbase:
                    ReadsCoverage += 1
    return ReadsCoverage

###############

for line in TranslocationsortedBedUnique:
    lineList = line.rstrip().split()
    TranslocationInfor = lineList[0]
    Identity = lineList[2]
    Chr = lineList[1]
    posF = lineList[8]
    posR = lineList[9]
    oneTranslocationLeftEndInfo = []
    oneTranslocationRightEndInfo = []    
    for bamfile in bamfilelist:
        TranslocationLeftDepth = readabsolutecoverage(bamfile, Chr, posF)
        if TranslocationLeftDepth >=5:
            LeftTranslocationOrNot = "C"   # "C" represent Normal
        else:
            LeftTranslocationOrNot = "A" # "A" represent Translocation
        TranslocationRightDepth = readabsolutecoverage(bamfile, Chr, posR)
        if TranslocationRightDepth >=5:
            RightTranslocationOrNot = "C"   # "C" represent Normal
        else:
            RightTranslocationOrNot = "A" # "A" represent Translocation
        oneTranslocationLeftEndInfo.append(LeftTranslocationOrNot)
        oneTranslocationRightEndInfo.append(RightTranslocationOrNot)
    print(TranslocationInfor,Identity,Chr,posF,'\t'.join(oneTranslocationLeftEndInfo),sep='\t',file=outputfile1)
    print(TranslocationInfor,Identity,Chr,posR,'\t'.join(oneTranslocationRightEndInfo),sep='\t',file=outputfile1)

outputfile1.close()

