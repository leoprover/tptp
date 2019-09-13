
from ...core import szs, ProblemWithStatus
from ...reasoning.localSolver import LocalSolverCall, LocalSolver
from ...reasoning import SolverResult, Solver

dummyResults = [
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('leo', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('leo', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('leo', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
    SolverResult(LocalSolverCall(ProblemWithStatus(None, None, None, szs.THM), solver=LocalSolver('satallax', command=None),
                                 timeout=None), szs.THM, 20.0, 30.0),
]