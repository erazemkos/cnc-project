import sqlite3
from sqlite3 import Error

DATABASE_SETUP_SCRIPT = "database_schema.sql"
DATABASE_NAME = "cnc_machining.db"

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def execute_sql(conn, sql):
    """ Execute SQL statement """
    try:
        cursor = conn.cursor()
        cursor.executescript(sql)
    except Error as e:
        print(e)

def main():
    with open(DATABASE_SETUP_SCRIPT, 'r') as file:
            sql_script = file.read()

    sql_create_tables = sql_script

    # create a database connection
    conn = sqlite3.connect(DATABASE_NAME)

    # create tables
    if conn is not None:
        execute_sql(conn, sql_create_tables)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

