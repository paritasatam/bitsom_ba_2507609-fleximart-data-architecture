import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="viditsql",
    database="fleximart",
    port=3306
)

cursor = conn.cursor()
cursor.execute("SELECT DATABASE();")
print("Connected. Current DB:", cursor.fetchone())

cursor.close()
conn.close()
print("Connection closed.")
