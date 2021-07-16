import sqlite3
from sqlite3 import Error

class SqliteDB:
    def __init__(self, db_name):
        self.db = self.create_connection(db_name)
        # TODO create tables from schema


    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def execute_query(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(query)
            self.db.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
            
        cursor = self.db.cursor()
        try:
            cursor.execute(query)
            self.db.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        cursor = self.db.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
            return []

    def create_tables(self, file_name):
        with open(file_name, 'r') as f:
            batch = f.read()
        for query in batch.split(';')[:-1]:
            self.execute_read_query(query+';')
