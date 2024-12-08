import sqlite3

# Connect to the database (or create it if it doesn't exist)
connection = sqlite3.connect('employee.db', check_same_thread=False)
cursor = connection.cursor()

# Create FIELD_OF_WORK table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS FIELD_OF_WORK (
    Field_of_Work TEXT PRIMARY KEY
)
''')
connection.commit()

# Define the roles to be added
roles = [
    'Software Development',
    'Data Analysis',
    'Graphic Design',
    'Project Management',
    'Quality Assurance'
]

# Insert roles into the FIELD_OF_WORK table
cursor.executemany("INSERT OR IGNORE INTO FIELD_OF_WORK (Field_of_Work) VALUES (?)", [(role,) for role in roles])
connection.commit()

# Fetch and display all rows to confirm insertion
cursor.execute("SELECT * FROM FIELD_OF_WORK")
rows = cursor.fetchall()

print("Roles in FIELD_OF_WORK table:")
for row in rows:
    print(row[0])

# Close the connection
connection.close()