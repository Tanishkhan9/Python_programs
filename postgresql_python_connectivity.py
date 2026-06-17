import psycopg2

try:
    # PostgreSQL Connection

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="your_password",
        port="5432"
    )

    print("Database Connected Successfully")

    cursor = conn.cursor()

    # Execute Query

    cursor.execute("SELECT version();")

    result = cursor.fetchone()

    print("PostgreSQL Version:")
    print(result)

    cursor.close()
    conn.close()

    print("Connection Closed")

except Exception as e:
    print("Error:", e)
