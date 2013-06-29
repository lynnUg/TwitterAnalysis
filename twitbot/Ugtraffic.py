import sys
import pprint
from time import sleep
 
import twitter
import redis
import twitter__login

LOLCOIFFEURS_KEYWORDS = ('coiffeur', 'coiffeurs')
LOLCOIFFEURS_LIST = "lolcoiffeurs"
 
BLACKLISTED_USERS = ['untel', 'untelautre', 'and so on']
 
RESPONSE = """ Les coiffeurs sont plus rigolos qu'ils n'en ont l'hair!\
 toi aussi vote pour tes lolcoiffeurs preferes! http://bit.ly/uiu8BZ"""
 
 
def auth_to_twitter():
    
    return twitter__login.login()
 
 
def get_since_id(redis, key):
    """"""
    # Fetching last value in keyword redis place
    since_id = redis.get(key + ":last_since_id")
 
    return since_id if since_id else None
 
 
def update_since_id(redis, key):
    """"""
    stored_since_id = redis.get(key + ":last_since_id")
 
    try:
        last_tweet_id = str(redis.lrange(key, 0, 0)[0])
    except IndexError:
        last_tweet_id = None
 
 
    if last_tweet_id and (last_tweet_id != stored_since_id):
        redis.set(key + ":last_since_id", last_tweet_id)
 
    return True
 
 
def update_search_stack(api_session, tweet_stack, keyword):
    """Searches for a specific term on twitter public timeline"""
    # Storing last fetched id in order to make fewer requests
    since_id = get_since_id(redis, "%s:%s" % (LOLCOIFFEURS_LIST, keyword))
    search_tweet = api_session.GetSearch(term=keyword, since_id=since_id)
 
    for t in search_tweet:
        computed_tweet = {
            "keyword": keyword,
            "username": t.user.screen_name,
            "created_at": t.created_at,
            "text": t.text,
        }
        sys.stdout.write("adding tweet with id %s by user %s to database\n" % (str(t.id), str(t.user.screen_name)))
        if (computed_tweet["username"] not in BLACKLISTED_USERS):
            redis.rpush((LOLCOIFFEURS_LIST + ":%s" % (keyword)), t.id)
            redis.hmset("%s:tweet:%s" % (LOLCOIFFEURS_LIST, t.id), computed_tweet)
 
    print "Last since id en vigueur pour ce mot cle : %s" % since_id
 
    return
 
 
def tweet_and_shout(api_session, redis, key, timeout=600):
    """"""
    for tweet_id in redis.lrange("%s:%s" % (LOLCOIFFEURS_LIST, key), 0, -1):
        tweet_dict = redis.hgetall("%s:tweet:%s" % (LOLCOIFFEURS_LIST, tweet_id))
 
        # Tracking answered tweets in a brand new set, and posting
        # a reply to it
        print "replying tweet : %s" % (tweet_id)
        redis.sadd((LOLCOIFFEURS_LIST + ":%s:answered" % (key)), tweet_id)
#        api_session.PostUpdate("@%s %s" % (tweet_dict["username"], RESPONSE), in_reply_to_status_id=tweet_id)
        # Popping out element from the left of the list
        # as we answer it
        redis.rpop("%s:%s" % (LOLCOIFFEURS_LIST, key))
 
        # Wait timeout before replying again
        sleep(timeout)
 
    return
 
def run_bot(api_session, redis, keywords):
    """"""
    while 42:
        for key in keywords:
            update_search_stack(api_session, redis, key)
            update_since_id(redis, "%s:%s" % (LOLCOIFFEURS_LIST, key))
            tweet_and_shout(api_session, redis, key, timeout=1)
        print "Waiting for one minute\n\n\n"
        sleep(60)
 
 
if __name__ == "__main__":
    twitter_session = auth_to_twitter()
    #twitter_session.statuses.update(status="Using sweet Python Twitter Tools.")
    #print x[0]['user']['screen_name']
    #twitter_session.statuses.update(status="Using sweet Python Twitter Tools :).")
    redis = redis.Redis("localhost")
    #print 'here'
    #run_bot(twitter_session, redis, LOLCOIFFEURS_KEYWORDS)
