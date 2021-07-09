# Usage: Rscript $0 depthfile_dir postfix_of_one_PAV_information_file outputfile thread_num
# This R script and depthFile are in the same directory
# the depthfile_dir contain the PAV_information_file. The PAV_information_file was outputfile by 1depth_call_pav.py
# parallel split by the samples
Args <- commandArgs()
library(hash)
library(parallel)
library(snowfall)
depthfile_dir = Args[6]
thread_num = as.numeric(Args[9])
h=hash()
for (file_name in list.files(path=depthfile_dir,pattern=paste('*',Args[7],sep=''))){    #All the depth file was plased in the directory
    .set(h, keys=file_name ,values= read.table(file=paste(depthfile_dir,"/",file_name,sep=''),header=F))  # read all the depth file
    }
list_chr <- unique(as.character(h[[keys(h)[1]]][,1]))
call_chr_pos  <- function(chr){#split one sample by chromosome, parallel with more than one CPU to headle the data
    pav_pos=NULL     # pav_pos will include all the position of the pav, like snp marker positon.
    for (i in keys(h)){
        sample_depth = h[[i]]
        one_chr = sample_depth[sample_depth[,1]==chr,]
        pav_pos=sort(unique(c(pav_pos,one_chr[,2,drop=T],one_chr[,6,drop=T])))
        }
    pav <- data.frame(pav_pos)
    pav <- cbind(chr,pav)
        colnames(pav)[c(1,2)] <- c('chr','pos')  #update the column name
        return(pav)
    }
call_onc_chr_pav <- function(chr){  #deal with every sample with the loop
    sample_depth = h[[each_sample]]   # in the function, each_sample is just one sample
        pav_pos <- all_chr_pos_frame[all_chr_pos_frame[,1]==chr,] #all the position of one chromosome
        pav <- pav_pos
        one_chr_depth = sample_depth[sample_depth[,1]==chr,]  #the initial data of one chromosome
        absence = data.frame(one_chr_depth[,2,drop=F],'A')
        presence = data.frame(one_chr_depth[,6,drop=F],'C')
        colnames(absence) <- c('depth','situation')
        colnames(presence) <- c('depth','situation')
        pv_gene_source <- rbind(absence,presence)
        pv_gene_source_sort <- pv_gene_source[order(pv_gene_source[,1]),]  #all the date of one chromosome, the format: 1 column is position; 2 column is A or C
        sample1_pv <- seq(nrow(pav_pos))
        for (i in seq(nrow(pav_pos))){  #call the absence(A)/presence(C) for every position
            marker_pos <- which(pv_gene_source_sort[,1] <= pav_pos[i,2])  #search the pav position in the pv_gene_source_sort
            if (length(marker_pos)==0){
                sample1_pv[i]<-'C'
                }
            else{
                marker_pos <- marker_pos[length(marker_pos)]       #In pv_gene_source_sort, for example it is  3  A   9  C   12 A  18 C, now i is 10, marker_pos contain all the position <= 9, and marker_pos get the last one
                sample1_pv[i]<-as.character(pv_gene_source_sort[marker_pos,2])    #i will get the C from 9, sample1_pv and pav have the same length, they can be merged by column.
                }
            }
        pav <- cbind(pav,sample1_pv)
        colnames(pav)[ncol(pav)] <- each_sample  #update column name, pav include 3 column, chr pos AorC
        return(pav)
        }

call_pav <- function(each_sample){  #deal with every sample with loop
    thread=hash()
    .set(thread,keys=paste(each_sample,'_thread',sep=''),values=makeCluster(1))
    clusterExport(thread[[paste(each_sample,'_thread',sep='')]],c('h','all_chr_pos_frame','list_chr','each_sample','call_onc_chr_pav','depthfile_dir'),envir=environment())
    clusterEvalQ(thread[[paste(each_sample,'_thread',sep='')]],library(hash))
    clusterEvalQ(thread[[paste(each_sample,'_thread',sep='')]],library(parallel))
    one_sample_result <- parLapply(thread[[paste(each_sample,'_thread',sep='')]],list_chr,call_onc_chr_pav)
    one_sample_results <- do.call('rbind',one_sample_result)
    stopCluster(thread[[paste(each_sample,'_thread',sep='')]])
    write.table(one_sample_results,file=paste(depthfile_dir,'/',each_sample,'_pav',sep=''), sep='\t', row.names=F, quote=F)
    #  now one_sample_all_info contain 3 column information of every chromosome on one sample
    return(one_sample_results[,3,drop=F])
    }


cl2 <- makeCluster(thread_num)
clusterExport(cl2,c('h'))
clusterEvalQ(cl2,library(hash))
pos_results <- parLapply(cl2, list_chr,call_chr_pos)
all_chr_pos_frame <- do.call('rbind',pos_results)
stopCluster(cl2)
write.table(all_chr_pos_frame,file='all_chr_pos_frame.txt', sep='\t', row.names=F, quote=F)


sfInit(parallel = TRUE, cpus = thread_num, slaveOutfile = 'progress.txt')
sfLibrary(hash)
sfLibrary(parallel)
sfExport('h','all_chr_pos_frame','list_chr','call_onc_chr_pav','depthfile_dir')
sample_name <- keys(h)
results <- sfLapply(sample_name,call_pav)
finall_pav_without_pos <- do.call('cbind',results)
finall_pav<- cbind(all_chr_pos_frame,finall_pav_without_pos)
sfStop()
write.table(finall_pav,file=Args[8],sep='\t',row.names=F,quote=F)

