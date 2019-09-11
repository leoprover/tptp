from ..core import Problem


class EncodingResult():
    def __init__(self, oldProblem:Problem, newProblem: Problem):
        self.oldProblem = oldProblem
        self.newProblem = newProblem
