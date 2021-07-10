class Insert:  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        self.join_chain = join_chain
        self.values = values

    def run(self, database):
        for table in self.join_chain:
            database[table].insert(self.values)


class Update:  # upd(j,pred,attr,val)
    def __init__(self, join_chain, predicate, attr, values):
        self.join_chain = join_chain
        self.predicate = predicate
        self.attr = attr
        self.values = values

    def run(self, database):
        for table in self.join_chain:
            database[table].update(self.predicate,self.attr,self.values)


class Delete:  # del(tables,j,phi)
    def __init__(self, tablelist, join_chain, predicate):
        self.tablelist = tablelist
        self.join_chain = join_chain
        self.predicate = predicate

    def run(self, database):
        for table in self.tablelist:
            database[table].delete()

class Project:  # proj(attrs, Q(j))
    def __init__(self, attrs, query):


class Filter:  # filter(phi,Q)
    def __init__(self, predicate, query):
        self.query = query
        self.predicate = predicate

    def infer(self):
        pred = self.predicate.infer()
        query = self.query.infer()
        return Filter(pred, query)

