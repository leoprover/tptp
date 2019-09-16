import glob
import sys
from importlib.machinery import SourceFileLoader

from typing import List, Callable, Iterable
from pathlib import Path

from ..frontend.statistics.competitionBarCharts import SolvedPerSolverChart
from ..core import SZSStatus
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
        outputDir: Path=None,
    ):
        super().__init__(name, solvers, problems, wcLimit, cpuLimit)
        self._results = []
        self._running = False
        self._resultCallbacks = []
        self._verbose = verbose
        self._silent = silent
        self._colored = colored
        self._outputDir = outputDir

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

    def addResultCallback(self, callback:Callable[[Iterable[SolverResult]], object]):
        self._resultCallbacks.append(callback)

    def getDefaultSolvedFigure(self):
        return SolvedPerSolverChart

    def resultString(self, results:List[SolverResult]):
        if len(results) == 0:
            print("No results so far.")
            return

        result = results[len(results)-1]
        call = result.call
        solver = call.solver
        problem = call.problem

        szsResult = result.szsStatus
        szsExspected = problem.szsStatus

        match = szsResult.matches(szsExspected)

        output = '% SZS status {result} which is {state} took {t}s'.format(
            result=result,
            state=match,
            t=int(result.wc),
        )
        if self._colored:
            print('{color}{output}{reset}'.format(
                output=output,
                color=self._color.Fore.GREEN if match.isCorrect() else (self._color.Fore.YELLOW if match.isSound() else self._color.Fore.RED),
                reset=self._color.RESET_ALL
            ))
        else:
            print(output)

        if self._outputDir:
            with open(self._outputDir / (solver.name + ".output"), "a") as f:
                print(output, file=f)
            with open(self._outputDir / (solver.name + "-" + problem.name + ".stdout"), "w") as f:
                print(result.stdout, file=f)
            with open(self._outputDir / (solver.name + "-" + problem.name + ".stderr"), "w") as f:
                print(result.stderr, file=f)
                if result.exception:
                    print(result.exception, file=f)

        # further output for error informations
        if result.exception:
            print(result.exception, file=sys.stderr)
        if not self._silent:
            if result.szsStatus == SZSStatus.Error:
                print(result.stdout, file=sys.stderr)
                print(result.stderr, file=sys.stderr)
            elif self._verbose:
                print(result.stdout)
                print(result.stderr)

        # flush chunked output
        sys.stdout.flush()
        sys.stderr.flush()

    def run(self):
        self._running = True
        wcLimit = self.wcLimit()
        self.addResultCallback(self.resultString)

        if self._outputDir:
            with open(self._outputDir / ("results.csv"), "a") as f:
                print('problem, exspected, ' + ', '.join(map(lambda s: str(s), self._solvers)), file=f)

        for p in self._problems:
            rs = []
            for s in self._solvers:
                call = s.call(p, timeout=wcLimit)
                print('% SZS status Started for {}'.format(call))

                result = call.run()
                rs.append(result.szsStatus)
                self.addResult(result)

            if self._outputDir:
                with open(self._outputDir / ("results.csv"), "a") as f:
                    print(p.name + ', ' + str(p.szsStatus) + ', ' + ', '.join(map(lambda s: str(s), rs)), file=f)
        self._running = False
        
    def results(self) -> List[SolverResult]:
        return self._results

    @staticmethod
    def configure(configurationModulePath:Path, *,
        verbose=False,
        silent=False,
        colored=False,
        outputDir: Path=None,
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
            outputDir=outputDir,
        )

