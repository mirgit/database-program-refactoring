class Schema:
    def __init__(self, s, tables=[]):
        self.schema = s
        self.cols = {x: self.schema[t][x] for t in self.schema for x in self.schema[t]}
        self.attr2id = {c: i+1 for i, c in enumerate(self.cols)}
        self.id2attr = {self.attr2id[c]: c for c in self.attr2id}
        self.tables = tables
        self.name2table = {table.name: table for table in tables}

    def __str__(self):
        return "".format("SchemaDef(%s)", self.tables)

    def get_table(self,table_name):
        for t in self.tables:
            if t.name == table_name:
                return t

    def name_to_id(self, a):  # if not exist...!!!!!!!!
        return self.attr2id[a]

    def id_to_name(self, a):  # if not exist...!!!!!!!!
        return self.id2attr[a]

    def id_to_type(self, a):  # if not exist...!!!!!!!!
        return self.cols[self.id2attr[a]]

    def size(self):
        return len(self.attr2id)

    def add_table(self, table):
        self.tables.append(table)
        self.name2table[table.name] = table
