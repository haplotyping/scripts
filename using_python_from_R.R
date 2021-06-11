library(reticulate)
library(this.path)

#set location of haplotyping library
parentPath = normalizePath(paste0(dirname(this.path()),.Platform$file.sep,".."))
haplotypingPath <- paste0(parentPath,.Platform$file.sep,"haplotyping")
#haplotypingPath = "/my/location/haplotyping"
print(paste0("assuming haplotyping library is at '",haplotypingPath,"'"))

#import library
haplotyping <- import_from_path("haplotyping", path=haplotypingPath)

#test getting canonical and reverse complement
print(haplotyping$General$canonical("TTTG"))
print(haplotyping$General$reverse_complement("TTTG"))
