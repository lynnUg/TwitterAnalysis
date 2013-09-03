import couchdb
import datetime
import csv
from twython import Twython
import twython
import operator
server=couchdb.Server()
def get_tweets():
    db=server['tweetsoccupynigeria']
    tweets_jan={}
    for id in db:
        date=datetime.datetime.fromtimestamp(int(db[id]['trackback_date'])).strftime('%Y-%m-%d %H:%M:%S')
        if (date[:7]=='2012-01'):
            if(date in tweets_jan):
                tweets_jan[date].append([(db[id]['trackback_author_nick']).lower(),db[id]['content']])
            else:
                tweets_jan[date]=[]
                tweets_jan[date].append([(db[id]['trackback_author_nick']).lower(),db[id]['content']])

    db_2=server['tweepsnigeria']
    users={}
    for id in db_2:
        users[(db_2[id]['screen_name']).lower()]=db_2[id]['id']
        
    get_mentions(tweets_jan,users)
        #print tweets_jan
    #get links
    #user against tweet
def get_mentions(tweets_jan,users):
    db_3=server['extratweeps']
    
    TWITTER_APP_KEY = 'U31NQIxZ1HcKeKTUtTW1w' #supply the appropriate value
    TWITTER_APP_KEY_SECRET = 'bZBtxjQurHUfjDvK8Pl5iJWhgvzejvC2HJHSN1E' 
    TWITTER_ACCESS_TOKEN = '1548279967-gDMrGBaZIb3jofVekP25SnpWZrnhxSSFra7GgRV'
    TWITTER_ACCESS_TOKEN_SECRET = 'zLwSwgsMZxtH0tlB2x1UU217nq0ujlpkzP8SCXa07u8'
    t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    
    file_1=open('nodes5.csv','w')
    headers = ['Id', 'Label']
    wr_1 = csv.writer(file_1, quoting=csv.QUOTE_ALL)
    wr_1.writerow(headers)
    file_2=open('edges5.csv','w')
    wr_2 = csv.writer(file_2, quoting=csv.QUOTE_ALL)
    headers = ['Id', 'Source', 'Target']
    wr_2.writerow(headers)
    count=0
    count2=0
    id_user={}
    for tweets,values in tweets_jan.items():
        for tweet in values:
            if(len(tweet[0])>0):
                l=[]
                try:
                    l.append(users[tweet[0]])
                except KeyError:
                    users[tweet[0]]=count
                    count+=1
                    l.append(users[tweet[0]])
                l.append(tweet[0])
                wr_1.writerow(l)
                long_word=tweet[1]
                mentions=[word[1:] for word in long_word.split() if word.startswith('@')]
                for mention in mentions:
                    if(mention[-1:]==':'):
                        mention=mention[:-1]
                    if (len(mention)>0):
                        z=[]
                        z.append(count2)
                        count2+=1
                        z.append(users[tweet[0]])
                        #print "mention", mention
                        try:
                            the_id=t.show_user(screen_name=mention)
                            if not( mention in users):
                                id_user[mention]=1
                                users[mention]=the_id['id']
                                u=[]
                                u.append(users[mention])
                                u.append(mention)
                            else:
                                if(mention in id_user):
                                    id_user[mention]+=1
                                else:
                                    id_user[mention]=1
                        except twython.exceptions.TwythonError:
                            if not( mention in users):
                                id_user[mention]=1
                                users[mention]=count
                                count+=1
                                u=[]
                                u.append(users[mention])
                                u.append(mention)
                            else:
                                if(mention in id_user):
                                    id_user[mention]+=1
                                else:
                                    id_user[mention]=1
                                    #print "doesn't exsist"
                            #print id_user
                        z.append(users[mention])
                        #print z
                        wr_2.writerow(z)
    sorted_x = sorted(id_user.iteritems(), key=operator.itemgetter(1))        
    print sorted_x
                #def get_links():

if __name__ == '__main__':
    get_tweets()
    
