from datetime import datetime
from MFI import *
from SqliteDB import SqliteDB
import os


class EquivalenceCheck:

    def __init__(self, p, p_prime, src_schema_file, tgt_schema_file):
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
        src_db = src_schema_file.replace('txt', 'sqlite')
        if os.path.exists(src_db):
            os.remove(src_db)

        tgt_db = tgt_schema_file.replace('txt', 'sqlite')
        if os.path.exists(tgt_db):
            os.remove(tgt_db)
        if os.path.exists(tgt_db):
            os.remove(tgt_db)

        self.src_db = SqliteDB(src_db)
        self.tgt_db = SqliteDB(tgt_db)
        self.src_db.create_tables(src_schema_file)
        self.tgt_db.create_tables(tgt_schema_file)

    def check_equivalence(self):
        mfi = MFI()
        for i in range(20):
            mfi.add_update_transaction(self.p['update'], self.p_prime['update'])
            for j in range(10):
                mfi.choose_query(self.p['query'], self.p_prime['query'])
                mfi.replace_random_update(self.p['update'], self.p_prime['update'])
                src_result = mfi.run_src_db(self.src_db)
                tgt_result = mfi.run_tgt_db(self.tgt_db)
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
