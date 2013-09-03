import couchdb
import json
def add():
    server = couchdb.Server()
    db = server['tweetsghanadecides']
    json_data=open('start38.txt').read()
    #print json_data
    data=json.loads(json_data)
    for line in data['response']['list']:
        try:
            db[line['url']] = line
        except couchdb.http.ResourceConflict:
            #print db[line['url']],"\n"
            #print line
            print "already exists"
        
    
if __name__ == '__main__':
    add()
    
