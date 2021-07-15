from datetime import datetime
from MFI import *


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

    def check(self):
        start = datetime.now
        mfi = MFI()
        for i in range(20):
            mfi.add_update_transaction(self.p['update'])
            for j in range(10):
                mfi.choose_query(self.p['query'])
                mfi.replace_random_update(options=self.p['update'])

