#!/usr/bin/env Rscript
# The following code is for handling the transferring of 4, 96-well plates
# to a 384 well plate in four quadrants that would be convenient for pipetting:
#
#        |
#   1    |   2
#        |
#-----------------
#        |
#   3    |   4
#        |  
#
# The files you select MUST GO IN THIS ORDER!
# 
# Additionally, the xlsx files should have two columns:
#   The first = Well Position (96 well format)
#   The second = Sample ID
# 
# The xlsx file should be ordered by Well Position
# before using this code (A1,A2,A3,A4...B1,B2...etc)
# (sorry I didn't make this sorting automatic but is something that could be done)
#
# To call the code simply enter the following:
# source('plate2384')
# main()
#
# you may need to use the absolute path to the plate2384.R file
# if your xlsx files are in a different directory than it.

require(xlsx)

main <- function() {
  xlsfile1 <- file.choose()
  xlsfile2 <- file.choose()
  xlsfile3 <- file.choose()
  xlsfile4 <- file.choose()
  
  plate384 <- matrix(data = NA, nrow = 16, ncol = 24)
  rownames(plate384) <- c('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P')
  colnames(plate384) <- seq(from =1, to = 24)
  
  # quadrant 1
  plate1 <- read.xlsx2(xlsfile1,1)
  plate384 <- insert_quadrant(plate96=plate1,plate384=plate384,p384_rowIx=seq(1,16,2),p384_colIx=seq(1,24,2))
  
  # quadrant 2
  plate2 <- read.xlsx2(xlsfile2,1)
  plate384 <- insert_quadrant(plate96=plate2,plate384=plate384,p384_rowIx=seq(1,16,2),p384_colIx=seq(2,24,2))
  
  # quadrant 3
  plate4 <- read.xlsx2(xlsfile4,1)
  plate384 <- insert_quadrant(plate96=plate4,plate384=plate384,p384_rowIx=seq(2,16,2),p384_colIx=seq(1,24,2))
  
  # quadrant 4
  plate3 <- read.xlsx2(xlsfile3,1)
  plate384 <- insert_quadrant(plate96=plate3,plate384=plate384,p384_rowIx=seq(2,16,2),p384_colIx=seq(2,24,2))
  
  
  
  # get indices for each entry
  for (j in 1:16) {
    indices <- matrix(NA,nrow=24,ncol=2)
    for (i in 1:24) {
      indices[i,1] = paste(rownames(plate384)[j],colnames(plate384)[i],sep="")
      indices[i,2] = plate384[j,i]
    }
    if (j==1) {
      I <- indices
    } else {
      I <- rbind(I,indices)
    }
  }
  colnames(I) <- c("Well", "Sample")
  
  write.csv(I, file = "IndexList.csv", row.names = F)
  write.csv(plate384, file = "PlateLayout.csv")
}

insert_quadrant <- function(plate96,plate384,p384_rowIx,p384_colIx) {
  p <- matrix(plate96$ID, nrow = 8)
  j<-1
  for (i in p384_colIx) {
    plate384[p384_rowIx,i] <- p[,j]
    j<-j+1
  }
  return(plate384)
}

if(!interactive()){
  main()
}
