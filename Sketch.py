

class Sketch:
    def __init__(self, program, phi):
        self.program = program  # dict of func_name:list of query/update objects
        self.sketch = None
        self.holes = None
        self.phi = phi

    def generateSketch(self):

        pass

    def encodeSketch(self):
        for hole in self.holes:
        # x = BoolVector('x', 15)
        # s = Solver()
        # s.add(Sum([If(i, 1, 0) for i in x]) == 1)
        # s.check()
        # print(s.model())

    def completeSketch(self):


