#TAKE HOME FILE WITH ALL PARTS

##SARAH CUMMINGS

###PART 1
import json, re, sqlite3
import time
import urllib.request as urllib

#Connect to database
conn=sqlite3.connect('csc455.db')
#Request a cursor from the database
c=conn.cursor()

###PART 1A
#Create geo Table-- note types PART1A
GeoTable= '''CREATE TABLE Geo
(
locationID VARCHAR(50),
type VARCHAR(10),
longitude NUMBER,
lattitude NUMBER,
CONSTRAINT Geo
    Primary Key(locationID)
);'''

#Create the user table
UserTable= '''CREATE TABLE User
(
id NUMBER(25),
name VARCHAR(50),
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
user_id NUMBER(20),
locID VARCHAR(50),

CONSTRAINT TwitterPK
Primary Key(id_str),

CONSTRAINT TwitterFK
Foreign Key(user_id)
REFERENCES User(id),

CONSTRAINT TwitterFK1
Foreign Key(locID)
REFERENCES Geo(locationID)
);'''



#drop tables if they exist
c.execute("DROP TABLE IF EXISTS User;")
c.execute("DROP TABLE IF EXISTS Twitter2;")
c.execute("DROP TABLE IF EXISTS Geo;")

#make the tables from table strings above
c.execute(UserTable)
c.execute(GeoTable)
c.execute(Twitter2table)

###PART 1B
start1B=time.time()

#read in the file from the web
tweetFile = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
#Create file of tweets
f= open('day_of_tweets99.txt','w')

#loop through tweets and read to file
for i in range(500000):
    #decode the tweets
    decodedTweets = tweetFile.readline().decode("utf8")
    try:
        f.write(decodedTweets)
    except(ValueError):
         pass
end1B= time.time()
f.close()

#Find the runtime
print ("Difference is ", (end1B-start1B), 'seconds for part 1B')
print ("Performance : ", 100000/(end1B-start1B), ' operations per second ')



###PART 1C
start1C=time.time()
#read in the file from the web
tweetFile = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
                         
#loop through tweets and read to file
for i in range(500000):
    #decode the tweets
    decodedTweets = tweetFile.readline().decode("utf8")
    try:
        tDict= json.loads(decodedTweets)
        userInsertVals= (tDict['user']['id'],tDict['user']['name'],tDict['user']['screen_name'],tDict['user']['description'], tDict['user']['friends_count'])
        c.execute('INSERT OR IGNORE into User VALUES (?,?,?,?,?)', userInsertVals)

        if str(tDict['geo']) == 'None':
            locId= 'None'
        else:
            locId = tDict['geo']['coordinates']
            latt= locId[0]
            long= locId[1]
            geoInsertVals= (str(tDict['geo']['coordinates']),tDict['geo']['type'], latt, long)#need better PK and split coordinates
            c.execute('INSERT OR IGNORE into Geo VALUES(?,?,?,?)',geoInsertVals)
        twitterInsertVals= (tDict['created_at'],tDict['id_str'],tDict['text'],tDict['source'],tDict['in_reply_to_user_id'],tDict['in_reply_to_screen_name'],tDict['in_reply_to_status_id'],tDict['retweet_count'],tDict['contributors'],tDict['user']['id'], str(locId))
        c.execute('INSERT OR IGNORE INTO Twitter2 VALUES (?,?,?,?,?,?,?,?,?,?,?);', twitterInsertVals)

    except(ValueError):
         pass

end1C= time.time()

#Find the runtime
print ("Difference is ", (end1C-start1C), 'seconds for part 1C')
print ("Performance : ", 100000/(end1C-start1C), ' operations per second ')

#Find the row counts
userRowsCount= c.execute("SELECT Count(*) FROM User;").fetchall()
geoRowsCount= c.execute("SELECT Count(*) FROM Geo;").fetchall()
tweetsRowsCount= c.execute("SELECT Count(*) FROM Twitter2;").fetchall()    

print("Number of rows in User table for part C: ",userRowsCount)
print("Number of rows in Geo table for part C: ",geoRowsCount)
print("Number of rows in Twitter2 for table part C: ",tweetsRowsCount)


###PART 1D

#drop tables if they exist
#we drop and re execute to get rid of 1C inserted data

c.execute("DROP TABLE IF EXISTS User;")
c.execute("DROP TABLE IF EXISTS Twitter2;")
c.execute("DROP TABLE IF EXISTS Geo;")

#make the tables from table strings above
c.execute(UserTable)
c.execute(GeoTable)
c.execute(Twitter2table)


#read in txt file
start1D= time.time()
tweetFile = open('day_of_tweets99.txt', 'r', encoding='utf8')


#loop through tweets and read to file
for tweet in tweetFile:
    try:
        tDict= json.loads(tweet)
        userInsertVals= (tDict['user']['id'],tDict['user']['name'],tDict['user']['screen_name'],tDict['user']['description'], tDict['user']['friends_count'])
        c.execute('INSERT OR IGNORE into User VALUES (?,?,?,?,?)', userInsertVals)

        if str(tDict['geo']) == 'None':
            locId= 'None'
        else:
            locId = tDict['geo']['coordinates']
            latt= locId[0]
            long= locId[1]
            geoInsertVals= (str(tDict['geo']['coordinates']),tDict['geo']['type'], latt, long)#need better PK and split coordinates
            c.execute('INSERT OR IGNORE into Geo VALUES(?,?,?,?)',geoInsertVals)
        twitterInsertVals= (tDict['created_at'],tDict['id_str'],tDict['text'],tDict['source'],tDict['in_reply_to_user_id'],tDict['in_reply_to_screen_name'],tDict['in_reply_to_status_id'],tDict['retweet_count'],tDict['contributors'],tDict['user']['id'], str(locId))
        c.execute('INSERT OR IGNORE INTO Twitter2 VALUES (?,?,?,?,?,?,?,?,?,?,?);', twitterInsertVals)

    except(ValueError):
         pass

end1D= time.time()

print ("Difference is ", (end1D-start1D), 'seconds for partD')
print ("Performance : ", 100000/(end1D-start1D), ' operations per second ')

userRowsCount= c.execute("SELECT Count(*) FROM User;").fetchall()
geoRowsCount= c.execute("SELECT Count(*) FROM Geo;").fetchall()
tweetsRowsCount= c.execute("SELECT Count(*) FROM Twitter2;").fetchall()    

print("Number of rows in User table for part D: ",userRowsCount)
print("Number of rows in Geo table for part D: ",geoRowsCount)
print("Number of rows in Twitter2 table for part D: ",tweetsRowsCount)



### Part 1E: I had a very small amount of rows in my tables after part E.
#I've attached a seperate file with part E
#So that my further questions use the tables populated with part D

##################################################################
###PART 2A
q1time= time.time()
q1=c.execute("SELECT * FROM Twitter2 WHERE id_str LIKE '%44%';").fetchall()
q1end=time.time()
print ('q1 took ',(q1end-q1time), 'seconds')


q2time= time.time()
q2=c.execute("SELECT count(DISTINCT in_reply_to_user_id) FROM Twitter2;").fetchall()
q2end=time.time()
print('q2 took ', (q2end-q2time),'seconds')


q3time= time.time()
q3=c.execute("SELECT max(text) FROM Twitter2;").fetchall()
q3end=time.time()
print('q3 took ', (q3end-q3time),'seconds')

q4time= time.time()
q4=c.execute('''SELECT user.screen_name, avg(lattitude), avg(longitude)
		FROM Geo, User, Twitter2
		WHERE Geo.locationID = Twitter2.locID AND User.id=Twitter2.user_id
		GROUP BY User.id;''').fetchall()
q4end=time.time()
print('q4 took ', (q4end-q4time),'seconds')

q5itime= time.time()
count= 0
while count<10:
    c.execute('''SELECT user.screen_name, avg(lattitude), avg(longitude)
		FROM Geo, User, Twitter2
		WHERE Geo.locationID = Twitter2.locID AND User.id=Twitter2.user_id
		GROUP BY User.id;''').fetchall()
    count=count+1
q5iend=time.time()
print('q4 ten times took ', (q5iend-q5itime),'seconds')

q5iitime= time.time()
count= 0
while count<100:
    c.execute('''SELECT user.screen_name, avg(lattitude), avg(longitude)
		FROM Geo, User, Twitter2
		WHERE Geo.locationID = Twitter2.locID AND User.id=Twitter2.user_id
		GROUP BY User.id;''').fetchall()
    count=count+1
q5iiend=time.time()
print('q4 100 times took ', (q5iiend-q5iitime),'seconds')

##PART 2B

#I skipped cause i ran out of time.

####################################################
###PART 3A
start3A=time.time()

def numbers2letters(int_str):
    res = []
    for i in str(int_str):
        res.append(chr(ord('a')+(int(i))))
    return "".join(res)

g= open('insertStatementsTakeHome25.txt','w')
IDS= c.execute("SELECT id FROM User;").fetchall()

count=0
insertVals= []

while count< (len(IDS)-1):
    chID= str(numbers2letters(IDS[count][0]))
    insertVals.append(chID)
    allRows = c.execute("SELECT * FROM User;").fetchall()
    for row in allRows:
        insertVals.append(row)
        insertVals2= str(insertVals)
        string=str('INSERT OR IGNORE into User VALUES '+ insertVals2+ ';')

        g.write(string)
    count=count+1    

g.close()
end3A=time.time()

#Find runtime
print('3A runtime: ', end3A-start3A)


##PART3B

start3B=time.time()

def numbers2letters(int_str):
    res = []
    for i in str(int_str):
        res.append(chr(ord('a')+(int(i))))
    return "".join(res)

h= open('insertStatementsTakeHome3.txt','w')
tweetFile= open('day_of_tweets99.txt', 'r', encoding='utf8')

for tweet in tweetFile:
    insertVals=[]
    decodedTweet = tweetFile.readline()
    tDict= json.loads(decodedTweet)
    ID= tDict['user']['id']
    chID= str(numbers2letters(ID))
    insertVals.append(chID)
    insertVals.append(tDict['user']['id'])
    insertVals.append(tDict['user']['name'])
    insertVals.append(tDict['user']['screen_name'])
    insertVals.append(tDict['user']['description'])
    insertVals.append(tDict['user']['friends_count'])
    insertVals2= str(insertVals)
    string=str('INSERT OR IGNORE into User VALUES '+ insertVals2+ ';')
    h.write(string)

h.close()
tweetFile.close()

end3B=time.time()

print('Runtime: ', end3B-start3B, 'seconds')

###########################################################
###PART 4A
q= open('geoTableFile9.txt','w')

q.write(' unknown|unknown|unknown|unknown'+'\n')
geoRows= c.execute('SELECT * FROM Geo').fetchall()
for row in geoRows:
    geoValsList= []
    for val in row:
        if type(val)==float:
            geoValsList.append(str(round(val,4)))
        else:
            geoValsList.append(str(val))
    newGeoRow="|".join(geoValsList)
    q.write(newGeoRow + '\n')
q.close    


###PART 4B
p= open('twitterTableFile2.txt','w')

twitterRows= c.execute('Select * From Twitter2').fetchall()
for row in twitterRows:
    twitterValsList=[]
    for val in row:
        if val== None:
            twitterValsList.append('unknown')
        else:
            twitterValsList.append(str(val))
    newTwitterRow="|".join(twitterValsList)
    p.write(newTwitterRow +'\n')
p.close


###PART 4C
r= open('userTablefiles3.txt','w')
userRows=c.execute('Select * From User').fetchall()
for row in userRows:
    UserRowVals= []
    name= str(row[1])
    screenName= str(row[2])
    description= str(row[3])
    for val in row:
        UserRowVals.append(str(val))
    if (name in screenName) or (name in description):
        UserRowVals.append('True'+'\n')
    else:
        UserRowVals.append('False'+'\n')
    newUserRow="|".join(UserRowVals)
    r.write(str(newUserRow))
                           
r.close                           


c.close()
conn.commit()
conn.close()
