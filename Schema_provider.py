from Schema import Schema
from Table import Table

# src = './benchmarkss/bench1/src-schema.txt'
# tgt = './benchmarkss/bench1/tgt-schema.txt'


class SchemaProvider:
    def __init__(self, src_schema_file, tgt_schema_file):
        with open(src_schema_file, "r") as f:
            file = f.read()
        src_queries = file.split(';')[:-1]
        schema, tables = self.create_tables(src_queries)#, self.src_db)#, self.src_schema)
        self.src_schema = Schema(schema,tables)

        with open(tgt_schema_file, "r") as f:
            file = f.read()
        tgt_queries = file.split(';')[:-1]
        schema, tables = self.create_tables(tgt_queries)#, self.src_db)#, self.src_schema)
        self.tgt_schema = Schema(schema, tables)

    def create_tables(self, table_queries):#, db, schema):
        schema = {}
        tables = []
        for q in table_queries:

            table_info = self.parse_table(q)
            tables.append(Table(table_info['name'], table_info['columns'], table_info['primaryKey'], table_info['foreignKeys']))
            schema[table_info['name']] = {i[0]: i[1] for i in table_info['columns']}

        return schema, tables

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
                line = line.replace('FOREIGN KEY', '')
                line = line.replace('REFERENCES ', '')
                line = line.split('(')
                thisKey = line[1].split(')')[0].strip()
                Fname = line[1].split(')')[1].strip()
                Fkey = line[2][:-1].strip()
                FK[(Tname, Tname+'.'+thisKey)] = (Fname, Fname+'.'+Fkey)
            elif line.find('PRIMARY KEY') != -1:
                PK = line.split('(')[1][:-1]
            else:
                n, t = [i.strip() for i in line.split()]
                cols.append((Tname + "." + n, t))
        info['name'] = Tname
        info['columns'] = cols
        info['primaryKey'] = PK
        info['foreignKeys'] = FK
        return info
