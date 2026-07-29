import mysql.connector

# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rocketsql12!"
)

cursor = connection.cursor()
cursor.execute("USE libraryDB");

print("Connected to MySQL!")
print("Type SQL commands. Type 'exit' to quit.")

while True:
    command = input("SQL> ")

    if command.lower() == "exit":
        break

    try:
        cursor.execute(command)

        # If the command returns data (SELECT)
        if cursor.description:
            results = cursor.fetchall()

            for row in results:
                print(row)

        else:
            connection.commit()
            print("Query executed successfully.")

    except Exception as e:
        print("Error:", e)


cursor.close()
connection.close()

print("Disconnected.")