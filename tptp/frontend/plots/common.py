from typing import Iterable

from tptp.reasoning import SolverResult, Solver


def createDict(results:Iterable[SolverResult]):
    d = {}
    for r in results:
        if not r.call.solver in d:
            d[r.call.solver] = []
        d[r.call.solver].append(r)
    return d

def sortSolvers(solvers:Iterable[Solver]):
    return sorted(solvers, key=(lambda s: s.name + str(s.version)))

def sortedSolverNames(solvers:Iterable[Solver]):
    return list(map(lambda s: s.name + ' ' + s.version if s.version else s.name, sortSolvers(solvers)))