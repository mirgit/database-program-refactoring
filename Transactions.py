# from itertools import combinations
# project(['name','Id'],select('name'=='mammad',teacher*student))
from Utils import JoinChain, Predicate

#
# class Hole:
#     def __init__(self, hid, options):
#         self.hid = hid
#         self.options = options

    # def infer(self):
    #     pass#!!!!!!!!!!!!!!!!!!!!!!!!


# def fill_val(phi, attr):
#     return phi[attr]


# def attr_infer(phi, attr):
#     # holes = []
#     #     holes.append(Hole(id,))
#     return phi[attr]

class Insert:  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        # if isinstance(join_chain, JoinChain):
        self.join_chain = join_chain
        # else:
        #     self.join_chain = JoinChain(join_chain)
        self.values = values
        self.holes = []
        self.tgt_transaction = None
        # self.chosen_join_chain = None
        # self.chosen_values = None
        # self.holes_id = 0
    # def Holer(self):
    #     return InsertHole(self.join_chain,self.values)

    def genSketch(self, phi, join_corr_supplier):
        tables = [join_corr_supplier.srcSchema.get_table(t) for t in self.join_chain]
        self.join_chain = JoinChain(tables)
        self.holes.append(self.join_chain.genSketch(phi, join_corr_supplier))
        sk_values = {}
        for a in self.values:
            self.holes.append(phi[a])
            # self.sk_values[h.hid] = self.values[a]
        return self.holes #, self.holes_id+len(self.holes)

    def fill(self, holes_value):
        JC = self.join_chain.fill(holes_value)
        holes_value.pop(0)
        V = {}
        for v in self.values:
            V[holes_value[0]] = self.values[v]
            holes_value.pop(0)
        self.tgt_transaction = Insert(JC, V)

    def to_sql(self):
        sql = 'INSERT INTO ' + self.tgt_transaction.join_chain.to_sql()
        cols = []
        vals = []
        for c in self.tgt_transaction.values:
            cols.append(c.split('.')[1])
            vals.append(self.tgt_transaction.values[c])
        sql = sql + ' '+str(tuple(cols))+' VALUES '+str(tuple(vals))+';'
        return sql


class Update:  # upd(j,pred,attr,val)

    def __init__(self, join_chain, predicate, attr, value):
        self.join_chain = join_chain
        self.predicate = predicate
        self.attr = attr
        self.value = value

        self.tgt_transaction = None
        self.holes = []

    def genSketch(self, phi, join_corr_supplier):
        tables = [join_corr_supplier.srcSchema.get_table(t) for t in self.join_chain]
        self.join_chain = JoinChain(tables)
        self.holes.append(self.join_chain.genSketch(phi, join_corr_supplier))
        # if self.attr.find('.')==-1:
        #     for t in self.join_chain.chain:
        #         for c in t.columns:
        #             if c[0].find(self.attr) != -1:
        #                 self.attr = c[0]
        self.holes.append(phi[self.attr])
        if self.predicate is not None:
            self.holes += self.predicate.genSketch(phi)
        # self.sk_values[h.hid] = self.values[a]
        return self.holes

    def fill(self, holes_value):
        JC = self.join_chain.fill(holes_value)
        holes_value.pop(0)
        attr = holes_value[0]
        holes_value.pop(0)
        P = self.predicate.fill(holes_value) if self.predicate is not None else None
        
        self.tgt_transaction = Update(JC, P, attr, self.value)

    def to_sql(self):
        tgt_transaction = self.tgt_transaction
        table_name, attr = tgt_transaction.attr.split('.')
        sql = 'UPDATE ' + table_name + ' SET ' + attr + ' = ' + tgt_transaction.value +\
              ' ' + tgt_transaction.predicate.to_sql() + ' ;'
        return sql


#     UPDATE Employee SET PhoneNumber = <phone> WHERE EmployeeNumber = <eid>;

class Delete:  # del(tables,j,phi)
    def __init__(self, tablelist, predicate):
        self.tablelist = tablelist
        self.join_chain = tablelist
        # l,p,r = predicate
        self.predicate = predicate  # (l,p,r)
        self.holes = []
        self.tgt_transaction = None

    def genSketch(self, phi, join_corr_supplier):
        tables = [join_corr_supplier.srcSchema.get_table(t) for t in self.join_chain]
        self.join_chain = JoinChain(tables)
        self.holes.append(self.join_chain.genSketch(phi, join_corr_supplier))
        if self.predicate is not None:
            self.holes += self.predicate.genSketch(phi)
        return self.holes

    def fill(self, holes_value):
        T = self.join_chain.fill(holes_value)
        holes_value.pop(0)
        P = self.predicate.fill(holes_value) if self.predicate is not None else None

        # l = P.tgt_lhs.spli
        self.tgt_transaction = Delete(T, P)
        # self.to_sql()

    def to_sql(self):
        tgt = self.tgt_transaction
        tgt_join_chain = tgt.join_chain    # [(tname, None), (t2name, (id, fk)), ...]
        tgt_predicate_str = tgt.predicate.to_sql() if tgt.predicate is not None else ''
        chain_str = tgt_join_chain.to_sql()
        queries = ''
        if len(tgt_join_chain.chosen_join_corr) == 1:
            query = 'DELETE FROM ' + tgt_join_chain.chosen_join_corr[0][0].name + ' ' + tgt_predicate_str + ';'
            return query

        for chain in tgt_join_chain.chosen_join_corr:
            query = 'DELETE FROM ' + chain[0].name + ' WHERE ' + chain[0].primaryKey + \
                    ' IN ( SELECT ' + chain[0].primaryKey + ' FROM ' + chain_str + ' '+\
                    tgt_predicate_str + ' ); \n'
            queries += query
        return queries


class Select:  # proj(attrs, Q(j))
    def __init__(self, attrs, join_chain, predicate):
        self.attrs = attrs
        self.join_chain = join_chain
        self.predicate = predicate

        self.holes = []
        self.tgt_transaction = None

    def genSketch(self, phi, join_corr_supplier):
        tables = [join_corr_supplier.srcSchema.get_table(t) for t in self.join_chain]
        self.join_chain = JoinChain(tables)
        self.holes.append(self.join_chain.genSketch(phi, join_corr_supplier))
        for a in self.attrs:
            self.holes.append(phi[a])
        
        if self.predicate is not None:
            self.holes += self.predicate.genSketch(phi)
        return self.holes

    def fill(self, holes_value):
        T = self.join_chain.fill(holes_value)
        attrs = {}
        for attr in self.attrs:
            attrs[holes_value[0]] = self.attrs[attr]
            holes_value.pop(0)
        P = self.predicate.fill(holes_value) if self.predicate is not None else None
        self.tgt_transaction = Select(attrs, T, P)

    def to_sql(self):
        cols =[]
        sql = 'SELECT '
        for c in self.tgt_transaction.values:
            cols.append(c.split('.')[1])
        sql += sql + ' ' + str(tuple(cols))
        sql += ' FROM ' + self.tgt_transaction.join_chain.to_sql()
        if self.predicate is not None:
            sql += ' ' + self.predicate.to_sql()
        sql += ' ;'
        return sql

    # def run(self, database):
    #     pass
    #
    # def Holer(self):
    #     return ProjectHole(self.attrs,self.query)
    # def genSketch(self):
    #     pass
    #
    # def fill(self):
    #     pass
    #
    # def to_sql(self):
    #     pass
    # def infer(self, phi):
    #     lhs = Hole(phi, self.lhs).infer()
    #     rhs = Hole(phi, self.rhs).infer()
    #     return Predicate(lhs, rhs, self.operand)


# class Filter:  # filter(phi,Q)
#     def __init__(self, predicate, query):
#         self.query = query
#         self.predicate = predicate
#
#     def run(self, database):
#         pass
#
#     def infer(self):
#         pred = self.predicate.infer()
#         query = self.query.infer()
#         return Filter(pred, query)
#
#     def Holer(self):
#         return FilterHole(self.predicate,self.query)
#
#
# '==========================================================================================' \
# '============================================================================================' \
# '=========================================================================================='
#
# class PredicateHole:
#     def __init__(self, lhs, rhs, operand):
#         self.rhs = attr_infer(
#             rhs)
#         self.lhs = attr_infer(lhs)
#         self.operand = operand
#
#     def fill(self):
#         L = attr_infer(self.lhs)
#         R = attr_infer(self.rhs)
#         return Predicate(L,R, self.operand)
#
#     def infer(self):
#         return self
#
# class InsertHole:  # ins(j,{a_i:v_i...})
#     def __init__(self, phi, join_chain, values):
#         self.join_chain = join_chain.infer()
#         self.values = attr_infer(phi, self.values)
#         self.holes = self.join_chain.holes + self.values.holes
#
#     def fill(self, holes_value):
#         J = self.join_chain.fill(holes_value)
#         V = self.values.fill(holes_value)
#         return Insert(J, V)
#
#     def infer(self):
#         return self
#
# class UpdateHole:  # upd(j,phi,attr,val)
#     def __init__(self, phi, join_chain, predicate, attr, values):
#         self.join_chain = join_chain.infer()#!!!!!!!!!!
#         self.predicate = predicate.infer()
#         self.attr = attr_infer(phi, attr)
#         self.values = values
#         self.holes = self.join_chain.holes + self.predicate.holes + self.attr.holes
#
#     def fill(self, holes_value):
#         J = self.join_chain.fill(holes_value)
#         P = self.predicate.fill(holes_value)
#         attr = attr_infer(self.attr)
#         return Update(J, P, attr, self.values)
#
#     def infer(self):
#         return self
#     # def infer(self):
#     #     jc = self.join_chain.infer()
#     #     pred = self.predicate.infer()
#     #     attr = attr_infer(self.attr)# !!!!!!! phi?
#     #     return Update(jc,pred,attr,self.values)
#
#
# class DeleteHole:  # del(tables,j,phi)
#     def __init__(self,phi, tablelist, join_chain, predicate):
#         self.join_chain = join_chain.infer(tablelist)
#         self.predicate = predicate.infer()
#         self.holes = self.join_chain.holes + self.predicate.holes
#         tablelist_options = [list(i) for r in range(1, len(self.join_chain) + 1) for i in combinations(self.join_chain, r)]
#         self.hole = Hole(len(self.holes), tablelist_options)
#         self.holes.append(self.hole)
#
#     def fill(self, holes_value):
#         L = holes_value[self.hole]####or ID?
#         J = self.join_chain.fill(holes_value)
#         P = self.predicate.fill(holes_value)
#         return Delete(L, J, P)
#
#     def infer(self):
#         return self
#
#
# class ProjectHole:  # proj(attrs, Q(j))
#     def __init__(self, phi, attrs, query):
#         self.attrs = attr_infer(phi, attrs)
#         self.query = query.infer()
#         self.holes = self.attrs.holes + self.query.holes
#
#     def fill(self, holes_value):
#         A = attr_infer(self.attrs)
#         Q = self.query.fill()
#         return Project(A, Q)
#
#     def infer(self):
#         return self
#
#
# class FilterHole:  # filter(pred,Q)
#     def __init__(self, phi, predicate, query):
#         self.query = query.infer()
#         self.predicate = predicate.infer()
#         self.holes = query.holes + self.predicate.holes
#
#     def fill(self, holes_value):
#         P = self.predicate.fill(holes_value)
#         Q = self.query.fill(holes_value)
#         return Filter(P, Q)
#
#     def infer(self):
#         return self
#     #
#     # def infer(self):
#     #     pred = self.predicate.infer()
#     #     query = self.query.infer()
#     #     return Filter(pred, query)
