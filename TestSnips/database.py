import sqlite3

connection = sqlite3.connect("Z:\\PSG\\FYear Project\\Project\\Flask Web App\\Website\\employee.db", check_same_thread=False)
print("qwerty")

try:
    cursor  = connection.cursor()

    # query = '''CREATE TABLE IF NOT EXISTS ADMIN_PLAN(FROM_DATE VARCHAR(255) NOT NULL, TO_DATE VARCHAR(255) NOT NULL,
    #                                             PROJECT VARCHAR(255) NOT NULL, FIELD_OF_WORK VARCHAR(255) NOT NULL,
    #                                             SECTION VARCHAR(255) NOT NULL, TOTAL_MAN_HOURS INT, PROGRESS VARCHAR(255), ASSIGNED_TO VARCHAR(255) NOT NULL,
    #                                             COMMENTS VARCHAR(255)); '''
    # cursor.execute(query)
    # connection.commit()
    # print("Table Done")

    list = ['']

    connection.close()
except sqlite3.Error:
    print(sqlite3.Error)