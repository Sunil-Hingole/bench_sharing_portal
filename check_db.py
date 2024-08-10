import sqlite3

# Connect to the database
conn = sqlite3.connect('site.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a simple query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch and print the results
tables = cursor.fetchall()
for table in tables:
    print(table)

# Close the connection
conn.close()
