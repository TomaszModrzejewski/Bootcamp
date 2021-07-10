import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
       specified by db_file
   :return: Connection object or None
   """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn
