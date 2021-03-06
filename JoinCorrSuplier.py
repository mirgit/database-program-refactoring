from Graph import *


class JoinCorrSupplier:
    def __init__(self, srcSchema, tgtSchema):
        self.srcSchema = srcSchema 
        self.tgtSchema = tgtSchema 
        assert self.srcSchema is not None and self.tgtSchema is not None 
        self.tableToVertices = {}
        self.vertexToTable = {}
        self.tableToComponents = {}
        self.buildTargetSchemaGraph() 

    def buildTargetSchemaGraph(self):
        # vertex data: table name, edge data: foreign key
        graph = Graph()
        # create a vertex for each table
        for table in self.tgtSchema.tables:#.values():
            tableName = table.name 
            vertex = graph.addVertex(tableName) 
            self.tableToVertices[tableName] = vertex
            self.vertexToTable[vertex] = table
        # create an edge for each foreign key
        for table in self.tgtSchema.tables:
            for src, dest in table.foreignKeys.items():
                ref_table = self.tableToVertices[dest[0]]
                fk_table = self.tableToVertices[src[0]]
                if fk_table is None or ref_table is None:
                    raise Exception("Cannot find dest or ref vertex") 
        
                graph.addEdge(fk_table, ref_table, (src[1], dest[1]))
                
        # decompose to connected components and update the map
        components = graph.connectedComponents() 
        for component in components:
            for vertex in component:
                tableName = vertex.val 
                if tableName in self.tableToComponents:
                    raise Exception("Overlapped components") 
                self.tableToComponents[tableName] = component
                
    def getJoinChains(self, valueCorr, chain):
        columns = []
        for t in chain:
            columns += [col[0] for col in t.columns]
        return self.getJoinChainsForColumns(valueCorr, chain, columns)

    def getJoinChainsForColumns(self, valueCorr, chain, columns):
        tableNames = self.tablesMappedTo(valueCorr, columns)
        if len(tableNames) == 1:
            return [[(t, None) for t in self.tgtSchema.tables if t.name in tableNames]]
        else:
            join_chain = self.getJoinChainsForTables(tableNames)
            ret_jc = []
            for jc in join_chain:
                tmp_jc = []
                for chain in jc:
                    edge_fk = None
                    if chain[1] is not None:
                        edge_fk = chain[1].on
                    jc2 = (self.vertexToTable[chain[0]], edge_fk)
                    tmp_jc.append(jc2)
                ret_jc.append(tmp_jc)

            return ret_jc

    def getJoinChainsForTables(self, tableNames):
        component = self.tableToComponents[tableNames[0]]
        joinVertices = [self.tableToVertices[t] for t in tableNames]
        for tableName in tableNames:
            #  directly compare the address
            if (self.tableToComponents[tableName] != component):
                raise Exception("Target tables cannot join together")
            
        # collect all join chains
        g = Graph(component)
        subgraphs = g.createAllSubgraphs(joinVertices)
        ret = set()
        for sg in subgraphs:
            joinChain = sg.getSpaning()
            if len(joinChain) > 0:
                ret.add(tuple(joinChain))
        return list(map(list, ret))

    def tablesMappedTo(self, value_corr, columns):
        tables = set()
        for col in columns:
            corr_col = value_corr[col]
            for col2 in corr_col:
                tables.add(col2[:col2.index('.')])
        return list(tables)
