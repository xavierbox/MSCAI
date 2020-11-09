
source("NearestNeighbours.R")

##################################
# test case 1
##################################
#test data as dataframes 
labelled_df <- data.frame()
labelled_df <- rbind ( c(1,1,1),c(2,2,2), c(3,3,3), c(4,4,4),c(5,5.,5),c(6.,6.2,6) )  
labelled_df <- as.data.frame( labelled_df )
colnames(labelled_df)<-c("v1","v2","label")
labelled_df

unlabelledData <- labelled_df[1:4,1:2]
unlabelledData
 
predictions <-  knnClassify( labelled_df, 2 , unlabelledData)
predictions 
class( predictions)


##################################
# test case 2
##################################
source("NearestNeighbours.R")
#test data as matrices 
labelled_df <- rbind ( c(1,1,1),c(1.3,1,1), c(3,1,3), c(3.4,1,3),c(5,1.,5),c(5.7,1,5) )  
unlabelledData <- rbind ( c(1,1),c(1.2,2), c(3.4,4), c(5,5) )  

predictions <-  knnClassify( labelled_df, 3 , unlabelledData)
predictions 
class( predictions)



##################################
# test case 3
##################################


set.seed( 4345 )
create_scatter_circles <-function(  ){
  
  plot(1, t= "n", xlim=c(0,15), ylim=c(0,6), main="Example", xlab="x", ylab="y")
  diam1 <- 3.0
  circle_center <- c(3.0,3.0)
  x1 <- circle_center[1] + runif(10,-1.0, 1.0 )* runif( 10,0.01, 1.0) *diam1
  y1 <- circle_center[2] + runif(10,-1.0, 1.0 )* runif( 10,0.01, 1.0) *diam1
  points(x1,y1,t="p",cex=1.2,col="red", bg="red", pch=23)
  
  labelled_data1 <- cbind( x=x1,y=y1,1)
  
  
  diam2 <- 3.0
  circle_center <- c(12.0,3.0)
  x2 <- circle_center[1] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2 
  y2 <- circle_center[2] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2
  points(x2,y2,t="p",cex=1.2,col="blue", bg="blue", pch=23)
  labelled_data2 <- cbind( x= x2,y = y2,0)

  labelled_data<-rbind( labelled_data2,labelled_data1)
  colnames( labelled_data)<-c("x","y","label")
  
  return (as.data.frame(labelled_data))
}

#scattred
labelled_data <- create_scatter_circles()

#line
unlabelled_data<-data.frame(x=1:15,y=2)

#more lines 
unlabelled_data <- rbind( unlabelled_data, data.frame(x=1:15,y=3 ) )
unlabelled_data <- rbind( unlabelled_data, data.frame(x=1:15,y=4 ) )
unlabelled_data <- rbind( unlabelled_data, data.frame(x=1:15,y=5 ) )
unlabelled_data <- rbind( unlabelled_data, data.frame(x=1:15,y=1 ) )

predictions <-  knnClassify( labelled_data, 3 , unlabelled_data)
predictions

reds <- which(predictions>0L) 
points(unlabelled_data[reds,]$x,unlabelled_data[reds,]$y,t="p",cex=1.4,col="red")#, bg=colors,pch=23)

blues <- which(predictions<1L) 
points(unlabelled_data[blues,]$x,unlabelled_data[blues,]$y,t="p",cex=1.4,col="blue")#, bg=colors,pch=23)
legend(0.25,6., legend=c("Filled: Training", "Empty: Test") )


