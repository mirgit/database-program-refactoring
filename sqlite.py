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

# q = """
#     SELECT address, city FROM MEMBER NATURAL JOIN ADDRESS  WHERE mname = 'Elizabeth';
# """
connection = create_connection("./test_app.sqlite")
# execute_query(connection, create_users_table)
# execute_query(connection, ADDRESS)
# execute_query(connection, add_addr)
# execute_query(connection, add_users)

def create_tables(connection,file_name):
    with open(file_name,'r') as f:
        batch = f.read()
    for query in batch.split(';')[:-1]:
        execute_read_query(connection,query+';')

def parse_program(file_path):
    with open(file_path,'r') as f:
        prog = f.read()
    clr1 = prog.split('}')
    clr2 = {clr1[ind].split('{')[0].strip(): clr1[ind].split('{')[1] for ind in range(len(clr1)-1)}
    program = {}#  return clr2 to have transaction type in the beginning
    for k in clr2:
        trans = clr2[k]
        k = k.split(' ')
        k = ' '.join(k[1:])
        name, params = k.split('(')
        params = params[:-1]
        params = params.split(',')
        program[name] = ({i.strip().split(' ')[1]:i.strip().split(' ')[0] for i in params}, trans)
    return program


def execute_query_batch(program, function_call):
    prog, params = function_call.split('(')
    params=params[:-1]
    params = params.split(',')
    program = program[prog]
    param_names = list(program[0].keys())
    parameters = {param_names[i]:params[i].strip() for i in range(len(params))}
    # print(program,'\n',parameters)
    program = program[1]
    for query in program.split(';')[:-1]:
        query = query.strip()
        # print(query)
        q1 = query.split("<")
        q2 = [q1[ind].split('>')[0] for ind in range(1,len(q1))]
        for p in q2:
            if p in parameters:
                query = query.replace('<'+p+'>', parameters[p])
            else:
                query = query.replace('<'+p+'>', '"N/A"')
        print(query,parameters,p)

        # print(query)
        # query.replace()
        print(execute_read_query(connection, query + ';'),'\n\n\n')
i=2
path = 'benchmarks/bench'+str(i)+'/src-prog.txt'
c = parse_program(path)
# [print(j,'\n',c[j]) for j in c]
create_tables(connection,'benchmarks/bench2/src-schema.txt')
execute_query_batch(c, 'createProject(1,"synthesis", "shabhaye bidar" )')
execute_query_batch(c, 'createEmployee(1,"Ahmad", "Home-street 4" )')
execute_query_batch(c, 'createAssignment(1, 1, 1)')
# #


####delete all tables
# q = """select 'drop table ' || name || ';' from sqlite_master
#     where type = 'table';"""
# d = execute_read_query(connection, q)
# print('d ===========',d)
# if len(d)>0:
#     for hmm in d:
#         dd = execute_read_query(connection, hmm[0])
#         print(dd)

# create_tables(connection,'benchmarks/bench3/tgt-schema.txt')
# create_tables(connection,'benchmarks/bench15/src-schema.txt')
# # q = """select name from sqlite_master where type = 'table';"""
# q = """select * from PROJ_EMP"""
# d = execute_read_query(connection, q)
# print(d)


q = """select 'drop table ' || name || ';' from sqlite_master
    where type = 'table';"""
# q = 'delete from where EMPLOYEE join PROJ_EMP on EMPLOYEE.eid = PROJ_EMP.eid_fk where eid = 3'
d = execute_read_query(connection, q)
print('d ===========',d)
if len(d)>0:
    for hmm in d:
        dd = execute_read_query(connection, hmm[0])
        print(dd)
























# find delete A,B FROM..
'''
# import sqlparse
# for i in range(1,21):
#     path = 'benchmarks/bench'+str(i)+'/src-prog.txt'
#     c = parse_program(path)
#     # [print(j,'\n',c[j]) for j in c]
#     # create_tables(connection,'benchmarks/bench2/src-schema.txt')
#     for ts in c:
#         qs = c[ts][1]
#         lqs = [i.strip() for i in qs.split(';')][:-1]
#         # print(lqs)
#         for line in lqs:
#             a = sqlparse.parse(line+';')[0]
#             # print(a,'\n\n\n')#[4].value.split(' '))
#             if a[0].value == 'DELETE':
#                 # print(a)
#                 if len(a[2].value.split(' '))>1:
#                 # [print(i.ttype, i) for i in a]
#                     print(i, a[2])
'''