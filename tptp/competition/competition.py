from typing import List
from pathlib import Path

from ..reasoning import SolverResult
from ..reasoning.core.solver import Solver
from ..core.problem import Problem


class Competition:
    def __init__(self, name:str, solvers:List[Solver], problems:List[Problem], wcLimit:int, cpuLimit:int):
        self.name = name
        self.solvers = solvers
        self.problems = problems
        self.wcLimit = wcLimit
        self.cpuLimit = cpuLimit

    @staticmethod
    def load(configurationModulePath:Path):
        raise NotImplementedError
    def test(self):
        '''
        tests all provers of the competition on a small set of problems for functionality
        :return:
        '''
        raise NotImplementedError
    def start(self):
        '''
        starts the competition
        :return:
        '''
        raise NotImplementedError
    def wait(self):
        '''
        blocks until all results are available i.e. competition is done
        :return:
        '''
        raise NotImplementedError
    def cancel(self):
        raise NotImplementedError
    def done(self) -> bool:
        '''
        Cancelled or finished execution
        :return:
        '''
        raise NotImplementedError
    def running(self) -> bool:
        '''
        still executing
        :return:
        '''
        raise NotImplementedError
    def cancelled(self) -> bool:
        '''
        cancelled
        :return:
        '''
        raise NotImplementedError
    def results(self) -> List[SolverResult]:
        raise NotImplementedError



