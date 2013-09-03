import couchdb
import csv
def query():
    server = couchdb.Server()
    db = server['tweepsnigeria']
    db2= server['tweepsnigeria_followers']
    file_2=open('nodes.csv','w')
    headers = ['Id', 'Label']
    wr = csv.writer(file_2, quoting=csv.QUOTE_ALL)
    wr.writerow(headers)
    names={}
    print "going in"
    tweeps=[]
    in_file=open('tweeps_no_followers.txt','rb')
    for row in in_file:
        tweeps.append(row.strip())
    in_file.close()
    in_file=open('tweeps_followers.txt','rb')
    for row in in_file:
        tweeps.append(row.strip())
    in_file.close()
    #print tweeps[0]
    for id in db:
        if( (db[id]['screen_name']).lower() in tweeps):
            names[(db[id]['screen_name']).lower()]=db[id]['id']
            l=[]
            l.append(db[id]['screen_name'])
            l.append(db[id]['id'])
            wr.writerow(l)
        #names2={}
    file_2.close()
    file_2=open('edges.csv','w')
    wr = csv.writer(file_2, quoting=csv.QUOTE_ALL)
    headers = ['Id', 'Source', 'Target']
    wr.writerow(headers)
    count=0
    print len(names)
    print names
    for id in db2:
        #names[db2[id]['_id']]
       if id.lower() in tweeps:
           for name ,value in names.items():
               if value in db2[id]['ids']:
                   l=[]
                   l.append(count)
                   l.append(names[str(id).lower()])
                   l.append(value)
                   wr.writerow(l)
                   count+=1
        
    file_2.close()
    
if __name__ == '__main__':
    query()
