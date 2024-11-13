#Database generator file.  This file will generate a database called "prodcuts.db" if one doesn't already exist
import sqlite3

def create_database():
    #Connects to the database
    conn = sqlite3.connect("products.db")

    #Creates a cursor object
    c = conn.cursor()

    #Drops the table if it exists
    c.execute("DROP TABLE IF EXISTS PRODUCTS")

    #Executes the SQL query to create the table
    tableString = """CREATE TABLE IF NOT EXISTS PRODUCTS (
            ID INTEGER NOT NULL PRIMARY KEY,
            NAME VARCHAR(30),
            PRICE REAL,
            QUANTITY INTEGER,
            QUALITY VARCHAR(30))"""

    c.execute(tableString)

    #Inserts these statements with single quotes (for SQL to read) for string values
    c.execute("INSERT INTO PRODUCTS VALUES (0, 'Apples', 0.75, 120, 'Fresh')")
    c.execute("INSERT INTO PRODUCTS VALUES (1, 'Bananas', 0.40, 200, 'Ripe')")
    c.execute("INSERT INTO PRODUCTS VALUES (2, 'Oranges', 0.60, 150, 'Juicy')")
    c.execute("INSERT INTO PRODUCTS VALUES (3, 'Carrots', 0.30, 300, 'Crisp')")
    c.execute("INSERT INTO PRODUCTS VALUES (4, 'Grapes', 1.20, 80, 'Sweet')")

    c.execute("SELECT * FROM PRODUCTS")
 
    records = c.fetchall()

    print(records)

    #Commits the changes and close the connection
    conn.commit()
    conn.close()

#Calls the main fuction (although I'm not sure this is necessary for this file since there's no main method)
if __name__ == "__main__":
    create_database()