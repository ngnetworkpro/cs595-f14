import requests
import pycurl
import re
from urlparse import urlparse
import urllib
import feedparser
from bs4 import BeautifulSoup
import clusters
import time
from math import log
import HTMLParser
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def check(url): 
  with open("blogs.txt") as f:
    found = False
    for line in f:  #iterate over the file one line at a time(memory efficient)
      if re.search(url, line):    #if string found is in current line then keep it
        found = True
  return found

blogger = 'https://www.blogger.com/next-blog?navBar=true&blogID=953024975153422094'
bfile = open('blogs.txt', 'w',0)
bfile.write('f-measure.blogspot.com\n')
bfile.write('ws-dl.blogspot.com\n')
bfile.close()
for i in range(1, 200):
  buffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL, blogger)
  c.setopt(c.WRITEDATA, buffer)
  c.setopt(c.FOLLOWLOCATION, True)
  c.setopt(c.HTTPHEADER, ['Accept-Language: en'])
  bfile = open('blogs.txt', 'a',0)
  try: 
    c.perform()
    if c.getinfo(c.RESPONSE_CODE) == 200:
      o = urlparse(c.getinfo(c.EFFECTIVE_URL))
      ch = check(o.netloc)
      if not ch:
        bfile.write(o.netloc + '\n')
        bfile.close()
      else:
  	    continue
    c.close()
  except pycurl.error, error:
    errno, errstr = error
    print 'An error occurred: ', errstr


	
def getwordcounts(url):
    #Returns title and dictionary of word counts for an RSS feed
    # Parse the feed
    d = feedparser.parse(url)
    wc = {}
    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return (d.feed.title, wc)

def getwords(html):
    # Remove all the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Convert to lowercase
    return [word.lower() for word in words if word != '']
	
def getFeed(feedurl):
    global wordcounts
    global apcount
    try:
        (title, wc) = getwordcounts(feedurl)
        if title in wordcounts:
            for (w, c) in wc.iteritems():
                if w in wordcounts[title].iteritems():
                    wordcounts[title][w] += c
                else:
                    wordcounts[title][w] = c
        else:
            wordcounts[title] = wc
        for (word, count) in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    except:
        print 'Failed to parse feed %s' % feedurl

pages = {}
feedlist = []
apcount = {}
wordcounts = {}
wordlist = []
scheme = 'http://'
path = '/feeds/posts/default'
query_arg = {'alt' : 'atom'}
udata = urllib.urlencode(query_arg)
f = open('blogs.txt', 'r', 0)
for line in f:
  line = line.strip()
  data = urllib.urlencode(query_arg)
  full_url = scheme+line+path+"?"+udata
  feedlist.append(full_url)
  r = requests.get(full_url) 
  getFeed(full_url)
  ddata = r.text
  soup = BeautifulSoup(ddata)
  next = soup.find('link', rel='next')
  count = 1
  while next:
    n= next.get('href')
    getFeed(n)
    r = requests.get(n) 
    data = r.text
    soup = BeautifulSoup(data)
    count = count + 1
    if count % 10 == 0:
      print ' -- parsing ' + line + ' ' + str(count) + ' pages so far'
    next = soup.find('link', rel='next')
  print 'Finished parsing ' + line + ' ' + str(count) + ' pages'
  if str(count) in pages:
    pages[str(count)].append(line)
  else:
    pages[str(count)] = []
    pages[str(count)].append(line)
f.close()

p = open('blog_pages.txt', 'w', 0)
p.write('Pages\tNumber of Blogs\n')
for (pg, num) in pages.iteritems():
  p.write(pg + '\t' + str(len(num)) + '\n')

a = sorted(apcount.items(), key=lambda x: x[1], reverse=True)
count = 0
for (w, bc) in a:
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)
        count = count + 1
        if count >= 500:
            break

_illegal_xml_chars_RE = re.compile(u'[\x00-\x08\x0b\xa9\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')

def remove_tags(text):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', text)
    cleantext = re.sub("\n", ' ', cleantext)
    cleantext = cleantext.strip()	
    return _illegal_xml_chars_RE.sub(' ', cleantext)

def getTitles():
  titles = {}
  global scheme, path, udata
  f = open('blogs.txt', 'r', 0)
  for line in f:
    line = line.strip()
    full_url = scheme+line+path+"?"+udata
    d = feedparser.parse(full_url)
    titles[d.feed.title] = remove_tags(d.feed.subtitle)
  return titles
 
titles = {}
titles = getTitles()
# Blog Term Matrix
out = file('blogdata.txt', 'w', 0)
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')

for (blog, wc) in wordcounts.items():
    if titles[blog] != '':
        blog = blog + ' - ' + titles[blog]
    blog = blog.replace(u'\u0144', 'n')
    blog = _illegal_xml_chars_RE.sub(' ', blog)
    blog = blog.strip()
    if len(blog) > 100:
        blog = blog[:99]
    print blog
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
out.close()
# Ascii 
old = sys.stdout
sys.stdout = open('blog_ascii.txt', 'w', 0)
blognames,words,data=clusters.readfile('blogdata.txt')
clust = clusters.hcluster(data)
clusters.printclust(clust,labels=blognames)
sys.stdout = old
# jpeg dendogram
clusters.drawdendrogram(clust,blognames,jpeg='blogclust.jpg')
# K-clustering
def printClusters(kclust, out):
  for i in range(0,len(kclust)):
    klist = [blognames[r] for r in kclust[i]]
    for x in range(0, len(klist)):
      out.write(klist[x] + '\n')
    out.write('\n')

k = open('blog_k.txt', 'w', 0)
k.write('K = 5\n')
kclust=clusters.kcluster(data,k=5)
printClusters(kclust, k)
k.write('K = 10\n')
kclust=clusters.kcluster(data,k=10)
printClusters(kclust, k)
k.write('K = 20\n')
kclust=clusters.kcluster(data,k=20)
printClusters(kclust, k)
k.close()
# MDS
coords = clusters.scaledown(data)
clusters.draw2d(coords,blognames,jpeg='blogs2d.jpg')
#
#Extra credit - TFIDF
#
google = 'http://www.google.com/search'
corp = 42000000000
idf = {}
for word in wordlist:
  print 'Searching for ' + word
  query_arg = {'q' : word}
  sdata = urllib.urlencode(query_arg)
  full_url = google+'?'+sdata
  r = requests.get(full_url) 
  ddata = r.text
  soup = BeautifulSoup(ddata)
  results = soup.find('div', id='resultStats')
  res = (results.text).rsplit()
  term = float(res[1].replace(',',''))
  idf[word] = log((corp/term),2)
  sl = random.randint(1, 100)
  time.sleep(sl)

ti = file('blog_tfidf.txt', 'w', 0)
ti.write('Blog')
for word in wordlist:
  ti.write('\t%s' % word)

ti.write('\n')

for (blog, wc) in wordcounts.items():
  if titles[blog] != '':
    blog = blog + ' - ' + titles[blog]
  blog = blog.replace(u'\u0144', 'n')
  blog = _illegal_xml_chars_RE.sub(' ', blog)
  blog = blog.strip()
  if len(blog) > 100:
    blog = blog[:99]
  ti.write(blog)
  if len(blog) > 100:
    blog = blog[0:99]
  for word in wordlist:
    if word in wc:
      tf = float(wc[word]) / len(wc)
      tfidf = round(tf * idf[word], 3)
      ti.write('\t' + str(tfidf))
    else:
      ti.write('\t0')
  ti.write('\n')

old = sys.stdout
sys.stdout = open('blog_tfidf_ascii.txt', 'w', 0)
blognames,words,data=clusters.readfile('blog_tfidf.txt')
clust = clusters.hcluster(data)
clusters.printclust(clust,labels=blognames)
sys.stdout = old
clusters.drawdendrogram(clust,blognames,jpeg='tfidfclust.jpg')    