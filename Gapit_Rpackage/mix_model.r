Args <- commandArgs()
setwd(Args[6]) # work directory with R.package and the data.
#BiocManager::install('multtest')
library(multtest)
library(gplots)
library(LDheatmap)
library(genetics)
library(ape)
library(EMMREML)
library(compiler) #this library is already installed in R
library("scatterplot3d")
source("./gapit_functions.txt")
source("./emma.txt")
setwd(Args[7])
#Step 1: Set working directory and import data
myY <- read.table(Args[8], head = TRUE)
myG <- read.table(Args[9] , head = FALSE)
#Step 2: Run GAPIT
myGAPIT <- GAPIT(
Y=myY,
G=myG,
PCA.total=3
)
