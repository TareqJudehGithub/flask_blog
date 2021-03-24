# import mysql.connector
#
# my_db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="pass123"
# )
#
# my_cursor = my_db.cursor()
# my_cursor.execute("CREATE DATABASE mysqlusers")
# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)