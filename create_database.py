import mysql.connector
from settings import passwd, host, user, database

mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=passwd,
    database=database
)
# Create a cursor and initialize it
my_cursor = mydb.cursor()
# Create a Database
my_cursor.execute("CREATE DATABASE IF NOT EXISTS PMS")

# Create a table
my_cursor.execute("CREATE TABLE IF NOT EXISTS users (application VARCHAR(255), \
                username VARCHAR(255), \
                password VARCHAR(255), \
                key_string VARCHAR(255), \
                addedby INT, \
                user_id INT AUTO_INCREMENT PRIMARY KEY)")

# my_cursor.execute("DROP TABLE users")

my_cursor.execute("CREATE TABLE IF NOT EXISTS complexity (uppercase int, \
                lowercase int, \
                symbols int, \
                numbers int, \
                complexity_id INT AUTO_INCREMENT PRIMARY KEY)")
# Create application_users table
my_cursor.execute("CREATE TABLE IF NOT EXISTS application_users (username VARCHAR(255) UNIQUE, \
                password VARCHAR(255), \
                role int, \
                username_id INT AUTO_INCREMENT PRIMARY KEY)")
