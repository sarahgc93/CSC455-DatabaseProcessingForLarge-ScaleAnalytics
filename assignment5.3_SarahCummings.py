import json
import urllib.request as urllib

#read in the file from the web
tweetFile = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt")

#create the file for the error tweets
f= open('error_tweets.txt','w')


friendCounts=[]
names=[]
userIDS=[]

lines=[]
for i in range(7000):
    #decode the tweets
    decodedTweets = tweetFile.readline().decode("utf8")
    #read just one line
    newLine=tweetFile.readline()
    #add that line to the list
    lines.append(newLine)
    #create twitter dictionary
    try:
        tDict= json.loads(decodedTweets)
        friendCounts.append(tDict['user']['friends_count'])
        names.append(tDict['user']['name'])
        userIDS.append(tDict['user']['id'])
    except(ValueError):
        pass

maxFriendCount= max(friendCounts)
maxIndex=friendCounts.index(maxFriendCount)
print('The info for the person with the most friends is as follows: \n', 'NAME:',names[maxIndex],'ID:',userIDS[maxIndex],'Friend Count:',maxFriendCount)
        
