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
    SOLVER_NAME = 'CoRe_solver'
    VERSION = '0.1.0'

    core_min   = get(prg.get_const("core_min"), clingo.Number(0))
    core_max   = prg.get_const("core_max")
    core_stop  = get(prg.get_const("core_stop"), clingo.String("SAT"))

    print_comment('%s version %s' % (SOLVER_NAME, VERSION))
    print_comment('author: Yuya Yamada, Kentaro Yamada, Mutsunori Banbara')

    step, ret = 0, None
    while ((core_max is None or step <= core_max.number) and
            (step == 0 or 
            (core_stop.string == "SAT" and not ret.satisfiable) or
            (core_stop.string == "UNSAT" and not ret.unsatisfiable))):
        
        parts = []
        parts.append(("check", [step]))
        parts.append(("step", [step]))
        if step > 0:
            prg.release_external(clingo.Function("query", [step-1]))
            prg.cleanup()
        else:
            parts.append(("base", []))
        prg.ground(parts)
        prg.assign_external(clingo.Function("query", [step]), True)
        ret, step = prg.solve(), step+1

    print_comment('step: %s' % str(step-1))
    if core_stop.string == "SAT":
        if ret.satisfiable:
            print_result('REACHABLE')
        elif ret.unsatisfiable and step == core_max.number + 1:
            print_result('UNREACHABLE')
        else:
            print_result('UNKNOWN')
#    elif istop.string == "UNSAT":
#end.

#program check(t).
#external query(t).
