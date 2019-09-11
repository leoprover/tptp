import os
from pathlib import Path

# type of the competition
COMPETITION_TYPE = "CASC"

# name of the competition
COMPETITION_NAME = "Test Competition"

# tuples of name and command of all solvers as list
# %s is the placeholder for a filename
# %d is the placeholder for a timeout
SOLVERS = (
    {
        'type': 'local',
        'name': 'cvc4',
        'command': 'cvc4 --output-lang tptp --produce-models --tlimit=%md %s',
    },
)

# a directory containing problems as Path object
# subdirectory structures are supported
basePath = Path(os.path.dirname(os.path.abspath(__file__))) / 'problems'
PROBLEMS = (
    (basePath / 'Sat1.cnf', 'Theorem'),
    (basePath / 'Unsat1.cnf', 'Unsatisfiable'),
)

# maximum wall clock time
WC_TIMEOUT = 60

# maximum cpu time
CPU_TIMEOUT = 60

