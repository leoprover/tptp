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
    {
        'type': 'local',
        'name': 'satisfiable-dummy',
        'command': './solvers/satisfiable-dummy.sh %s -t %d',
    },
    {
        'type': 'local',
        'name': 'unsatisfiable-dummy',
        'command': './solvers/unsatisfiable-dummy.sh %s -t %d',
    },
#    {
#        'type': 'local',
#        'name': 'picosat',
#        'command': './solvers/picosat-tptp.sh -L %d %s',
#    },
#    {
#        'type': 'local',
#        'name': 'nitpick',
#        'version': '2018',
#        'pretty-name': 'Nitpick',
#        'command': 'nitpick %d %s',
#        'encoding': 'tptp-cnf',
#    },
)

# a directory containing problems as Path object
# subdirectory structures are supported
basePath = Path(os.path.dirname(os.path.abspath(__file__))) / 'problems'
PROBLEMS = (
    (basePath / 'Sat1.cnf', 'Satisfiable'),
    (basePath / 'Sat2.cnf', 'Satisfiable'),
    (basePath / 'Sat3.cnf', 'Satisfiable'),
    (basePath / 'Sat4.cnf', 'Satisfiable'),
    (basePath / 'Sat5.cnf', 'Satisfiable'),
    (basePath / 'Sat6.cnf', 'Satisfiable'),
    (basePath / 'Sat7.cnf', 'Satisfiable'),
    (basePath / 'Sat8.cnf', 'Satisfiable'),
    (basePath / 'Unsat1.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat2.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat3.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat4.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat5.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat6.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat7.cnf', 'Unsatisfiable'),
    (basePath / 'Unsat8.cnf', 'Unsatisfiable'),
)

# maximum wall clock time
WC_TIMEOUT = 60

# maximum cpu time
CPU_TIMEOUT = 60
