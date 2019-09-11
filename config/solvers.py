

SOLVERS = (
    {
        'type': 'local', 
        'name': 'leo3', 
        'pretty-name': 'Leo III', 
        'version': '1.4', 
        'command': 'leo3 %s -t %d',
    },
    {
        'type': 'local',
        'name': 'cvc4',
        'command': 'cvc4 --output-lang tptp --produce-models --tlimit=%md %s',
    },
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
)