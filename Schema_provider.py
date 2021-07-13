from Schema import Schema
from SqliteDB import SqliteDB
import re

from Table import Table

src = './benchmark/bench1/src-schema.txt'
tgt = './benchmark/bench1/tgt-schema.txt'


class SchemaProvider:
    def __init__(self, src_schema_file=src, tgt_schema_file=tgt):
        # self.src_db = SqliteDB("./src_db.sqlite")
        # self.tgt_db = SqliteDB("./tgt_db.sqlite")
        #
        # self.src_schema = Schema({})
        # self.tgt_schema = Schema({})
        
        with open(src_schema_file, "r") as f:
            file = f.read()
        src_queries = file.split(';')[:-1]
        schema,tables = self.create_tables(src_queries)#, self.src_db)#, self.src_schema)
        self.src_schema = Schema(schema,tables)

        with open(tgt_schema_file, "r") as f:
            file = f.read()
        tgt_queries = file.split(';')[:-1]
        schema, tables = self.create_tables(tgt_queries)#, self.src_db)#, self.src_schema)
        self.tgt_schema = Schema(schema, tables)
        # text_file = open(tgt_schema_file, "r")
        # tgt_queries = text_file.read().replace('\n', ' ')
        # tgt_queries = re.sub('\s+',' ',tgt_queries).split(';')
        # if tgt_queries[-1] == ' ':
        #     del tgt_queries[-1]
        #
        # text_file.close()
        # self.create_tables(tgt_queries, self.tgt_db, self.tgt_schema)

        
    def create_tables(self, table_queries):#, db, schema):
        schema = {}
        for q in table_queries:
            # db.execute_query(q)
            # if q[-1] == ' ':
            #     print("yredjtyhfhhh")
            #     del q[-1]
            table_info = self.parse_table(q)
            table = Table(table_info['name'], table_info['columns'], table_info['primaryKey'], table_info['foreignKeys'])
            schema[table_info['name']] = {i[0]: i[1] for i in table_info['columns']}
            # for s[table.name] = table.columns
            # schema.tables.append(table)

        return schema, table

    def parse_table(self, q):
        info = {}
        q = q.replace('CREATE TABLE','')
        b = q.find('(')
        q = [q[:b], q[b:]]
        Tname = q[0].strip()
        q = q[1][1:-2]
        q = [i.strip() for i in q.split(',')]
        FK = {}
        cols = []
        for line in q:
            if line.find('FOREIGN KEY') != -1:
                line = line.replace('FOREIGN KEY','')
                line = line.replace('REFERENCES ','')
                line = line.split('(')
                thisKey = line[1].split(')')[0].strip()
                Fname = line[1].split(')')[1].strip()
                Fkey = line[2][:-1].strip()
                FK[(Tname,thisKey)] =(Fname,Fkey)
            elif line.find('PRIMARY KEY') != -1:
                PK = line.split('(')[1][:-1]
            else:
                n,t = [i.strip() for i in line.split()]
                cols.append((n,t))
        info['name'] = Tname
        info['columns'] = cols
        info['primaryKey'] = PK
        info['foreignKeys'] = FK
        return info
s = SchemaProvider()