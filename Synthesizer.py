from Schema_provider import SchemaProvider
from parsing import *  #parse_program, sql_to_transaction
from z3 import *
from ValueCorrespondance import ValCorrGenerator
from JoinCorrSuplier import JoinCorrSupplier
from SketchSolver import SketchSolver
import pickle
from EquivalenceCheck import EquivalenceCheck
class Synthesizer:
    def __init__(self, src_schema_file, tgt_schema_file, src_program_file):
        S = SchemaProvider(src_schema_file, tgt_schema_file)
        src_schema, tgt_schema = [S.src_schema, S.tgt_schema]
        program = parse_program(src_program_file)
        for func_name in program:
            trans = program[func_name][1]
            trans = trans.replace('<','__')
            trans = trans.replace('>','__')
            program[func_name] = (program[func_name][0],trans)
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
                        final_trans = trans.to_sql()
                        while final_trans.find('__') != -1:
                            final_trans = final_trans.replace('__', '<', 1)
                            final_trans = final_trans.replace('__', '>', 1)
                        new_func.append(final_trans)
                    # print(new_func)
                    new_program[func_name] = (program[func_name][0], '\n  '.join(new_func))
                # with open('example.prog','wb') as f:
                #     pickle.dump(new_program, f)
                # raise 1

                        # for fn in transactions:
                        #     for tr in transactions[fn]:
                        #
                #test the new program and return
                if EquivalenceCheck(parse_program(src_program_file), new_program, src_schema_file, tgt_schema_file).check_equivalence():
                    file_name = src_program_file.replace('src', 'tgt')
                    save_program(new_program, file_name)
                    return
                holes_value = solver.get_solution()

            phi = phi_generator.get_solution()
        raise Exception("Unable to find a proper program!")

path = "./benchmarks/bench6/"
Synthesizer(path+"src-schema.txt", path+'tgt-schema.txt', path+'src-prog.txt')