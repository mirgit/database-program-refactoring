from random import randint
import string
import random


class MFI:

    def __init__(self):
        self.src_query = None
        self.src_updates = []
        self.tgt_query = None
        self.tgt_updates = []
        self.last_id = 0

    def add_update_transaction(self, src_options, tgt_options):
        i = randint(0, len(tgt_options)-1)
        t1 = src_options[i]
        t2 = tgt_options[i]
        valuation = self.get_random_valuation(t1)
        self.tgt_updates.append((t2[1], valuation))
        self.src_updates.append((t1[1], valuation))
        
    def choose_query(self, src_options, tgt_options):
        i = randint(0, len(tgt_options) - 1)
        t1 = src_options[i]
        t2 = tgt_options[i]
        valuation = self.get_random_valuation(t1)
        
        self.src_query = (t1[1], valuation)
        self.tgt_query = (t2[1], valuation)

    def replace_random_update(self, src_options, tgt_options):
        i = randint(0, len(tgt_options) - 1)
        t1 = src_options[i]
        t2 = tgt_options[i]
        valuation = self.get_random_valuation(t1)
        j = randint(0, len(self.tgt_updates)-1)
        self.tgt_updates[j] = (t2[1], valuation)
        self.src_updates[j] = (t1[1], valuation)

    def get_random_id(self):
        self.last_id += 1
        return self.last_id

    def run_src_db(self, db):
        for u in self.src_updates:
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

        method = self.src_query[0]
        # print(method)
        for arg, val in self.src_query[1].items():
            if isinstance(val, str):
                val = '"' + val + '"'
            arg2 = '<' + arg + '>'
            while arg2 in method:
                method = method.replace(arg2, str(val))
        transactions = method.split(';')[:-1]
        q1 = db.execute_read_query(transactions[0])
        return q1

    def run_tgt_db(self, db):
        for u in self.tgt_updates:
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

        method = self.tgt_query[0]
        # print(method)
        for arg, val in self.tgt_query[1].items():
            if isinstance(val, str):
                val = '"' + val + '"'
            arg2 = '<' + arg + '>'
            while arg2 in method:
                method = method.replace(arg2, str(val))
        transactions = method.split(';')[:-1]
        q1 = db.execute_read_query(transactions[0])
        return q1

    def get_random_valuation(self, method):
        args, body = method
        attrs = {}
        for arg, t in args.items():
            if t == 'int':
                if 'id' in arg or 'ID' in arg or 'Id' in arg:
                    random_attr = self.get_random_id()
                else:
                    random_attr = get_random_int()
                attrs[arg] = random_attr

            elif t == 'String':
                random_attr = get_random_str()
                attrs[arg] = random_attr
            else:
                print("****************   invalid type " + t + "***************")
                raise Exception("invalid type " + t)
        return attrs


def get_random_str():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return str(ran)


def get_random_int():
    ran = random.randint(-100, 100)
    return ran
