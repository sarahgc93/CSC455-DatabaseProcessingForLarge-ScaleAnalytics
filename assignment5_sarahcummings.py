import json, re, sqlite3
import urllib.request as urllib

#Connect to database
conn=sqlite3.connect('csc455.db')
#Request a cursor from the database
c=conn.cursor()

#Create the user table
UserTable= '''CREATE TABLE User
(
id NUMBER(25),
name VARCHAT(50),
screen_name VARCHAR(60),
description VARCHAT(50),
friends_count NUMBER(100), 
CONSTRAINT User
    Primary Key(id)
);'''

#Create twitter table 
Twitter2table= '''CREATE TABLE Twitter2
( 
created_at VARCHAR(50),  
id_str NUMBER(50),  
text VARCHAR(160),  
source VARCHAR(100),  
in_reply_to_user_id VARCHAR(25),  
in_reply_to_screen_name VARCHAR(25), 
in_reply_to_status_id VARCHAR(25), 
retweet_count NUMBER(5), 
contributors  VARCHAR(25),
user_id VARCHAR(20),

CONSTRAINT TwitterPK
Primary Key(id_str),

CONSTRAINT TwitterFK
Foreign Key(user_id)
REFERENCES User(id)
);'''

#drop tables if they exist
c.execute("DROP TABLE IF EXISTS User;")
c.execute("DROP TABLE IF EXISTS Twitter2;")

#make the tables from table strings above
c.execute(UserTable)
c.execute(Twitter2table)

#read in the file from the web
tweetFile = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt")

#create the file for the error tweets
f= open('error_tweets.txt','w')

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
        userInsertVals= (tDict['user']['id'],tDict['user']['name'],tDict['user']['screen_name'],tDict['user']['description'], tDict['user']['friends_count'])
        c.execute('INSERT OR IGNORE into User VALUES (?,?,?,?,?)', userInsertVals)
        twitterInsertVals= (tDict['created_at'],tDict['id_str'],tDict['text'],tDict['source'],tDict['in_reply_to_user_id'],tDict['in_reply_to_screen_name'],tDict['in_reply_to_status_id'],tDict['retweet_count'],tDict['contributors'],tDict['user']['id'])
        c.execute('INSERT INTO Twitter2 VALUES (?,?,?,?,?,?,?,?,?,?);', twitterInsertVals)
        # use this for a test: print('For tweet #',i,' the id is : ',tDict['id'], ' and tweet text is: ',tDict['text'])
    except(ValueError):
        string='For tweet #'+str(i)+' the Tweet is corrupted'
        f.write(string)
        f.close
        
conn.commit()
conn.close()

