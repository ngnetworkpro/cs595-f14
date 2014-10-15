
#Twitter Friends
udata = read.table("C:/Users/sybil/Documents/2014 Fall/Web Science/A5/counts.txt", header=T, sep="\t")
tc <- c(udata$Count)
tu <- c(udata$No.)

df1 <- data.frame(users = factor(tu), tc)

plot(df1, type="l",xlab="User Number", ylab="Friend Count")
lines(df1, lty=1, lwd=2)
text(12,72,'Me',adj=0,3)
points(12,72,pch=22,bg="red")


#################################################
#Linkedin Connections
ldata = read.table("C:/Users/sybil/Documents/2014 Fall/Web Science/A5/linkedin.txt", header=T, sep="\t")
lc <- c(ldata$Count)
lu <- c(ldata$No.)

dfl <- data.frame(users = factor(lu), lc)

plot(dfl, type="l",xlab="User Number", ylab="Connections")
lines(dfl, lty=1, lwd=2)
text(5,39,'Me',adj=0,3)
points(5,39,pch=22,bg="red")

#################################################
#Facebook Friends
fbdata = read.table("C:/Users/sybil/Documents/2014 Fall/Web Science/A5/facebook.txt", header=T, sep="\t")
fbc <- c(fbdata$Count)
fbu <- c(fbdata$No.)

dfu <- data.frame(users = factor(fbu), fbc)

plot(dfu, type="l",xlab="User Number", ylab="Friend Count")
lines(dfu, lty=1, lwd=2)
text(9,95,'Me',adj=0,3)
points(9,95,pch=22,bg="red")
