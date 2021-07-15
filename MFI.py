from random import randint
import string
import random   # define the random module


class MFI :

    def __init__(self):
        self.query = None
        self.updates = []
        self.last_id = 0


        # self.query = self.choose_query(queries)
        
    def add_update_transaction(self, options):
        t = options(randint(0, len(options)))
        valuation = t.get_random_valuation()
        self.updates.append((t, valuation))
        
    def choose_query(self, options):
        t = options(randint(0, len(options)))
        valuation = t.get_random_valuation()   #TODO whaAAt?
        self.query = (t, valuation)
        return t, valuation

    def replace_random_update(self, options):
        i = randint(0, len(self.updates)-1)
        t = options(randint(0, len(options)))
        valuation = t.get_random_valuation()

    def get_random_id(self):
        return self.last_id + 1

    def run_in_DB(db):
        pass


def get_random_str():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return str(ran)


def get_random_int():
    ran = random.randint(-100, 100)
    return ran
