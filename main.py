import mysql.connector

# Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Samadhan@21416",
    database="smart_retail_system"
)

cursor = connection.cursor()


# View Products
def view_products():
    query = "SELECT * FROM products"
    cursor.execute(query)

    products = cursor.fetchall()

    print("\n📦 Product List:\n")

    for product in products:
        print(product)


# Add Product
def add_product():
    name = input("Enter Product Name: ")
    category = input("Enter Category: ")
    price = float(input("Enter Price: "))
    stock = int(input("Enter Stock Quantity: "))
    supplier_id = int(input("Enter Supplier ID: "))

    query = """
    INSERT INTO products
    (product_name, category, price, stock_quantity, supplier_id)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (name, category, price, stock, supplier_id)

    cursor.execute(query, values)
    connection.commit()

    print("✅ Product Added Successfully!")


# Search Product
def search_product():
    product_name = input("Enter Product Name: ")

    query = """
    SELECT * FROM products
    WHERE product_name = %s
    """

    cursor.execute(query, (product_name,))
    result = cursor.fetchall()

    if result:
        print("\n🔍 Product Found:\n")

        for row in result:
            print(row)

    else:
        print("❌ Product Not Found")


# Delete Product
def delete_product():
    try:
        product_id = int(input("Enter Product ID to Delete: "))

        query = "DELETE FROM products WHERE product_id = %s"

        cursor.execute(query, (product_id,))
        connection.commit()

        print("🗑️ Product Deleted Successfully!")

    except mysql.connector.Error:
        print("❌ Cannot delete product because it is linked to orders.")


# Update Product
def update_product():
    try:
        product_id = int(input("Enter Product ID to Update: "))
        new_price = float(input("Enter New Price: "))
        new_stock = int(input("Enter New Stock Quantity: "))

        query = """
        UPDATE products
        SET price = %s,
            stock_quantity = %s
        WHERE product_id = %s
        """

        values = (new_price, new_stock, product_id)

        cursor.execute(query, values)
        connection.commit()

        print("✏️ Product Updated Successfully!")

    except ValueError:
        print("❌ Please enter numbers only.")


# Product Statistics Dashboard
def product_statistics():

    # Total Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total Stock
    cursor.execute("SELECT SUM(stock_quantity) FROM products")
    total_stock = cursor.fetchone()[0]

    # Average Price
    cursor.execute("SELECT AVG(price) FROM products")
    avg_price = cursor.fetchone()[0]

    # Most Expensive Product
    cursor.execute("""
        SELECT product_name, price
        FROM products
        ORDER BY price DESC
        LIMIT 1
    """)

    expensive_product = cursor.fetchone()

    print("\n📊 PRODUCT STATISTICS DASHBOARD\n")
    print(f"📦 Total Products: {total_products}")
    print(f"📦 Total Stock: {total_stock}")
    print(f"💰 Average Price: ₹{avg_price:.2f}")
    print(
        f"🏆 Most Expensive Product: "
        f"{expensive_product[0]} (₹{expensive_product[1]})"
    )


# Menu
print("\n🛒 SMART RETAIL SYSTEM\n")
print("1. View Products")
print("2. Add Product")
print("3. Search Product")
print("4. Delete Product")
print("5. Update Product")
print("6. Product Statistics")

choice = input("Enter Choice: ")

if choice == "1":
    view_products()

elif choice == "2":
    add_product()

elif choice == "3":
    search_product()

elif choice == "4":
    delete_product()

elif choice == "5":
    update_product()

elif choice == "6":
    product_statistics()

else:
    print("❌ Invalid Choice")

connection.close()