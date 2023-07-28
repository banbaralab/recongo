# recongo
Recongo is a solver for solving Combinatorial Reconfiguration
Problems (CRPs) based on the bounded combinatorial
reconfiguration with Answer Set Programming (ASP).
As a backend solver, we use clingo, a high-speed ASP solver.

## Requirements
- python3 (version 3.8.3 or higher)
- [clingo](https://potassco.org/clingo/) (version 5.6.2 or higher)

## Execution example
The following is a basical command.
Recongo output a shortest solution if reachable, otherwise, namely unreachable, recongo will not stop.
```
python recongo.py example/isrp/encoding/isrpTJ_ex1_basic_nohints_inc.lp example/isrp/benchmark/original/isrp-ex.lp example/isrp/benchmark/original/isrp-ex_01.lp
```

<details><summary>Output example</summary>

```
recongo version 0.3 (compet 2023 version)
Reading from encoding/isrp/isrpTJ_ex1_basic_inc.lp ...
c Step: 0
Solving...
c Result: UNSAT
c Step: 1
Solving...
c Result: UNSAT
c Step: 2
Solving...
c Result: UNSAT
c Step: 3
Solving...
Answer: 1
start(1) start(2) start(4) node(1) node(2) node(3) node(4) node(5) node(6) node(7) node(8) k(3) edge(1,3) edge(2,5) edge(3,4) edge(3,6) edge(4,5) edge(5,8) edge(6,7) edge(7,8) goal(3) goal(5) goal(7) n(8) e(8) in(1,0) in(2,0) in(4,0) in(7,1) token_added(7,1) in(1,1) in(2,1) in(3,2) in(7,2) in(2,2) token_added(3,2) query(3) in(3,3) in(5,3) in(7,3) token_added(5,3)
c Result: SAT
a Answer: start(1) start(2) start(4) in(1,0) in(2,0) in(4,0) in(1,1) in(2,1) in(7,1) in(2,2) in(3,2) in(7,2) in(3,3) in(5,3) in(7,3) node(1) node(2) node(3) node(4) node(5) node(6) node(7) node(8) k(3) edge(1,3) edge(2,5) edge(3,4) edge(3,6) edge(4,5) edge(5,8) edge(6,7) edge(7,8) token_added(7,1) token_added(3,2) token_added(5,3) query(3) goal(3) goal(5) goal(7) n(8) e(8)
s REACHABLE
a Step: 3 

SATISFIABLE

Models       : 1+
Calls        : 4
Time         : 0.006s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.005s
```

</details>

If you want to solve unreachable instances, you can use `--imax` option.
Recongo will output unreachable when there are no reconfiguration sequence where the length from 0 to $ imax - 1 $.
The following is an example.
```
python recongo.py example/isrp/encoding/isrpTJ_ex1_basic_nohints_inc.lp example/isrp/benchmark/core_challenge2022_1st-benchmark/hc-toyno-01.lp example/isrp/benchmark/core_challenge2022_1st-benchmark/hc-toyno-01_01.lp --imax=6
```

<details><summary>Output Example</summary>

```
recongo version 0.3 (compet 2023 version)
Reading from encoding/isrp/isrpTJ_ex1_basic_inc.lp ...
c Step: 0
Solving...
c Result: UNSAT
c Step: 1
Solving...
c Result: UNSAT
c Step: 2
Solving...
c Result: UNSAT
c Step: 3
Solving...
c Result: UNSAT
c Step: 4
Solving...
c Result: UNSAT
c Step: 5
Solving...
c Result: UNSAT
s UNREACHABLE
a Step: -1 

UNSATISFIABLE

Models       : 0
Calls        : 6
Time         : 0.008s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.006s
```

</details>

Please use option `-h` (`--help`) to see more detail.

## Directory
Please see README in each directory for the details.
### example
- In this directory, there are benchmarks, encodings and utility programs for some combinatorial reconfiguration problems.

## Known issues
- Recongo somtimes output nothing in signal interrupted.

## Other link
- [CoRe Challenge 2022](https://core-challenge.github.io/2022/)
  - You can get more ISRP instances.
- [CoRe Challenge 2023](https://core-challenge.github.io/2023/)