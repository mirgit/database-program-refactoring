import sqlparse
from Transactions import *
from ValueCorrespondance import ValCorrGenerator
# from Schema import Schema
from JoinCorrSuplier import JoinCorrSupplier
from Schema_provider import SchemaProvider
from z3 import *

# ********test*********

src = './benchmarks/bench3/src-schema.txt'
tgt = './benchmarks/bench3/tgt-schema.txt'
S = SchemaProvider(src, tgt)
src_schema,tgt_schema = [S.src_schema,S.tgt_schema]
# oldSchema = {'A': {'B': 'int', 'C': 'int'}}
# newSchema = {'M': {'B': 'int'}, 'N': {'D': 'bool', 'E': 'int'}}
# S1 = Schema(oldSchema)
# S2 = Schema(newSchema)
phi = ValCorrGenerator(src_schema, tgt_schema)
phi = phi.get_solution()
print(phi)
join_supplier = JoinCorrSupplier(src_schema,tgt_schema)
q = 'SELECT A.i, B.i FROM A JOIN B ON A.a = B.b WHERE A.c = 5'
u = 'SELECT CustomerID FROM Customer WHERE Name = <name>;'
u = 'SELECT order_items.order_id, items.name, order_items.quantity FROM order_items JOIN items ON order_items.item_id = items.id WHERE order_items.id = <id>;'
# u = 'UPDATE A SET A.b = 5 WHERE A.c = 2'
# u = 'UPDATE customers SET customers.email = email WHERE customers.id = id;'
u = 'INSERT INTO A (B, C) VALUES (3, 4);'
u = 'INSERT INTO ADDRESS (aid, address, city, state, zipcode) VALUES (FRESH(1), <addr>, <ct>, <st>, <zip>);'
# u = 'DELETE FROM line_items WHERE line_items.id = <id>;'
u = """INSERT INTO Employee (EmployeeNumber, Name, PhoneNumber, Picture, VoicePrint, RetinalPrint) VALUES (<eid>, <name>, <phone>, <pic>, <voice>, <retinal>);
"""
u = 'DELETE FROM Employee WHERE VoicePrint = <eid>;'
u = u.replace('<', '__')
u = u.replace('>', '__')
parsed_query = sqlparse.parse(u)[0]
hq = sqlparse.parse(q)[0]
# print(hu.tokens,'\n', hq.tokens)
# [print(i.ttype,i) for i in parsed_query.tokens]
if parsed_query[0].value == 'UPDATE':
    jc = parsed_query[2]
    attr,value = [i.strip() for i in parsed_query[6].value.split('=')]
    l, op, r = [ i.strip() for i in parsed_query[8].value.replace(';','').split()[1:4]]
    transaction = Update(jc,Predicate(l,r,op),attr,value)
    print(transaction)
    # while i < len(parsed_query):
    #     i, token = parsed_query.token_next(i)
    #
    # print(parsed_query.token_next(0))
elif parsed_query[0].value == 'DELETE':
    jc = [parsed_query[4].value]
    l, op, r = [i.strip() for i in parsed_query[6].value.replace(';', '').split()[1:4]]
    l = jc[0] + '.' + l if l.find('.') == -1 and l[0:2] != '__'else l
    r = jc[0] + '.' + r if r.find('.') == -1 and r[0:2] != '__'else r
    print(l,r,jc)
    transaction = Delete(jc, Predicate(l, op, r))


    holes = transaction.genSketch(phi, join_supplier)
    parameters = []
    i = 0
    solver = Solver()
    for hole in holes:
        parameters.append(BoolVector(i, len(hole)))
        i += 1
    for x in parameters:
        solver.add(Sum([If(i, 1, 0) for i in x]) == 1)
    time = 3
    for times in range(time):
        if solver.check() == sat:
            holes_value = {}
            model = solver.model()
            negation = []
            for par in model.decls():
                if model[par]:
                    negation.append(model[par])
                    holeID, opt = par.name().split('__')
                    holes_value[holeID] = holes[int(holeID)][int(opt)]
            solver.add(Not(And(negation)))
        solution = []
        for i in range(len(holes)):
            solution.append(holes_value[str(i)])

    print(solution)
    transaction.fill(solution)
    k = transaction.to_sql()
    while k.find('__') != -1:
        k = k.replace('__', '<', 1)
        k = k.replace('__', '>', 1)
    print(k)
elif parsed_query[0].value == 'INSERT':
    tName = parsed_query[4].value.split()[0].strip()
    jc = [t.strip() for t in tName.split(',')]#src_schema.get_table(t)
    attrs = [i.replace(',', '').strip() for i in parsed_query[4].value.replace('(', '').replace(')', '').split()[1:]]
    vals = [i.replace(',', '').strip() for i in parsed_query[6].value.replace('(', '').replace(')', '').split()[1:]]
    ins = {tName+'.'+attrs[i]: vals[i] for i in range(len(vals))}
    print(jc,ins)
    transaction = Insert(jc, ins)
    # transaction.to_sql()
    holes = transaction.genSketch(phi, join_supplier)
    parameters = []
    i = 0
    solver = Solver()
    for hole in holes:
        parameters.append(BoolVector(i, len(hole)))
        i += 1
    for x in parameters:
        solver.add(Sum([If(i, 1, 0) for i in x]) == 1)
        # DELETE FROM Employee WHERE EmployeeNumber IN ( SELECT EmployeeNumber FROM Employee WHERE Employee.EmployeeNumber = <eid> );
    time = 3
    for times in range(time):
        if solver.check() == sat:
            holes_value = {}
            model = solver.model()
            negation = []
            for par in model.decls():
                if model[par]:
                    negation.append(model[par])
                    holeID, opt = par.name().split('__')
                    holes_value[holeID] = holes[int(holeID)][int(opt)]
            solver.add(Not(And(negation)))
        solution = []
        for i in range(len(holes)):
            solution.append(holes_value[str(i)])

    print(solution)
    transaction.fill(solution)

    k =transaction.to_sql()

elif parsed_query[0].value == 'SELECT':
    attrs = [i.strip() for i in parsed_query[2].value.split(',')]


