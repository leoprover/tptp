import glob
import sys
from importlib.machinery import SourceFileLoader

from typing import List
from pathlib import Path

from .competition import Competition
from ..reasoning import SolverResult
from ..reasoning.core.solver import Solver
from ..core.problem import TPTPProblem

class CASC(Competition):
    def __init__(self, name: str, solvers: List[Solver], problems: List[TPTPProblem], wcLimit: int, cpuLimit: int):
        super().__init__(name, solvers, problems, wcLimit, cpuLimit)
        self._results = []

    def __repr__(self):
        sb = []
        sb.append("competition mode: CASC")
        sb.append("competition name: " + self._name)
        sb.append("competition WC limit: " + str(self._wcLimit))
        sb.append("competition CPU limit: " + str(self._cpuLimit))
        sb.append("competition reasoners:")
        sb.extend(sorted(list(map(lambda s: '    ' + s.name(), self._solvers))))
        sb.append("competition problems:")
        sb.extend(sorted(list(map(lambda p: '    ' + p.name(), self._problems))))
        return '\n'.join(sb)

    @staticmethod
    def configure(configurationModulePath:Path):
        configuration = SourceFileLoader('configuration', str(configurationModulePath)).load_module()
        solvers = list(map(lambda t: Solver(t[0], t[1]), configuration.SOLVERS))
        problemPaths = [f for f in glob.glob(str(configuration.PROBLEM_PATH) + "/**/*.p", recursive=True)]
        problems = list(map(lambda p: TPTPProblem.readFromFile(Path(p)),problemPaths))
        return CASC(configuration.COMPETITION_NAME, solvers, problems, configuration.WC_TIMEOUT, configuration.CPU_TIMEOUT)

    def addResult(self, result:SolverResult):
        self._results.append(result)

    def test(self):
        raise NotImplementedError
    def start(self):
        raise NotImplementedError
    def wait(self):
        raise NotImplementedError
    def cancel(self):
        raise NotImplementedError
    def done(self) -> bool:
        raise NotImplementedError
    def running(self) -> bool:
        raise NotImplementedError
    def cancelled(self) -> bool:
        raise NotImplementedError
    def results(self) -> List[SolverResult]:
        raise NotImplementedError


def main(configurationModulePath:Path):
    casc = CASC.configure(configurationModulePath)
    print(casc)

if __name__ == '__main__':
   main(Path(sys.argv[1]))