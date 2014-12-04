bdata = read.table("C:/Users/sybil/Documents/2014 Fall/Web Science/A9/output/blog_pages.txt", header=T, sep="\t")

newdata <- bdata[order(pages),] 
pages <- c(newdata$Pages)
blogs <- c(newdata$Number.of.Blogs)

barplot(blogs, names.arg=pages, xlab="Pages", ylab="Number of Blogs")

