import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name=None):
    """
    Establish a connection to the MySQL database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if connection.is_connected():
            print("✅ Connection to MySQL was successful.")
    except Error as e:
        print(f"❌ The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    """
    Execute a single SQL query.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("✅ Query executed successfully.")
    except Error as e:
        print(f"❌ The error '{e}' occurred")

def fetch_query_results(connection, query):
    """
    Fetch results from a SELECT query.
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"❌ The error '{e}' occurred")
        return result


if __name__ == "__main__":
    # Update with your MySQL credentials
    host = "localhost"
    user = "root"
    password = "your_password"
    database = "test_db"

    # Create a connection
    conn = create_connection(host, user, password, database)

    if conn:
        # Example: Create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            age INT,
            PRIMARY KEY (id)
        );
        """
        execute_query(conn, create_table_query)

        # Example: Insert data
        insert_query = "INSERT INTO users (name, age) VALUES ('Alice', 25);"
        execute_query(conn, insert_query)

        # Example: Fetch data
        select_query = "SELECT * FROM users;"
        results = fetch_query_results(conn, select_query)
        for row in results:
            print(row)

        conn.close()
        print("🔒 Connection closed.")
