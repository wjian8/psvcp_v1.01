# psvcp: Pan-genome Construction and Population Structure Variation Calling Pipeline

### 1. Introduction

We have developed a user-friendly pangenome construction and PAV genotype calling pipeline.

​    The pipeline  is composed of:
* Linear pan-genome construction based on some assembled genomes.
* Structure Variation (Presence/Absence variation) detecting based on Next generation sequencing data and Linear pan-genome
* Population genotype of PAV calling based on the samples' PAV

### 2. Installation

#### Dependencies
MUMMER (https://github.com/mummer4/mummer)
Assemblytics (https://github.com/marianattestad/assemblytics)
BWA (http://bio-bwa.sourceforge.net/)
Picard (https://github.com/broadinstitute/picard)
Samtools (https://github.com/samtools/samtools)
bedtools (https://github.com/arq5x/bedtools2)
R 4.0.3 or later (https://www.r-project.org/) and packages: 
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

Make sure the Dependencies was installed correctly. In the Linux bash shell environment, you can run "nucmer -h" for testing MUMmer installation, run "python3 -h" for testing python3 installation, run "Assemblytics " for testing Assemblytics installation, run "Rscript" for testing R installation, run "bwa" for testing bwa installation, run "picard" for testing picard installation, run "samtools" for testing samtools installation, run "mosdepth -h" for testing mosdepth installation. In the R environment, you can run "library(hash)" for checking R hash package, etc.. In the python environment, you can run "import re" for checking python re package, etc.

Download the psvcp toolbox from github:
`git clone git@github.com:wjian8/psvcp.git`


Alternatively, you also could obtain the toolbox in the psvcp website and uncompress the psvcp toolbox package:

`tar -zxvf psvcp-v**.tar.gz`

### 3. Main analysis procedures

#### Example data

For the Users can use the pipeline easily, there are example data for testing. The example data including two directory and one file in the work directory.

Here we show the tree of the two directory :

`tree $work_directory`
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

The genome_gff_dir_example is a directory which has the some genome.fa files and genome_annotation.gff files.
The fq_dir_example is a directory which has Next generation sequencing data (fq.gz file). 
The one input file named genome_list is a text file including the genome name. First line is the reference genome, the second line is the first genome which will be compared to reference genome. The third line is the second genome which will be compared to the first linear pan. and so on. Here we show the content of the file:

`cat genome_list`
MSU_0-2M.fa
Lemont_0-2M.fa
CN1_0-2M.fa
R498_0-2M.fa
FH838_0-2M.fa

#### Usage

The pipeline can be used like this:

`python3 $path_of_the_pipeline/Construct_pan_and_Call_sv.py \`
`genome_gff_dir \`
`genome_list \`
`-fqd fq_dir \`
`-o population_hmp`

the ouput file population_hmp is the prefix of a genotype file which is hapmap format.

---

The pipeline can be split into four parts.

1. If you just want to construct a linear pan-genome by two genome.

   `bash $path_of_the_pipeline/1Genome_construct_Pangenome.sh ref.fa query.fa > job.sh && bash job.sh`

   or you want to construct pan-genome by several (more than 2) genome.

   `python3 $path_of_the_pipeline/Construct_pan_and_Call_sv.py genome_example_dir genome_list `

2. It's easy to use bwa to map Next generation sequencing data of one sample against a large reference genome.

   `python3  $path_of_the_pipeline/2Map_fq_to_Pan.py -t 4 -fqd fq_dir -r ReferenceFile -br bam_dir`

   Put the *1.fq.gz and *2.fq.gz file into the fq_dir, the 2Map_fq_to_Pan.py script can map all samples to the reference.

3. Based on the depth information from every bam file. The PAV genotype will be achieved by:

   `python3  $path_of_the_pipeline/3Call_sv_to_genotype.py -br bam_dir -o hmp_prefix`

4. The last part is for GWAS. GWAS will perform with GAPIT.

   `python3 $path_of_the_pipeline/4GWAS_gapit.py phenotype.txt genotype.hmp.txt`

---

If you want to check the insertion sequence from one assembled genome and the insertion sequence in the pan genome. Just run the python script:
`python3 $path_of_the_pipeline/Check_pav.py pan.fa genome_example_dir/R498_0-2M.fa  pan.pav.gff`
The output will show the PAV sequece transport from R498_0-2M.fa to pan.fa

If you want to check the pan gene annotation.
`gffread pan.gff -g pan.fa -y pan.pep.fa `     # pan protain sequence

`python3 $path_of_the_pipeline/Check_gff.py pan.pep.fa genome_example_dir/MSU_0-2M.pep.fa`
The output will show the number of proteins ID in MSU_0-2M.pep.fa and in pan.pep.fa. The output also show the number of proteins sequence in  MSU_0-2M.pep.fa which are the same in pan.pep.fa.

#### Bugs or suggestions
Any bugs or suggestions, please contact the authors.