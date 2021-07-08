# !pip install python-sat[pblib,aiger]
# !pip install python-Levenshtein

from pysat.formula import WCNF
from Levenshtein import distance as levenshtein_distance
# from pysat.solvers import Solver
from pysat.examples.rc2 import RC2
from schema import schema

# !!!! bug: -0 is meaningless
class val_corr_generator:
    def __init__(self, S1, S2):
        alpha = 15
        size1 = S1.size()
        size2 = S2.size()
        self.size1 = size1
        self.S1 = S1
        self.S2 = S2

        self.cnf = RC2(WCNF())

        ## hard: variables !!!!!! really needed?
        for i in range(size1 * size2):
            self.cnf.add_clause([i, -i])

        ## hard: type-matching-conditions
        for i in range(size1):
            for j in range(size2):
                if S1.id_to_type(i) != S2.id_to_type(j):
                    self.cnf.add_clause([-self.twoD2oneD(i, j)])

        ## hard: match each i to some j !!!!!!change to a_is that are queried in p
        # js=[x for x in range(size2)]
        for i in range(size1):
            all_poss = [self.twoD2oneD(i, j) for j in range(size2)]
            self.cnf.add_clause(all_poss)

        ## soft: prefer 1-1 to 1-many
        for i in range(size1):
            for j in range(size2):
                for k in range(j, size2):
                    self.cnf.add_clause([-self.twoD2oneD(i, j), -self.twoD2oneD(i, k)], weight=alpha)

        ## soft: similar names: more score!!!!!! change similarity maybe..
        for i in range(size1):
            for j in range(size2):
                similarity = 20 - levenshtein_distance(S1.id_to_name(i), S2.id_to_name(j))
                self.cnf.add_clause([self.twoD2oneD(i, j)], similarity)

        # last_sol?(use in update)
        # self.solver = Solver()
        # self.solver.append_formula(self.cnf.clauses, no_return=False)#!!!!!no_return?!

    def max_sat_solver(self):
        self.last_solution = self.cnf.compute()
        # self.solver.solve()
        # print(self.solver.get_model())
        # solver.delete()

    def max_sat_updater(self):
        for x in self.last_solution:
            self.cnf.add_clause([-x])

    def return_sol(self):
        matching = {}
        for i in self.last_solution:
            if i > 0:
                a, b = self.oneD2twoD(i)
                a = self.S1.id_to_name(a)
                b = self.S2.id_to_name(b)
                if a in matching:
                    matching[a].append(b)
                else:
                    matching[a] = [b]
        print(matching)

    def twoD2oneD(self, i, j):
        return j * self.size1 + i

    def oneD2twoD(self, x):
        return (x % self.size1, int(x / self.size1))

# phi = val_corr_generator(s1, s2)
# a = phi.max_sat_solver()
# phi.return_sol()
#
# phi.max_sat_updater()