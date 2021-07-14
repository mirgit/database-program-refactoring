from Schema_provider import SchemaProvider
from parsing import parse_program, sql_to_transaction
from z3 import *
from ValueCorrespondance import ValCorrGenerator
from JoinCorrSuplier import JoinCorrSupplier

class Synthesizer:
    def __init__(self, srs_schema_file, tgt_schema_file, srs_program_file):
        S = SchemaProvider(srs_schema_file, tgt_schema_file)
        src_schema, tgt_schema = [S.src_schema, S.tgt_schema]
        program = parse_program(srs_program_file)
        phi_generator = ValCorrGenerator(src_schema, tgt_schema)
        join_supplier = JoinCorrSupplier(src_schema, tgt_schema)
        for function_name in program:
            transactions = program[function_name][1]
            transactions = transactions.split(';').strip()
            for trans in transactions:
                transaction = sql_to_transaction(trans)




