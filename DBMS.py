import mysql.connector
from tabulate import tabulate
import os



# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rocketsql12!"
)
cursor = connection.cursor()
cursor.execute("USE libraryDB")


# is this okay to keep or should i make this dictionary from our DB?
criteria = {"1": "book_id",
        "2": "title",
        "3": "author",
        "4": "genre"
    }

def browse_books(search_type = "all", search_id = "all", avail_type = "all", avail_id = "all"):

# what to do if no books are found?

    # view all books
    if search_type == "all" and avail_type == "all":
        command = "SELECT * FROM books"
    # view specific books based on a search menu
    elif avail_type == "all":
        command = f"SELECT * FROM books WHERE {search_type} LIKE '%{search_id}%'"
    # view available books at a specific library
    elif search_type == "all":
         command = f"SELECT b.* \
                    FROM books AS b \
                    JOIN available_books AS a\
                    ON b.book_id = a.book_id\
                    WHERE {avail_type} = '{avail_id}'"
    else:
        # not used yet, needed for checkout?
        command = f"SELECT b.* AND a.city AND a.name \
                    FROM books AS b \
                    JOIN available_books AS a\
                    ON b.book_id = a.book_id\
                    WHERE b.{search_type} LIKE '%{search_id}% AND {avail_type} = '{avail_id}'"
        
    try:
        cursor.execute(command)
        if cursor.description:
            results = cursor.fetchall()

            headers = [column[0] for column in cursor.description]

            print(tabulate(results, headers=headers, tablefmt="grid"))

        
        #     results = cursor.fetchall()
        #     for row in results:
        #         print(f"""
        #             # Book ID: {row[0]}
        #             # Title: {row[1]}
        #             # Author: {row[2]}
        #             # Published: {row[3]}
        #             # Genre: {row[4]}
        #             # ------------------------
        #             # """)

        else:
            connection.commit()
            print("Query executed successfully.")
    except Exception as e:
        print("Error:", e)
    
    


# missing AC 02.4 (you skipped 3?)
def search_books():

    print("""
╔══════════════════════════════════════╗
║            🔎 Search Books           ║
║              Search By               ║
╠══════════════════════════════════════╣
║  1.) By ID                           ║
║  2.) By Title                        ║
║  3.) By Author                       ║
║  4.) By Genre                        ║
║                                      ║
║  5.) return to main menu             ║
╚══════════════════════════════════════╝
""")
    user_choice = input("Choose criteria for searching (1-4): ")

    if user_choice not in criteria and user_choice != "5":
        print("Invalid choice.")
        user_choice = input("Press Enter to continue...")
        os.system('cls')
        search_books()
        return

    if user_choice == "5":
        return

    os.system('cls')
    search_by = input(f"Enter the {criteria[user_choice]} of the books you're looking for: ")

    
    os.system('cls')
    print(f"""
        ╔══════════════════════════════════════════╗
        ║              SEARCH RESULTS              ║
        ╚══════════════════════════════════════════╝
        """)
    print(f"Books where {criteria[user_choice]} contains '{search_by}':\n")
    # print(f"Results for books with {criteria[user_choice]} including '{search_by}'")
    browse_books(criteria[user_choice], search_by)
    user_choice = input("Press Enter to continue...")
    os.system('cls')





def view_book_availability():
    # Implementation for viewing book availability
    print("""
╔══════════════════════════════════════╗
║          📚 Book Availability        ║
║              Options                 ║
╠══════════════════════════════════════╣
║  1.) View Library Inventory          ║
║  2.) View Specific Book Availability ║
╚══════════════════════════════════════╝
""")

    user_choice = input("Select an option (1-2): ")
    os.system('cls')

    match user_choice:
        case "1":
            # Implementation for viewing library inventory
            try:
                cursor.execute("SELECT * FROM Libraries")
                if cursor.description:
                    results = cursor.fetchall()
                    headers = [column[0] for column in cursor.description]
                    print(tabulate(results, headers=headers, tablefmt="grid"))

                else:
                    connection.commit()
                    print("Query executed successfully.")

            except Exception as e:
                print("Error:", e)

            user_choice = input("please select the ID of a library above: ")
            os.system('cls')


            try:
                cursor.execute("SELECT title FROM books WHERE book_id = %s", (user_choice,))
                result = cursor.fetchone()
                
                print(f"\n\nLibraries that have '{result[0]}':\n")

                cursor.execute("SELECT b.* \
                                FROM books AS b  \
                                INNER JOIN availability as a \
                                ON b.book_id = a.book_id \
                                WHERE a.library_id = %s", (user_choice,))
                
                if cursor.description:
                    results = cursor.fetchall()
                    headers = [column[0] for column in cursor.description]
                    print(tabulate(results, headers=headers, tablefmt="grid"))

                else:
                    connection.commit()
                    print("Query executed successfully.")

            except Exception as e:
                print("Error:", e)


        case "2":
            print("(enter menu to go back to main menu)")
            browse_books()
            # Implementation for viewing specific book availability
            
            user_choice = input("enter the book ID you are looking for: ")
            os.system('cls')
            try:
                cursor.execute("SELECT title FROM books WHERE book_id = %s", (user_choice,))
                result = cursor.fetchone()

                print(f"\n\nLibraries that have '{result[0]}':\n")
            
                cursor.execute("SELECT l.city, l.name \
                                FROM libraries AS l  \
                                INNER JOIN availability as a \
                                ON l.library_id = a.library_id \
                                WHERE a.book_id = %s", (user_choice,))
                
                if cursor.description:
                    results = cursor.fetchall()
                    headers = [column[0] for column in cursor.description]
                    print(tabulate(results, headers=headers, tablefmt="grid"))

                else:
                    connection.commit()
                    print("Query executed successfully.")

            except Exception as e:
                print("Error:", e)


def checkout():
    print("To checkout a book, please enter the following information:")
    user_fname = input("Enter your first name: ")
    user_lname = input("Enter your last name: ")
    book_id = input("Enter the book ID you are looking for: ")
    library_id = input("Enter the library ID where you want to check out the book: ")

    try:
        cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
        
        s = input("Press e...")
        book_name = cursor.fetchone()
        
        s = input("Press e...")
        cursor.execute("SELECT city, name FROM libraries WHERE library_id = %s", (library_id,))
        
        s = input("Press e...")
        library_info = cursor.fetchone()
        
        s = input("Press e...")

        print(f"\n\nchecking out '{book_name}' from '{library_info[0]}, {library_info[1]}':\n")

        s = input("Press e...")
        

        cursor.execute("""
            DELETE FROM availability
            WHERE library_id = %s
            AND book_id = %s
        """, (library_id, book_id))

        s = input("Press e...")


        if cursor.rowcount == 0:
            s = input("Your book does not exist in the specified library.")
            return
        
     
        s = input("Book updated successfully.")


        cursor.execute("""
            INSERT INTO users (fname, lname)
            VALUES (%s, %s);
        """, (user_fname, user_lname))
        

        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO checkouts (book_id, user_id, lib_id, checkout_date, due_date)
            VALUES (%s, %s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 2 MONTH));
        """, (book_id, user_id, library_id, ))
        connection.commit()

    except Exception as e:
        
        print("Error:", e)
        s = input("Press Enter fdfdfdfdfto asdfasdfsafcontinue...")



# -----------------------------------------------
# -----------------------------------------------
# -----------------------------------------------



print("Connected to MySQL!")

os.system('cls')

print("\n\n\n\n-------------------------------------------------------")
print("\tWelcome to the Fake Library Association")
print("-------------------------------------------------------\n")

while True:
    # print("Please Choose an Option Below (ex.1,2,3,4)\n")
    # print("1.) Browse All Books")
    # print("2.) Search for a Book")
    # print("3.) View Book Location Availability")
    # print("4.) Exit\n")

    print("""
╔══════════════════════════════════════╗
║          📚 Library Database         ║
║              Main Menu               ║
╠══════════════════════════════════════╣
║  1.) Browse All Books                ║
║  2.) Search for a Book               ║
║  3.) View Book Location Availability ║
║  4.) Check Out a Book                ║
║                                      ║
║  5.) Exit                            ║
╚══════════════════════════════════════╝
""")

    user_choice = input("Select an option (1-5): ")
    
    os.system('cls')
    match user_choice :
        case "1":
            browse_books()
            user_choice = input("Press Enter to continue...")
        case "2":
            search_books()
        case "3":
            view_book_availability()
            user_choice = input("Press Enter to continue...")
        case "4":
            checkout()
        case "5":
            break
        case _:
            print("Invalid Option")
            user_choice = input("Press Enter to continue...")

    os.system('cls')

cursor.close()
connection.close()

print("Disconnected.")

