import csv as csv
import numpy as np
import operator
from operator import itemgetter
from guess_language import guessLanguage

csv_file_object=csv.reader(open('tweet.csv','rb'))
header=csv_file_object.next()
train_data=[]
for row in csv_file_object: #for every row in the csv_file object
    train_data.append(row)
train_data=np.array(train_data)
#print train_data.shape
Text =train_data[:,0]
#print train_data[355,0]
#print Text[478]
other={}
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
text_file = open("Output3.txt", "w")
the_max=1
for key,value in hcount_sorted:
    if(count==21):
        the_max=value
    if(count>=21 and count<=71):
        #print "%s %.3f" %(key.decode('utf-8',), value)
        output=key+"	"+str(float(value)/float(the_max))+"	m"
        text_file.write(output+"\n")
    count+=1

