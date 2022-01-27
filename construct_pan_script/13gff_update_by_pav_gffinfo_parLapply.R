
#Usage: Rscript $0 snp.gff.file  pav.gff.file update1.gff
Args <- commandArgs()
gff <- read.table(file=Args[6],header=F)
pavgff <- read.table(file=Args[7],header=F)

library(parallel)
updata_gff_each_chr <- function(chr){
    one_chr_pavgff <- pavgff[pavgff[,1]==chr,]
    one_chr_gff <- gff[gff[,1]==chr,]
    one_chr_pavgff <- one_chr_pavgff[order(one_chr_pavgff[,4]),]
    if (nrow(one_chr_pavgff) !=0 && nrow(one_chr_gff) !=0){
        new_start <- NULL
        for (j in seq(nrow(one_chr_gff))){
            gene_start <- one_chr_gff[j,4]
            for (i in seq(nrow(one_chr_pavgff))){
                if (gene_start>one_chr_pavgff[i,4]){
                    gene_start <- gene_start + one_chr_pavgff[i,5] - one_chr_pavgff[i,4]
                    }
                else{
                     break
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
clusterExport(cl,c('gff','pavgff'))
chr_in_pavgff=unique(pavgff[,1])
chr_in_gff=unique(gff[,1])
chr_not_in_pavgff_but_in_gff=setdiff(chr_in_gff,chr_in_pavgff)
results <- parLapply(cl, chr_in_pavgff, updata_gff_each_chr)
update_gff <- do.call('rbind',results)
stopCluster(cl)
gff_with_chr_no_in_pavgff=gff[gff[,1] %in% chr_not_in_pavgff_but_in_gff,]
update_all_chr_gff <- rbind(update_gff,gff_with_chr_no_in_pavgff)
write.table(update_all_chr_gff ,file=Args[8],sep='\t',col.names=F,row.names=F,quote=F)
