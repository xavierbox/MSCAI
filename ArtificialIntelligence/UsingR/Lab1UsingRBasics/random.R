

a <- runif( 1,24)


a <- trunc( runif( 10 , 6,12 ) ) 
a

for( n in 1:length(a))
{
  print( a[n] )
  
  if( a[n]%%2 == 0 ){
    print( c(a[n], "It is even"))
  }else{
    print("It is odd")
  }
  
}

