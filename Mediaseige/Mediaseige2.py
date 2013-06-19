#Simple python script that reads tweets from a CSV file ,tweets were under the hashtag #Mediasiege
#Extraction of users and followers to be used in graph visualization with Gelphi
#Extraction of words in tweets and counting the frequency of occurance in order to create a word cloud with processing
import twitter__login #python that logs into twitter api and authenticates access key and consumer key
import pickle
import time
import numpy as np
from operator import itemgetter
import csv

def readfile():
	#read in csv file and extract tweets
	csv_file_object=csv.reader(open('tweet.csv','rb'))
	header=csv_file_object.next()
	data=[]
	for row in csv_file_object: #for every row in the csv_file object
		data.append(row)
	data=np.array(data)
	return data

def getUsers(names):
	#extract names, further processing happens to load followers , inorder to create nodes and edges
	print names
	text_file = open("users.txt", "w")
	names_list=[] #names list
	for name in names:#for every name in the column
		if (not(names_list.__contains__(name))):
			text_file.write(name+"\n")
        	names_list.append(name)
	text_file.close()

def CreateWordCloud(Text):
  #extract words 
    count_words={}
    for words in Text:#for tweet in the column
    	words=words.split()
    	for word in words:
        	if(count_words.get(word)):
        		count_words[word]+=1 #increment word count every time found in word
        	else:
        		if(len(word)>3):
        			#elimnate links from word count
        			if(not(word[:4]=='http')):
        				count_words[word]=1
            
	hcount_sorted=sorted([(value,key) for (value,key) in count_words.items()] ,key=itemgetter(1), reverse=True)#sort dictonary starting with the word with the highest frequency
	count=1
	the_max=1
	text_file = open("words2.txt", "w")
	#place 100 words with the highest occurance in text file.Occurance is weighted as it is to visualized in processing
	for key,value in hcount_sorted:
		if(count==1):
			the_max=value
		if(count<=100):
			output=key+"	"+str(float(2*value)/float(the_max))+"	m"
        	text_file.write(output+"\n")
   		count+=1

	text_file.close()

def load_followers():
	#for each user extracted getusers method , load followers from twitter 
	t=twitter__login.login()
	in_file=open('users.txt','rb')
	count=1
	count2=1
	#twitter only allows 15 users's followers upload once every 30 min ,so this method is run a complete with adjustments in the count variable
	for row in in_file:
		name=row.strip()
		if (count>=47):
			followers=t.followers.ids(screen_name=name)
			#for every user obtain list of followers an store in follower text file (use user name for identifcation)
        	out_file=name+".txt"
        	out=open(out_file,'w')
        	pickle.dump(followers['ids'],out)
        	out.close()
        	count2+=1
		count+=1
	#tried adding a time variable to sleep after every 15 users, worked sometimes
	if(count2%15==0):
		time.sleep(180)
		count2=1

def GetIds():
	#obtain the ids for every uses, these are to be used to create nodes and edges that will be used to 
	t=twitter__login.login()
	file_1=open('users.txt','rb')
	file_2=open('user_id.txt','w')
    for row in file_1:
 		name=row
    	response = t.users.show(screen_name=name)
    	file_2.write(response['id_str']+"\n")
	file_1.close()
	file_2.close()

def CreateNodes():
	#create node (Id, label) where id is the user_id and lable is user name
	#load user name file and place them in list
	file_1=open('users.txt','rb')
	names=[]
	for row in file_1:
    	name =row.strip()
    	names.append(name)
	file_1.close()
	count=0
	#create output csv file with label
	headers = ['Id', 'Label']
	myfile=(open('node.csv','wb'))
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(headers)
	#load user ids and create nodes
	file_1=open('user_id.txt.txt','rb')
	for row in file_1:
    	name=row.strip()
    	x=[]#empty node
    	x.append(name)
    	x.append(names[count])
    	count+=1
    	wr.writerow(x)
    file_1.close()

def CreateEdges():
	#create edges in the format (Id, source, target) where is a Id is a general count ,source is a user_id and target is another user_id
	ids=[]
	#load user_ids
	file_1=open('user_id.txt','rb')
    for row in file_1:
    	name =row.strip()
    	ids.append(name)
	file_1.close()

	#load user names
	file_1=open('users.txt','rb')
	count=0
	#create edge.csv output file with header 
	headers = ['Id', 'Source','Target']
	myfile_1=open('edge.csv','wb')
	wr = csv.writer(myfile_1, quoting=csv.QUOTE_ALL)
	wr.writerow(headers)
	count2=0
	count3=0
	#load user's follower file , for every follower ,check if they exsist in id list , if yes create edge
	for row in file_1:
    	name=row.strip()+".txt"
    	other_file=open(name,'rb')
    	itemlist = pickle.load(other_file)
    	for item in itemlist:
        	if (ids.__contains__(str(item))):
            	l=[]
            	l.append(count3)
            	l.append(ids[count2])
            	l.append(str(item))
            	wr.writerow(l)
            	count3+=1
    other_file.close()
    count2+=1
	file_1.close()
if __name__ == '__main__':
  tweets=readfile()
  #getUsers(tweets[:,9])
  #CreateWordCloud(tweets[:,0])
  #load_followers()
  #GetIds()
  #CreateNodes()
  #CreateEdges()