from operator import itemgetter
import urllib.request as urllib
import json

#read in the file from the web
tweetFile = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt")

#create the file for the error tweets
f= open('error_tweets.txt','w')

text= '.'
lines=[]
for i in range(700):
    #decode the tweets
    decodedTweets = tweetFile.readline().decode("utf8")
    #read just one line
    newLine=tweetFile.readline()
    #add that line to the list
    lines.append(newLine)
    #create twitter dictionary
    try:
        tDict= json.loads(decodedTweets)
        text= text + str(tDict['text'])

    except(ValueError):
        text= text
        
words = text.split(' ')
dCount = {}

for word in words:
    if word != '':
        if word not in dCount.keys():
            dCount[word] = 0
        dCount[word] = dCount[word]+1

countKeys = dCount.keys()
countVals = dCount.values()
countPairs = zip(countVals, countKeys)

# Sort the words by descending frequency
sorted_countPairs = sorted(countPairs, key=itemgetter(0), reverse=True)

#print the three most frequent words and their count
print (sorted_countPairs[0:3])

