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

    def call(self, problem_file, *, timeout) -> str:
        c0 = self._command
        c1 = c0.replace('%s', str(problem_file))
        c2 = c1.replace('%d', str(int(timeout)))

        return c2

class LocalSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, stdout:str, stderr:str, returnCode:int):
        super().__init__(call, szs, cpu, wc)
        self._stdout = stdout
        self._stderr = stderr
        self._returnCode = returnCode

    def stdout(self):
        return self._stdout

    def stderr(self):
        return self._stderr

    def returnCode(self):
        return self._returnCode

class LocalSolverCall(SolverCall):
    def __init__(self, problem:Problem, *, solver:LocalSolver, timeout):
        self._problem = problem
        self._process = LocalProcess(
            timeout=timeout, 
            call=lambda t: solver.call(problem.source(), timeout=t)
        )

    def started(self) -> bool:
        self._process.started()

    def running(self) -> bool:
        self._process.running()

    def done(self) -> bool:
        self._process.done()

    def run(self):
        stdout, stderr = self._process.run()
        call = self._process.calculatedCall()

        szs = re.search('% SZS status ([^ ]+)', stdout, re.I).group(1)
        #cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', stdout, re.I).group(1))
        #wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', stdout, re.I).group(1))

        return LocalSolverResult(
            call=call,
            szs=szs,
            cpu=self._process.wc(),
            wc=None,
            stdout=stdout,
            stderr=stderr,
            returnCode=0,
        )

    def cancle(self) -> None:
        self._process.cancle()

    def terminate(self) -> None:
        self._process.terminate()

    def kill(self) -> None:
        self._process.kill()

    def calculatedTimeout(self) -> float:
        """
        Returns calculated the timeout.
        If the reasoning call has not been started this method will throw an exception.
        Since a timeout can be a float or a callable object the timeout is evaluated when the method start is invoked.
        :return:
        """
        self._process.calculatedTimeout()

    def timeout(self):
        """
        Returns the timeout if it is a float or the callable object that calculates the timeout during the start method.
        :return:
        """
        self._process.timeout()
