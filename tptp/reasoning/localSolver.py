from typing import List
import re

from ..encoding.encodingChooser import getEncoder
from ..core import Problem, TPTPDialect, SZSStatus, UnknownSZSStatusError
from .core import Solver, SolverCall, SolverType, SolverResult

from ..utils.concurrent.localProcess import LocalProcess

class LocalSolver(Solver):
    def __init__(self, name: str, *,
                 command: str,
                 version: str= None,
                 prettyName: str= None,
                 encoding: str=None,
                 inputLanguages: List[TPTPDialect]= [],
                 applications: List[SolverType]= [],
                 ):
        super().__init__(
            name=name, 
            prettyName=prettyName,
            command=command,
            version=version,
        )
        self._encoding = encoding
        self._inputLanguages = inputLanguages
        self._applications = applications

    def __repr__(self):
        return ', '.join([
            str(self._name), 
            str(self._prettyName),
            str(self._version),
            str(self._command), 
            ' '.join(map(lambda x: str(x), self._inputLanguages)), 
            ' '.join(map(lambda x: str(x), self._applications))],
        )

    @property
    def name(self):
        return self._name

    @property
    def command(self) -> str:
        return self._command

    @property
    def inputLanguages(self):
        return self._inputLanguages

    @property
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
        command:str,
    ):
        super().__init__(call, szs, cpu, wc)
        self._stdout = stdout
        self._stderr = stderr
        self._returnCode = returnCode
        self._exception = exception
        self._command = command

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    @property
    def output(self):
        return self.stdout

    @property
    def returnCode(self):
        return self._returnCode

    @property
    def exception(self):
        return self._exception

    @property
    def command(self):
        return self._command

class LocalSolverCall(SolverCall):
    def __init__(self, problem:Problem, *, solver:LocalSolver, timeout):
        self._problem = problem
        self._solver = solver
        self._timeout = timeout
        if solver._encoding:
            problem = getEncoder(problem, solver._encoding).encode(problem, tempSource=True).newProblem
        self._process = LocalProcess(
            timeout=timeout, 
            call=lambda t: self._generateCall(problem, timeout=t)
        )

    def _generateCall(self, problem, *, timeout) -> str:
        c0 = self._solver.command
        # filename
        c1 = c0.replace('%s', str(problem.source))
        # timeout in s
        c2 = c1.replace('%d', str(int(timeout)))
        # timeout in ms
        c3 = c2.replace('%md', str(int(timeout*1000)))

        return c3

    def isStarted(self) -> bool:
        return self._process.isStarted()

    def isRunning(self) -> bool:
        return self._process.isRunning()

    def isDone(self) -> bool:
        return self._process.isDone()

    def timeScheduled(self) -> float:
        return self._process.timeScheduled()

    def timeRunning(self) -> float:
        return self._process.timeRunning()

    def run(self):
        exception = None
        stdout = None
        stderr = None

        try:
            stdout, stderr, returncode = self._process.run()
        except Exception as e:
            exception = e
            returncode = None

        szs = SZSStatus.Unknown
        if stdout:
            g = re.search('% SZS status ([^\s]+)', stdout, re.I)
            if g:
                try:
                    szs = SZSStatus.get(g.group(1))
                except UnknownSZSStatusError:
                    pass

            #cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', stdout, re.I).group(1))
            #wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', stdout, re.I).group(1))
        if szs == SZSStatus.Unknown:
            if self._process.isTimeout():
                szs = SZSStatus.Timeout
            elif self._process.isInterupted():
                szs = SZSStatus.User
            elif exception:
                szs = SZSStatus.Error

        return LocalSolverResult(
            call=self,
            szs=szs,
            cpu=None, # TODO
            wc=self._process.timeRunning(),
            stdout=stdout,
            stderr=stderr,
            returnCode=returncode,
            exception=exception,
            command=self._process.estimatedCall(),
        )

    def cancel(self) -> None:
        self._process.cancel()

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
        return self._process.timeout()

    def estimatedTimeout(self) -> float:
        """
        Estimated timeout of the call. If the timeouts has allready been calculatd the result is equal to ```timeout()```.
        Otherwise timeout is precalulated and may be differ from the finally used timeout.
        :return:
        """
        return self._process.estimatedTimeout()
