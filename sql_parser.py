import sqlparse
from Transactions import *

q = 'SELECT A.i, B.i FROM A JOIN B ON A.a = B.b WHERE A.c = 5'
u = 'SELECT CustomerID FROM Customer WHERE Name = <name>;'
u = 'SELECT order_items.order_id, items.name, order_items.quantity FROM order_items JOIN items ON order_items.item_id = items.id WHERE order_items.id = <id>;'
# u = 'UPDATE A SET A.b = 5 WHERE A.c = 2'
# u = 'UPDATE customers SET customers.email = email WHERE customers.id = id;'
# u = 'INSERT INTO Customer (CustomerID, Fname) VALUES (id, name);'
# u = 'DELETE FROM line_items WHERE line_items.id = <id>;'
parsed_query = sqlparse.parse(u)[0]
hq = sqlparse.parse(q)[0]
# print(hu.tokens,'\n', hq.tokens)
[print(i.ttype,i) for i in parsed_query.tokens]
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
    l, op, r = [ i.strip() for i in parsed_query[6].value.replace(';','').split()[1:4]]
    transaction = Delete(jc,jc,Predicate(l,r,op))

elif parsed_query[0].value == 'INSERT':
    jc = parsed_query[4].value.split()[0].strip()
    attrs = [i.replace(',','').strip() for i in parsed_query[4].value.replace('(', '').replace(')', '').split()[1:]]
    vals = [i.replace(',','').strip() for i in parsed_query[6].value.replace('(', '').replace(')', '').split()[1:]]
    ins = {attrs[i]:vals[i] for i in range(len(vals))}
    transaction = Insert(jc, ins)
elif parsed_query[0].value == 'SELECT':
    attrs = [i.strip() for i in parsed_query[2].value.split(',')]
