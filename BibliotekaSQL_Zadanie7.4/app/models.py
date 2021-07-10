import sqlite3
from app.conn_to_db import create_connection


class Books:
    def __init__(self):
        self.db_file = 'library.db'

    def execute_sql(self, sql, *args):
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        cur.execute(sql, *args)
        conn.commit()

    def create_table(self):
        sql = """
        -- books table
        CREATE TABLE IF NOT EXISTS books (
            id integer PRIMARY KEY,
            title text NOT NULL,
            author text,
            year text,
            genre text,
            done TEXT
        );
        """
        self.execute_sql(sql)

    def add_book(self, book):
        sql = '''INSERT INTO books(title, author, year, genre, done)
                 VALUES(?,?,?,?,?)'''
        self.execute_sql(sql, book)

    def select_all(self, table):
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows

    def select_book(self, table, **query):
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows

    def update(self, table, id, data):
        parameters = [f"{k} = ?" for k in data]
        parameters = ", ".join(parameters)
        values = tuple(v for v in data.values())
        values += (id,)

        sql = f''' UPDATE {table}
                 SET {parameters}
                 WHERE id = ?'''
        try:
            self.execute_sql(sql, values)
        except sqlite3.OperationalError as e:
            print(e)

    def delete_book(self, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        self.execute_sql(sql, values)


books = Books()
