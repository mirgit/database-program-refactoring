import sqlparse
from Transactions import *

def save_program(program,file_name):
    with open(file_name, 'w') as file_writer:
        for function_name in program:
            arg_list = [program[function_name][0][item]+' '+item for item in program[function_name][0]]
            args = ', '.join(arg_list)
            file_writer.write(function_name+'('+args+') {\n')
            file_writer.write(program[function_name][1])
            file_writer.write('}\n\n')
    # print(program)

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
        trans = trans.replace('<','__')
        trans = trans.replace('>','__')
        program[name] = ({i.strip().split(' ')[1]: i.strip().split(' ')[0] for i in params}, trans)
    return program


def sql_to_transaction(transaction):
    parsed_query = sqlparse.parse(transaction)[0]
    if parsed_query[0].value == 'UPDATE':
        jc = [parsed_query[2].value]
        attr, value = [i.strip() for i in parsed_query[6].value.split('=')]
        l, op, r = [i.strip() for i in parsed_query[8].value.replace(';', '').split()[1:4]]
        transaction = Update(jc, Predicate(l, op, r), attr, value)
        return transaction
        # while i < len(parsed_query):
        #     i, token = parsed_query.token_next(i)
        #
        # print(parsed_query.token_next(0))
    elif parsed_query[0].value == 'DELETE':
        # print([ for t in parsed_query.tokens[0])
        jc = [parsed_query[4].value]
        l, op, r = [i.strip() for i in parsed_query[6].value.replace(';', '').split()[1:4]]
        l = jc[0] + '.' + l if l.find('.') == -1 and l[0:2] != '__' else l
        r = jc[0] + '.' + r if r.find('.') == -1 and r[0:2] != '__' else r
        transaction = Delete(jc, Predicate(l, op, r))
        return transaction

    elif parsed_query[0].value == 'INSERT':
        # phi = phi_generator.get_solution()
        print([i.value for i in parsed_query.tokens])
        if parsed_query[4].value.find('(') != -1:
            tName = parsed_query[4].value.split()[0].strip()
            attrs = [i.replace(',', '').strip() for i in
                     parsed_query[4].value.replace('(', '').replace(')', '').split()[1:]]
            vals = [i.replace(',', '').strip() for i in
                    parsed_query[6].value.replace('(', '').replace(')', '').split()[1:]]
            ins = {tName + '.' + attrs[i]: vals[i] for i in range(len(vals))}
        else:
            raise Exception("insert with a join!")

        # jc = [src_schema.get_table(t) for t in tName.split(',')]

        jc = [t.strip() for t in tName.split(',')]
        transaction = Insert(jc, ins)
        return transaction
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
        # print([i.value for i in parsed_query.tokens])
        attrs = [i.strip() for i in parsed_query[2].value.split(',')]
        qu = [i.value for i in parsed_query.tokens]
        from_index = qu.index('FROM')
        # to_inex =
        jc = []
        # while from_index < len(qu)-2:
        jc.append(qu[from_index + 2])
        if qu[from_index+4]=='JOIN':
            jc.append(qu[from_index + 6])
        # from_index += 12

        l, op, r = [i.strip() for i in parsed_query[-1].value.replace(';', '').split()[1:4]]
        # print(attrs, jc, (l, op, r))
        transaction = Select(attrs, jc, Predicate(l, op, r))
        return transaction

# u = 'SELECT order_items.order_id, items.name, order_items.quantity FROM order_items JOIN items ON order_items.item_id = items.id WHERE order_items.id = <id>;'
# sql_to_transaction(u)
