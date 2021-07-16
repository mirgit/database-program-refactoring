from Schema_provider import SchemaProvider
from parsing import *  #parse_program, sql_to_transaction
from z3 import *
from ValueCorrespondance import ValCorrGenerator
from JoinCorrSuplier import JoinCorrSupplier
from SketchSolver import SketchSolver
import pickle
from EquivalenceCheck import EquivalenceCheck
class Synthesizer:
    def __init__(self, srs_schema_file, tgt_schema_file, srs_program_file):
        S = SchemaProvider(srs_schema_file, tgt_schema_file)
        src_schema, tgt_schema = [S.src_schema, S.tgt_schema]
        program = parse_program(srs_program_file)
        phi_generator = ValCorrGenerator(src_schema, tgt_schema)
        join_supplier = JoinCorrSupplier(src_schema, tgt_schema)
        phi = phi_generator.get_solution()
        while phi != unsat:
            transactions = {}
            for func_name in program:
                transactions[func_name] = []
                for t in program[func_name][1].split(';')[:-1]:
                    transactions[func_name].append(sql_to_transaction(t.strip()))
            holes = []
            for func_name in transactions:
                for trans in transactions[func_name]:
                    holes.extend(trans.genSketch(phi, join_supplier))
            solver = SketchSolver(holes)
            holes_value = solver.get_solution()
            while holes_value != unsat:
                # fill, test,
                new_program = {}
                for func_name in transactions:
                    new_func = []
                    for trans in transactions[func_name]:
                        trans.fill(holes_value)
                        new_func.append(trans.to_sql())
                    print(new_func)
                    new_program[func_name] = (program[func_name][0], '\n  '.join(new_func))
                # with open('example.prog','wb') as f:
                #     pickle.dump(new_program, f)
                # raise 1

                        # for fn in transactions:
                        #     for tr in transactions[fn]:
                        #
                #test the new program and return
                if EquivalenceCheck(program, new_program):
                    file_name = srs_program_file.replace('srs', 'tgt')
                    save_program(new_program, file_name)
                    return
                holes_value = solver.get_solution()

            phi = phi_generator.get_solution()
        raise Exception("Unable to find a proper program!")

path = "./benchmarks/bench3/"
Synthesizer(path+"src-schema.txt", path+'tgt-schema.txt', path+'src-prog.txt')