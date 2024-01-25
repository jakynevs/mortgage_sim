import sqlite3
from sqlite3 import Error

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("db/mortgage.db")
    except Error as e:
        print(e)
    return conn

# Remove this?
# if __name__ == '__main__':
#     create_connection('db/mortgage.db')

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def main():
    database = "db/mortgage.db"

    # Check what can be null
    # Check what are the best data types   
    sql_create_clients_table = """ CREATE TABLE IF NOT EXISTS Client (
                      client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      dni TEXT UNIQUE NOT NULL,
                      email TEXT,
                      requested_capital DECIMAL);
                      """

    sql_create_mortgage_sim_table = """ CREATE TABLE IF NOT EXISTS MortgageSimulation (
                      mortgage_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      client_id INTEGER NOT NULL,
                      tae DECIMAL NOT NULL,
                      repayment_term INTEGER NOT NULL,
                      monthly_instalment DECIMAL NOT NULL,
                      total DECIMAL NOT NULL,
                      FOREIGN KEY (client_id) REFERENCES Client (id)
                      );"""
    
    # Create the db connection
    conn = create_connection(database)

    # Create the db tables
    if conn is not None:
        # Create client table
        create_table(conn, sql_create_clients_table)
        # Create mortgage table
        create_table(conn, sql_create_mortgage_sim_table)
    
    else:
        print("Error, cannot create db connection.")

if __name__ == '__main__':
    main()