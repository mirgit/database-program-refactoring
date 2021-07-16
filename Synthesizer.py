from Schema_provider import SchemaProvider
from parsing import *  #parse_program, sql_to_transaction
from z3 import *
from ValueCorrespondance import ValCorrGenerator
from JoinCorrSuplier import JoinCorrSupplier
from SketchSolver import SketchSolver
import time
from EquivalenceCheck import EquivalenceCheck


class Synthesizer:
    def __init__(self, b, src_schema_file, tgt_schema_file, src_program_file):
        all_time = time.time()
        S = SchemaProvider(src_schema_file, tgt_schema_file)
        src_schema, tgt_schema = [S.src_schema, S.tgt_schema]
        program = parse_program(src_program_file)
        for func_name in program:
            trans = program[func_name][1]
            trans = trans.replace('<','__')
            trans = trans.replace('>','__')
            program[func_name] = (program[func_name][0], trans)
        phi_generator = ValCorrGenerator(src_schema, tgt_schema)
        join_supplier = JoinCorrSupplier(src_schema, tgt_schema)
        phi = phi_generator.get_solution()
        start_time = time.time()
        iteration = 1
        value_corr =1
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
                    new_program[func_name] = (program[func_name][0], '\n  '.join(new_func))
                if EquivalenceCheck(parse_program(src_program_file), new_program, src_schema_file, tgt_schema_file).check_equivalence():
                    file_name = src_program_file.replace('src', 'tgt')
                    save_program(new_program, file_name)
                    now = time.time()
                    print('time for synthesis of '+str(b) + ' is :'+str(now - start_time))
                    print('total time for benchmark '+str(b)+' is :'+str(now - all_time))

                    return
                iteration+=1
                holes_value = solver.get_solution()

            value_corr +=1
            phi = phi_generator.get_solution()
        raise Exception("Unable to find a proper program!")


for b in range(8, 11):
    path = "./benchmarks/bench"+str(b)+"/"
    Synthesizer(b, path+"src-schema.txt", path+'tgt-schema.txt', path+'src-prog.txt')