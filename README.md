# psvcp

## Pan-genome Construction and Population Structure Variation Calling pipeline

The pipeline  is composed of:

* Linear pan-genome construction based on some assembled genome.
* Structure Variation (Presence/Absence variation) calling based on Next generation sequencing data and Linear pan-genome
* Population genotype of PAV construction based on the samples' PAV

## Dependencies
MUMMER
Assemblytics
BWA
Picard
Samtools
bedtools
R
  -hash
  -parallel
  -snowfall
python3
  -pandas
  -gzip
  -argparse
  -threading
  -re

## Usage

The software from 'dependencies' list should be installed.

The pipeline can be used like this:

`python3 $path_of_the_pipeline/Construct_pan_and_Call_sv.py \`

`genome_gff_dir \`

`genome_list \`

`-fqd fq_dir \`

`-o population_hmp`

This is an example of input file and directory:

1. tree work_directory

├── fq_dir
│   ├── L32-DSW42950-S_L8_1.fq.gz
│   ├── L32-DSW42950-S_L8_2.fq.gz
│   ├── P109-DSW43014-S_L2_1.fq.gz
│   ├── P109-DSW43014-S_L2_2.fq.gz
│   ├── P149-DSW43053-S_L2_1.fq.gz
│   ├── P149-DSW43053-S_L2_2.fq.gz
│   ├── P35-DSW43287-S_L6_1.fq.gz
│   └── P35-DSW43287-S_L6_2.fq.gz
├── genome_gff_dir
│   ├── 02428.fa
│   ├── 02428.gff
│   ├── DHX2.fa
│   ├── DHX2.fa.fai
│   ├── DHX2.gff
│   ├── MSU.fa
│   └── MSU.gff
├── genome_list

2. cat genome_list
MSU.fa
   DHX2.fa
02428.fa

The genome_gff_dir is a directory which has the some genome.fa files and genome_annotation.gff files.

The genome_list is a text file including the genome name. First line is the reference genome, the second line is the first genome which will be compared to reference genome. The third line is the second genome which will be compared to the first linear pan. and so on. 

The fq_dir is a directory which has Next generation sequencing data (fq.gz file).

population_hmp is the prefix of a genotype file which is hapmap format.



The pipeline can be split into three parts.

1. If you just want to construct a linear pan-genome by two genome.

   `bash $path_of_the_pipeline/1Genome_construct_Pangenome.sh ref.fa query.fa > job.sh && bash job.sh`

2. It's easy to use BWA to map Next generation sequencing data of one sample against a large reference genome.

   ` python3  $path_of_the_pipeline/2Map_fq_to_Pan.py -t 4 -fqd fq_dir -r ReferenceFile -br bam_dir`

   Put the fq.gz file into the fq_dir, the 2Map_fq_to_Pan.py script can map all samples to the reference.

3. Based on the depth information from every bam file. The PAV genotype will be achieved by:

   `python3  $path_of_the_pipeline/3Call_sv_to_genotype.py -br bam_dir -o hmp_prefix`
