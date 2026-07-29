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

def browse_books(type = "all", search_by = "all", avail_loc_id = "all"):

# what to do if no books are found?


    if type == "all" and avail_loc_id == "all":
        command = "SELECT * FROM books"
    elif avail_loc_id == "all":
        command = f"SELECT * FROM books WHERE {type} LIKE '%{search_by}%'"
    else:
        command = f"SELECT b.* \
                    FROM books AS b \
                    JOIN availabile_books AS a\
                    ON b.book_id = a.book_id\
                    WHERE b.{type} LIKE '%{search_by}% AND a.location_id = '{avail_loc_id}'"
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
    user_choice = input("Press Enter to continue...")
    os.system('cls')



def search_books():

    print("Type 'menu' to go back to the main menu\n")
    print("1.) By ID\n2.) By Title\n3.) By Author\n4.) By Genre\n")
    user_choice = input("Choose criteria for searching (1-4):")

    if user_choice not in criteria and user_choice != "menu":
        print("Invalid choice.")
        user_choice = input("Press Enter to continue...")
        search_books()
        return

    if user_choice == "menu":
        return
    
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

    search_books()



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
║  4.) Exit                            ║
╚══════════════════════════════════════╝
""")

    user_choice = input("Select an option (1-4): ")
    
    os.system('cls')
    match user_choice :
        case "1":
            browse_books()
        case "2":
            search_books()
        case "3":
            # view_book_availability()
            user_choice = input("Press Enter to continue...")
        case "4":
            break
        case _:
            print("Invalid Option")
            user_choice = input("Press Enter to continue...")

    os.system('cls')

cursor.close()
connection.close()

print("Disconnected.")