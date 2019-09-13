# A TPTP python package

## Installation
* install python >= 3.5
* clone this repository

## Usage

### Run locally:
List all solvers
```
python3 -m tptp local list-solvers
```

Run Leo III.
```
$ python3 -m tptp local run --solver-name leo3 --problem problems/SYN001+1.p --timeout 60
```

Run cvc4
```
$ python3 -m tptp local run --solver-name cvc4 --problem problems/SYN001+1.p --timeout 60
```

### Run System-on-TPTP:

List all solvers
```
$ python3 -m tptp system-on-tptp list-solvers
```

Run Leo III.
```
$ python3 -m tptp system-on-tptp request --solver-name "Leo-III---1.4" --solver-command "run_Leo-III %s %d" --problem "problems/SYN001+1.p" 
```

### Test the competition mode
```
$ python3 -m tptp competition competition-test/definition.py
```

Run with more output. Good for error tracking.
```
$ python3 -m tptp competition competition-test/definition.py --verbose
```

## Making a solver TPTP ready
### SZS Status, SZS Ontology
A solver can be used by this libary if it supports the SZS Ontology as its result on the ```stdout```.

The solution status should be reported exactly once, in a line starting ```% SZS status"``` (the leading '%' makes the line into a TPTP language comment). 

For instance, a SAT-solver started for problem ```SYN001+1``` should output the line
```
% SZS status Satisfiable for SYN001+1
```
as part of its output if it proves the problem is ```satisfiable```.

Consequently:
* if your solver proves the problem is ```unsatisfiable```, the line ```% SZS status Unsatisfiable for SYN001+1```.
* if your solver ```gaves up``` the prove, the line ```% SZS status GaveUp for SYN001+1```.
* a full list of possible values for the SZS Status can be found at the [SZS Ontology](http://www.tptp.org/cgi-bin/SeeTPTP?Category=Documents&File=SZSOntology) definition.

Any prove or prove-model should additionally be printed on the stdout in the following form.
```
% SZS output start CNFRefutation for SYN001+1
  ...
% SZS output end CNFRefutation for SYN001+1
```

### Test your solver
To test your solve add it to our test competition, which can be found at
```
competition-test/definition.py
```

Here you add your solver to the ```SOLVERS``` constant
```python
SOLVERS = (
    ...
    {
        'type': 'local',
        'name': 'my-solver',
        'pretty-name': 'MySolver'
        'command': 'my-solver-binary-or-shell-script %s -t %d',
    },
    ...
)
```

This will ensure that your solver
* is called ```my-solver``` and is pretty printed ```MySolver```
* when invoked to solve the problem ```absolute/path/SYN001+1.p``` within a timeout of ```60``` seconds the
  program/shellscript ```my-solver-binary-or-shell-script "absolute/path/SYN001+1.p" -t 60``` is called
* your problem should output an SZS Status from the SZS Ontology (see above)

Running our test competition should now list your solver.
```
$ python3 -m tptp competition competition-test/definition.py
...
% Satisfiable for Sat1.cnf expecting Satisfiable with MySolver -t 60s which is correct
...
```
