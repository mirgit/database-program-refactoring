class Transaction:
    def __init__(self):
        pass


class UpdateTrans(Transaction):
    def __init__(self):
        Transaction.__init__(self)


class QueryTrans(Transaction):
    def __init__(self):
        Transaction.__init__(self)


class Insert(UpdateTrans):
    def __init__(self, join_chain, values):
        UpdateTrans.__init__(self)
    def infer(self):
        Join

class Update(UpdateTrans):
    def __init__(self):
        UpdateTrans.__init__(self)


class Delete(UpdateTrans):
    def __init__(self):
        UpdateTrans.__init__(self)

class Project(QueryTrans):
    def __init__(self):
        QueryTrans.__init__(self)


class Filter(QueryTrans):
    def __init__(self):
        QueryTrans.__init__(self)
