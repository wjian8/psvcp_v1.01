#Usage: python3 $0 gwas.result.csv
import sys
result_file=sys.argv[1]
f=open(result_file,"r")
fout=open(result_file+"_for_qqman.txt","w")
for l in f.readlines():
    line=l.split(",")
    if line[0]=="SNP":
            fout.writelines("SNP")
            fout.writelines("\t")
            fout.writelines("CHR")
            fout.writelines("\t")
            fout.writelines("BP")
            fout.writelines("\t")
            fout.writelines("P")
            fout.writelines("\t")
            fout.writelines("\n")
            continue
    for j in range(4):
        fout.writelines(line[j])
        fout.writelines("\t")
    fout.writelines("\n")
f.close
fout.close()

