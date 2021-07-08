from Levenshtein import distance as levenshtein_distance
from schema import schema
from z3 import *


class ValCorrGenerator:
    def __init__(self, s1, s2):
        alpha = 15
        size1 = s1.size()
        size2 = s2.size()
        self.size1 = size1
        self.S1 = s1
        self.S2 = s2

        self.cnf = Optimize()
        x = [[]]
        for i in range(1, size1+1):
            x.append([None])
            for j in range(1, size2+1):
                x[i].append(Bool(str(i)+'_'+str(j)))

        # hard: type-matching-constraints
        for i in range(1, size1+1):
            for j in range(1, size2+1):
                if s1.id_to_type(i) != s2.id_to_type(j):
                    self.cnf.add(Not(x[i][j]))

        ## hard: match each i to some j !!!!!!change to a_is that are queried in p
        for i in range(1, size1+1):
            self.cnf.add(Or([x[i][j] for j in range(1, size2+1)]))

        # soft: prefer 1-1 to 1-many
        for i in range(1, size1+1):
            for j in range(1, size2+1):
                for k in range(j, size2+1):
                    self.cnf.add_soft(Or(Not(x[i][j]), Not(x[i][k])), weight=alpha)

        # soft: similar names: more score
        for i in range(1, size1+1):
            for j in range(1, size2+1):
                similarity = 20 - levenshtein_distance(s1.id_to_name(i), s2.id_to_name(j))
                self.cnf.add_soft(x[i][j], similarity)
        self.vars = x
        self.solution = {attr: [] for attr in self.S1.cols}  ##!!!!!!only queried attrs are needed

    def get_solution(self):
        check = self.cnf.check()
        for k in self.solution.keys():
            self.solution[k].clear()
        if check == sat:
            m = self.cnf.model()
            solution = []
            for var in m:
                i, j = var.name().split('_')
                if m[var]:
                    solution.append(self.vars[int(i)][int(j)])
                    self.solution[self.S1.id_to_name(int(i))].append(self.S2.id_to_name(int(j)))
                else:
                    solution.append(Not(self.vars[int(i)][int(j)]))
            self.cnf.push()
            self.cnf.add(Not(And(solution)))
        else:
            return check
        return self.solution

    def print_sol(self):
        for k in self.solution:
            print(k, '  -->  ', self.solution[k])
        print('========================================================')
# oldSchema = {'Class': {'ClassId': 'int', 'InstId': 'int', 'TaId': 'int'},
#              'Instructor': {'InstId': 'int', 'IName': 'string', 'IPic': 'picture'},
#              'TA': {'TaId': 'int', 'TName': 'string', 'TPic': 'picture'}}
# newSchema = {'Class': {'ClassId': 'int', 'InstId': 'int', 'TaId': 'int'},
#              'Instructor': {'InstId': 'int', 'IName': 'string', 'PicId': 'int'},
#              'TA': {'TaId': 'int', 'TName': 'string', 'PicId': 'int'}, 'Picture': {'PicId': 'int', 'Pic': 'picture'}}
# oldSchema = {'A': {'B': 'int', 'C': 'int'}}
# newSchema = {'M': {'B': 'int'}, 'N': {'D': 'bool', 'E': 'int'}}
# S1 = schema(oldSchema)
# S2 = schema(newSchema)
#
# phi = ValCorrGenerator(S1, S2)
# a = phi.get_solution()
# while a != unsat:
#     phi.print_sol()
#     a = phi.get_solution()
