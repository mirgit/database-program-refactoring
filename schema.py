class Schema:
    def __init__(self, s):
        self.schema = s
        self.cols = {t + '.' + x: self.schema[t][x] for t in self.schema for x in self.schema[t]}
        self.attr2id = {c: i+1 for i, c in enumerate(self.cols)}
        self.id2attr = {self.attr2id[c]: c for c in self.attr2id}

    def name_to_id(self, a):  # if not exist...!!!!!!!!
        return self.attr2id[a]

    def id_to_name(self, a):  # if not exist...!!!!!!!!
        return self.id2attr[a]

    def id_to_type(self, a):  # if not exist...!!!!!!!!
        return self.cols[self.id2attr[a]]

    def size(self):
        return len(self.attr2id)
