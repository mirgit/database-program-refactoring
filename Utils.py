class Hole:
    def __init__(self, id, options):
        self.id = id
        self.options = options

def attr_infer(phi, attr):
    return phi[attr]



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


class PredicateHole:
    def __init__(self, lhs, rhs, operand):
        self.rhs = attr_infer(rhs)
        self.lhs = attr_infer(lhs)
        self.operand = operand

    def fill(self):
        L = attr_fill(self.lhs)
        R = attr_fill(self.rhs)
        return Predicate(L,R, self.operand)

    def infer(self):
        return self