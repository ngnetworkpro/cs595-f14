
import csv
import calculate

def writeToFile(ulist):
  #write facebook friends and counts
  with open('facebook.txt', 'w') as O:
    O.write('No.\tName\tCount\n')
    for i in range(len(ulist)):
      O.write(str(i+1)+'\t'+ulist[i]['name']+'\t'+str(ulist[i]['count'])+'\n')
  #compute and save mean, median, and standard deviation
  with open('calculations.txt', 'a') as O:
    clist = []
    O.write('Facebook\n')
    for u in ulist:
      clist.append(u['count'])
    mean = calculate.getMean(clist)  
    O.write('Mean: ' + str(mean) + '\n')
    median = calculate.getMedian(clist)
    O.write('Median: ' + str(median) + '\n')
    stdev = calculate.standardDev(clist)
    O.write('Standard Deviation: ' + str(stdev) + '\n')
	  
with open('facebookFriendFriendsCountTuples.txt', 'r') as csvfile:
  ulist = []
  reader = csv.reader(csvfile)
  for row in reader:
    if row[0] == "USER":
      continue
    else:
      c = row[1].rstrip()
      c = int(c)
      ulist.append({'name':row[0], 'count':c})
  ulist.append({'name':'me', 'count':len(ulist)})
  sorted_u = sorted(ulist, key=lambda k : k['count'])
  writeToFile(sorted_u)