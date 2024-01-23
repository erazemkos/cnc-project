import os
import sqlite3
from sqlite3 import Error

from constants import DATABASE_NAME, DATABASE_SETUP_SCRIPT


def execute_sql(conn, sql):
    """ Execute SQL statement """
    try:
        cursor = conn.cursor()
        cursor.executescript(sql)
    except Error as e:
        print(e)


def create_database():
    """ Deletes then creates the database specified by the database_schema.sql script """
    if not os.path.exists(DATABASE_SETUP_SCRIPT):
        print("Database script missing! Can't create the tables.")
        return

    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

    with open(DATABASE_SETUP_SCRIPT, 'r') as file:
        sql_script = file.read()

    # create a database connection
    conn = sqlite3.connect(DATABASE_NAME)

    # create tables
    if conn is not None:
        execute_sql(conn, sql_script)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    create_database()

