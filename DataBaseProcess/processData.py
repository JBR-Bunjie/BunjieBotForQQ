import sqlite3


def insertData():
    conn = sqlite3.connect("../postInfo.db")
    c = conn.cursor()

    print("Opened Database Successfully")
    c.execute(
        """
        
        """
    )
    print("Data Inserted Successfully")

    c.commit()
    c.close()
