#Usage: Rscript $0 bed3.file a4.file
Args <- commandArgs()
bed3 <- read.table(file=Args[6],header=F)
gene_in_pv <- read.table(file=Args[7],header=F)

PVgene_in_update_genome = data.frame()
PVgene_in_update_genome_more_info  = data.frame()
for (i in seq(nrow(gene_in_pv))){
    gene_i_in_bed3_line  = which(bed3[,7]==gene_in_pv[i,16] & bed3[,8]==gene_in_pv[i,17])
    if (length(gene_i_in_bed3_line) != 1){
        print(paste("line ",i,"in gene_in_pv could be found in bed3 or bed3 have more than one PV in one position"))
        next
        }
    gene_start_in_update_genome <- bed3[gene_i_in_bed3_line,2]+gene_in_pv[i,4]-gene_in_pv[i,17]
    gene_end_in_update_genome <- bed3[gene_i_in_bed3_line,2]+gene_in_pv[i,5]-gene_in_pv[i,17]
    PVgene_in_update_genome = rbind(PVgene_in_update_genome,cbind(bed3[gene_i_in_bed3_line,1],gene_in_pv[i,2:3],gene_start_in_update_genome,gene_end_in_update_genome,gene_in_pv[i,6:9]))
    #PVgene_in_update_genome_more_info = rbind(PVgene_in_update_genome_more_info,cbind(bed3[gene_i_in_bed3_line,1],gene_in_pv[i,2:3],gene_start_in_update_genome,gene_end_in_update_genome,gene_in_pv[i,6:18],gene_in_pv[i,4:5]))
   }
write.table(PVgene_in_update_genome,file=Args[8],sep='\t',col.names=F,row.names=F,quote=F)
#write.table(PVgene_in_update_genome_more_info,file=paste("a5_",Args[7],".more.info",sep=''),sep='\t',col.names=F,row.names=F,quote=F)
