import csv as csv
import numpy as np
import operator
from operator import itemgetter
from guess_language import guessLanguage
from numpy import newaxis, r_, c_, mat, e
csv_file_object=csv.reader(open('tweet_2.csv','rb'))
header=csv_file_object.next()
train_data=[]
for row in csv_file_object: #for every row in the csv_file object
    train_data.append(row)
train_data=np.array(train_data)
ids=train_data[:,6]
names=train_data[:,9]
Text =train_data[:,0]
retweet=train_data[:,10].astype(np.float)
#print train_data[355,0]
#print Text[478]
other={}
names_list=[]
print np.max(retweet)
text_file2 = open("users2.txt", "w")
i=0
for name in names:
    if (not(names_list.__contains__(name))):
        text_file2.write(name+"\n")
        names_list.append(name)
    i+=1
print len(names_list)
text_file2.close()


for words in Text:
    #print words
    words=words.split()
    for word in words:
        if(other.get(word)):
            other[word]+=1
        else:
            if(len(word)>3):
                if(not(word[:4]=='http')):
                    other[word]=1
            
hcount_sorted=sorted([(value,key) for (value,key) in other.items()] ,key=itemgetter(1), reverse=True)
count=1
text_file = open("words2.txt", "w")

the_max=1
for key,value in hcount_sorted:
    if(count==1):
        the_max=value
    if(count<=100):
        #print "%s %.3f" %(key.decode('utf-8',), value)
        output=key+"	"+str(float(2*value)/float(the_max))+"	m"
        text_file.write(output+"\n")
    count+=1

text_file.close()
