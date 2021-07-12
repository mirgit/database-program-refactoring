import subprocess

from z3 import *

class Sketch:
    def __init__(self, program, phi):
        self.program = program  # dict of func_name:list of query/update objects
        self.sketch = None
        self.holes = None
        self.phi = phi
        self.holes_value = {}
        self.generatedProgram = {}
        self.solver = None

    def generateSketch(self):
        for m in self.program:
            self.sketch[m] = []
            for t in self.program[m]:
                t_hole = t.Holer()
                self.sketch[m].append(t_hole)

    def encodeSketch(self):
        parameters = []
        for hole in self.holes:
            parameters.append(BoolVector(hole.id, len(hole.options)))
        self.solver = Solver()
        for x in parameters:
            self.solver.add(Sum([If(i, 1, 0) for i in x]) == 1)


    def getModel(self):
        if self.solver.check() == sat:
            model = self.solver.model()
            negation = []
            for par in model.decls():
                if model[par]:
                    negation.append(par)
                    holeID,opt = par.split('__')
                    self.holes_value[holeID] = self.holes[holeID][opt]
            self.solver.add(Not(negation))
            return model

    def completeSketch(self):
        self.generatedProgram.clear()
        for m in self.sketch:
            for t in self.sketch[m]:
                self.generatedProgram[m] = t.fill()




