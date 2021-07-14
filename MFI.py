from random import randint
class MFI :
    def __init__(self, queries):
        self.update_tranactions =[]
        self.query = self.choose_query(queries)
        
    def add_update_tranaction(self, options):
        t = options(randint(0, len(options)))
        valuation = t.get_random_valuation()
        self.update_tranactions.append((t, valuation))
        
    def choose_query(self, options):
        t = options(randint(0, len(options)))
        valuation = t.get_random_valuation()
        return (t, valuation)
    
    def run_in_DB():
        