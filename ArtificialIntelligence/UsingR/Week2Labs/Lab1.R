#
#
#  WORKSHEET 1
# 
#

#############################
#  TASK 3 SIMPLE NUMERICS
#############################

result <- 21 * 37  + 2
print(result)

print( sqrt(2) )

print( sqrt(4 - (9/2)) )

result<- 10^200 * 10^150 
print( result )
if (is.infinite(result)){
  print("It is infinite")
}else if(is.nan(result)){
  print("It is nan")
}else{
  print("It is not inf and not nan")
}

#############################
#  TASK 4 vector operations
#############################
#Vector operations. Given vectors x = (1,2,3)^T
#and y = (2,1,−3)^T, write R code to compute the 
#dot product

x <- c( 1,2, 3)
y <- c( 2,1,-3)
print(x)
print(y)

#one way 
element_mult <- x * y 
dot_product  <- sum (element_mult )
print( dot_product )

#another way: using the internal product %*%  
dot_product <- x %*% y 
print( dot_product )

#but neither of these used the transpose. They used x and y 
#as vectors. If we assume that x,y a row vectors, then we 
#need to proceed differently. Lets use matrices 
tx <-  t(cbind( 1,2,3  ))
ty <-  t(cbind( 2,1,-3 ))
print(tx)
print(ty)

#element-wise 
element_mult = t(x) * t(y) 
dot_product  <- sum (element_mult )
print( dot_product )
print( element_mult)


#error, non- conformable arguments.
tx %*% ty 
dim(tx)
dim(ty)
#cannot use dot product because it dfoenst make sense 
#but we can always multiply element by element and sum 





#############################
#  TASK 5: Matrices 
#Study the documentation of the matrix function and construct two matrices
#m1 = 
#1 2
#4 5 

#m2 =
#1 0
#0 2 

#Consult the documentation of the function t and infix operator %*% in the base package, and use these to
#compute their transposes, their sum, and their product. Verify that m1· m2 is different from m2· m1). Can you
#use transposition to compensate for switching the order in which you multiply the matrices?
# Also try to use the %*% operator to compute the inner product of two vectors, e.g. as requested in Task

#############################

m1 = cbind( c(1,4), c(2,5))
m2 = rbind( c(1,0), c(0,2))
m1
m2
dim(m1)
dim(m2)

#matrix product 
m1 %*% m2 
m2 %*% m1 

#sum 
result <- m1 + m2 
result 


#Can you use transposition to compensate for switching 
#the order in which you multiply the matrices?
 
m1 %*% t(m2 )
m2 %*% t(m1 )

#m1 x t( m2 ) = m2 x t( m1 ): good to know 




#############################
#  TASK 6: Plotting 
#Review the documentation for the functions plot and points. 
#Use these functions to plot a graph of the function
#f(x) = x*x  −2x.
#Can you plot the graph as a line, and to use the points function to highlight the minimum of the function
#with a red dot?
################################

library( graphics )
x <- as.numeric( 1:10 )  
fx <- as.numeric( x*x -2*x ) 
x
fx
length(x)
length(fx)


#scatter plot 
plot(x = x ,y = fx )

#as line 
plot(x = x ,y = fx, type = 'l')

#as line and marks 
plot(x = x ,y = fx, col="red", type = 'b', xlab="axis x", ylab = "y axis", main="Chart title")

#plot two lines 
fx2 <- x

cl <- c("red","blue")# rainbow(5)
plot(0,0,xlim = c(0,10),ylim = c(0,100))
data = list(fx,fx2)
for( line in 1:length(data)){
lines(y = unlist( data[line] ) ,x = x, col=cl[line], type = 'b', xlab="axis x", ylab = "y axis", main="Chart title")
}



#############################
#  TASK 7: Reading and Plotting 
#Reading and plotting data. Download the disastersim01.
#sv file from Canvas. Consult the documentation for the 
#read.table function and its variants. Use the appropriate function to load the data into a data
#frame.
#Can you produce some plots resembling those shown in the introductory lecture?
################################

#option 1
datafile = "disastersim01.csv"
path = file.path(getwd(), datafile)
data = read.csv( datafile )
View(data)
class( data )

#option 2
data2 = read.table( datafile, header = TRUE, sep = "," )
View(data2)
class( data2 )
colnames( data2 )

#lets plot something 
colors<- c("red","blue")
plot( x = data2$landX, y = data2$landY,col=colors[1+data2$state], xlab="X", ylab="y", main="state" )


