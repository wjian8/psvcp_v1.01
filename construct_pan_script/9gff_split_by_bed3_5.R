#Usage: Rscript $0 a1.gff a3.bed3
Args <- commandArgs()
a1_gff <- read.table(file=Args[6],header=F)
bed3 <- read.table(file=Args[7],header=F)

library(parallel)
#a1_gff <- read.table(file='bchr2.txt',header=F)
#bed3 <- read.table(file='b3.txt',header=F)
split_gff_gene_by_bed3_each_chr <- function(chr){
    one_chr_bed3  <- bed3[bed3[,1]==chr,]
    one_chr_gff <- a1_gff[a1_gff[,1]==chr,]
    pv_split=data.frame()
    for (j in seq(nrow(one_chr_bed3))){
        for (i in seq(nrow(one_chr_gff))){
            if (one_chr_gff[i,3] != 'gene' & one_chr_gff[i,4] < one_chr_bed3[j,2] & one_chr_bed3[j,2] < one_chr_gff[i,5]){
                split_gene_inside <- rbind(one_chr_gff[i,],one_chr_gff[i,])
                split_gene_inside[1,5] <- one_chr_bed3[j,2]    #split_up    cds_start    pv_start
                split_gene_inside[2,4] <- one_chr_bed3[j,3]+1    #split_donw    pv_end     cds_start
                split_gene_inside[1,9] <-  gsub('(ID=.+?);','\\1_1;',one_chr_gff[i,9]) 
                split_gene_inside[2,9] <-  gsub('(ID=.+?);','\\1_2;',one_chr_gff[i,9])
                nrow_one_chr_gff <- nrow(one_chr_gff)
                one_chr_gff <- rbind(one_chr_gff[1:(i-1),], split_gene_inside, one_chr_gff[(i+1):nrow_one_chr_gff,])
                }
            else if (one_chr_gff[i,3] == 'gene' & one_chr_gff[i,4] < one_chr_bed3[j,2] & one_chr_bed3[j,2] < one_chr_gff[i,5]){
                pv_split <- rbind(pv_split,cbind(one_chr_bed3[j,],one_chr_gff[i,]))
                }
            }
        }
    #write.table(pv_split,file=paste("a13_",chr,"pv_split.gff",sep=''),sep='\t',col.names=F,row.names=F,quote=F)
    return(one_chr_gff)
    }
cl <- makeCluster(12)
clusterExport(cl,c('a1_gff','bed3'))
chr_in_bed3=unique(bed3[,1])
chr_in_gff=unique(a1_gff[,1])
chr_not_in_bed3_but_in_gff=setdiff(chr_in_gff,chr_in_bed3)
results <- parLapply(cl, chr_in_bed3, split_gff_gene_by_bed3_each_chr)
update_gff <- do.call('rbind',results)
stopCluster(cl)
gff_with_chr_no_in_bed3=a1_gff[a1_gff[,1] %in% chr_not_in_bed3_but_in_gff,]
update_all_chr_gff <- rbind(update_gff,gff_with_chr_no_in_bed3)
write.table(update_all_chr_gff,file=Args[8],sep='\t',col.names=F,row.names=F,quote=F)



