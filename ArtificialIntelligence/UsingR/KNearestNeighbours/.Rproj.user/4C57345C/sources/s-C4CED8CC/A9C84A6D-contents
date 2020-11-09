####################################################
# KNN implementation. Xavier Garcia Teijeiro, 2020 #
# Assignment number 1 (quiz)                       #
####################################################
#
#' @returns  Returns an integer with the predicted labels for the unlabelledData 
# The label predicted wll be the mode of the labels of the k nearest neighbours 
# to each observation. In case of multi-mode situations, the numerical smallest
# mode will be returned
#

#' @parameter labelledData is a dataframe or a matrix, the columns are the 
# features + 1 label column, rows = observations 
#     x11,x12....x1n, y1 
#     x21,x22....x2n, y2
#     x31,x32....x3n, y3 
#     x41,x42....x4n, y4
#
#' @parameter unlabeledData is also a data.frame or matrix, but without the label.
# k corresponds to the number of nearest neighbors to consider
#
#' @notes nans are assumed to have been removed and no exception handling 
# was implemented yet 
#
knnClassify <- function( labelledData, k, unlabelledData)
{
  
  if( k<1 ){
    print("The value of K must be greater than or equal to 1")
    return (NA)
  } 
  if(ncol(labelled_df) - ncol( unlabelledData) != 1L){
    print("The number of columns in the train/test datasets is not correct")
    return (NA)
  }
  
  
  #helper function defined inside the main function to keep it self-contained 
  #returns the mode of the argument. If it is a multi-mode input, the returned 
  #will still be a numeric but indexable -no dims-
  vals_mode <- function(data) {                     
    unique_values <- unique(data)
    tab_values <- tabulate(match(data, unique_values))
    unique_values[tab_values == max(tab_values)]
  }
  
  #helper function 
  #returns a dataframe. column1 = distance(euclidean) column2=label #nrows = 1
  #labelledData is as described before, the_point_df is a dataframe that corresponds
  #to one row in the test set 
  get_keuclid_dist_labels<-function(labelledData, the_point_df, k ){
    
    #we do this to be able to accept either a matrix or a data.frame in line 39
    point_df <- as.numeric( the_point_df )

    #create a data.frame that will be returned 
    dist <- data.frame() 
    nfeatures <- ncol(labelledData) - 1
    for( n in 1:nrow(labelledData)) dist<- rbind(  dist, (labelledData[n,1:nfeatures]- point_df[1]) ) 
    dist<- sqrt(rowSums( dist*dist) )
    

    #also add some more meaningful column names 
    dist <- data.frame( "distance"=dist,  "label" = labelledData[,nfeatures+1])

    #now lets sort the data in ascending order according to distance 
    dist <- dist [ order( dist["distance"]), ] 
    
    #keep only the first k neighbours 
    dist <- dist [ 1:k, ]
    
    return( dist )  
  }
   
  #initialize the matrix to return (its integer class will be enforced later)
  pred_labels<-matrix( ncol =1, nrow = 0)
  
  #for each row
  for( n in 1:nrow(unlabelledData )){        
    
    #get one datum either as a data frame or matrix 
    point_df <- unlabelledData[n, ]
    
    #get a dtaframe of distances and labels of the k-closest neighbours 
    distances_df <- get_keuclid_dist_labels( labelledData, point_df,  k ) 
    #distance     label 
    # 1.407160     4    
    # 4.035402     1    
    # 8.035402     2    
    #    (...etc...)
    
    #with the stored distances we could weight their contributions(next version). 
    modes <- vals_mode(  distances_df$label )
    
    #returns always the smallest of the modes if multi-mode, ex: 1,1,1,2,3,3,3)
    mode  <- modes[ which.min(modes) ] 
    
    pred_labels<- rbind( pred_labels, "label"=mode)
  }
  
  return (as.integer(pred_labels ))
  
}

#potential enhancements: 
#manage exceptions, 
#weighted distance as opposed to mode. 
#It would be good to be able to configure the distance so we could choose 
#other distance options (manhattan for instance) as opposed to euclidean 
#This is better done if we could pass a lambda as argument but didnt manage 
#to do that in this version 


