import sqlite3
from sqlite3 import OperationalError

conn = sqlite3.connect('csc455_HW3.db')
c = conn.cursor()

# Open and read the file as a single buffer
fd = open('SarahC_Assignment3.sql', 'r')
# Read as a single document (not individual lines)
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';' which separates them)
sqlCommands = sqlFile.split(';')

# Execute every command from the input file (separated by ";")
for command in sqlCommands:
    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands
    try:
        c.execute(command).fetchall()
    except OperationalError:
        print ("Command skipped: "+ command)

print("Answer to Part 1 Number 1: ")
print( c.execute(sqlCommands[30]).fetchall())

#I can't get #2 to work because FULL OUTER JOINS aren't supported in sqllite



print("Answer to Part 1 Number 4: ")
print(c.execute(sqlCommands[33]).fetchall())

print("Answer to Part 1 Number 5: ")
print(c.execute(sqlCommands[34]).fetchall())


c.close()
conn.commit()
conn.close()
