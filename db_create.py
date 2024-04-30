import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ghost25000$",
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()
# apres execution de db_create.py avce python db_create.py la premiere fois
# on desactive cette creatuion pour ne pas avoir a recreer la base de données un seconde fois

#my_cursor.execute("CREATE DATABASE our_users")
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)