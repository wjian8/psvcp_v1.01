# python3 $0 L032 L032.bed.Assemblytics_structural_variants.bed  L032.coords.bed
import sys,os
print("""awk -v OFS='\\t'  '{{ if ($7 == "Insertion" && $8 >= -10 && $8 <= 10 && $9 >= 50) {{ print $1, $2, $2+$9, $4, ".", $7, $10, ".", "%s""_"$10 }} else if ($7 == "Deletion" && $9 >= 0 && $9 < 20 && $8 > 40) {{ print $1, $2, $2+$8, $4, ".", $7, $1":"$2"-"$3, ".", "%s""_"$10 }} }}' %s | sort -k1,1 -k2,2n -k5,5 -u > %s """ % (sys.argv[1],sys.argv[1],sys.argv[2],sys.argv[3]))
