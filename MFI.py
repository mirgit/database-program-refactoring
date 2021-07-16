from random import randint
import string
import random
# Program = {'func_name': ([inputs]{'id':int, 'name':'char'}, [body](str))}
# options (update or select)  = [(inputs, body)]
# method = (<inputs>{'id':int, 'name':'char'}, <body>(str))


class MFI:

    def __init__(self):
        self.query = None
        self.updates = []
        self.last_id = 0

    def add_update_transaction(self, options):
        t = options[randint(0, len(options)-1)]
        valuation = self.get_random_valuation(t)
        self.updates.append((t[1], valuation))
        
    def choose_query(self, options):
        method = options[randint(0, len(options)-1)]
        valuation = self.get_random_valuation(method)
        self.query = (method[1], valuation)
        return method, valuation

    def replace_random_update(self, options):
        i = randint(0, len(self.updates)-1)
        method = options[randint(0, len(options)-1)]
        valuation = self.get_random_valuation(method)
        self.updates[i] = (method[1], valuation)

    def get_random_id(self):
        return self.last_id + 1

    def run_in_DB(self, db):
        for u in self.updates:
            # replace args with values
            method = u[0]
            for arg, val in u[1].items():
                if isinstance(val, str):
                    val = '"' + val + '"'
                arg2 = '<' + arg + '>'
                while arg2 in method:
                    method = method.replace(arg2, str(val))

            transactions = method.split(';')[:-1]
            for transaction in transactions:
                db.execute_query(transaction)

        method = self.query[0]
        # print(method)
        for arg, val in self.query[1].items():
            if isinstance(val, str):
                val = '"' + val + '"'
            arg2 = '<' + arg + '>'
            while arg2 in method:
                method = method.replace(arg2, str(val))
        transactions = method.split(';')[:-1]
        return db.execute_read_query(transactions[0])

    def get_random_valuation(self, method):
        args, body = method
        attrs = {}
        for arg, t in args.items():
            if t == 'int':
                random_attr = get_random_int()
                attrs[arg] = random_attr

            elif t == 'String':
                random_attr = get_random_str()
                attrs[arg] = random_attr
            else:
                print("****************   invalid type " + t + "***************")
        return attrs


def get_random_str():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return str(ran)


def get_random_int():
    ran = random.randint(-100, 100)
    return ran
