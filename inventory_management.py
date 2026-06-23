import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

conn.commit()


def add_product():
    name = input("Product Name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))

    cursor.execute("""
    INSERT INTO products(name, quantity, price)
    VALUES (?, ?, ?)
    """, (name, quantity, price))

    conn.commit()
    print("Product Added Successfully")


def view_products():

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    print("\n===== Inventory =====")

    for p in products:
        print(
            f"ID:{p[0]} | "
            f"Name:{p[1]} | "
            f"Qty:{p[2]} | "
            f"Price:₹{p[3]}"
        )


def update_stock():

    pid = int(input("Product ID: "))
    qty = int(input("New Quantity: "))

    cursor.execute("""
    UPDATE products
    SET quantity=?
    WHERE id=?
    """, (qty, pid))

    conn.commit()

    print("Stock Updated")


def delete_product():

    pid = int(input("Product ID: "))

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (pid,)
    )

    conn.commit()

    print("Product Deleted")


def low_stock():

    cursor.execute("""
    SELECT * FROM products
    WHERE quantity < 10
    """)

    items = cursor.fetchall()

    print("\nLow Stock Products")

    for p in items:
        print(p)


while True:

    print("\n1.Add Product")
    print("2.View Products")
    print("3.Update Stock")
    print("4.Delete Product")
    print("5.Low Stock Report")
    print("6.Exit")

    choice = input("Choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        view_products()

    elif choice == "3":
        update_stock()

    elif choice == "4":
        delete_product()

    elif choice == "5":
        low_stock()

    elif choice == "6":
        break

    else:
        print("Invalid Choice")

conn.close()
