#Usage: Rscript $0 bed2.file 
Args <- commandArgs()
bed2 <- read.table(file=Args[6],header=F)
bed2_new <- bed2

for (chr in unique(bed2[,1])){
    one_chr_bed2 <- bed2[bed2[,1]==chr,]  
    one_chr_bed2_new <- bed2_new[bed2_new[,1]==chr,]
    new_start <- NULL
    for (j in seq(nrow(one_chr_bed2_new))){
        pv_start <-one_chr_bed2_new[j,2]
        for (i in seq(nrow(one_chr_bed2))){
            if (one_chr_bed2_new[j,2]>one_chr_bed2[i,2]){
                pv_start <- pv_start + nchar(as.character(one_chr_bed2[i,5]))-1
                }
            else{
                 break
                 }
            }
        new_start <- c(new_start,pv_start)
        }
    bed2_new[bed2_new[,1]==chr,2] <-  new_start
    }

bed2_new[,3] <- nchar(as.character(bed2_new[,5]))+bed2_new[,2]-1
#bed2_new$ins_stop <- nchar(as.character(bed2_new[,5]))+bed2_new[,8]-1
bed3_name = gsub('bed2$','bed3',Args[6])
write.table(bed2_new,file=bed3_name,sep='\t',col.names=F,row.names=F,quote=F)
