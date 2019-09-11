import os
import tempfile

from ..core import Problem


def modifyProblemSourceTemporary(problem:Problem):
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    f.write(problem.problem())
    problem._source = os.path.abspath(f.name)
    f.close()
