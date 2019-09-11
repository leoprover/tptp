from typing import List
from pathlib import Path
from copy import deepcopy

from ..reasoning import SolverResult
from ..reasoning.core.solver import Solver
from ..core.problem import Problem


class Competition:
    def __init__(self, name:str, solvers:List[Solver], problems:List[Problem], wcLimit:int, cpuLimit:int):
        self._name = name
        self._solvers = solvers
        self._problems = problems
        self._wcLimit = wcLimit
        self._cpuLimit = cpuLimit
    
    def __repr__(self):
        return "Competition: " + self._name
    
    @staticmethod
    def configure(configurationModulePath:Path, *,
        verbose=False,
    ):
        """
        
        :param configurationModulePath: 
        :return: 
        """
        raise NotImplementedError
    
    def test(self):
        """
        tests all provers of the competition on a small set of problems for functionality
        :return:
        """
        raise NotImplementedError
    def start(self):
        """
        starts the competition
        :return:
        """
        raise NotImplementedError
    def wait(self):
        """
        blocks until all results are available i.e. competition is done
        :return:
        """
        raise NotImplementedError
    def cancel(self):
        """

        :return:
        """
        raise NotImplementedError
    def done(self) -> bool:
        """
        Cancelled or finished execution
        :return:
        """
        raise NotImplementedError
    def running(self) -> bool:
        """
        still executing
        :return:
        """
        raise NotImplementedError
    def cancelled(self) -> bool:
        """
        cancelled
        :return:
        """
        raise NotImplementedError
    
    def results(self) -> List[SolverResult]:
        raise NotImplementedError

    def name(self) -> str:
        return self._name

    def solvers(self) -> List[Solver]:
        return deepcopy(self._solvers)

    def problems(self) -> List[Problem]:
        return deepcopy((self._problems))

    def wcLimit(self) -> int:
        return self._wcLimit

    def cpuLimit(self) -> int:
        return self.cpuLimit()
