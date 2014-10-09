import random
from bs4 import BeautifulSoup

#read the file from the downloads directory
#after reading the file, feed the data into beautiful soup to get the links
#write them to the output file, in the links directory
def getLinks(u,f):
  inFile = 'downloads/'+f  
  outFile = 'links/'+f
  with open(inFile, 'r') as file:
    data = file.read()
 
  soup = BeautifulSoup(data)
  if len(soup.find_all('a')) > 0:
    with open(outFile, 'a', 0) as O:
      O.write('site:\nhttp://')
      O.write(u)
      O.write('\nlinks:\n')
      for link in soup.find_all('a'):  #http://www.crummy.com/software/BeautifulSoup/bs4/doc/
        l = str(link.get('href'))
        if l.startswith('http'):
          O.write(l)
          O.write('\n')
  else:
    print 'no links found in ' + f

if __name__ == '__main__':
  mFile = open('mapping.txt')
  uri = list()
  out = list()
  ran = list()
  
  try:
    for line in mFile:
      mapping = line.split('\t')
      uri.append(mapping[0])
      out.append(mapping[1].rstrip())
# create a list of random numbers that will be used to chose the uri
    i = 0
    while i < 100:
      ran.append(random.randint(0, len(uri)))
      i += 1
  finally:
    mFile.close()
  
  for r in ran:
    getLinks(uri[r],out[r])
