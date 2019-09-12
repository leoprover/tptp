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
        silent:bool= False,
        colored: bool= False,
    ):
        super().__init__(name, solvers, problems, wcLimit, cpuLimit)
        self._results = []
        self._running = False
        self._resultCallbacks = []
        self._verbose = verbose
        self._silent = silent
        self._colored = colored

        if self._colored:
            from ..utils import color
            self._color = color

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

        output = '% SZS status {result} which is {state}'.format(
            result=lastResult,
            state="correct" if szsResultMatches else "wrong",
        )
        if self._colored:
            print('{color}{output}{reset}'.format(
                output=output,
                color=self._color.Fore.GREEN if szsResultMatches else self._color.Fore.RED,
                reset=self._color.RESET_ALL
            ))
        else:
            print(output)

        # further output for error informations
        exception = lastResult.exception()
        if exception:
            print(exception, file=sys.stderr)
        if not self._silent:
            if lastResult.szsStatus() == SZSStatus.get("Error"):
                print(lastResult.stdout(), file=sys.stderr)
                print(lastResult.stderr(), file=sys.stderr)
            elif self._verbose:
                print(lastResult.output())
                print(lastResult.stderr())

        # flush chunked output
        sys.stdout.flush()
        sys.stderr.flush()

    def run(self):
        self._running = True
        wcLimit = self.wcLimit()
        self.addResultCallback(self.resultString)
        for p in self._problems:
            for s in self._solvers:
                call = s.call(p, timeout=wcLimit)
                print('% SZS status Started for {}'.format(call))

                result = call.run()
                self.addResult(result)
        self._running = False
        
    def results(self) -> List[SolverResult]:
        return self._results

    @staticmethod
    def configure(configurationModulePath:Path, *,
        verbose=False,
        silent=False,
        colored=False,
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
            silent=silent,
            colored=colored,
        )

