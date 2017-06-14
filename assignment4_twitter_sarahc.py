import sqlite3
import json

#Connect to database
conn=sqlite3.connect('csc455.db')

#Request a cursor from the database
c=conn.cursor()

#Create the table
TwitterTable= '''CREATE TABLE Twitter
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
CONSTRAINT TwitterPK
	Primary Key(id_str)
);'''

#Drop tables if they exists
c.execute("DROP TABLE IF EXISTS Twitter")

#Create the tables
c.execute(TwitterTable)

#Open and read file
fd = open('/Users/sarahcummings/Documents/csc455/Assignment4.txt', 'r', encoding='utf8')

#split file on end of tweet deliminator and creates strings for each line 
tweetList = fd.readline().split('EndOfTweet')
fd.close()

for tweet in tweetList:
    decoded_line = json.loads(tweet)
    insertvalues2 = (decoded_line.get(u'created_at'), decoded_line.get(u'id_str'), decoded_line.get(u'text'), decoded_line.get(u'source'), decoded_line.get(u'in_reply_to_user_id'), decoded_line.get(u'in_reply_to_screen_name'), decoded_line.get(u'in_reply_to_status_id'), decoded_line.get(u'retweet_count'), decoded_line.get(u'contributors'))
    c.execute('INSERT INTO Twitter VALUES (?,?,?,?,?,?,?,?,?);', insertvalues2)

#Use the code in comments below to see what's in the table
#allSelectedRows = c.execute("SELECT * FROM Twitter;").fetchall()
#for eachRow in allSelectedRows:
    #for value in eachRow:
        #print (value, "\t",)
    #print ("\n",) # \n is the end of line symbol


 
conn.commit()
conn.close()
