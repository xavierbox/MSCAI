
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

unlabelledData <- rbind ( c(1.01,1.0) )  
unlabelledData <- labelled_df[1:4,1:2]
unlabelledData
 
predictions <-  knnClassify( labelled_df, 3 , unlabelledData)
predictions 
class( predictions)


##################################
# test case 2
##################################
#test data as matrices 
labelled_df<- as.matrix( labelled_df )
labelled_df
unlabelledData<- as.matrix( unlabelledData )
unlabelledData
predictions <-  knnClassify( labelled_df, 3 , unlabelledData)
predictions 
class( predictions)



##################################
# test case 3
##################################
set.seed( 4345 )
create_scatter_circle <-function(  ){
  
  plot(1, t= "n", xlim=c(0,15), ylim=c(0,10), main="Example", xlab="x", ylab="y")
  diam1 <- 3.0
  circle_center <- c(3.0,3.0)
  x1 <- circle_center[1] + runif(10,-1.0, 1.0 )* runif( 10,0.01, 1.0) *diam1
  y1 <- circle_center[2] + runif(10,-1.0, 1.0 )* runif( 10,0.01, 1.0) *diam1
  points(x1,y1,t="p",cex=1.2,col="red", bg="red", pch=23)
  
  labelled_data1 <- cbind( x=x1,y=y1,1)
  
  
  diam2 <- 3.0
  circle_center <- c(12.0,5.0)
  x2 <- circle_center[1] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2 
  y2 <- circle_center[2] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2
  points(x2,y2,t="p",cex=1.2,col="blue", bg="blue", pch=23)
  labelled_data2 <- cbind( x= x2,y = y2,0)

  labelled_data<-rbind( labelled_data2,labelled_data1)
  colnames( labelled_data)<-c("x","y","label")
  
  diam2 <- 3.0
  circle_center <- c(7.0,6.0)
  x3 <- circle_center[1] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2 
  y3 <- circle_center[2] + runif(10,-1.0, 1.0 )* runif( 1,0.1, 1.0) * diam2
  #points(x3,y3,t="p",cex=1.2,col="black", bg="black", pch=21)
  unlabelled_data <- cbind( x= x3,y = y3)

  return ( list(as.data.frame(labelled_data), as.data.frame(unlabelled_data )   ) )
}

#scattred
data <- create_scatter_circle()
unlabelled_data <- data[[2]]
labelled_data   <- data[[1]]
predictions <-  knnClassify( labelled_data, 3 , unlabelled_data)
predictions
co=c("blue", "red")
colors = co[1+predictions]
points(unlabelled_data$x,unlabelled_data$y,t="p",cex=1.4,col=colors)#, bg=colors,pch=23)

#line
unlabelled_data<-data.frame(x=0:12,y=6)
predictions <-  knnClassify( labelled_data, 3 , unlabelled_data)
predictions
co=c("blue", "red")
colors = co[1+predictions]
points(unlabelled_data$x,unlabelled_data$y,t="p",cex=1.4,col=colors)#, bg=colors,pch=23)
legend(1.,9, legend=c("Filled: Training", "Empty: Test") )






