library(graphics)
library(stats)


plot_kmeans_final<-function( k, df,colname1="x", colname2="y")
  {
  
  #empty plot 
  plot(1,t="n", xlim=range(df[colname1]), ylim = range(df[colname2]), xlab=colname1, ylab=colname2, main="Clusters" )
  
  
  
  
  #first the cluster centers in black and big. 
  points( x = k[["centers"]][,1],  y = k[["centers"]][,2], pch ="*", cex=4,col="black" )
  
  
  #now the data colored by cluster 
  colors <- rainbow( nrow(k[["centers"]]) )
  points( x = df[,colname1],  y = df[,colname2], col = colors[ k$cluster  ], pch =  19 )
  }



plot_kmeans<-function( k, df,colname1="x", colname2="y")
{
  
  plot_kmeans_final( k,df,colname1, colname2)

  if( is.null(k[["x_centroids_history"]])) return
  if( is.null(k[["y_centroids_history"]])) return
  
  
  ys <- k[["y_centroids_history"]]
  xs <- k[["x_centroids_history"]]
  

  
  points(x = xs[1,], y = ys[1,], pch ="*", cex=2,col="black")
  
  
  #if the displacement is nearly zsro, the arrow length throws an exception. 
  #it is safe to ignore it 

  for(  n in 2:nrow(xs))
  {
    if( xs[n-1,]!=xs[n,] ||  ys[n-1,]!=ys[n,])
    arrows( xs[n-1,] , ys[n-1,], xs[n,],ys[n,])
  }
  
}

historic_kmeans<- function( df, codevectors, max_iterations = 100, change_threshold = 0.01 )
{
  continue_working = TRUE 
  counter <- 1 
  
  #1-row matrix with 
  #x1 y2  x2 y2 .....xn yn for t = 0, where x,y are the initial centroids 
  centers<- as.matrix ( k["centers"][[1]])
  xs = rbind( codevectors[,1])
  ys = rbind( codevectors[,2])
  
  
  initial_centroids <- codevectors 
  
  while( continue_working == TRUE ) {
    k<-  kmeans( x = df, centers = codevectors, iter.max = 881)
    new_centers = as.matrix( k["centers"][[1]])  
    

    #termination criteria based on the relative amount of change
    
    #how much the centroids changed?
    delta <-  new_centers - codevectors 
    #lengths of the delta vectors
    delta <-  as.matrix( sqrt (rowSums( delta*delta )), ncol = 1 )  
    
    #length of the codevectors before the last step  
    vectors_mod= as.matrix (sqrt( rowSums(codevectors*codevectors) ), ncol =1 ) 
    delta<-delta/vectors_mod
    
    #are there any relative big changes ?
    any_big_changes = length ( which ( delta > change_threshold ))
    if( any_big_changes <= 0 ) continue_working = FALSE 
    
    
    #termination criterion based on maximum iterations 
    counter<- counter + 1
    if( counter >= max_iterations ){
      continue_working = FALSE 
    }
    
    
    xs <- rbind( xs,  new_centers[,1]) #all the x of each step in rows
    ys <- rbind( ys,  new_centers[,2]) #same for y, makes easy to plot 
    
    
    codevectors <- new_centers
    print(continue_working)
  }
  
  k[["x_centroids_history"]] <- xs
  k[["y_centroids_history"]] <- ys
  k[["initial_centroids"]]<-initial_centroids
  
  
  #returns the last ran kmeans with the historic info
  return(k)
} 


