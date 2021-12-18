import sqlite3

conn = sqlite3.connect('../postInfo.db')

print("Opened database successfully")
c = conn.cursor()

c.execute('''CREATE TABLE ProducerDynamicInfo
    (ID INT PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL,
    DynamicNumber String NOT NULL,
    lastInfo CHAR(5000));''')
print("Table created successfully")

conn.commit()
conn.close()
