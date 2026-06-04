import mysql.connector

# Connect to MySQL Database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Samadhan@2141",
    database="smart_retail_system"
)

print("Database Connected Successfully 😄")

cursor = connection.cursor()

# Fetch products data
cursor.execute("SELECT * FROM products")

result = cursor.fetchall()

for row in result:
    print(row)

connection.close()