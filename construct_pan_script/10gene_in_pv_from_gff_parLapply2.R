#Usage: Rscript $0 L032_RAGOO.all.gene.gff IRGSP_L032_bed3
# fix 2024.9.14    add:   (nrow(one_chr_bed3) > 0 & nrow(one_chr_gff) > 0)
Args <- commandArgs()
RAGOO_gff <- read.table(file=Args[6],header=F) #gff
bed3 <- read.table(file=Args[7],header=F) #bed3

library(parallel)

get_pv_gene_each_chr <- function(chr){
    one_chr_bed3  <- bed3[bed3[,7]==chr,]
    one_chr_gff <- RAGOO_gff[RAGOO_gff[,1]==chr,]
    gene_in_pv = data.frame()
    if (nrow(one_chr_bed3) > 0 & nrow(one_chr_gff) > 0) {
        for (i in seq(nrow(one_chr_gff))){
            for (j in seq(nrow(one_chr_bed3))){
                    if (one_chr_bed3[j,8]<=one_chr_gff[i,4] & one_chr_gff[i,5]<=one_chr_bed3[j,8]+nchar(one_chr_bed3[j,5])-1){
                    gene_in_pv  <- rbind(gene_in_pv,cbind(one_chr_gff[i,],one_chr_bed3[j,]))
                    }
                }
            }
        }
    return(gene_in_pv)
    }
cl <- makeCluster(12)
clusterExport(cl,c('RAGOO_gff','bed3'))
results <- parLapply(cl, unique(bed3[,1]), get_pv_gene_each_chr)
all_gene_in_pv <- do.call('rbind',results)
stopCluster(cl)
print(nrow(all_gene_in_pv))
if (nrow(all_gene_in_pv) > 0){
    write.table(all_gene_in_pv,file=Args[8],sep='\t',col.names=F,row.names=F,quote=F)
    }
