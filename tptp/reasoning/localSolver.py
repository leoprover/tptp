from typing import List
import re

from ..core import Problem, TPTPInputLanguage, SZSStatus
from .core import Solver, SolverCall, SolverType, SolverResult

from ..utils.concurrent.localProcess import LocalProcess

class LocalSolver(Solver):
    def __init__(self, name: str, command: str, inputLanguages: List[TPTPInputLanguage],
                 applications: List[SolverType]):
        super().__init__(name, command)
        self._inputLanguages = inputLanguages
        self._applications = applications

    def __repr__(self):
        return ','.join([self._name, self._command, ' '.join(map(lambda x: str(x),self._inputLanguages)), ' '.join(map(lambda x: str(x),self._applications))])

    def name(self):
        return self._name

    def command(self) -> str:
        return self._command

    def inputLanguages(self):
        return self._inputLanguages

    def applications(self):
        return self._applications

    def call(self, problem:Problem, *, timeout):
        return LocalSolverCall(
            problem=problem,
            solver=self,
            timeout=timeout,
        )

class LocalSolverResult(SolverResult):
    def __init__(self, *, 
        call, 
        szs: SZSStatus, 
        cpu: float, 
        wc: float, 
        stdout:str, 
        stderr:str, 
        returnCode:int,
        exception:Exception,
    ):
        super().__init__(call, szs, cpu, wc)
        self._stdout = stdout
        self._stderr = stderr
        self._returnCode = returnCode
        self._exception = exception

    def stdout(self):
        return self._stdout

    def stderr(self):
        return self._stderr

    def returnCode(self):
        return self._returnCode

    def exception(self):
        return self._exception

class LocalSolverCall(SolverCall):
    def __init__(self, problem:Problem, *, solver:LocalSolver, timeout):
        self._problem = problem
        self._solver = solver
        self._timeout = timeout
        self._process = LocalProcess(
            timeout=timeout, 
            call=lambda t: self._generateCall(problem, timeout=t)
        )

    def _generateCall(self, problem, *, timeout) -> str:
        c0 = self._solver.command()
        c1 = c0.replace('%s', str(problem.source()))
        c2 = c1.replace('%d', str(int(timeout)))

        return c2

    def started(self) -> bool:
        self._process.isStarted()

    def running(self) -> bool:
        self._process.isRunning()

    def done(self) -> bool:
        self._process.isDone()

    def run(self):
        exception = None
        stdout = None
        stderr = None

        try:
            stdout, stderr, returncode = self._process.run()
        except Exception(e):
            exception = e

        call = self._process.calculatedCall()
        if stdout:
            szs = re.search('% SZS status ([^ ]+)', stdout, re.I).group(1)      
            #cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', stdout, re.I).group(1))
            #wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', stdout, re.I).group(1))      
        elif self._process.isTimeout():
            szs = "Timeout"
        elif self._process.isInterupted():
            szs = "User"
        else:
            raise NotImplementedError()

        return LocalSolverResult(
            call=call,
            szs=szs,
            cpu=None,
            wc=self._process.timeRunning(),
            stdout=stdout,
            stderr=stderr,
            returnCode=returncode,
            exception=exception,
        )

    def cancle(self) -> None:
        self._process.cancle()

    def terminate(self) -> None:
        self._process.terminate()

    def kill(self) -> None:
        self._process.kill()

    def timeout(self) -> float:
        """
        Returns calculated the timeout.
        If the reasoning call has not been started this method will throw an exception.
        Since a timeout can be a float or a callable object the timeout is evaluated when the method start is invoked.
        :return:
        """
        self._process.timeout()

    def estimatedTimeout(self):
        """
        Estimated timeout of the call. If the timeouts has allready been calculatd the result is equal to ```timeout()```.
        Otherwise timeout is precalulated and may be differ from the finally used timeout.
        :return:
        """
        self._process.estimatedTimeout()
