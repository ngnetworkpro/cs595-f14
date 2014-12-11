
import urllib
import feedparser
from bs4 import BeautifulSoup
import requests
import docclass
import feedfilter
import re

entries = []
blog = 'http://theinvisiblethings.blogspot.com/'
path = '/feeds/posts/default'
query_arg = {'alt' : 'atom'}
udata = urllib.urlencode(query_arg)

full_url = blog+path+"?"+udata
r = requests.get(full_url) 
f=feedparser.parse(full_url)
entries = f['entries']
bsdata = r.text
soup = BeautifulSoup(bsdata)
next = soup.find('link', rel='next')
for x in range(1,4):
  n= next.get('href')
  f=feedparser.parse(n)
  entries.extend(f['entries'])
  r = requests.get(n) 
  bsdata = r.text
  soup = BeautifulSoup(bsdata)
  next = soup.find('link', rel='next')

_illegal_xml_chars_RE = re.compile(u'[\x00-\x08\x0b\xa9\xae\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')

def remove_tags(text):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', text)
    cleantext = re.sub("\n", ' ', cleantext)
    cleantext = cleantext.strip()	
    cleantext = cleantext.replace(u'\u201c', '')
    cleantext = cleantext.replace(u'\u201d', '')
    cleantext = cleantext.replace(u'\u2019', '\'')
    cleantext = cleantext.replace('-&gt;', '')
    return _illegal_xml_chars_RE.sub(' ', cleantext)

for x in range(0,100):
  entries[x]['content'][0]['value'] = remove_tags(entries[x]['content'][0]['value'])
  entries[x]['title'] = remove_tags(entries[x]['title'])

cl=docclass.fisherclassifier(docclass.getwords)
cl.setdb('feed.db')

feedfilter.read(entries, cl)

#write results to file, for table creation
tab = open('table.txt', 'w', 0)
tab.write('Title\tClassifier\tPredicted\tActual\tcprob()\n')
for x in range(0, 50):
  tab.write(entries[x]['title'] + '\t' + entries[x]['classifier'] + '\t' + ' '+ '\t' + entries[x]['actual']+'\n')

for x in range(50, 100):
  tab.write(entries[x]['title'] + '\t' + ' ' + '\t' + entries[x]['pred']+'\t' + entries[x]['actual']+'\t'+str(entries[x]['cprob'])+'\n')

tab.close()

# compute Precision, recall, f1
# tp is labelled correctly, fn is not labelled but should have been, fp is incorrectly labelled
tp = 0
fn = 0
fp = 0
for x in range(50, 100):
  if entries[x]['pred'] == entries[x]['actual']:
    tp += 1
  elif not entries[x]['pred'] and entries[x]['actual']:
    fn += 1
  else:  #labelled incorrectly
    fp += 1

precision = float(tp) / (tp + fp)
recall = float(tp) / (tp + fn)

f1 = 2 * ((precision * recall) / (precision + recall))

# print the entries to file
out = open('entries.txt', 'w', 0)
for e in entries:
  print>>out, e

out.write('\n----------------------\n')
out.write("Precision: " + str(precision)+'\n')
out.write("Recall: " + str(recall)+'\n')
out.write("F1: " + str(f1)+'\n')
out.close()

print "Precision: " + str(precision)
print "Recall: " + str(recall)
print "F1: " + str(f1)
