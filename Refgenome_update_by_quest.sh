#!/bin/bash

# Usage: bash $0 ref.fa query.fa
# Author: Jian Wang
# Email: wjian@gdaas.cn

script_dir=${0%/*}
ref_fa=${1##*/}  #del the path of the file
query_fa=${2##*/}
ref_genome_dir=${1%/*}
query_genome_dir=${2%/*}
prefix_base=${ref_fa%.fa}_${query_fa%.fa}
echo "if [ ! -d 'temp' ]; then mkdir temp; fi"
echo "mkdir ${ref_genome_dir}/$prefix_base ${ref_genome_dir}/$prefix_base/temp"
echo "nucmer -t 32  --maxgap 500 --mincluster 1000 --diagdiff 20 $1 $2 --prefix ${ref_genome_dir}/${prefix_base}/$prefix_base"
echo "echo '1 nucmer ok'"
echo "Assemblytics ${ref_genome_dir}/${prefix_base}/${prefix_base}.delta ${ref_genome_dir}/${prefix_base}/${prefix_base}.bed   1000 50 10000000"
python3 ${script_dir}/construct_pan_script/2variants_to_coords.bed.py ${query_fa%.fa} ${ref_genome_dir}/${prefix_base}/${prefix_base}.bed.Assemblytics_structural_variants.bed ${ref_genome_dir}/${prefix_base}/${prefix_base}.coords.bed
echo "echo '2 Assemblytics ok'"
echo "python3 ${script_dir}/construct_pan_script/3replace_regions_with_nucleotides1.2.py ${ref_genome_dir}/${prefix_base}/${prefix_base}.coords.bed $1 $2 $prefix_base > ${ref_genome_dir}/${prefix_base}/${prefix_base}.final.bed"
echo "echo '3 final.bed ok'"
echo "grep Deletion ${ref_genome_dir}/${prefix_base}/${prefix_base}.final.bed > ${ref_genome_dir}/${prefix_base}/${prefix_base}.del.bed"
echo "grep Insertion ${ref_genome_dir}/${prefix_base}/${prefix_base}.final.bed > ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.bed"
python3 ${script_dir}/construct_pan_script/4ins_more_50.py ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.bed ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed
echo "echo '4 more_50.bed ok'"
echo "python3 ${script_dir}/construct_pan_script/5ins.bed_to_bed2.py ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed"
echo "echo '5 more_50.bed2 ok'"
echo "python3 ${script_dir}/construct_pan_script/6update_ref_by_nucmer.py $1 ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed2 ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.fa"
echo "echo '6 6update_ref_by_nucmer.py ok'"
echo "Rscript ${script_dir}/construct_pan_script/7bed2_update_bed3.R ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed2"
echo "echo '7 7bed2_update_bed3.R ok'"

echo "python3 ${script_dir}/construct_pan_script/7.2bed3_to_gff.py ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed3 ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.bed3.pav.gff"
echo "echo '7.2 7.2bed3_to_gff.py ok'"

echo "if [ $ref_fa == 'ref0.fa' ]; 
then 
ln ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.bed3.pav.gff ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.pav.gff;
else 
Rscript ${script_dir}/construct_pan_script/8.2pav_gff_update_by_bed2info_parLapply.R ${ref_genome_dir}/${ref_fa%.fa}.pav.gff ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed2 ${ref_genome_dir}/${ref_fa%.fa}.update1.pav.gff;
cat ${ref_genome_dir}/${ref_fa%.fa}.update1.pav.gff ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.bed3.pav.gff > ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.pav.gff;
fi"

echo "Rscript ${script_dir}/construct_pan_script/8gff_update_by_bed2info_parLapply.R ${ref_genome_dir}/${ref_fa%.fa}.gff ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed2 ${ref_genome_dir}/${ref_fa%.fa}.update1.gff"
echo "echo '8 8gff_update_by_bed2info_parLapply.R ok'"
echo "Rscript ${script_dir}/construct_pan_script/9gff_split_by_bed3_6.R ${ref_genome_dir}/${ref_fa%.fa}.update1.gff ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed3 ${ref_genome_dir}/${ref_fa%.fa}.update2.gff"   #output update2.gff
echo "echo '9 9gff_split_by_bed3_5.R ok'"

echo "Rscript ${script_dir}/construct_pan_script/10gene_in_pv_from_gff_parLapply2.R ${query_genome_dir}/${query_fa%.fa}.gff ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed3 ${ref_genome_dir}/${query_fa%.fa}.gff.in_pv"   #output gff.in_pv 
echo "echo '10 10gene_in_pv_from_gff_parLapply2.R ok'"
echo "python3 ${script_dir}/construct_pan_script/11gene_in_pv_screen.py ${ref_genome_dir}/${query_fa%.fa}.gff.in_pv ${ref_genome_dir}/${query_fa%.fa}.gff_gene_absolutly.in_pv"   #gff_gene_absolutly.in_pv
echo "echo '11 11gene_in_pv_screen.py ok'"
echo "Rscript ${script_dir}/construct_pan_script/12bed3_update_gff.R ${ref_genome_dir}/${prefix_base}/${prefix_base}.ins.more_50.bed3 ${ref_genome_dir}/${query_fa%.fa}.gff_gene_absolutly.in_pv ${ref_genome_dir}/${query_fa%.fa}.gene_absolutly_in_pv.gff" #output gene_absolutly_in_pv.gff
echo "echo '12 12bed3_update_gff.R ok'"
echo "cat ${ref_genome_dir}/${ref_fa%.fa}.update2.gff ${ref_genome_dir}/${query_fa%.fa}.gene_absolutly_in_pv.gff > ${ref_genome_dir}/${ref_fa%.fa}${query_fa%.fa}.gff"
echo "echo '13 cat gff ok'"
