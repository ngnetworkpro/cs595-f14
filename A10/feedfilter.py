import feedparser
import re

# Takes a filename of URL of a blog feed and classifies the entries
def read(entries,classifier):
# classify the first 50 and train the classifer
  for x in range(0, 50):
    print
    print '-----'
    # Print the contents of the entry
    print 'Title:     '+entries[x]['title'].encode('utf-8')
    print
    print entries[x]['content'][0]['value'].encode('utf-8')
    
    # Combine all the text to create one item for the classifier
    fulltext= entries[x]['title'] + ', ' + entries[x]['content'][0]['value']

    # Ask the user to specify the correct category and train on that
	tr=raw_input('Enter classifier: ')
    entries[x]['classifier'] = tr
    cl=raw_input('Enter category: ')
	entries[x]['actual'] = cl
    classifier.train(fulltext,cl)

# classify the final 50 and get the guess and cprob
	for x in range(50, 100):
    print
    print '-----'
    # Print the contents of the entry
    print 'Title:     '+entries[x]['title'].encode('utf-8')
    print
    print entries[x]['content'][0]['value'].encode('utf-8')
    
    # Combine all the text to create one item for the classifier
    fulltext= entries[x]['title'] + ', ' + entries[x]['content'][0]['value']

    # Ask the user to specify the correct category
    cl=raw_input('Enter category: ')
    entries[x]['actual'] = cl
    # Print the best guess at the current category
    guess = classifier.classify(fulltext)
    entries[x]['pred'] = str(guess[0])
    entries[x]['cprob'] = round(guess[1], 3)
    print 'Guess: '+ str(guess[0])
