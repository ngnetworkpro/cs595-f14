def getRatings(n=5):  #get top average, most rated, ratings by gender
    rate = loadMovieRatings()
    # Get the average ratings per movie
    for r in rate:
        rate[r]['average'] = ratingAverage(rate[r])
    print 'Top ' + str(n) + ' movies by Average Rating:'
    printRatings(rate.items(), 'average', n)
    rsort = sorted(rate.items(), key=lambda x: len(x[1]['ratings']), reverse=True)
    print '\nTop ' + str(n) + ' movies by most ratings:'
    for x in range(0, n):
        print 'Title: ' + rsort[x][1]['title'] + ' Ratings: ' + str(len(rsort[x][1]['ratings']))
    # Get ratings per gender
    users = loadUserInfo()
    women = {}
    men = {}
    for u in users:
        if users[u]['info']['gender'] == 'F':
            for r in rate:
                if women.has_key(r):
                    continue
                else:
                    women[r] = {}
                if users[u].has_key(r):
                    if women[r].has_key('ratings'):
                        women[r]['ratings'].append(users[u][r])
                    else:
                        women[r]['ratings'] = []
                        women[r]['ratings'].append(users[u][r])
        else:
            for r in rate:
                if men.has_key(r):
                    continue
                else:
                    men[r] = {}
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
 