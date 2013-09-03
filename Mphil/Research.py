import os
from twython import Twython
import time
import couchdb
def login():

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token
    server = couchdb.Server()
    db = server['tweepsnigeria_followers']
    db2= server['tweetsoccupynigeria']
    APP_NAME = 'traffic_ug'
    TWITTER_APP_KEY = 'U31NQIxZ1HcKeKTUtTW1w' #supply the appropriate value
    TWITTER_APP_KEY_SECRET = 'bZBtxjQurHUfjDvK8Pl5iJWhgvzejvC2HJHSN1E' 
    TWITTER_ACCESS_TOKEN = '1548279967-gDMrGBaZIb3jofVekP25SnpWZrnhxSSFra7GgRV'
    TWITTER_ACCESS_TOKEN_SECRET = 'zLwSwgsMZxtH0tlB2x1UU217nq0ujlpkzP8SCXa07u8'
    t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    names=[]
    in_file=open('tweeps_no_followers.txt','rb')
    count=1
    count2=1
    for row in in_file:
        name=row.strip()
        if (count>=608):
            print count, row 
            profile=t.get_followers_ids(screen_name=name)
            db[name] = profile
            count2+=1
        count+=1
        if((count2%16)==0):
            time.sleep(15*60)
            count2=1
        
    in_file.close()
         
        
    
if __name__ == '__main__':
    login()
    

           


