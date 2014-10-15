#credit to:
#https://gist.github.com/leostera/3535568
#https://pypi.python.org/pypi/selenium
#cookies problem: http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2
#http://stackoverflow.com/questions/14583560/selenium-retrieve-data-that-loads-while-scrolling-down

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import os, sys
from bs4 import BeautifulSoup
import codecs
from random import randint
import getpass
import os


globalHtmlOutputFile = 'allFacebookFriends.html'
globalCSVOutputFile = 'facebookFriendFriendsCountTuples.txt'

#output file: globalHtmlOutputFile
def getHtmlOfAllFriends(userFaceBookEmail, userFaceBookPassword):

	if( len(userFaceBookEmail) > 0 and len(userFaceBookPassword) > 0 ):
		pass
	else:
		print "userFaceBookEmail and/or userFaceBookPassword: bad length"
		return

	try:
		htmlOutputFile = open(globalHtmlOutputFile, 'w')
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print fname, exc_tb.tb_lineno, sys.exc_info()
		return

	myFirefoxBrowser = webdriver.Firefox()
	myFirefoxBrowser.implicitly_wait(3)
	# or you can use Chrome(executable_path="/usr/bin/chromedriver")
	myFirefoxBrowser.get("http://www.facebook.org")
	assert "Facebook" in myFirefoxBrowser.title


	elem = myFirefoxBrowser.find_element_by_id("email")
	elem.send_keys(userFaceBookEmail)
	elem = myFirefoxBrowser.find_element_by_id("pass")
	elem.send_keys(userFaceBookPassword)
	elem.send_keys(Keys.RETURN)


	#http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2
	all_cookies = myFirefoxBrowser.get_cookies()
	#cookies = {}
	#for s_cookie in all_cookies:
	#    cookies[s_cookie["name"]]=s_cookie["value"]


	#open friends page
	friendsLink = 'https://www.facebook.com/friends/'
	myFirefoxBrowser.get(friendsLink)
	myFirefoxBrowser.maximize_window()


	#scroll to bottom of page
	previousCountOfFriends = -1
	while True:

		myFirefoxBrowser.execute_script("return window.scrollTo(0, document.body.scrollHeight);")
		html = myFirefoxBrowser.page_source.encode('utf-8') 

		soup = BeautifulSoup(html)
		parentOfUIProfileBlockContent = soup.findAll('div', { 'class' : 'uiProfileBlockContent' })

		#lastIndexOfFriends = html.rfind('<div class="uiProfileBlockContent">')
		lastIndexOfFriends = len(parentOfUIProfileBlockContent)

		#'Friends' not found
		if( lastIndexOfFriends == -1 ):
			break

		#No new entry
		if( previousCountOfFriends == lastIndexOfFriends ):
			htmlOutputFile.write(html)
			break
		else:
			previousCountOfFriends = lastIndexOfFriends

		sleepTime = randint(3,7)
		print "...sleeping for", sleepTime, "seconds"
		time.sleep(sleepTime)


	myFirefoxBrowser.close()
	return previousCountOfFriends

def getCredentials():

	userName = ''
	password = ''

	try:
		credentialsFile = open('credentials.txt')
		credInfo = credentialsFile.readlines()

		if( len(credInfo) > 1 ):
			userName = credInfo[0]
			password = credInfo[1]
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print fname, exc_tb.tb_lineno, sys.exc_info()
		return


	return userName, password

def getFBHtmlDump(inputFileName):

	htmlText = ''

	if( len(inputFileName) > 0 ):
		try:
			inputFile = open(inputFileName, 'r')
			htmlText = inputFile.read()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print fname, exc_tb.tb_lineno, sys.exc_info()


	return htmlText

#writes tuples <friend, friendCount> into globalCSVOutputFile
def getFriendOfFriendsFromHtml(htmlText):

	goAheadFlag = False

	if( len(htmlText) > 0 ):

		try:
			outputFile = codecs.open(globalCSVOutputFile, 'w', 'utf-8')
			outputFile.write('"USER", "FRIENDCOUNT"\n')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print fname, exc_tb.tb_lineno, sys.exc_info()
			return


		soup = BeautifulSoup(htmlText)
		parentOfUIProfileBlockContent = soup.findAll('div', { 'class' : 'uiProfileBlockContent' })

		for profile in parentOfUIProfileBlockContent:

				friendName = profile.find('div', { 'class' : 'fsl fwb fcb' })
				potentialFriendsCount = profile.find('a', { 'class' : 'uiLinkSubtle' })

				#potentialFriendsCount: x (f)riends | x mutual friends, etc, so split
				if( potentialFriendsCount is not None ):

					potentialFriendsCount = potentialFriendsCount.text.split(' ')

					if( len(potentialFriendsCount) > 1 ):
						if( len(potentialFriendsCount[1]) > 0):
							if( potentialFriendsCount[1][0].lower() == 'f' ):

								friendCount = potentialFriendsCount[0].replace(',','')

								stringToWrite = friendName.text + ', ' + friendCount + '\n'
								outputFile.write(stringToWrite)
								goAheadFlag = True
							

		outputFile.close()


	return goAheadFlag

if __name__ == "__main__":

	
	print ''

	print 'Welcome to get fb friends of friends. If all goes well,'
	print 'The application will write your fb friends of friends into ./' + globalCSVOutputFile

	print ''
	userNameFacebook = raw_input("Email ID: ")
	passwordFacebook = getpass.getpass('Password: ')

	userNameFacebook = str(userNameFacebook)
	passwordFacebook = str(passwordFacebook)

	userNameFacebook = userNameFacebook.strip()
	passwordFacebook = passwordFacebook.strip()

	intGoAheadFlag = getHtmlOfAllFriends(userNameFacebook, passwordFacebook)

	if ( intGoAheadFlag > -1 ):
		facebookDumpInputFileName = globalHtmlOutputFile
		htmlText = getFBHtmlDump(facebookDumpInputFileName)
		boolGoAhead = getFriendOfFriendsFromHtml(htmlText)

		#open file
		if( boolGoAhead ):
			myFirefoxBrowser = webdriver.Firefox()
			filePath = 'file:///' + os.getcwd() + '/' + globalCSVOutputFile
			myFirefoxBrowser.get(filePath)
			


