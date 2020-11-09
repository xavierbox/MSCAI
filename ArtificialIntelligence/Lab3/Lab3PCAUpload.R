
library(stats)
library(graphics)
library(datasets)


getwd()
setwd("D:/Projects/Personal/TechLe/MsCAI/ArtificialIntelligence/Lab3") 
getwd()


add_column <- function( df )
{
  df$z <- 2.0*df$x
  return( df ) 
}

trace <-function( df )
{
  t =0.0
  for(n in 1:ncol( df ))
  {
    t = t + ( df[n,n]);
  }
  return (t); 
}

center <- function( df )
{
  for( c in 1:ncol( df ))
  {
    m = mean( df[,c])
    df[,c]<-df[,c]-m
  }
  
  return (df); 
}

############   TASK 1 ############################################
#########  CONDUCT A PCS MANUALLY                     ############
##################################################################

#generate a test data frame and remove the mean from each column 
d <- expand.grid(x=1:5, y=1:5);
d <- add_column( d ) 
d <- center(d)

#lets get the covariance matrix 
c1 <- cov( d )
print( c1 )

#the trace of the covariance matrix 
print( "trace"); print( trace(c1) )

#lets diagonalize the covariance matrix. This is not the method used by prcomp
solved <-eigen( c1 )
eigen_vectors <- solved$vectors
eigen_values  <- solved$values 
print(eigen_vectors)

print("It is verified that the trace of the original covariance matrix equals the sum of the eigen-values")
print(sum(eigen_values))
print((eigen_values))
barplot( names=c("1","2","3"), height = eigen_values, xlab="Eigen value", ylab="magnitude", main="Diagonalization of the covariance matrix by hand" )
print("The third( smallest) eigenvalue is zero because z = multiple of x (linear dependency)")

#plot the points 
#pairs( d, labels=c("X","Y","Z") )

#lets now do a transformation of the original coordinates to the new space.
#but remove the last eigenvector, which is adding nothing. 
# [a1 b1 c1 ] e11 e21 e31
# [a2 b2 c2 ] e12 e22 e32 
# [a3 b3 c3 ] e13 e23 e33 
#   n x d       d x d    
transf_data <- as.matrix(d, ncol=ncol(d)) %*% eigen_vectors[,-3]
print( transf_data[1:15,] )
colnames(transf_data) <- c("PC1","PC2", "PC3")
plot( transf_data[,1], transf_data[,2], xlab="PC1", ylab="PC2", main="Principal component space", t="p")

#lets see again the covariance matrix in this transformed space 
#it is verified that the matrix is diagonal !!!
cov( transf_data )
print( trace(cov( transf_data ))) #same value!!! 


#using the pcs functions 
pca <- prcomp( d,  retx=TRUE , scale = FALSE, center = TRUE, tol=0.001) #removing the mean does not make difference as expected. 
pca$x[1:15,] #computed new data
(pca$sdev * pca$sdev) 
sum( pca$sdev * pca$sdev ) #must be 12.5 as before
pca$rotation
pca$x[1:5,]

pca_data <- pca$x
plot( pca_data[,1], pca_data[,2], xlab="PC1", ylab="PC2", main="Principal component space", t="p")
#same plot as before !!


biplot( pca, c(1,2), pc.biplot = TRUE,var.axes=TRUE  )


##################################################
#               IRIS DATASET
##################################################

iris_data <- iris 
#View( iris_data )
pairs(iris_data,  pch = 21, main="Iris Dataset", lower.panel=NULL,bg= rainbow(10) [unclass(iris_data$Species)] , labels=c("SL","SW","PL","PW","SP"), font.labels=2, cex.labels=3.5)

pca<-prcomp( iris_data[-5],  retx=TRUE , scale = FALSE, center = TRUE, tol=0.0001)
pca
pca$vars <- pca$sdev*pca$sdev
pca$vars 
barplot( pca$vars,main="PCA -Iris dataset-. Eigen values (variances)",  names=c("PC1","PC2","PC3","PC4"),col=rainbow(5),legend.text=c("PC1","PC2","PC3","PC4"))

biplot( pca, c(1,2), pc.biplot = TRUE,var.axes=TRUE, main="Biplot of 4 P.components"  )
biplot( pca, c(2,3), pc.biplot = TRUE,var.axes=TRUE, main="Biplot of 4 P.components"  )
biplot( pca, c(1,3), pc.biplot = TRUE,var.axes=TRUE, main="Biplot of 4 P.components"  )

pca$rotation
pca$sdev
pc_data <- as.data.frame( pca$x  )  
pc_data$Species <- iris_data$Species
pairs( ~ PC1 + PC2 + PC3 + PC4  + Species, main="Iris dataset after PCA tranform", pch=21, bg=rainbow(10) [unclass(pc_data$Species)], lower.panel=NULL,pc_data, font.labels=2,cex.labels=3) 

#lets repeat but use a tolerance for the magnitude of the variance 
pca2<-prcomp( iris_data[-5],  retx=TRUE , scale = FALSE, center = TRUE, tol=0.2)
pc_data2 <- as.data.frame( pca$x  )  
pc_data2$Species <- iris_data$Species
pairs( ~ PC1 + PC2 + PC3 + Species, main="Iris dataset Only 3 PC's", pch=21, bg=rainbow(10) [unclass(pc_data2$Species)], lower.panel=NULL,pc_data, font.labels=2,cex.labels=3) 


#####################################################







cov( pc_data[,-5] )
#species 
species_names<-unique( iris_data$Species )
print( species_names ) 


