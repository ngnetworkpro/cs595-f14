from linkedin import linkedin # pip install python-linkedin
import json
import codecs
import calculate

# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application

def writeToFile(ulist):
  with codecs.open('linkedin.txt', 'w', encoding='utf-8') as O:
    O.write('No.\tName\tCount\n')
    for i in range(len(ulist)):
      O.write(str(i+1)+'\t'+ulist[i]['name']+'\t'+str(ulist[i]['count'])+'\n')
#compute and save mean, median, and standard deviation
  with open('calculations.txt', 'a') as O:
    clist = []
    O.write('Linkedin\n')
    for u in ulist:
      clist.append(u['count'])
    mean = calculate.getMean(clist)  
    O.write('Mean: ' + str(mean) + '\n')
    median = calculate.getMedian(clist)
    O.write('Median: ' + str(median) + '\n')
    stdev = calculate.standardDev(clist)
    O.write('Standard Deviation: ' + str(stdev) + '\n')
  
CONSUMER_KEY = '776k21mop4bbh5'
CONSUMER_SECRET = 'QK7bWW9O7eAk4Wte'
OAUTH_TOKEN = '2780f3f9-132e-4228-8077-9500b0d9933d'
OAUTH_TOKEN_SECRET = '858813cb-f727-46bd-b730-aeddbcf97129'

RETURN_URL = 'http://localhost:8000' # Not required for developer authentication

# Instantiate the developer authentication class
auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                OAUTH_TOKEN, OAUTH_TOKEN_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())

# Pass it in to the app...
app = linkedin.LinkedInApplication(auth)
# Use the app...
#app.get_profile()

my_conn = app.get_profile(selectors=['num-connections'])
num = my_conn['numConnections']

connections = app.get_connections()
people = connections['values']

ulist = []
for i in range(len(people)):
  conn_id = connections['values'][i]['id']
  if conn_id == 'private':
    continue  #user has profile set to private
  conn_num = app.get_profile(member_id=conn_id, selectors=['num-connections'])
  n = conn_num['numConnections']
  conn_name = connections['values'][i]['lastName']
  ulist.append({'name':conn_name, 'count':n})
  
ulist.append({'name':'me', 'count':num})
sorted_u = sorted(ulist, key=lambda k : k['count'])
writeToFile(sorted_u)
