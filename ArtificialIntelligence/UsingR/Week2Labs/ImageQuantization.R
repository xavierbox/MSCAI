


#FIRST: install.packages## if necessary
library(imager)
library(graphics)
library(png)
library(jpeg)


file = "CoronaCat.jpg"
path = getwd()
full_path1 = file.path( path, file )
plot( load.image(full_path1) )


image1<- readJPEG(full_path1)
str(image1)

#produce a number of images with 2,4,.32,1024 colors
for( n in c(2,4,6,8,16,32,64,128,256,1024)){
  
  file_name2 = paste( paste( "ReducedCoronaCat", n ), ".jpg")
  full_path2 = file.path( path, file_name2 )
  
  #from the docs 
  red_channel    <- matrix(image1[,, 1], ncol=1) #255x255 matrix to 1 column matrix 
  green_channel  <- matrix(image1[,, 2], ncol=1) #255x255 matrix   ...
  blue_channel   <- matrix(image1[,, 3], ncol=1) #255x255 matrix   ...
  
  #the dataframe
  df <- as.data.frame( cbind(red_channel, green_channel, blue_channel) )
  colnames(df)<-c("RED","GREEN","BLUE")
  head( df )
  
  #kmeans 
  kresult <- kmeans( df , n, iter.max = 1000 )
  print("done")
  clusters <- kresult["cluster"]
  df["cluster"]<- clusters
  
  #replace the colors by the average values of the cluster the pixel belongs to
  for ( n in range( clusters))
  {
    meanr = mean( df$RED[ which( df$cluster == n )] )
    meang = mean( df$GREEN[ which( df$cluster == n )] )
    meanb = mean( df$BLUE[ which( df$cluster == n )] )
    
    df$RED[ which( df$cluster == n ) ]   <- meanr 
    df$GREEN[ which( df$cluster == n ) ] <- meang 
    df$BLUE[ which( df$cluster == n ) ]  <- meanb 
  }
  
  #not longer needed, free memory 
  df$cluster <- NULL 
  
  #creating an image from the arrays only should be easy but...I couldnt
  #so i just made a copy of the original and then replaced the channels 
  image2<-image1 
  
  image2[,,1]<-df$RED
  image2[,,2]<-df$GREEN
  image2[,,3]<-df$BLUE
  
  written <- writeJPEG(image2, full_path2, quality=1.0)
  
  #plot in the project 
  plot( load.image(full_path2) )
  
}

















