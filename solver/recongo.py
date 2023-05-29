'''
recongo solver
  Time-stamp: <2023-04-12 23:10:17 banbara>
  @author NU-ASP team (banbara@nagoya-u.jp)
  @note This code is based on inc.py in the clingo package.
'''

import sys
import math
from typing import cast, Any, Callable, Optional, Sequence

from clingo.application import clingo_main, Application, ApplicationOptions
from clingo.control import Control, Model
from clingo.solving import SolveResult
from clingo.symbol import Function, Number


class RecongoConfig:
    '''
    Configuration object for incremental solving.
    '''
    imin: int
    imax: Optional[int]
    istop: str
    isearch: str
    istrategy: str
    
    def __init__(self):
        self.imin = 1
        self.imax = None
        self.istop = "SAT"
        self.isearch = "shortest"
        self.istrategy = "lin"


def parse_int(conf: Any,
              attr: str,
              min_value: Optional[int] = None,
              optional: bool = False) -> Callable[[str], bool]:
    '''
    Returns a parser for integers.

    The parser stores its result in the `attr` attribute (given as string) of
    the `conf` object. The parser can be configured to only accept integers
    having a minimum value and also to treat value `"none"` as `None`.
    '''
    def parse(sval: str) -> bool:
        if optional and sval == "none":
            value = None
        else:
            value = int(sval)
            if min_value is not None and value < min_value:
                raise RuntimeError("value too small")
        setattr(conf, attr, value)
        return True
    return parse

def parse_stop(conf: Any, attr: str) -> Callable[[str], bool]:
    '''
    Returns a parser for `istop` values.
    '''
    def parse(sval: str) -> bool:
        if sval not in ("SAT", "UNSAT", "UNKNOWN"):
            raise RuntimeError("invalid value")
        setattr(conf, attr, sval)
        return True
    return parse

def parse_search(conf: Any, attr: str) -> Callable[[str], bool]:
    '''
    Returns a parser for `isearch` values.
    '''
    def parse(sval: str) -> bool:
        if sval not in ("existent", "shortest", "longest"):
            raise RuntimeError("invalid value")
        setattr(conf, attr, sval)
        return True
    return parse

def parse_strategy(conf: Any, attr: str) -> Callable[[str], bool]:
    '''
    Returns a parser for `strategy` values.
    '''
    def parse(sval: str) -> bool:
        if sval not in ("lin", "sqr", "exp"):
            raise RuntimeError("invalid value")
        setattr(conf, attr, sval)
        return True
    return parse


def print_message(*args):
    elems = [str(x) for x in args]
    print(" ".join(elems), flush=True)

def print_comment(*args):
    print_message('c', *args)
    
def print_result(*args):
    print_message('s', *args)

def print_answer(*args):
    print_message('a', *args)

def print_error(*args):
    print_message('e *** ', *args)

def print_debug(*args):
    print_message('d', *args)
    
def is_square(x):
    return math.sqrt(x).is_integer()

def is_pow2(x):
    if (x == 0):
        return False
    return (x & (x - 1)) == 0


class RecongoApp(Application):
    '''
    The example application implemeting incremental solving.
    '''
    program_name: str = "recongo"
    version: str = "0.3 (compet 2023 version)"
    _conf: RecongoConfig
    _model: Optional[str]
    _step: int
    
    def __init__(self):
        self._conf = RecongoConfig()
        self._model = None
        self._step = -1
        
    def register_options(self, options: ApplicationOptions):
        '''
        Register program options.
        '''
        group = "Recongo Options"

        options.add(
            group, "imin",
            "Minimum number of steps [{}]".format(self._conf.imin),
            parse_int(self._conf, "imin", min_value=0),
            argument="<n>")

        options.add(
            group, "imax",
            "Maximum number of steps [{}]".format(self._conf.imax),
            parse_int(self._conf, "imax", min_value=0, optional=True),
            argument="<n>")

        options.add(
            group, "istop",
            "Stop criterion [{}]".format(self._conf.istop),
            parse_stop(self._conf, "istop"))

        options.add(
            group, "isearch",
            "Search path [{}]".format(self._conf.isearch),
            parse_search(self._conf, "isearch"))        

        options.add(
            group, "istrategy",
            "Search strategy [{}]".format(self._conf.istrategy),
            parse_strategy(self._conf, "istrategy"))

    def _on_model(self, model: Model):
        self._model = str(model)
        
    def _on_finish(self, ret: SolveResult):
        print_comment("Result: {}".format(ret))

    def step_to_run(self, x: int):
        if (x == 0):
            return True
        if (self._conf.imax is not None and x == self._conf.imax - 1):
            return True
        if (self._conf.istrategy == "sqr"):
            return is_square(x)
        if (self._conf.istrategy == "exp"):
            return is_pow2(x)
        return True
        
    def main(self, ctl: Control, files: Sequence[str]):
        '''
        The main function implementing incremental solving.
        '''
        if not files:
            files = ["-"]
        for file_ in files:
            ctl.load(file_)
        ctl.add("check", ["t"], "#external query(t).")

        conf = self._conf
        step = 0
        ret: Optional[SolveResult] = None
        if conf.isearch == "longest":
            conf.imin = conf.imax

        try:
            while ((conf.imax is None or step < conf.imax) and
                   (conf.imin is None or step < conf.imin or ret is None or (
                       (conf.istop == "SAT" and not ret.satisfiable) or
                       (conf.istop == "UNSAT" and not ret.unsatisfiable) or
                       (conf.istop == "UNKNOWN" and not ret.unknown)))):
                parts = []
                parts.append(("check", [Number(step)]))
                parts.append(("step", [Number(step)]))
                if step > 0:
                    ctl.release_external(Function("query", [Number(step - 1)]))
                else:
                    parts.append(("base", []))
                ctl.ground(parts)
                ctl.assign_external(Function("query", [Number(step)]), True)
                print_comment("Step: {}".format(step))
                if self.step_to_run(step):
                    ret = cast(SolveResult, ctl.solve(on_model=self._on_model, on_finish=self._on_finish))
                    if ret.satisfiable:
                        self._step = step
                else:
                    print_comment("Skipping")
                    
                step = step + 1

                
        except RuntimeError as e:
            print_error(type(e), e)

        except KeyboardInterrupt as e:
            print_error(type(e), e)

        finally:
            if self._model is not None:
                print_answer("Answer:", self._model)
                print_result("REACHABLE")
            elif conf.imax is not None and step >= conf.imax:
                print_result("UNREACHABLE")
            else:
                print_result("REACHABILITY UNKNOWN")

            print_answer("Step:", self._step, "\n")


clingo_main(RecongoApp(), sys.argv[1:])
