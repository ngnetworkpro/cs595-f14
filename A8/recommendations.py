#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import sqrt
import operator
import string

def sim_distance(prefs, p1, p2):
    '''
    Returns a distance-based similarity score for person1 and person2.
    '''
    # Get the list of shared_items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they have no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[p1][item] - prefs[p2][item], 2) for item in
                         prefs[p1] if item in prefs[p2]])
    return 1 / (1 + sum_of_squares)

def sim_pearson(prefs, p1, p2):
    '''
    Returns the Pearson correlation coefficient for p1 and p2.
    '''
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they are no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Sum calculations
    n = len(si)
    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r

def getRecommendations(prefs, person, similarity=sim_pearson):
    '''
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    '''
    totals = {}
    simSums = {}
    for other in prefs:
    # Don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
    # Ignore scores of zero or lower
        if sim <= 0:
            continue
    for item in prefs[other]:
        # Only score movies I haven't seen yet
        if item not in prefs[person] or prefs[person][item] == 0:
            # Similarity * Score
            totals.setdefault(item, 0)
            # The final score is calculated by multiplying each item by the
            #   similarity and adding these products together
            totals[item] += prefs[other][item] * sim
            # Sum of similarities
            simSums.setdefault(item, 0)
            simSums[item] += sim
    # Create the normalized list
    rankings = [(total / simSums[item], item) for (item, total) in
                totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    '''
    Transform the recommendations into a mapping where persons are described
    with interest scores for a given title e.g. {title: person} instead of
    {person: title}.
    '''
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for (item, score) in
                scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings
#-------------------------------------------------------------
def getMovieTitles(path='data'):
  # Get movie titles
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
    return movies
	
def loadMovieRatings(path='data'):  #load movies with title and ratings list
    # Get movie titles
    movies = getMovieTitles()
    # Get all ratings for each movie
    rate = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        rate.setdefault(movieid, {})
        rate[movieid]['title'] = movies[movieid]
        if rate[movieid].has_key('ratings'):
            rate[movieid]['ratings'].append(float(rating))
        else:
            rate[movieid]['ratings'] = []
            rate[movieid]['ratings'].append(float(rating))
    return rate

def ratingAverage(ratings):  #get average of a list of movie ratings
    sum = 0.0
    for i in range(0, len(ratings['ratings'])):
        sum = sum + ratings['ratings'][i]
    avg = sum / len(ratings['ratings'])
    return avg

def getTop(sort, type, n=5):
    max = sort[0][1][type]
    top = []
    top.append(sort[0])
    for s in range(1, len(sort)):
        if sort[s][1][type] == max:
            top.append(sort[s])
        else:
            break
    while len(top) < n:
        max = sort[len(top)][1][type]
        for s in range(len(top), len(sort)):
            if sort[s][1][type] == max:
                top.append(sort[s])
            else:
                break
    return top

def printRatings(items, type, n):  #print list of ratings
    sort = sorted(items, key=lambda x: x[1][type], reverse=True)
    col_width = 0
    top = getTop(sort, type, n)
    # Get longest title for printed column width
    for x in range(0, len(top)):
        if len(top[x][1]['title']) > col_width:
            col_width = len(top[x][1]['title']) + 2
    # print the result
    print string.ljust('Title', col_width), string.rjust('Average Rating', 3)
    print string.ljust('\n------', col_width), string.rjust('----------------', 3)
    for x in range(0, len(top)):
        print string.ljust(top[x][1]['title'], col_width), string.rjust(str(top[x][1][type]), 3)

def getRatings(n=5):  #get top average, most rated
    rate = loadMovieRatings()
    # Get the average ratings per movie
    for r in rate:
        rate[r]['average'] = ratingAverage(rate[r])
    print 'Top ' + str(n) + ' movies by Average Rating:'
    printRatings(rate.items(), 'average', n)
    # Get the most rated movies
    rsort = sorted(rate.items(), key=lambda x: len(x[1]['ratings']), reverse=True)
    print '\nTop ' + str(n) + ' movies by most ratings:'
    col_width = 0
    for x in range(0, n):
        if len(rsort[x][1]['title']) > col_width:
            col_width = len(rsort[x][1]['title']) + 2
    print string.ljust('Title', col_width), string.rjust('Number of Ratings', 3)
    print string.ljust('------', col_width), string.rjust('----------------', 3)
    for x in range(0, n):
        print string.ljust(rsort[x][1]['title'], col_width), string.rjust(str(len(rsort[x][1]['ratings'])), 3)
#-----------------------------------------------------------
def loadUserInfo(path='data'):  #load users with info and movie ratings
  # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movieid] = float(rating)
    for line in open(path + '/u.user'):
        (user, age, gender, job, zip) = line.split('|')
        prefs[user]['info'] = {}
        prefs[user]['info']['age'] = int(age)
        prefs[user]['info']['gender'] = gender
    return prefs

def getRatingsByGender(n=5):  #get top average, most rated, ratings by gender
    rate = loadMovieRatings()
        # Get ratings per gender
    users = loadUserInfo()
    women = {}
    men = {}
    for r in rate:
        women[r] = {}
        men[r] = {}
    for u in users:
        if users[u]['info']['gender'] == 'F':
            for r in rate:
                if users[u].has_key(r):
                    if women[r].has_key('ratings'):
                        women[r]['ratings'].append(users[u][r])
                    else:
                        women[r]['ratings'] = []
                        women[r]['ratings'].append(users[u][r])
        else:
            for r in rate:
                if users[u].has_key(r):
                    if men[r].has_key('ratings'):
                        men[r]['ratings'].append(users[u][r])
                    else:
                        men[r]['ratings'] = []
                        men[r]['ratings'].append(users[u][r])
    # Get the average ratings per movie per gender
    for w in women:
        if women[w].has_key('ratings'):
            rate[w]['women'] = ratingAverage(women[w])
    for m in men:
        if men[m].has_key('ratings'):
            rate[m]['men'] = ratingAverage(men[m])
    for r in rate:
        if rate[r].has_key('women'):
            continue
        else:
            rate[r]['women'] = 0
    for r in rate:
        if rate[r].has_key('men'):
            continue
        else:
            rate[r]['men'] = 0
    # Print results per gender
    print '\nTop ' + str(n) + ' movies Rated by Women:'
    printRatings(rate.items(), 'women', n)
    print '\nTop ' + str(n) + ' movies Rated by Men:'
    printRatings(rate.items(), 'men', n)
#-----------------------------------------------------------
def topMatches(prefs, original, n=5, similarity=sim_pearson):
    '''
    Returns the best matches for an item from the prefs dictionary. 
    Number of results and similarity function are optional params.
    '''
    scores = [(similarity(prefs, original, other), other) for other in prefs
              if other != original]
    scores.sort()
    scores.reverse()
    return scores[0:n]
	
def botMatches(prefs, original, n=5, similarity=sim_pearson):
    '''
    Returns the worst matches for an item from the prefs dictionary. 
    Number of results and similarity function are optional params.
    '''
    scores = [(similarity(prefs, original, other), other) for other in prefs
              if other != original]
    scores.sort()
    return scores[0:n]

def calculateSimilarItems(prefs, n=10):
    '''
    Create a dictionary of items showing which other items they are
    most similar to. 
    '''
    result = {}
    c = 0
    for item in prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print '%d / %d' % (c, len(prefs))
        # Find the most similar items to this one
        scores = topMatches(prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result
	
def calculateDissimilarItems(prefs, n=10):
    '''
    Create a dictionary of items showing which other items they are
    most similar to. 
    '''
    result = {}
    c = 0
    for item in prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print '%d / %d' % (c, len(prefs))
        # Find the most similar items to this one
        scores = botMatches(prefs, item, n, similarity=sim_distance)
        result[item] = scores
    return result
	
def loadMovie(path='data'): #movies, with per user ratings
  # Get movie titles
    movies = getMovieTitles()
  # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(movieid, {})
        prefs[movieid][user] = float(rating)
    return prefs

def getTopGunCorrelation(path='data'): #get movies most alike and unlike Top Gun
    #load list of movies, with per user ratings
    mList = loadMovie()
    topGun = 0
     # Get movie titles
    movies = getMovieTitles()
    for m in movies:
        if 'Top Gun' in movies[m]:
            topGun = m
    sim = calculateSimilarItems(mList, 1)
    neg = calculateDissimilarItems(mList, 1)
    print '\nMovie most like Top Gun: '
    print movies[sim[m][0][1]]
    print '\nMovie least like Top Gun: '
    print movies[neg[m][0][1]]
#------------------------------------------------------------  
def loadUserRatings(path='data'): # users with per movie ratings
  # Get movie titles
    movies = getMovieTitles()
  # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movieid] = float(rating)
    return prefs

def getTopRaters(n=5):  #get users that rated the most movies
    users = loadUserRatings()
    rsort = sorted(users.items(), key=lambda x: len(x[1]), reverse=True)
    print '\nTop 5 users by most ratings:'
    print string.ljust('User', 12), string.rjust('Number of Ratings', 3)
    print string.ljust('------', 12), string.rjust('----------------', 3)
    for x in range(0, n):
        print string.ljust(rsort[x][0], 12), string.rjust(str(len(rsort[x][1])), 3)
#--------------------------------------------------------------------------------
def getUserCorrelation(n=5):  #get users that are most correlated with each other
    '''
    Finds the 5 users that agree the most by finding the users that are closest
    '''
    users = loadUserRatings()
    alike = calculateSimilarItems(users, 1)
    min = float('inf')
    minid = 0
    chain = {}
    r = {}
    for a in alike:
        sum = 0
        c = alike[a]
        chain[a] = {}
        links = []
        links.append(a)
        r[a] = [a, alike[a][0][1], sim_pearson(users, str(a), alike[a][0][1]), sim_distance(users, str(a), alike[a][0][1])]
        sum = sum + sim_distance(users, str(a), alike[a][0][1])
        for i in range(0, n):
            add = links[i]
            links.append(alike[add][0][1])
            next = alike[alike[add][0][1]][0][1]
            sum = sum + sim_distance(users, alike[add][0][1], alike[alike[add][0][1]][0][1])
            chain[a]['links'] = list(set(links))
        chain[a]['distance'] = sum
    for c in chain:
        if len(chain[c]['links']) >= 5:
            if chain[c]['distance'] < min:
                min = chain[c]['distance']
                minid = c
    chain[minid]['r'] = {}
    for i in range(0, len(chain[minid]['links'])):
        chain[minid]['r'][i] = r[chain[minid]['links'][i]] 
    csort = sorted(chain[minid]['r'].items(), key=lambda x: x[1][2], reverse=True)
    print '5 closest raters with r values and distance: '
    for c in csort:
        print 'User ' + c[1][0] + ' to ' + c[1][1] + ', r = ' + str(c[1][2]) + ', distance= ' + str(c[1][3])
    #Finds the 5 users that disagree the most by finding the users that are farthest away
    unlike = calculateDissimilarItems(users, 1)
    max = float('-inf')
    maxid = 0
    uchain = {}
    ur = {}
    for u in unlike:
        sum = 0
        c = unlike[u]
        uchain[u] = {}
        links = []
        links.append(u)
        ur[u] = [a, unlike[u][0][1], sim_pearson(users, str(u), unlike[u][0][1]), sim_distance(users, str(u), unlike[u][0][1])]
        sum = sum + sim_distance(users, str(u), unlike[u][0][1])
        for i in range(0, n):
            add = links[i]
            links.append(unlike[add][0][1])
            next = unlike[unlike[add][0][1]][0][1]
            sum = sum + sim_distance(users, unlike[add][0][1], unlike[unlike[add][0][1]][0][1])
            uchain[u]['links'] = list(set(links))
        uchain[u]['distance'] = sum
    for c in uchain:
        if len(uchain[c]['links']) == 5:
            if uchain[c]['distance'] > max:
                max = uchain[c]['distance']
                maxid = c
    uchain[maxid]['ur'] = {}
    for i in range(0, len(uchain[maxid]['links'])):
        uchain[maxid]['ur'][i] = ur[uchain[maxid]['links'][i]] 
    csort = sorted(uchain[maxid]['ur'].items(), key=lambda x: x[1][2], reverse=True)
    print '5 farthest raters, with r values and distance: '
    for c in csort:
        print 'User ' + c[1][0] + ' to ' + c[1][1] + ', r = ' + str(c[1][2]) + ', distance= ' + str(c[1][3])

#------------------------------------------------------------ 	
def getRatingsByAge(n=5):  #get top average, most rated, ratings by gender
    rate = loadMovieRatings()		
    users = loadUserInfo()
    women = {}
    w40 = {}
    men = {}
    m40 = {}
    for r in rate:
        women[r] = {}
        men[r] = {}
        w40[r] = {}
        m40[r] = {}
    for u in users:
        if users[u]['info']['gender'] == 'F':
            if int(users[u]['info']['age']) < 40:
                for r in rate:
                    if users[u].has_key(r):
                        if women[r].has_key('ratings'):
                            women[r]['ratings'].append(users[u][r])
                        else:
                            women[r]['ratings'] = []
                            women[r]['ratings'].append(users[u][r])
            else:
                for r in rate:
                    if users[u].has_key(r):
                        if w40[r].has_key('ratings'):
                            w40[r]['ratings'].append(users[u][r])
                        else:
                            w40[r]['ratings'] = []
                            w40[r]['ratings'].append(users[u][r])
        else:
            if int(users[u]['info']['age']) < 40:
                for r in rate:
                    if users[u].has_key(r):
                        if men[r].has_key('ratings'):
                            men[r]['ratings'].append(users[u][r])
                        else:
                            men[r]['ratings'] = []
                            men[r]['ratings'].append(users[u][r])
            else:
                for r in rate:
                    if users[u].has_key(r):
                        if m40[r].has_key('ratings'):
                            m40[r]['ratings'].append(users[u][r])
                        else:
                            m40[r]['ratings'] = []
                            m40[r]['ratings'].append(users[u][r])
    # Get the average ratings per movie per gender
    for w in women:
        if women[w].has_key('ratings'):
            rate[w]['women'] = ratingAverage(women[w])
        else:
            rate[w]['women'] = float('-inf')
    for m in men:
        if men[m].has_key('ratings'):
            rate[m]['men'] = ratingAverage(men[m])
        else:
            rate[m]['men'] = float('-inf')
    for w in w40:
        if w40[w].has_key('ratings'):
            rate[w]['w40'] = ratingAverage(w40[w])
        else:
            rate[w]['w40'] = float('-inf')
    for m in m40:
        if m40[m].has_key('ratings'):
            rate[m]['m40'] = ratingAverage(m40[m])
        else:
            rate[m]['m40'] = float('-inf')
    # Print results per gender
    print '\nTop ' + str(n) + ' movies Rated by Men under 40:'
    printRatings(rate.items(), 'men', n)  
    print '\nTop ' + str(n) + ' movies Rated by Men over 40:'
    printRatings(rate.items(), 'm40', n)  	
    print '\nTop ' + str(n) + ' movies Rated by Women under 40:'
    printRatings(rate.items(), 'women', n)
    print '\nTop ' + str(n) + ' movies Rated by Women over 40:'
    printRatings(rate.items(), 'w40', n)  