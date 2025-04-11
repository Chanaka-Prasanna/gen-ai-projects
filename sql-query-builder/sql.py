import sqlite3 
import random

#Coonect to sqlite
connection = sqlite3.connect("student.db")

# create a cursor object to inserrt record, create table and retrive
cursor = connection.cursor()

# Create the table (if not exists)
table_info = '''
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25) COLLATE NOCASE, 
    CLASS VARCHAR(25) COLLATE NOCASE, 
    SECTION VARCHAR(25) COLLATE NOCASE, 
    MARKS INT
)
'''
cursor.execute(table_info)

# Sample data for random selection
names = ['Chanaka', 'Prasanna', 'John', 'Alice', 'Bob', 'Emma', 'Liam', 'Olivia', 'Noah', 'Sophia',
         'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia', 'Elijah', 'Harper', 'Lucas', 'Evelyn']
classes = ['Data Science', 'Machine Learning', 'Artificial Intelligence', 'Cyber Security', 'Software Engineering', 'Computer Science']
sections = ['A', 'B', 'C']
records = [(random.choice(names), random.choice(classes), random.choice(sections), random.randint(50, 100)) for _ in range(100)]

#Insert some records
# cursor.execute('''INSERT INTO STUDENT VALUES('Chanaka','Data Science','A',90)''')

cursor.executemany('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)''', records)

# Display all the records
print("The inserted recordes are: ")

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()
