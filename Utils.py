
from JoinCorrSuplier import JoinCorrSupplier


class JoinChain:
    def __init__(self, tables):
        self.chain = tables#[i.strip() for i in name_string.split(',')]
        self.holes = []
        self.chosen_join_corr = []

    def genSketch(self, phi, supplier):
        self.holes = supplier.getJoinChains(phi, self.chain)
        return self.holes

    def fill(self, holes_value):
        self.chosen_join_corr = holes_value[0]
        return self

    def to_sql(self):
        print(self.chosen_join_corr)
        sql = self.chosen_join_corr[0][0].name
        if len(self.chosen_join_corr) > 1:
            self.chosen_join_corr.pop(0)
            for tup in self.chosen_join_corr:
                A = tup[0].name
                p1, p2 = tup[1]
                sql = sql + ' JOIN '+A+' ON '+p1+' = '+p2
        return sql




    def joinChainToSql(self, join_chain):
        if len(join_chain) == 0:
            return ''
        join_sql = join_chain[0][0]
        join_chain = join_chain.pop(0)
        for j in join_chain:
            join_sql += ' JOIN '
            join_sql += j[0]
            join_sql += " ON "
            join_sql += j[1][0] + " = " + j[1][1]
        return join_sql
