from datetime import datetime
from MFI import *   
class EquivalenceCheck:
    def __init__(self, p, p_prime):
        self.p = p
        self.p_prime = p_prime
        self.timeOut = 5*60
        self.sqlite = 
        
    def check(self):
        start = datetime.now
        mfi = MFI(self.p.q_tranactions)
        while (datetime.now - start < self.timeOut):
            mfi.add_update_tranaction(self.p.q_tranactions)
        sqlite.run(mfi, p,p_prime)
            
        