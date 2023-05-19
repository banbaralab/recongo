#script (python) 

import clingo

def get(val, default):
    return val if val != None else default

def print_message(str_list):
    print(' '.join(str_list))

def print_ans(str):
    print_message(['a', str])

def print_comment(str):
    print_message(['c', str])

def print_result(str):
    print_message(['s', str])

def main(prg):
    SOLVER_NAME = 'recongo'
    SOLVER_VERSION = '0.1.1'

    core_min   = get(prg.get_const("core_min"), clingo.Number(0))
    core_max   = prg.get_const("core_max")
    core_stop  = get(prg.get_const("core_stop"), clingo.String("SAT"))

    print_comment('%s: an ASP-based CoRe Solver' % SOLVER_NAME)
    print_comment('version: %s' % SOLVER_VERSION)
    print_comment('author: Yuya Yamada, Kentaro Yamada, Mutsunori Banbara')

    step, ret = 0, None
    while ((core_max is None or step <= core_max.number) and
            (step == 0 or step < core_min.number or
            (core_stop.string == "SAT" and not ret.satisfiable) or
            (core_stop.string == "UNSAT" and not ret.unsatisfiable))):
        
        parts = []
        parts.append(("check", [clingo.Number(step)]))
        parts.append(("step", [clingo.Number(step)]))
        if step > 0:
            prg.release_external(clingo.Function("query", [clingo.Number(step-1)]))
            prg.cleanup()
        else:
            parts.append(("base", []))
        prg.ground(parts)
        prg.assign_external(clingo.Function("query", [clingo.Number(step)]), True)
        ret, step = prg.solve(), step+1

    print_comment('step: %s' % str(step-1))

    if (step != 0 and step >= core_min.number and
        (core_stop.string != "SAT" or ret.satisfiable) and
        (core_stop.string != "UNSAT" or ret.unsatisfiable)):
        print_result('REACHABLE')
    else:
        print_result('UNREACHABLE')

#end.

#program check(t).
#external query(t).
