import couchdb
def query():
    server = couchdb.Server()
    db = server['tweetsoccupynigeria']
    for id in db:
        print db[id]['title'],"\n"
        
    
if __name__ == '__main__':
    query()
