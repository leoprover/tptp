import glob
import sys
from importlib.machinery import SourceFileLoader

from typing import List, Callable, Iterable
from pathlib import Path

from ..core import SZSStatus
from ..reasoning.localSolver import LocalSolver
from .competition import Competition
from ..reasoning import Solver, SolverResult, loadSolvers
from ..core import TPTPProblem, ProblemWithStatus

class CASC(Competition):
    def __init__(self, name: str, *, 
        solvers: List[Solver], 
        problems: List[TPTPProblem], 
        wcLimit: int, 
        cpuLimit: int,
        verbose: bool= False,
    ):
        super().__init__(name, solvers, problems, wcLimit, cpuLimit)
        self._results = []
        self._running = False
        self._resultCallbacks = []
        self._verbose = verbose

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

    def addResult(self, result:SolverResult):
        self._results.append(result)
        for c in self._resultCallbacks:
            c(self._results)

    def addResultCallback(self, callback:Callable[[List[SolverResult]], object]):
        self._resultCallbacks.append(callback)

    def resultString(self, results:List[SolverResult]):
        if len(results) == 0:
            print("No results so far.")
            return

        lastResult = results[len(results)-1]
        szsResultMatches = lastResult._szs.matches(lastResult._call._problem.szs())
        print('%', lastResult, "which is", szsResultMatches)

        # further output for error informations
        exception = lastResult.exception()
        if exception:
            print(exception, file=sys.stderr)
        if lastResult.szsStatus() == SZSStatus.get("Error"):
            print(lastResult.stdout(), file=sys.stderr)
            print(lastResult.stderr(), file=sys.stderr)
        elif self._verbose:
            print(lastResult.output())
            print(lastResult.stderr())

    def run(self):
        self._running = True
        wcLimit = self.wcLimit()
        self.addResultCallback(self.resultString)
        for p in self._problems:
            for s in self._solvers:
                call = s.call(p, timeout=wcLimit)
                result = call.run()
                self.addResult(result)
        self._running = False
        
    def results(self) -> List[SolverResult]:
        return self._results

    @staticmethod
    def configure(configurationModulePath:Path, *,
        verbose=False
    ):
        configuration = SourceFileLoader('configuration', str(configurationModulePath)).load_module()
        solvers = loadSolvers(configuration.SOLVERS)
        #problemPaths = [f for f in glob.glob(str(configuration.PROBLEM_PATH) + "/**/*.p", recursive=True)]
        #problems = list(map(lambda p: TPTPProblem.readFromFile(Path(p)),problemPaths))
        problems = list(map(lambda p: ProblemWithStatus(Path(p[0]).name, Path(p[0]).absolute(), None, SZSStatus.get(p[1])), configuration.PROBLEMS))
        return CASC(configuration.COMPETITION_NAME, 
            solvers=solvers, 
            problems=problems, 
            wcLimit=configuration.WC_TIMEOUT, 
            cpuLimit=configuration.CPU_TIMEOUT,
            verbose=verbose,
        )

def main(configurationModulePath:Path):
    casc = configure(configurationModulePath)
    print(casc)

if __name__ == '__main__':
   main(Path(sys.argv[1]))
