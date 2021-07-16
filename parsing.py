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
        name, params = k.split('(')
        params = params[:-1]
        params = params.split(',')
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
    elif parsed_query[0].value == 'DELETE':
        # print([ for t in parsed_query.tokens[0])
        jc = [parsed_query[4].value]
        l, op, r = [i.strip() for i in parsed_query[6].value.replace(';', '').split()[1:4]]
        l = jc[0] + '.' + l if l.find('.') == -1 and l[0:2] != '__' else l
        r = jc[0] + '.' + r if r.find('.') == -1 and r[0:2] != '__' else r
        transaction = Delete(jc, Predicate(l, op, r))
        return transaction

    elif parsed_query[0].value == 'INSERT':
        if parsed_query[4].value.find('(') != -1:
            tName = parsed_query[4].value.split()[0].strip()
            attrs = [i.replace(',', '').strip() for i in
                     parsed_query[4].value.replace('(', '').replace(')', '').split()[1:]]
            vals = [i.replace(',', '').strip() for i in
                    parsed_query[6].value.replace('(', '').replace(')', '').split()[1:]]
            ins = {}
            for i in range(len(vals)):
                k = tName + '.' + attrs[i] if attrs[i].find('.') == -1 else attrs[i]
                ins[k] = vals[i]
        else:
            raise Exception("insert with a join!")

        jc = [t.strip() for t in tName.split(',')]
        transaction = Insert(jc, ins)
        return transaction

    elif parsed_query[0].value == 'SELECT':
        # print([i.value for i in parsed_query.tokens])
        attrs = [i.strip() for i in parsed_query[2].value.split(',')]
        qu = [i.value for i in parsed_query.tokens]
        from_index = qu.index('FROM')
        jc = []

        jc.append(qu[from_index + 2])
        if qu[from_index+4]=='JOIN':
            jc.append(qu[from_index + 6])

        l, op, r = [i.strip() for i in parsed_query[-1].value.replace(';', '').split()[1:4]]
        transaction = Select(attrs, jc, Predicate(l, op, r))
        return transaction
