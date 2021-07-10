from Transactions import Insert


class InsertHole:  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        self.join_chain = join_chain.infer()
        self.values = attr_infer(self.values)
        self.holes = join_chain.holes()+values.holes()

    def fill(self,holes_value):
        J = self.join_chain.fill(holes_value)
        V = self.values.fill(holes_value)
        return Insert(J, V)


class UpdateHole:  # upd(j,phi,attr,val)
    def __init__(self, join_chain, predicate, attr, values):
        self.join_chain = join_chain.infer()
        self.predicate = predicate.infer()
        self.attr = attr_infer(attr)
        self.values = values

    def fill(self,holes_value):
        J = self.join_chain.fill(holes_value)
        P = self.predicate.fill(holes_value)
        attr = attr_fill(self.attr)
        return Update(J, P, attr, self.values)

    def infer(self):
        jc = self.join_chain.infer()
        pred = self.predicate.infer()
        attr = attr_infer(self.attr)# !!!!!!! phi?
        return Update(jc,pred,attr,self.values)


class DeleteHole:  # del(tables,j,phi)
    def __init__(self, tablelist, join_chain, predicate):
        self.tablelist = tablelist
        self.join_chain = join_chain
        self.predicate = predicate
        hole = 0

    def infer(self):
        #!!!!!!!!!!!!!hole

class ProjectHole:  # proj(attrs, Q(j))
    def __init__(self, attrs, query):


class FilterHole:  # filter(phi,Q)
    def __init__(self, predicate, query):
        self.query = query.infer()
        self.predicate = predicate.infer()

    def fill(self,holes_value):
        

    def infer(self):
        pred = self.predicate.infer()
        query = self.query.infer()
        return Filter(pred, query)

