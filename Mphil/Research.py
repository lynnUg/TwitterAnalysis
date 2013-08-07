import os
from twython import Twython
import time
import couchdb
def login():

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token
    server = couchdb.Server()
    db = server['tweetsoccupynigeria']
    APP_NAME = 'Research_masters'
    TWITTER_APP_KEY = '**************' #supply the appropriate value
    TWITTER_APP_KEY_SECRET = '*****************************' 
    TWITTER_ACCESS_TOKEN = '******************************'
    TWITTER_ACCESS_TOKEN_SECRET = '*************************************'
    t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
   
    search = t.search(q='#OccupyNigeria', count=100)
    #print tweets[1]
    tweets = search['statuses']
    print len(tweets)
    for tweet in tweets :
        db[tweet['id_str']] = tweet
        
    
if __name__ == '__main__':
    login()
    

           


