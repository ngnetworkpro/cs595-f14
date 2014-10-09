
import os
import urlparse

def allLabels(i, O):
  for x in range(3, len(i)):  #node label for links
    #parsed = urlparse.urlsplit(i[x].rstrip())
    #loc = parsed.netloc
    O.write('\t"')
    O.write(i[x].rstrip())
    O.write('" [label= ""];\n')

def listAll(i, O):
  for x in range(3, len(i)):  #adjacency list
    O.write('"')
    O.write(i[x].rstrip())
    O.write('";')

if __name__ == '__main__':
  links = list()
  files = list()
  site = str()
  for file in os.listdir("/root/webscience/class/A4/links"):
    files.append(file)
  O = open('a4.dot', 'w', 0)
  O.write('digraph a4 {\n')
  for l in files:
    l = 'links/'+l
    with open(l) as lFile:
      i = list()
      for line in lFile:
        i.append(line)
      site = i[1].rstrip()
      parsed = urlparse.urlsplit(site)
      loc = parsed.netloc
      O.write('\t"')
      O.write(site)
      O.write('" [label="')  #node label for site
      O.write(loc)
      O.write('"];\n')
      allLabels(i,O)          #label all connected
      O.write('\t"')
      O.write(site)
      O.write('" -> {')
      listAll(i,O)            #Create adjacency list
      O.write('}\n')
  O.write('}\n')
  O.close()
