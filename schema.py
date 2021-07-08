# sum((len(v) for v in newSchema.values()))
class schema:
    def __init__(self, s):
        self.schema = s

        self.cols = {t + '.' + x: self.schema[t][x] for t in self.schema for x in self.schema[t]}
        self.attr2id = {c: i for i, c in enumerate(self.cols)}
        self.id2attr = {self.attr2id[c]: c for c in self.attr2id}

    def name_to_id(self, a):  # if not exist...!!!!!!!!
        return self.attr2id[a]

    def id_to_name(self, a):  # if not exist...!!!!!!!!
        return (self.id2attr[a])

    def id_to_type(self, a):  # if not exist...!!!!!!!!
        return (self.cols[self.id2attr[a]])

    def size(self):
        return len(self.attr2id)


oldSchema = {'Class': {'ClassId': 'int', 'InstId': 'int', 'TaId': 'int'},
             'Instructor': {'InstId': 'int', 'IName': 'string', 'IPic': 'picture'},
             'TA': {'TaId': 'int', 'TName': 'string', 'TPic': 'picture'}}
newSchema = {'Class': {'ClassId': 'int', 'InstId': 'int', 'TaId': 'int'},
             'Instructor': {'InstId': 'int', 'IName': 'string', 'PicId': 'int'},
             'TA': {'TaId': 'int', 'TName': 'string', 'PicId': 'int'}, 'Picture': {'PicId': 'int', 'Pic': 'picture'}}
s2 = schema(newSchema)
s1 = schema(oldSchema)
s1.name_to_id('TA.TName')
# s2.size()