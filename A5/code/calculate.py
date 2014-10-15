
import math

def standardDev(clist):
  mean = getMean(clist)
  var = 0
  for c in clist:
    v = pow(c-mean, 2)
    var += v
  var = var/len(clist)
  stdev = math.sqrt(var)
  return stdev
  
  
def getMean(clist):
  sum = float(0)
  for c in clist:
    sum += c
  mean = sum/len(clist)
  return mean
  
def getMedian(clist):
  median = 0
  # if list has even number of elements:
  if len(clist) % 2 == 0:
    m1 = clist[len(clist)/2]
    m2 = clist[(len(clist)/2)+1]
    median = (m1 + m2) /2
  else:
    median = clist[(len(clist)/2)+1]
  return median