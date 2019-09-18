from typing import List

from ..core import Problem, TPTPInputLanguage, SZSStatus, UnknownSZSStatusError
from .core import Solver, SolverCall, SolverType, SolverResult
from . localSolver import LocalSolver, LocalSolverResult, LocalSolverCall

class DockerSolver(LocalSolver):
    def __init__(self, name: str, *,
        dockerConfig: str,
        version: str,
        prettyName: str= None,
        encoding: str=None,
        inputLanguages: List[TPTPInputLanguage]= [],
        applications: List[SolverType]= [],
    ):
        command = 'cat %s | docker run -i tptp-solver/{name}:{version} - -t %d'.format(
            name=name,
            version=version,
        )

        super().__init__(
            name=name, 
            prettyName=prettyName,
            command=command,
            version=version,
            encoding=encoding,
            inputLanguages=inputLanguages,
            applications=applications,
        )
        self._dockerConfig = dockerConfig

    def call(self, problem:Problem, *, timeout):
        return DockerSolverCall(
            problem=problem,
            solver=self,
            timeout=timeout,
        )

    @property
    def dockerConfig(self):
        return self._dockerConfig

class DockerSolverResult(LocalSolverResult):
    pass

class DockerSolverCall(LocalSolverCall):
    pass
