from abc import ABC, abstractmethod


class Transaction(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def infer(self):
        pass

    @abstractmethod
    def run(self):
        pass


class UpdateTrans(Transaction):
    def __init__(self):
        Transaction.__init__(self)


class QueryTrans(Transaction):
    def __init__(self):
        Transaction.__init__(self)


class Insert(UpdateTrans):  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        UpdateTrans.__init__(self)
        self.join_chain = join_chain
        self.values = values

    def infer(self):
        join_chain = self.join_chain.infer()
        values = attr_infer(self.values)# !!!!!!! phi?
        return Insert(join_chain, values)


class Update(UpdateTrans):  # upd(j,phi,attr,val)
    def __init__(self, join_chain, predicate, attr, values):
        UpdateTrans.__init__(self)
        self.join_chain = join_chain
        self.predicate = predicate
        self.attr = attr
        self.values = values

    def infer(self):
        jc = self.join_chain.infer()
        pred = self.predicate.infer()
        attr = attr_infer(self.attr)# !!!!!!! phi?
        return Update(jc,pred,attr,self.values)


class Delete(UpdateTrans):  # del(tables,j,phi)
    def __init__(self, tablelist, join_chain, predicate):
        UpdateTrans.__init__(self)
        self.tablelist = tablelist
        self.join_chain = join_chain
        self.predicate = predicate

    def infer(self):
        #!!!!!!!!!!!!!hole

class Project(QueryTrans):  # proj(attrs, Q(j))
    def __init__(self, attrs, query):
        QueryTrans.__init__(self)


class Filter(QueryTrans):  # filter(phi,Q)
    def __init__(self, predicate, query):
        QueryTrans.__init__(self)
        self.query = query
        self.predicate = predicate

    def infer(self):
        pred = self.predicate.infer()
        query = self.query.infer()
        return Filter(pred, query)


###### باید بسازم توی اینیت یه نسخه از هر چیزیش نه؟