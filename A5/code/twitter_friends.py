from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
import urllib
import json
import codecs

def get_oauth():
  oauth = OAuth1(CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=OAUTH_TOKEN,
        resource_owner_secret=OAUTH_TOKEN_SECRET)
  return oauth
  
def getUser(user, page):
  params = urllib.urlencode({'cursor' : page,'screename': user, 'count': 200, 'skip_status':'true', 'include_user_entities':'false'}) #https://docs.python.org/2/library/urllib.html
  urli = "https://api.twitter.com/1.1/friends/list.json?"
  full_url = urli+params
  r = requests.get(url=full_url, auth=oauth) 
  data = json.loads(r.text)
  slist = list(data[u'users'])
  parse_List(slist, user)

def parse_List(slist, user):
  ulist = []
  for i in range(len(slist)):
    ulist.append({'name':slist[i][u'name'], 'count': slist[i][u'friends_count']})
  # add the searched user
  ulist.append({'name': user, 'count': len(ulist)})
	#sort list by user count
  sorted_u = sorted(ulist, key=lambda k : k['count'])
  writeToFile(sorted_u)

def writeToFile(ulist):
  with codecs.open('counts.txt', 'w', encoding='utf-8') as O:
    O.write('No.\tName\tCount\n')
    for i in range(len(ulist)):
      O.write(str(i+1)+'\t'+ulist[i][u'name']+'\t'+str(ulist[i][u'count'])+'\r')
#compute and save mean, median, and standard deviation
  with open('calculations.txt', 'a') as O:
    clist = []
    O.write('Twitter\n')
    for u in ulist:
      clist.append(u['count'])
    mean = calculate.getMean(clist)  
    O.write('Mean: ' + str(mean) + '\n')
    median = calculate.getMedian(clist)
    O.write('Median: ' + str(median) + '\n')
    stdev = calculate.standardDev(clist)
    O.write('Standard Deviation: ' + str(stdev) + '\n')
	
CONSUMER_KEY = "NlcSlE8LpTNQ6HOvyunMVx4EN"
CONSUMER_SECRET = "fB5hyOpBG9cklmPHvGVPyOJALX7UEG3SPWjjn0aRXq3TgzRGkx"

OAUTH_TOKEN = "2815818894-fhOZj1FomjECCvDc62EPpxyKJT0ktOuk5cl7BOR"
OAUTH_TOKEN_SECRET = "GIMhewOb2ZMjG0MgEddRlHzuFPQFbfAWn8mecw1yNrboK"

oauth = get_oauth()
getUser('LilyMotoko', -1)