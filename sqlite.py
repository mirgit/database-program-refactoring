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
INSERT INTO
  MEMBER (mname, afk)
VALUES
  ('James', 1),
  ('Leila', 5),
  ('Brigitte', 3),
  ('Mike', 2),
  ('Elizabeth', 2);
"""

q = """
    SELECT address, city, state, zipcode, aid FROM MEMBER NATURAL JOIN ADDRESS  WHERE mname = 'Elizabeth';
"""
connection = create_connection("./test_app.sqlite")
# execute_query(connection, create_users_table)  
# execute_query(connection, ADDRESS)  
# execute_query(connection, add_addr)  
# execute_query(connection, add_users)  
d = execute_read_query(connection, q)
print(d)