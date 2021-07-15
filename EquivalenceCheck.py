from datetime import datetime
from MFI import *
from SqliteDB import SqliteDB


class EquivalenceCheck:

    def __init__(self, p, p_prime):
        self.p = {'update': [], 'query': []}
        self.p_prime = {'update': [], 'query': []}
        for func in p:
            if 'update' in func:
                self.p['update'].append(p[func])
            elif 'query' in func:
                self.p['query'].append(p[func])
        for func in p_prime:
            if 'update' in func:
                self.p_prime['update'].append(p_prime[func])
            elif 'query' in func:
                self.p_prime['query'].append(p_prime[func])

        self.src_db = SqliteDB('src_db')
        self.tgt_db = SqliteDB('tgt_db')

    def check_equivalence(self):
        mfi = MFI()
        for i in range(20):
            mfi.add_update_transaction(self.p['update'])
            for j in range(10):
                mfi.choose_query(self.p['query'])
                mfi.replace_random_update(options=self.p['update'])
                src_result = mfi.run_in_DB(self.src_db)
                tgt_result = mfi.run_in_DB(self.tgt_db)
                is_equivalent = self.check_results(src_result, tgt_result)
                if not is_equivalent:
                    return False
        return True

    def check_results(self, src, tgt):
        if len(src) != len(tgt):
            return False
        if len(src)>0 and len(src[0]) != len(tgt[0]):
            return False
        for row in src:
            if row not in tgt:
                return False
        return True


