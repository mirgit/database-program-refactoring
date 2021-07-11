import subprocess

from z3 import *

class Sketch:
    def __init__(self, program, phi):
        self.program = program  # dict of func_name:list of query/update objects
        self.sketch = None
        self.holes = None
        self.phi = phi
        self.holes_value = {}
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
            for par in model.decls():
                if model[par]:
                    holeID,opt = par.split('__')
                    self.holes_value[holeID]=self.holes[holeID][opt]
            ## add not(solution) to constraints

    def completeSketch(self):
        pass


