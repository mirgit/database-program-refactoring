import sqlite3
from sqlite3 import Error
import logging


class SqliteDB:
    def __init__(self, db_name):
        self.db = self.create_connection(db_name)

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            logging.error(f"The error '{e}' occurred")

        return connection

    def execute_query(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(query)
            self.db.commit()
        except Error as e:
            pass

    def execute_read_query(self, query):
        cursor = self.db.cursor()
        result = None
        try:
            # print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            return []

    def create_tables(self, file_name):
        with open(file_name, 'r') as f:
            batch = f.read()
        for query in batch.split(';')[:-1]:
            self.execute_query(query+';')
