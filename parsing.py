import sqlparse
from Transactions import *


def parse_program(program_file):
    with open(program_file, 'r') as f:
        program = f.read()
    clr1 = program.split('}')
    clr2 = {clr1[ind].split('{')[0].strip(): clr1[ind].split('{')[1] for ind in range(len(clr1) - 1)}
    program = {}  # return clr2 to have transaction type in the beginning
    for k in clr2:
        trans = clr2[k]
        # k = k.split(' ')
        # k = ' '.join(k[1:])
        name, params = k.split('(')
        params = params[:-1]
        params = params.split(',')
        program[name] = ({i.strip().split(' ')[1]: i.strip().split(' ')[0] for i in params}, trans)
    return program


def sql_to_transaction(transaction):
    parsed_query = sqlparse.parse(transaction)[0]
    if parsed_query[0].value == 'UPDATE':
        jc = parsed_query[2]
        attr, value = [i.strip() for i in parsed_query[6].value.split('=')]
        l, op, r = [i.strip() for i in parsed_query[8].value.replace(';', '').split()[1:4]]
        transaction = Update(jc, Predicate(l, r, op), attr, value)
        print(transaction)
        # while i < len(parsed_query):
        #     i, token = parsed_query.token_next(i)
        #
        # print(parsed_query.token_next(0))
    elif parsed_query[0].value == 'DELETE':
        jc = [parsed_query[4].value]
        l, op, r = [i.strip() for i in parsed_query[6].value.replace(';', '').split()[1:4]]
        transaction = Delete(jc, jc, Predicate(l, r, op))

    elif parsed_query[0].value == 'INSERT':
        # phi = phi_generator.get_solution()

        tName = parsed_query[4].value.split()[0].strip()
        # jc = [src_schema.get_table(t) for t in tName.split(',')]
        jc = [t.strip() for t in tName.split(',')]
        attrs = [i.replace(',', '').strip() for i in
                 parsed_query[4].value.replace('(', '').replace(')', '').split()[1:]]
        vals = [i.replace(',', '').strip() for i in
                parsed_query[6].value.replace('(', '').replace(')', '').split()[1:]]
        ins = {tName + '.' + attrs[i]: vals[i] for i in range(len(vals))}
        transaction = Insert(jc, ins)
        print(type(transaction))
        # transaction.to_sql()
        # holes = transaction.genSketch(phi, join_supplier)
        # parameters = []
        # i = 0
        # solver = Solver()
        # for hole in holes:
        #     parameters.append(BoolVector(i, len(hole)))
        #     i += 1
        # for x in parameters:
        #     solver.add(Sum([If(i, 1, 0) for i in x]) == 1)
        # holes_value = {}
        # if solver.check() == sat:
        #     model = solver.model()
        #     negation = []
        #     for par in model.decls():
        #         if model[par]:
        #             negation.append(model[par])
        #             holeID, opt = par.name().split('__')
        #             holes_value[holeID] = holes[int(holeID)][int(opt)]
        #     solver.add(Not(And(negation)))
        #     solution = []
        #     for i in range(len(holes)):
        #         solution.append(holes_value[str(i)])
        #
        # print(solution)
        # transaction.fill(solution)
        # print(transaction.to_sql())

    elif parsed_query[0].value == 'SELECT':
        attrs = [i.strip() for i in parsed_query[2].value.split(',')]

a = 'INSERT INTO A (id,name) VALUES (1,"Ali")'
sql_to_transaction(a)