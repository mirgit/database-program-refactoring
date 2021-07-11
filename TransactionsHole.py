from itertools import combinations

from Transactions import Insert, Update, Filter, Project, Delete


#### project(['name','Id'],select('name'=='mammad',teacher*student))
from Utils import Hole


class InsertHole:  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        self.join_chain = join_chain.infer()
        self.values = attr_infer(self.values)
        self.holes = self.join_chain.holes + self.values.holes

    def fill(self, holes_value):
        J = self.join_chain.fill(holes_value)
        V = self.values.fill(holes_value)
        return Insert(J, V)

    def infer(self):
        return self

class UpdateHole:  # upd(j,phi,attr,val)
    def __init__(self, join_chain, predicate, attr, values):
        self.join_chain = join_chain.infer()#!!!!!!!!!!
        self.predicate = predicate.infer()
        self.attr = attr_infer(attr)
        self.values = values
        self.holes = self.join_chain.holes + self.predicate.holes + self.attr.holes

    def fill(self, holes_value):
        J = self.join_chain.fill(holes_value)
        P = self.predicate.fill(holes_value)
        attr = attr_fill(self.attr)
        return Update(J, P, attr, self.values)

    def infer(self):
        return self
    # def infer(self):
    #     jc = self.join_chain.infer()
    #     pred = self.predicate.infer()
    #     attr = attr_infer(self.attr)# !!!!!!! phi?
    #     return Update(jc,pred,attr,self.values)


class DeleteHole:  # del(tables,j,phi)
    def __init__(self, tablelist, join_chain, predicate):
        self.join_chain = join_chain.infer()###!!!!!!!!!!! بابا l رو بده بهش یه جوری اقلا:/
        self.predicate = predicate.infer()
        self.holes = self.join_chain.holes + self.predicate.holes
        tablelist_options = [list(i) for r in range(1, len(self.join_chain) + 1) for i in combinations(self.join_chain, r)]
        self.hole = Hole(len(self.holes), tablelist_options)
        self.holes.append(self.hole)

    def fill(self, holes_value):
        L = holes_value[self.hole]####or ID?
        J = self.join_chain.fill(holes_value)
        P = self.predicate.fill(holes_value)
        return Delete(L, J, P)

    def infer(self):
        return self


class ProjectHole:  # proj(attrs, Q(j))
    def __init__(self, attrs, query):
        self.attrs = attr_infer(attrs)
        self.query = query.infer()
        self.holes = self.attrs.holes + self.query.holes

    def fill(self, holes_value):
        A = attr_fill(self.attrs)
        Q = self.query.fill()
        return Project(A, Q)

    def infer(self):
        return self


class FilterHole:  # filter(pred,Q)
    def __init__(self, predicate, query):
        self.query = query.infer()
        self.predicate = predicate.infer()
        self.holes = query.holes + self.predicate.holes

    def fill(self, holes_value):
        P = self.predicate.fill(holes_value)
        Q = self.query.fill(holes_value)
        return Filter(P, Q)

    def infer(self):
        return self
    #
    # def infer(self):
    #     pred = self.predicate.infer()
    #     query = self.query.infer()
    #     return Filter(pred, query)
    #
