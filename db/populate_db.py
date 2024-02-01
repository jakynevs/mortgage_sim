import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn

def create_client(conn, client):
    sql = ''' INSERT INTO Client(name,dni,email,requested_capital)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, client)
    conn.commit()
    return cur.lastrowid

def main():
    database = "db/test_database.db"

    # Create a database connection
    conn = create_connection(database)

    # Test data for the Client table
    test_clients = [
        ('John Doe', '77654321L', 'john.doe@example.com', 25000.0),
        ('Jane Smith', '12345666W', 'jane.smith@example.com', 30000.0),
        # Add more test clients as needed
    ]

    # Insert test data into the table
    if conn is not None:
        for client in test_clients:
            create_client(conn, client)
        print("Test data has been inserted successfully.")
    else:
        print("Error! cannot create the database connection.")

    # Close the connection
    if conn:
        conn.close()

if __name__ == '__main__':
    main()
