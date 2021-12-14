# python3 $0 IRGSP_L032P035P109P149_ins.L032_RAGOO.ins.bed    IRGSP_L032P035P109P149_ins.L032_RAGOO.ins.more_50.bed
import sys,os
print("""awk 'length($7)>50 {print $0}' %s > %s""" % (sys.argv[1],sys.argv[2]))
