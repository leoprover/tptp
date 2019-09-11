from ..core import Problem
from .dimacs import DimacsEncoder


def getEncoder(problem:Problem, outputEncoding):
    """
    Returns an Encoder instance for a problem
    Exception if the encoding is not possible or available
    :param problem:
    :return:
    """
    return DimacsEncoder('tptp-cnf')