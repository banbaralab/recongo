# recongo
Recongo is a solver for solving Combinatorial Reconfiguration Problems (CRPs)
with Answer Set Programming (ASP). As a backend solver, we use clingo, a high-speed
ASP solver.

## Requirements
- python3 (version 3.8.3 or higher)
- [clingo](https://potassco.org/clingo/) (version XXX or higher)

## Execution example

## Directory
### benchmark
- The benchmark sets of small insctances. There are some CRPs like
  Independent Set Reconfiguration Problems (ISRPs) and so on.

### old_recongo
- Recongo in this directory was uesd in CoRe Challenge 2022.
  Be careful, we will not update this recongo.

### solver
- There are files for running recongo.
  We strongly recommend using this recongo (not `old_recongo`)

## Known issues
- Recongo somtimes output nothing in signal interrupted.

## Other link
- [CoRe Challenge 2022](https://core-challenge.github.io/2022/)
  - You can get more ISRP instances.
- [CoRe Challenge 2023](https://core-challenge.github.io/2023/)