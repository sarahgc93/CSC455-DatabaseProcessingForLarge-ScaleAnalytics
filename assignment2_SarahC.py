import sqlite3

#Connect to database
conn=sqlite3.connect('csc455.db')

#Request a cursor from the database
c=conn.cursor()

LicenseTable= '''CREATE TABLE License
(
    LicenseNumber NUMBER(10),
    Renewed VARCHAR(10),
    Status VARCHAR(10),
    StatusDate VARCHAR(10),
    DriverType VARCHAR(20),
    LicenseType VARCHAR(10),
    OriginalIssueDate VARCHAR(12), 
    Name VARCHAR(20),
    Sex VARCHAR(6), 
    ChauffeurCity VARCHAR(20),
    ChauffeurState VARCHAR(2),
    RecordNumber VARCHAR(15),
    CONSTRAINT LicenseFK
       Foreign Key(ChauffeurCity)
    REFERENCES Chauffeur(ChauffeurCity),
    CONSTRAINT LicensePK
       Primary Key(RecordNumber)
    );'''



ChauffeurTable= '''CREATE TABLE Chauffeur
(
    ChauffeurCity VARCHAR(20),
    ChauffeurState VARCHAR(2),
    CONSTRAINT ChauffeurPK
        Primary Key(ChauffeurCity)
);'''

#Drop tables if they exists
c.execute("DROP TABLE IF EXISTS License")
c.execute("DROP TABLE IF EXISTS Chauffeur")

#Create the tables
c.execute(LicenseTable)
c.execute(ChauffeurTable)

#Open and read file
fd= open('Public_Chauffeurs_Short.csv','r')
#Read all lines from the file into variable
allLines= fd.readlines()
fd.close() #close file

#Create new variable that eliminates First Row of file
dataLines= allLines[1:]

#Replace Null strings with None
for line in dataLines:
    valueList = line.strip().split(',')
    for n,i in enumerate(valueList):
        if i == 'NULL':
           valueList[n] = None
    #Add all data into SQL table
    c.execute("INSERT INTO License VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", valueList)




#Take Distinct ChauffeurCity and ChauffeurState data from License table and add it to Chauffeur Table
c.execute("INSERT INTO Chauffeur(ChauffeurCity, ChauffeurState) SELECT DISTINCT ChauffeurCity, ChauffeurState FROM License;")



#Create new license table without Chauffeur State Data
License1NF = '''CREATE TABLE License2
(
    LicenseNumber NUMBER(10),
    Renewed VARCHAR(10),
    Status VARCHAR(10),
    StatusDate VARCHAR(10),
    DriverType VARCHAR(20),
    LicenseType VARCHAR(10),
    OriginalIssueDate VARCHAR(12), 
    Name VARCHAR(20),
    Sex VARCHAR(6), 
    ChauffeurCity VARCHAR(20),
    RecordNumber VARCHAR(15),
    CONSTRAINT LicenseFK
       Foreign Key(ChauffeurCity)
    REFERENCES Chauffeur(ChauffeurCity),
    CONSTRAINT LicensePK
       Primary Key(RecordNumber)
    );'''

#Drop new license table if it exists
c.execute("DROP TABLE IF EXISTS License2")
#Create the table
c.execute(License1NF)
#Insert all columns from original License table except ChauffeurState
c.execute('''INSERT INTO License2(LicenseNumber,
    Renewed, Status, StatusDate, DriverType, LicenseType,
    OriginalIssueDate, Name, Sex, ChauffeurCity, RecordNumber)
    SELECT LicenseNumber, Renewed, Status, StatusDate, DriverType,
    LicenseType, OriginalIssueDate, Name, Sex, ChauffeurCity, RecordNumber FROM License;''')

#Get rid of previous license table
c.execute("DROP TABLE License")


conn.commit()
conn.close()

