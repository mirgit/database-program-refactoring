class Hole:
    def __init__(self, id, options):
        self.id = id
        self.options = options


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
    def __init__(self):
        pass
