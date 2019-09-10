import os
from pathlib import Path

# type of the competition
COMPETITION_TYPE = "CASC"

# name of the competition
COMPETITION_NAME = "Chris' private CASC 2019"

# tuples of name and command of all solvers as list
# %s is the placeholder for a filename
# %d is the placeholder for a timeout
SOLVERS = [
    ("leo","leo3 %s -t %d"),
    ("satallax", "satallax %s -t %d")
]

# a directory containing problems as Path object
# subdirectory structures are supported
PROBLEM_PATH = Path(os.path.dirname(os.path.abspath(__file__))) / "problems"

# maximum wall clock time
WC_TIMEOUT = 60

# maximum cpu time
CPU_TIMEOUT = 60

