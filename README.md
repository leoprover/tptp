# A TPTP python package

# Installation

# Usage
## Run System-on-TPTP:

List all solvers
```
python3 -m tptp system-on-tptp list-solvers
```

Run Leo III.
```
python3 -m tptp system-on-tptp request --solver-name "Leo-III---1.4" --solver-command "run_Leo-III %s %d" --problem "problems/SYN001+1.p" 
```

## Run locally:

List all solvers
```
python3 -m tptp local list-solvers
```

Run Leo III.
```
python3 -m tptp local request --solver-name "leo3" --solver-command "leo3 %s -t %d" --problem "problems/SYN001+1.p" --timeout 60
--timeout 60
```
