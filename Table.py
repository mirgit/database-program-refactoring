"""/**
 * The definition of a table in a schema.
 */"""


class Table:
    """/**
     * Constructs the definition of a table with the given name
     * and columns with the given primary and foreign keys.
     *
     * @param name        the name of the table
     * @param columns     the columns in the table -- list of tuple (col_name, col_type)
     * @param primaryKey  the primary key of the table -- string
     * @param foreignKeys Dict {(src_table_name, src_col_name): (dest_table_name, dest_col_name)}
     */"""
    def __init__(self, name, columns, primaryKey, foreignKeys):
        self.name = name
        self.columns = columns
        self.primaryKey = primaryKey
        self.foreignKeys = foreignKeys
        self.data = []

    def __str__(self) :
        return " ".format("TableDef(%s, %s, %s, %s)", self.name, self.columns, self.primaryKey, self.foreignKeys)

    def insert(self,row):  # row is dictionary of attrs:values
        if not self.primaryKey in row.keys():  # generate new primary key
            i = 0
            while i < len(self.columns):
                if self.columns[i][0] == self.primaryKey:
                    break
            max_prim_key = 0
            for r in self.data:
                max_prim_key = max(max_prim_key, r[i])
            row[self.primaryKey] = max_prim_key + 1
        new_row = []
        for col, t in self.columns:
            if col in row.keys():
                new_row.append(row[col])
            else:
                new_row.append(None)
        self.data.append(new_row)

    def delete(self, predicate):  # {a_i:v_i, ...}
        indices = {}
        for i in range(len(self.columns)):
            if self.columns[i][0] in predicate.keys():
                indices[self.columns[i][0]] = i
        for ind in range(len(self.data)):
            row = self.data[ind]
            match = True
            for attr in predicate.keys():
                if row[indices[attr]] != predicate[attr]:
                    match = False
            if match:
                del (self.data[ind])

    def update(self, predicate, values):  # predicate:{a_i:v_i, ...}, vals:{a_j:v_j, ...}
        indices = {}
        for i in range(len(self.columns)):
            if self.columns[i][0] in predicate.keys() or self.columns[i][0] in values.keys():
                indices[self.columns[i][0]] = i
        for ind in range(len(self.data)):
            row = self.data[ind]
            match = True
            for attr in predicate.keys():
                if row[indices[attr]] != predicate[attr]:
                    match = False
            if match:
                for attr in values.keys():
                    self.data[ind][attr] = values[attr]
