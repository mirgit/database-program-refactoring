'''/**
 * The definition of a table in a schema.
 */'''
class Table:
    '''/**
     * Constructs the definition of a table with the given name
     * and columns with the given primary and foreign keys.
     *
     * @param name        the name of the table 
     * @param columns     the columns in the table -- list of tuple (col_name, col_type)
     * @param primaryKey  the primary key of the table -- string
     * @param foreignKeys Dict {(src_table_name, src_col_name): (dest_table_name, dest_col_name)}
     */'''
    def __init__( self, name, columns, primaryKey, foreignKeys):
        self.name = name;
        self.columns = columns;
        self.primaryKey = primaryKey;
        self.foreignKeys = foreignKeys;


    def __str__(self) :
        return " ".format("TableDef(%s, %s, %s, %s)", self.name, self.columns, self.primaryKey, self.foreignKeys)
