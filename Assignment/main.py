#Program to view and edit files within the database
#Imports the sql library
import sqlite3
#Imports the products class
from products import Product

#Note:  This program DOES provide error handling on all inputs

def main():
    #Connects to the products database
    try:
        conn = connect_to_database("products.db")
        if conn:
            while True:
                #Displays menu
                display_row_count(conn)
                print("\nMenu options: \n1: Print all data \n2: Insert data \n3: Find data \n4: Delete data \nType Q to quit")
                user_input = input("\nWhat is your selection? ").strip().upper()

                #Match statements that will be used based on the user's input from above
                match user_input:
                    case "Q":
                        print("\nTerminating program. Goodbye!\n")
                        break
                    case "1":
                        display_all_data(conn)
                    case "2":
                        display_insert_data(conn)
                    case "3":
                        display_find_data(conn)
                    case "4":
                        display_delete_data(conn)
                    case _:
                        print("\nInvalid input. Please enter a number between 1 and 4 or type 'Q' to quit.")
                        continue

                #Asks the user if they want to return to the main menu or quit
                while True:
                    start_over = input("\nDo you want to return to the main menu? Y/N: ").strip().upper()
                    if start_over == "Y":
                        break
                    elif start_over == "N":
                        print("\nTerminating program. Goodbye!\n")
                        return
                    else:
                        print("\nInvalid input. Please enter 'Y' or 'N'.")
        else:
            print("\nFailed to connect to the database!")
    except Exception as e:
        print(f"\nAn error occurred: {e}.")
    finally:
        #Ensures the database connection is closed
        if conn:
            conn.close()

#Method to connect to the database.  Throws an error message if database cannot be found.
def connect_to_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
        print(f"\nConnected to the database file {db_name} successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"\nError connecting to the database file {db_name}: {e}.")
        return None

#Displays the row count of the database above the menu
def display_row_count(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM PRODUCTS")
        count = c.fetchone()[0]
        print(f"\nThere are currently {count} rows in the database table.")
    except Exception as e:
        print(f"\nAn error occurred while counting rows: {e}.")

#Displays all the data in the database
def display_all_data(conn):
    product_list = []
    
    try:
        #Do any operations needed with the database connection
        c = conn.cursor()

        #Fetces and displays all records from the PRODUCTS table
        c.execute("SELECT * FROM PRODUCTS")
        records = c.fetchall()

        #Checks if records are found. Prints error if no data is found.
        if records:
            for record in records:
                #Creates Product instances with the appropriate arguments: id, name, price, quantity, quality
                newProd = Product(record[0], record[1], record[2], record[3], record[4])
                product_list.append(newProd)
            for product in product_list:
                print(product)
        else:
            print("\nNo data was found!")
    except Exception as e:
        print(f"\nAn error occurred: {e}.")

#Allows the user to add a new item to the database. Checks if both ID and name have already been added.
def display_insert_data(conn):
    try:
        c = conn.cursor()
        while True:
            try:
                product_id = int(input("\nEnter new product ID: "))
                c.execute("SELECT * FROM PRODUCTS WHERE ID=?", (product_id,))
                if c.fetchone() is None:
                    break
                else:
                    #Displays error if product already exists in the database
                    print("\nThis ID already exists. Please enter a different ID.")
            except ValueError:
                print("\nInvalid input. Please enter a valid integer for the product ID.")

        while True:
            name = input("\nEnter new product name: ").strip()
            if name.isdigit():
                print("\nInvalid input. Please enter a valid string for the product name.")
                continue
            c.execute("SELECT * FROM PRODUCTS WHERE LOWER(NAME)=?", (name.lower(),))
            if c.fetchone() is None:
                break
            else:
                #Displays error if product already exists in the database
                print("\nThis product name already exists. Please enter a different product name.")

        while True:
            try:
                price = float(input("\nEnter new product price: ").replace(",", ""))
                break
            except ValueError:
                print("\nInvalid input. Please enter a valid float for the product price.")

        while True:
            try:
                quantity = int(input("\nEnter new product quantity: ").replace(",", ""))
                break
            except ValueError:
                print("\nInvalid input. Please enter a valid integer for the product quantity.")

        quality = input("\nEnter new product quality: ").strip()
        
        c.execute("INSERT INTO PRODUCTS (ID, NAME, PRICE, QUANTITY, QUALITY) VALUES (?, ?, ?, ?, ?)",
                  (product_id, name, price, quantity, quality))
        conn.commit()
        print("\nProduct added successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

#Allows user to find item based on ID or Name (is not case sensitive for "Name")
def display_find_data(conn):
    try:
        c = conn.cursor()
        while True:
            search_type = input("\nDo you want to search by ID or Name? (Enter 'ID' or 'Name'): ").strip().upper()
            if search_type == 'ID':
                try:
                    product_id = int(input("\nEnter the product ID: "))
                    c.execute("SELECT * FROM PRODUCTS WHERE ID=?", (product_id,))
                    record = c.fetchone()
                    if record:
                        print(f"\nProduct found: ID: {record[0]}, Name: {record[1]}, Price: {record[2]}, Quantity: {record[3]}, Quality: {record[4]}")
                    else:
                        print(f"\nThe ID {product_id} is not in the database.")
                except ValueError:
                    print("\nPlease enter a valid numerical ID.")
                break
            elif search_type == 'NAME':
                product_name = input("\nEnter the product name: ").strip().title()
                c.execute("SELECT * FROM PRODUCTS WHERE LOWER(NAME)=?", (product_name.lower(),))
                record = c.fetchone()
                if record:
                    print(f"\nProduct found: ID: {record[0]}, Name: {record[1]}, Price: {record[2]}, Quantity: {record[3]}, Quality: {record[4]}")
                else:
                    print(f"\nThe item name '{product_name}' is not in the database.")
                break
            else:
                print("\nInvalid input. Please enter 'ID' or 'Name'.")
    except Exception as e:
        print(f"\nAn error occurred while searching for data: {e}.")

#Allows user to find an item based on ID or name to delete
def display_delete_data(conn):
    try:
        c = conn.cursor()
        search_type = input("\nDo you want to delete by ID or Name? (Enter 'ID' or 'Name'): ").strip().upper()
        
        if search_type == 'ID':
            product_id = int(input("\nEnter the product ID to delete: "))
            c.execute("SELECT * FROM PRODUCTS WHERE ID=?", (product_id,))
            record = c.fetchone()
            
            if record:
                #If the item exists, allows user to confirm delete
                print(f"\nProduct found: ID: {record[0]}, Name: {record[1]}, Price: {record[2]}, Quantity: {record[3]}, Quality: {record[4]}")
                confirm = input("\nAre you sure you want to delete this product? (Y/N): ").strip().upper()
                if confirm == 'Y':
                    c.execute("DELETE FROM PRODUCTS WHERE ID=?", (product_id,))
                    conn.commit()
                    print("\nProduct deleted successfully!")
                else:
                    print("\nDeletion cancelled!")
            else:
                print("\nProduct ID not found!")
        
        elif search_type == 'NAME':
            product_name = input("\nEnter the product name to delete: ").strip().title()
            c.execute("SELECT * FROM PRODUCTS WHERE LOWER(NAME)=?", (product_name.lower(),))
            record = c.fetchone()
            
            if record:
                print(f"\nProduct found: ID: {record[0]}, Name: {record[1]}, Price: {record[2]}, Quantity: {record[3]}, Quality: {record[4]}")
                confirm = input("\nAre you sure you want to delete this product? (Y/N): ").strip().upper()
                if confirm == 'Y':
                    c.execute("DELETE FROM PRODUCTS WHERE LOWER(NAME)=?", (product_name.lower(),))
                    conn.commit()
                    print("\nProduct deleted successfully!")
                else:
                    print("\nDeletion cancelled!")
            else:
                print("\nProduct name not found!")
        else:
            print("\nInvalid input. Please enter 'ID' or 'Name'.")
        
    except ValueError:
        print("\nPlease enter a valid input.")
    except Exception as e:
        print(f"\nAn error occurred while deleting data: {e}.")

#This method saves the updated data to the database so that while the program is still running, the file is updating properly
def save_to_database(data, filename):
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS PRODUCTS (ID INTEGER NOT NULL PRIMARY KEY, NAME VARCHAR(30), PRICE REAL, QUANTITY INTEGER, QUALITY VARCHAR(30))")
        c.executemany("INSERT INTO PRODUCTS (ID, NAME, PRICE, QUANTITY, QUALITY) VALUES (?, ?, ?, ?, ?)", [(d.id, d.name, d.price, d.quantity, d.quality) for d in data])
        conn.commit()
        conn.close()
        print(f"\nData saved to the database file {filename}.")
    except Exception as e:
        print(f"\nAn error occurred while saving to {filename}: {e}.")

def handle_filtered_data(filtered_data):
    if not filtered_data:
        print("\nNo results!")
    else:
        #Prints the data in a pretty format in the terminal while maintaining the format from the original SQL database
        for data in filtered_data:
            print(data)

#Calls the main function
if __name__ == "__main__":
    main()