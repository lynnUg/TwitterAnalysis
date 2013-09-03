import couchdb
def query():
    server = couchdb.Server()
    db = server['tweetsoccupynigeria']
    names={}
    print "going in"
    for id in db:
        #print db[id]['title'],"\n"
        if  db[id]['trackback_author_nick'] not in names:
            print 'here'
            names[db[id]['trackback_author_nick']]=1
        else:
            names[db[id]['trackback_author_nick']]+=1
            #print names
    file_2=open('all_users3.txt','w')
    for name, value in names.items():
        file_2.write(name+"\n")
    file_2.close()
if __name__ == '__main__':
    query()
