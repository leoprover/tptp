import os
from pathlib import Path

# type of the competition
COMPETITION_TYPE = "CASC"

# name of the competition
COMPETITION_NAME = "Test DIMACS CNF Competition"

# tuples of name and command of all solvers as list
# %s is the placeholder for a filename
# %d is the placeholder for a timeout
SOLVERS = (
    #{
    #    'type': 'local',
    #    'name': 'cvc4',
    #    'command': 'cvc4 --output-lang tptp --produce-models --tlimit=%md %s',
    #},
    {
        'type': 'local',
        'name': 'nitpick',
        'version': '2018',
        'pretty-name': 'Nitpick',
        'command': 'nitpick %d %s',
        'encoding': 'tptp-cnf',
    },
)

# a directory containing problems as Path object
# subdirectory structures are supported
basePath = Path(os.path.dirname(os.path.abspath(__file__))) / 'problems'
PROBLEMS = (
    (basePath / 'Sat1.cnf', 'Satisfiable'),
    #(basePath / 'Sat2.cnf', 'Satisfiable'),
    #(basePath / 'Sat3.cnf', 'Satisfiable'),
    #(basePath / 'Sat4.cnf', 'Satisfiable'),
    #(basePath / 'Sat5.cnf', 'Satisfiable'),
    #(basePath / 'Sat6.cnf', 'Satisfiable'),
    #(basePath / 'Sat7.cnf', 'Satisfiable'),
    #(basePath / 'Sat8.cnf', 'Satisfiable'),
    #(basePath / 'Unsat1.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat2.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat3.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat4.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat5.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat6.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat7.cnf', 'CounterSatisfiable'),
    #(basePath / 'Unsat8.cnf', 'CounterSatisfiable'),
)

# maximum wall clock time
WC_TIMEOUT = 60

# maximum cpu time
CPU_TIMEOUT = 60
