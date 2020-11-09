
setwd("D:/Projects/Personal/TechLe/MsCAI/ArtificialIntelligence/PersonalMnist/")

rotate <- function(x) t(apply(x, 2, rev))

plot_image<-function( m ){
  sample_4 <- matrix(as.numeric(m), nrow = 28, byrow = TRUE)
  image( rotate(sample_4) , col = grey.colors(255))
  
}



data <- read.csv ("train.csv")

labels<-data[,1]
images<-data[,2:785]
plot_image( images[914,])

dim(images)

xx<- as.matrix( images, ncol=784 )
plot_image( xx[14,])

picture <- rotate(t(matrix( xx[45,], ncol = 28, nrow = 28   ))) 
image(picture)
labels[45]

image( picture )
