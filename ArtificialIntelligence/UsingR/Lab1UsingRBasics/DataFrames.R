

#create a fake dataframe

#it can be seen as a collection of vectors of the same length

#three vectors of 18 components 
a <- c(1:17, NA)
b <- letters[1:18]
c <- factor( sample( c("RED", "BLUE", "GREEN"), 18, replace = T ))

length( a )
length( b )
length( c )


#convert to dataframe 
df <- data.frame( v1 = a, v2 = b, v3 = c )

#get the size 
nrow( df )
ncol( df )

#view some rows 
head( df )
head( df,12 )

rownames (df )
colnames(df)

colnames(df) <- c("Col1", "col2", "col3")
colnames(df)

View( df )
class (df )
class( view )
summary(df )

colnames( df )

#get columns and change them 
col1 = df$Col1
col1 <- col1*10 

df$col1 <- col1 
df[2]

#rows 2-12 and columns 1,2 
df [2:12,c(1,2)] 
names <- colnames(df )
df[1:4, c( names[2], names[1])  ] 

#use which

df[ which( df$Col1 > 3 ),  ] 

df[ which( df$col3 == "BLUE")  ] 

condition1 = which( df$Col1 > 4 )
condition2 = which( df$col3 =="BLUE")
condition1
condition2


#import dataframes
library(help="datasets")
head( mtcars )

wd = getwd()
write.csv( mtcars, "mtcars.csv", row.names = F )
wd
cars <- read.csv( file.path( wd,"mtcars.csv") )
cars
class( cars )
colnames(cars )
summary(cars)

filename =  file.path( wd,"mtcars.csv")
data <- read.table( filename, sep =',', header = T)
head( data )  
class ( data )


m <- as.matrix( data )
object.size( m )
object.size( data )

diag( m )
colnames( m )

w = data.frame("cyl"=cars$cyl, "gear"=cars$gear) 
colnames(w)   <- c("cyl", "gear")

#how many cars of 4 cylinders and 6 gears ?
indices = which(  w$cyl ==4 & w$gear > 4 )
indices

w[ indices, ]

library ( stringr )
colnames( w ) <- str_to_upper( colnames(w) )
indices = is.na( w ) 
indices 

w <- na.omit( w )
w[1:10, ] 




circles <- function( number = 5, points = c(25,50), radlimits = c(1.0,6.0),minlimits = c(0,0), maxlimits=c(50,50) ){

  number = 8 
  
  #x and y coordinates 
  rx <- vector(mode="numeric", length=0)
  ry <- vector(mode = "numeric", length = 0 )
  
    for( n in 1:number)
      {

      #center of circle n 
      xo   <- runif( 1, minlimits[1],maxlimits[1])
      yo   <- runif( 1, minlimits[2],maxlimits[2])
      rad  <- runif( 1, radlimits[1],radlimits[2])
      
      #all the points of circle n 
      pts = sample(points,1) 
      print("points in this cirle ")
      print( pts )
      angles <- runif(pts,-3.14,3.14 )
      scale <-  runif(pts, 0.0,1.0)
      
      x <- xo + rad * scale * cos( angles )
      y <- yo + rad * scale * sin( angles )

      ##append to the list of coordinates 
      rx<- c( rx, x )  
      ry<- c( ry, y )  
      }

  return( list(rx,ry) )  
      
  }

set.seed(24335434)
ww = 35 
coords = circles( number = ww )
ww 

x <- unlist(coords[1])
y <- unlist(coords[2])
plot(x,y)



c1 = c( 1:10)
c2 = c( 1:10)
c3 = c( 1:10)
c4 = c( 1:10)

df = data.frame("col1"=c1 , "col2" = c2, "col3" = c3, "col4" = c4 )
df
colnames(df)

#pick one row at random 
i <- sample( 1L:nrow( df ),1  )
datum<- as.numeric( df[ i,  ] ) 
datum 


df - datum 








