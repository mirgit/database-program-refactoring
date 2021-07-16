from z3 import *


class SketchSolver:
    def __init__(self, holes):
        self.holes = holes
        self.parameters = []
        self.solver = Solver()
        i = 0
        for hole in holes:
            self.parameters.append(BoolVector(i, len(hole)))
            i += 1
        for x in self.parameters:
            self.solver.add(Sum([If(i, 1, 0) for i in x]) == 1)

    def get_solution(self):
        if self.solver.check() == sat:
            holes_value = {}
            model = self.solver.model()
            negation = []
            for par in model.decls():
                if model[par]:
                    negation.append(model[par])
                    holeID, opt = par.name().split('__')
                    holes_value[holeID] = self.holes[int(holeID)][int(opt)]
            self.solver.add(Not(And(negation)))
            solution = []
            for i in range(len(self.holes)):
                solution.append(holes_value[str(i)])

            return solution
        return unsat
