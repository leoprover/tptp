import os
from pathlib import Path

# type of the competition
COMPETITION_TYPE = "CASC"

# name of the competition
COMPETITION_NAME = "Chris' private CASC 2019"

# tuples of name and command of all solvers as list
# %s is the placeholder for a filename
# %d is the placeholder for a timeout
"""
SOLVERS = (
    {
        'type': 'local',
        'pretty-name': 'Leo-III',
        'name': 'leo',
        'version': '1.3',
        'command': 'leo3 %s -t %d',
    },
    {
        'type': 'local',
        'pretty-name': 'Satallax',
        'name': 'satallax',
        'version': '3.3',
        'command': 'satallax %s -t %d',
    },
)
"""
SOLVERS = (
    ("local""leo","leo3 %s -t %d"),
    ("satallax", "satallax %s -t %d")
)

# a directory containing problems as Path object
# subdirectory structures are supported
basePath = Path(os.path.dirname(os.path.abspath(__file__))) / 'problems'
PROBLEMS = (
    (basePath / 'problem1.p', 'Theorem'),
    (basePath / 'problem2.p', 'Theorem'),
)

# maximum wall clock time
WC_TIMEOUT = 60

# maximum cpu time
CPU_TIMEOUT = 60

