# psvcp: Pan-genome Construction and Population Structure Variation Calling Pipeline

### 1. Introduction

We have developed a user-friendly pangenome construction and PAV genotype calling pipeline.

​    The pipeline  is composed of three main functions:
* Linear pan-genome construction using different assembled genomes.
* Structure Variation (Presence/Absence variation) detecting based on Next-generation sequencing data and Linear pan-genome
* Genotyping of PAV at population level based on the samples' PAVs
 ![1642075445921](README.assets\diagram of workflow.png)
Fig 1 Scheme diagram of PSVCP pipeline. a. construction of linearized pan-genome
b. PAV was re-calling by sequencing coverage calculation. c. population PAV genotype calling


### 2. Installation

#### Dependencies
MUMMER Version: 4.0.0rc1(https://github.com/mummer4/mummer)
Assemblytics (https://github.com/marianattestad/assemblytics)
BWA Version: 0.7.17-r1198-dirty (http://bio-bwa.sourceforge.net/)
Picard (https://github.com/broadinstitute/picard)
Samtools Version: 1.9-49-gb321ed1(https://github.com/samtools/samtools)
bedtools Version: 2.29.2 (https://github.com/arq5x/bedtools2)
R  Version: 4.0.3 (https://www.r-project.org/) and packages: 
    -hash
    -parallel
    -snowfall
Python Version: 3.7.9  (https://www.python.org/) and packages:
    -pandas
    -gzip
    -argparse
    -threading
    -re

#### Installation procedures

Make sure all the Dependencies were installed correctly before running the psvcp toolbox.

Download the psvcp toolbox from github: git clone git@github.com:wjian8/psvcp_v1.01.git


Alternatively, you also could obtain the toolbox in the psvcp website and uncompress the psvcp toolbox package:

`tar -zxvf psvcp-v**.tar.gz`

### 3. Main analysis procedures

#### Example data

Here we provided some example data and a short tutorial to guide the users to use our pipeline. The example data includes two directories and one file in the working directory.

Here are the folders and files structure of the two directories :

```
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
```



The genome_gff_dir_example is a directory that contains different genome assemblies (different genome.fa files) and genome annotations (genome_annotation.gff files). The fq_dir_example is a directory that contains the Next generation sequencing data (fq.gz file). 

The input file named genome_list is a text file including the genome name. It determines the order of whole genome comparison. The first line[[RH1\]](#_msocom_1)  of genome_list fle is the ref0 genome name, the second line is the first genome assemblies which will be compared to the ref0 genome. The ref0 genome will be updated to ref1 genome by adding segments not present in ref0 genome into ref0 genome. The third line is the second genome assemblies which will be compared to the ref1 genome. and so on. In the example, MSU_0-2M.fa is ref0 genome. We perform whole genome comparison between MSU_0-2M.fa (ref0) and Lemont_0-2M.fa, the updated genome will be named ref1 genome. Next, whole genome comparison between ref1 genome and CN1_0-2M.fa will be performed. The second round updated genome will be named ref2 genome. Then we will perform whole genome comparison between ref2 genome and R498_0-2M.fa. And so on. 

Here we show the content of the file:

```
cat genome_list 
MSU_0-2M.fa
Lemont_0-2M.fa
CN1_0-2M.fa
R498_0-2M.fa
FH838_0-2M.fa
```



#### Usage

```
Available commands:

  RefGenomeUpdateByQuest    # Whole genome comparison between refGenome and questGenome, update refGenome by PAV

  GenomeConstructPangenome      # Whole genome comparison between genomes and the reference genome, pan-genome construction

  MapFqToPan # Map short read resequencing data to the pan-genome and detect the PAVs

  CallSVtoGenotype      # Calling population PAV genotype based on all samples’ PAVs

  GWASgapit    

  ConstructPanAndCallPAV # One step for Pan-genome Construction and Population Structure Variation Calling

  CheckGff # Check the pan gene annotation by protein sequence

  CheckPAV      # Check the pan gene annotation by PAV sequence
```

The pipeline can be used like this:

```
python3 $path_of_the_pipeline/psvcp.py ConstructPanAndCallPAV \
 genome_gff_dir \
 genome_list \
 -fqd fq_dir \
 -o population_hmp
```

the ouput file population_hmp is the prefix of a genotype file which is hapmap format.

---

The pipeline can be split into four parts.

1. If you just want to construct a linear pan-genome by two genome.

   ```
   python3 $path_of_the_pipeline/psvcp.py RefGenomeUpdateByQuest ref.fa query.fa
   ```

   or you want to construct pan-genome by several (more than 2) genome.

   ```
   python3 $path_of_the_pipeline/psvcp.py  GenomeConstructPangenome genome_example_dir genome_list
   ```

   

2. It's easy to use bwa to map Next generation sequencing data of one sample against a large reference genome.

   ```
   python3 $path_of_the_pipeline/psvcp.py MapFqToPan -t 4 -fqd fq_dir -r ReferenceFile -br bam_dir
   ```

   Put the *1.fq.gz and *2.fq.gz file into the fq_dir, the 2Map_fq_to_Pan.py script can map all samples to the reference.

3. Based on the depth information from every bam file. The PAV genotype will be achieved by:

   ```
   python3 $path_of_the_pipeline/psvcp.py CallSVtoGenotype -br bam_dir -o hmp_prefix
   ```

4. The last part is for GWAS. GWAS will perform with GAPIT.

    ```
python3 $path_of_the_pipeline/psvcp.py GWASgapit phenotype.txt genotype.hmp.txt
    ```

---

If you want to check the insertion sequence from one assembled genome and the insertion sequence in the pan genome. Just run the python script:

```
python3 $path_of_the_pipeline/psvcp.py CheckPAV pan.fa genome_example_dir/R498_0-2M.fa pan.pav.gff
```


The output will show the PAV sequece transport from R498_0-2M.fa to pan.fa

If you want to check the pan gene annotation.

```
gffread pan.gff -g pan.fa -y pan.pep.fa # pan protain sequence
python3 $path_of_the_pipeline/psvcp.py CheckGff  pan.pep.fa genome_example_dir/MSU_0-2M.pep.fa 
```


The output will show the number of proteins ID in MSU_0-2M.pep.fa and in pan.pep.fa. The output also show the number of proteins sequence in  MSU_0-2M.pep.fa which are the same in pan.pep.fa.

#### Bugs or suggestions
Any bugs or suggestions, please contact the authors.