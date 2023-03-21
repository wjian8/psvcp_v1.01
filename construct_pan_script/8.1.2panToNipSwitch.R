
#Usage: Rscript $0    output_pos_in_pan.txt    pan.pav.sorted.gff.no_overlap.bed   output_pos_in_ref0.txt
Args <- commandArgs()
gff <- read.table(file=Args[6],header=F)
bed2 <- read.table(file=Args[7],header=F)

library(parallel)
updata_gff_each_chr <- function(chr){
    one_chr_bed2 <- bed2[bed2[,1]==chr,]
    one_chr_gff <- gff[gff[,1]==chr,]
    one_chr_bed2 <- one_chr_bed2[order(one_chr_bed2[,2]),]
    if (nrow(one_chr_bed2) !=0 && nrow(one_chr_gff) !=0){
        new_start <- NULL
        for (j in seq(nrow(one_chr_gff))){
            gene_start <- one_chr_gff[j,4]
            gene_start_copy <- gene_start
            for (i in seq(nrow(one_chr_bed2))){
                if (gene_start_copy>one_chr_bed2[i,2]){
                    gene_start <- gene_start - (one_chr_bed2[i,3] - one_chr_bed2[i,2])
                    }
                else{
                     next
                     }
                }
            new_start <- c(new_start,gene_start)
            }
        gff[gff[,1]==chr,4] <-  new_start
        return(gff[gff[,1]==chr,])
        }
    else{
        return(NULL)
        }
    }

cl <- makeCluster(12)
clusterExport(cl,c('gff','bed2'))
chr_in_bed2=unique(bed2[,1])
chr_in_gff=unique(gff[,1])
chr_not_in_bed2_but_in_gff=setdiff(chr_in_gff,chr_in_bed2)
results <- parLapply(cl, chr_in_bed2, updata_gff_each_chr)
update_gff <- do.call('rbind',results)
stopCluster(cl)
gff_with_chr_no_in_bed2=gff[gff[,1] %in% chr_not_in_bed2_but_in_gff,]
update_all_chr_gff <- rbind(update_gff,gff_with_chr_no_in_bed2)
write.table(update_all_chr_gff ,file=Args[8],sep='\t',col.names=F,row.names=F,quote=F)
