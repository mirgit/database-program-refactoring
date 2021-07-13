import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        
        
create_users_table = """
CREATE TABLE MEMBER (
    mid INT,
    mname VARCHAR,
    afk INT,
    FOREIGN KEY (afk) REFERENCES ADDRESS (aid),
    PRIMARY KEY (mid)
);
"""
ADDRESS = """
CREATE TABLE ADDRESS (
    aid INT,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zipcode VARCHAR,
    PRIMARY KEY (aid)
);
"""
add_addr = """
INSERT INTO
  ADDRESS (address,
city,
state,
zipcode)
VALUES
  ('James', '25', 'male', 'USA'),
  ('Leila', '32', 'female', 'France'),
  ('Brigitte', '35', 'female', 'England'),
  ('Mike', '40', 'male', 'Denmark'),
  ('Elizabeth', '21', 'female', 'Canada');
"""

add_users = """
    DELETE FROM MEMBER WHERE mname = 'Elizabeth';

"""

q = """
    SELECT address, city, state, zipcode, aid FROM MEMBER NATURAL JOIN ADDRESS  WHERE mname = 'Elizabeth';
"""
connection = create_connection("./test_app.sqlite")
# execute_query(connection, create_users_table)  
# execute_query(connection, ADDRESS)  
# execute_query(connection, add_addr)  
execute_query(connection, add_users)  
d = execute_read_query(connection, q)
print(d)

class Sqlite:
    def __init__(self):
        self.db = self.create_connection('./db.sqlite')
        self.db_prime = self.create_connection('./db_prime.sqlite')
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
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
            
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")


    def execute_read_query(self,query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
            
        