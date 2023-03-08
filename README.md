# psvcp: Pan-genome Construction and Population Structure Variation Calling Pipeline

### 1. Introduction

We have developed a user-friendly pangenome construction and PAV genotype calling pipeline.

​    The pipeline  is composed of:
* Linear pan-genome construction based on assembled genomes.
* Structure Variations (Presence/Absence variations, Inversions and translocations) detection based on Next generation sequencing data and the Linear pan-genome
* Population genotype of PAV calling based on the samples' PAV

### 2. Installation

#### Dependencies
MUMMER v4.0.0 (https://github.com/mummer4/mummer)

Assemblytics v1.2.1 (https://github.com/marianattestad/assemblytics)

BWA-MEM v0.7.17-r1198-dirty (http://bio-bwa.sourceforge.net/)

Picard (https://github.com/broadinstitute/picard)

Samtools v.1.9-49-gb321ed1 (https://github.com/samtools/samtools)

bedtools v2.29.2 (https://github.com/arq5x/bedtools2)

seqkit v1.2 (https://bioinf.shenwei.me/seqkit/)

blastn v2.2.3 (https://blast.ncbi.nlm.nih.gov/Blast.cgi)

R v3.5.0 or later (https://www.r-project.org/) and packages: 
    -hash
    -parallel
    -snowfall
    
python3 (https://www.python.org/) and packages:
    -pandas
    -gzip
    -argparse
    -threading
    -re

#### Installation procedures

Make sure the Dependencies were installed correctly. In the Linux bash shell environment, you can run "nucmer -h" for testing MUMmer installation, run "python3 -h" for testing python3 installation, run "Assemblytics " for testing Assemblytics installation, run "Rscript" for testing R installation, run "bwa" for testing bwa installation, run "picard" for testing picard installation, run "samtools" for testing samtools installation, run "mosdepth -h" for testing mosdepth installation. In the R environment, you can run "library(hash)" to check R hash package, etc. In the python environment, you can run "import re" to check the python re package, etc.

Download the psvcp toolbox from github: https://github.com/wjian8/psvcp_v1.01

Alternatively, you also could obtain the toolbox in the psvcp website and uncompress the psvcp toolbox package:

```tar -zxvf psvcp-v**.tar.gz```

### 3. Main analysis procedures

#### Example data

For the Users can use the pipeline easily, there are example data for testing. The example data including two directory and one file in the work directory.

Here we show the tree of the two directory :

```tree $work_directory```

```
 genome_gff_dir_example
  ├── CN1_0-2M.fa
  ├── CN1_0-2M.fa.fai
  ├── CN1_0-2M.gff
  ├── FH838_0-2M.fa
  ├── FH838_0-2M.fa.fai
  ├── FH838_0-2M.gff
  ├── Lemont_0-2M.fa
  ├── Lemont_0-2M.fa.fai
  ├── Lemont_0-2M.gff
  ├── MSU_0-2M.fa
  ├── MSU_0-2M.gff
  ├── R498_0-2M.fa
  ├── R498_0-2M.fa.fai
  └── R498_0-2M.gff

  fq_dir_example
  ├── IRRI2K_1374_1.fq.gz
  ├── IRRI2K_1374_2.fq.gz
  ├── IRRI2K_1377_1.fq.gz
  ├── IRRI2K_1377_2.fq.gz
  ├── IRRI2K_1380_1.fq.gz
  ├── IRRI2K_1380_2.fq.gz
  ├── IRRI2K_1387_1.fq.gz
  ├── IRRI2K_1387_2.fq.gz
  ├── IRRI2K_1388_1.fq.gz
  ├── IRRI2K_1388_2.fq.gz
  ├── IRRI2K_1390_1.fq.gz
  ├── IRRI2K_1390_2.fq.gz
```

The genome_gff_dir_example is a directory that has the genome.fa files and genome_annotation.gff files. The fq_dir_example is a directory that has Next generation sequencing data (fq.gz file). The one input file named genome_list is a text file including the genome name. The first line is the reference genome, and the second line is the first genome which will be compared to the reference genome. The third line is the second genome which will be compared to the first linear pan. and so on. Here we show the content of the file:

```
cat genome_list
MSU_0-2M.fa
Lemont_0-2M.fa
CN1_0-2M.fa
R498_0-2M.fa
FH838_0-2M.fa
```
High-quality genome assemblies enable high accuracy in genome comparison and SVs identification. Therefore, we suggest that users should use high-quality genome assemblies for pangenome construction by our pipeline.

#### Usage

The pipeline can be used like this:

```
python3 $path_of_the_pipeline/Construct_pan_and_Call_sv.py 
    genome_gff_dir 
    genome_list 
    -fqd fq_dir 
    -o population_hmp
```

the ouput file population_hmp is the prefix of a genotype file which is hapmap format.

---

The pipeline can be split into several parts.

1. If you just want to construct a linear pan-genome by two genome. We recommend users use high-quality genomes for pangenome constructions.  

   ```
   bash $path_of_the_pipeline/1Genome_construct_Pangenome.sh ref.fa query.fa > job.sh && bash job.sh
   ```

   or you want to construct pan-genome by several (more than 2) genome.

   ```
   python3 $path_of_the_pipeline/Construct_pan_and_Call_sv.py genome_example_dir genome_list 
   ```

2. It's easy to use bwa to map Next generation sequencing data of one sample against a pangenome. Put the *1.fq.gz and *2.fq.gz file into the fq_dir, the 2Map_fq_to_Pan.py script can map all samples to the reference.

   ```
   python3  $path_of_the_pipeline/2Map_fq_to_Pan.py -t 4 -fqd fq_dir -r ReferenceFile -br bam_dir
   ```   
Based on our evaluation, with sufficient sequencing coverage of short-read sequencing data, mapping coverage decreased near breakpoints does not affect PAV calling in our pipeline. We recommend sequencing coverage of more than 10x for users using our pipeline.

3. Based on the depth information from every bam file. The PAV genotype will be achieved by:

   ```
   python3  $path_of_the_pipeline/3Call_sv_to_genotype.py -br bam_dir -o hmp_prefix
   ```


4. The last part is for GWAS. GWAS will perform with GAPIT.

   ```
   python3 $path_of_the_pipeline/4GWAS_gapit.py phenotype.txt genotype.hmp.txt
   ```

---
For the Translocation

1. It's easy to use seqkit to get the all PAV sequences with pan sequences and PAV annonotation.
```
seqkit subseq --gtf  pan.pav.sorted.gff -o pan_pav.fa pan.fa
```
2. The PAV sequences were aligned against the reference genome using BLASTN.
```
blastn -task blastn -query pan_pav.fa -db  pan.fa -out pan_pav.fa.blasn.peridentity95long1k.txt -outfmt 6 -num_threads 16 -evalue 1e-10  -word_size 1000 -perc_identity 95
```
3. The translocations could be filter from the BLAST result .
```
python3  $path_of_the_pipeline/translocation_and_inversion/1Translocation_filter_from_blast.py pan_pav.fa.blasn.peridentity95long1k.txt
```
PAV sequences larger than 1kb and matched to 2 or more sequences on pangenome positions with sequences similarity larger than 95% were identified as potential translocations. The positions of the translocations were recorded. The output file "pan_pav.fa.blasn.peridentity95long1k.txt_Translocation" contains all the tranlocations.

4. The population translocations were genotyped by checking the read mapping around translocations' breakpoints, which reads spanning a 39 bp region with a conjunction point at the center. 
```
python3 $path_of_the_pipeline/translocation_and_inversion/2TranslocationBlastSamtoolsGenotype1.02.py -i pan_pav.fa.blasn.peridentity95long1k.txt_Translocation -br bam_dir -o PopulationTranslocationGenotype.txt
```
We counted the number of the reads spanning a 39 bp region with a conjunction point at the centre. If the mapping coverage of translocation's breakpoint was less than 5x, we defined the genotype of the breakpoint as absence ("A"). Otherwise, we defined the genotype (>=5x) as presence ("C").

---
For the Inversion

We have updated the Assemblytics for inversions detecting. You can download the Assemblytics_between_alignments.pl file and overwrite the old one of the Assemblitics V1.2.1. (Assemblytics-master/scripts/Assemblytics_between_alignments.pl).

1. We identified inversions by comparing each genome used for pangenome construction with the pangenome using MUMmer v4.0.0 and Assemblitics V1.2.1. 
Here is the example. We MUMmer CG14 genome against pangenome.
```
mkdir $workplace/pan_CG14;mkdir $workplace/pan_CG14/temp;

nucmer -t 32  --maxgap 500 --mincluster 1000 --diagdiff 20 $workplace/pan.fa $workplace/CG14.fa --prefix $workplace/pan_CG14/pan_CG14

Assemblytics $workplace/pan_CG14/pan_CG14.delta $workplace/pan_CG14/pan_CG14.bed 1000 50 10000000
```

2. We used "grep" and "sort" to get the Inversion information. 

```
for i in  `cat genome_list`; do  grep 'Inversion'  /workplace/${i%.fa}/pan_${i%.fa}/pan_${i%.fa}.bed.variants_between_alignments.bed >> PanGenomeInversion.bed  ;done

sort -nk 1.4 -nk 2 PanGenomeInversion.bed > PanGenomeInversionsorted.bed
```

3. We got the union of the inversions. 

```
python3  $path_of_the_pipeline/translocation_and_inversion/3InversionBedunique.py PanGenomeInversionsorted.bed
```
The output was "PanGenomeInversionsorted.bed_unique"

4. We further genotyped each potential inversion in the pangenome using the short-read sequencing data of accessions by the same method used for translocation genotyping (examining the mapping coverage of the 39 bp region with breakpoints in the centre). 

```
python3 $path_of_the_pipeline/translocation_and_inversion/4InversionBedSamtoolsGenotype1.01.py -i PanGenomeInversionsorted.bed_unique -br bam_dir -o PopulationInversionGenotype.txt
```
We counted the number of the reads spanning a 39 bp region with a conjunction point at the centre. If the mapping coverage of inversion's breakpoint was less than 5x, we defined the genotype of the breakpoint as absence ("A"). Otherwise, we defined the genotype (>=5x) as presence ("C"). "A" means the inversion and "C" means it is synthetic with our pangenome.

PSVCP is robust in placing novel PAV sequences into the linear pangenome, it may be limited to display more complex SVs such as translocations and inversions, which is a challenge in current pangenomics studies, even for the advanced graph-based pangenome. In addition, due to its read length, short-read sequencing data may have lower sensitivity for SVs detection compared with long-read sequencing data.

---



If you want to check the insertion sequence from one assembled genome and the insertion sequence in the pan genome. Just run the python script:

```
python3 $path_of_the_pipeline/Check_pav.py pan.fa genome_example_dir/R498_0-2M.fa  pan.pav.gff
```

The output will show the PAV sequece transport from R498_0-2M.fa to pan.fa

If you want to check the pan gene annotation.
```
gffread pan.gff -g pan.fa -y pan.pep.fa    # pan protain sequence
```

```
python3 $path_of_the_pipeline/Check_gff.py pan.pep.fa genome_example_dir/MSU_0-2M.pep.fa
```
The output will show the number of proteins ID in MSU_0-2M.pep.fa and in pan.pep.fa. The output also show the number of proteins sequence in  MSU_0-2M.pep.fa which are the same in pan.pep.fa.

### Potentail Limitations in the pipeline
PSVCP is robust in placing novel PAV sequences into the linear pangenome, it may be limited to display more complex SVs such as translocations and inversions, which is a challenge in current pangenomics studies, even for the advanced graph-based pangenome. In addition, due to its read length, short-read sequencing data may have lower sensitivity for SVs detection compared with long-read sequencing data. 

#### Bugs or suggestions
Any bugs or suggestions, please contact the authors.

```
wjian@gdaas.cn
```

#### update
2023.3.8
Add a checkpoint in the script "Refgenome_update_by_quest.sh". If no new insertions were identified in comparison to the reference file. The script will skip those steps and generate the new reference from the previous reference without adding insertions.
