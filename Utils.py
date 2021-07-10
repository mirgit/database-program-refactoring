class Hole:
    def __init__(self, phi, attr):
        self.attr = attr
        self.phi = phi

    def infer(self):
        hole = self.phi[self.attr]
        return hole


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
