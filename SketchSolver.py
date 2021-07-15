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


#
# class Sketch:#sql-parser + valcorr -> transactions.genSketch(phi,..) -> self.solve -> trans.fill:program -> get string?
#
#     def __init__(self, program, phi):
#         self.program = program  # dict of func_name:list of query/update objects
#         self.sketch = None
#         self.holes = None
#         self.phi = phi
#         self.holes_value = {}
#         self.generatedProgram = {}
#         self.solver = Solver()
#
#     def generateSketch(self):
#         for m in self.program:
#             self.sketch[m] = []
#             for t in self.program[m]:
#                 t_hole = t.Holer()
#                 self.sketch[m].append(t_hole)
#
#     def encodeSketch(self):
#         parameters = []
#         i = 0
#         for hole in self.holes:
#
#             parameters.append(BoolVector(i, len(hole.options)))
#             i += 1
#         for x in parameters:
#             self.solver.add(Sum([If(i, 1, 0) for i in x]) == 1)
#
#
#     def getModel(self):
#         if self.solver.check() == sat:
#             model = self.solver.model()
#             negation = []
#             for par in model.decls():
#                 if model[par]:
#                     negation.append(par)
#                     holeID,opt = par.split('__')
#                     self.holes_value[holeID] = self.holes[int(holeID)][int(opt)]
#             self.solver.add(Not(negation))
#             return model
#
#     def completeSketch(self):
#         self.generatedProgram.clear()
#         for m in self.sketch:
#             for t in self.sketch[m]:
#                 self.generatedProgram[m] = t.fill()
#
#
#
#
