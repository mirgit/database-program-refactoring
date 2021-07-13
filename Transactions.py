from itertools import combinations

#### project(['name','Id'],select('name'=='mammad',teacher*student))


class PredicateHole:
    def __init__(self, lhs, rhs, operand):
        self.rhs = attr_infer(rhs)
        self.lhs = attr_infer(lhs)
        self.operand = operand

    def fill(self):
        L = attr_infer(self.lhs)
        R = attr_infer(self.rhs)
        return Predicate(L,R, self.operand)

    def infer(self):
        return self


class Insert:  # ins(j,{a_i:v_i...})
    def __init__(self, join_chain, values):
        self.join_chain = join_chain
        self.values = values

    def run(self, database):
        for table in self.join_chain:
            database[table].insert(self.values)

    def Holer(self):
        return InsertHole(self.join_chain,self.values)


class Update:  # upd(j,pred,attr,val)
    def __init__(self, join_chain, predicate, attr, values):
        self.join_chain = join_chain
        self.predicate = predicate
        self.attr = attr
        self.values = values

    def run(self, database):
        for table in self.join_chain:
            database[table].update(self.predicate,self.attr,self.values)

    def Holer(self):
        return UpdateHole(self.join_chain,self.predicate,self.attr,self.values)


class Delete:  # del(tables,j,phi)
    def __init__(self, tablelist, join_chain, predicate):
        self.tablelist = tablelist
        self.join_chain = join_chain
        self.predicate = predicate

    def run(self, database):
        for table in self.tablelist:
            database[table].delete()

    def Holer(self):
        return DeleteHole(self.tablelist,self.join_chain,self.predicate)


class Project:  # proj(attrs, Q(j))
    def __init__(self, attrs, query):
        self.attrs = attrs
        self.query = query

    def run(self, database):
        pass

    def Holer(self):
        return ProjectHole(self.attrs,self.query)


class Filter:  # filter(phi,Q)
    def __init__(self, predicate, query):
        self.query = query
        self.predicate = predicate

    def run(self, database):
        pass

    def infer(self):
        pred = self.predicate.infer()
        query = self.query.infer()
        return Filter(pred, query)

    def Holer(self):
        return FilterHole(self.predicate,self.query)


'==========================================================================================' \
'============================================================================================' \
'=========================================================================================='


class Hole:
    def __init__(self, id, options):
        self.id = id
        self.options = options

    def infer(self):
        pass#!!!!!!!!!!!!!!!!!!!!!!!!1

def attr_infer(phi, attr):
    return phi[attr]


class InsertHole:  # ins(j,{a_i:v_i...})
    def __init__(self, phi, join_chain, values):
        self.join_chain = join_chain.infer()
        self.values = attr_infer(phi, self.values)
        self.holes = self.join_chain.holes + self.values.holes

    def fill(self, holes_value):
        J = self.join_chain.fill(holes_value)
        V = self.values.fill(holes_value)
        return Insert(J, V)

    def infer(self):
        return self

class UpdateHole:  # upd(j,phi,attr,val)
    def __init__(self, phi, join_chain, predicate, attr, values):
        self.join_chain = join_chain.infer()#!!!!!!!!!!
        self.predicate = predicate.infer()
        self.attr = attr_infer(phi, attr)
        self.values = values
        self.holes = self.join_chain.holes + self.predicate.holes + self.attr.holes

    def fill(self, holes_value):
        J = self.join_chain.fill(holes_value)
        P = self.predicate.fill(holes_value)
        attr = attr_infer(self.attr)
        return Update(J, P, attr, self.values)

    def infer(self):
        return self
    # def infer(self):
    #     jc = self.join_chain.infer()
    #     pred = self.predicate.infer()
    #     attr = attr_infer(self.attr)# !!!!!!! phi?
    #     return Update(jc,pred,attr,self.values)


class DeleteHole:  # del(tables,j,phi)
    def __init__(self,phi, tablelist, join_chain, predicate):
        self.join_chain = join_chain.infer(tablelist)
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
    def __init__(self, phi, attrs, query):
        self.attrs = attr_infer(phi, attrs)
        self.query = query.infer()
        self.holes = self.attrs.holes + self.query.holes

    def fill(self, holes_value):
        A = attr_infer(self.attrs)
        Q = self.query.fill()
        return Project(A, Q)

    def infer(self):
        return self


class FilterHole:  # filter(pred,Q)
    def __init__(self, phi, predicate, query):
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



class Predicate:
    def __init__(self, lhs, rhs, operand):
        self.lhs = lhs
        self.rhs = rhs
        self.operand = operand
        # operands = {'gt', 'st', 'eq', 'ge', 'se'}

    def infer(self, phi):
        lhs = Hole(phi, self.lhs).infer()
        rhs = Hole(phi, self.rhs).infer()
        return Predicate(lhs, rhs, self.operand)

    
def joinChainToSql(join_chain):
    if len(join_chain)==0:
        return ''
    join_sql = join_chain[0][0]
    join_chain = join_chain.pop(0)
    for j in join_chain:
        join_chain += ' JOIN ' 
        join_chain += j[0] 
        join_chain += " ON "
        join_chain +=  j[1][0] + " = " + j[1][1]
        