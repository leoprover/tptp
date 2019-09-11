from ...core import Problem


class Solver():
    def __init__(self, name:str, command:str):
        self._name = name
        self._command = command

    def __repr__(self):
        return ','.join([self._name, self._command])

    def name(self):
        return self._name

    def command(self):
        return self._command

    def call(self, problem:Problem, *, timeout):
        raise NotImplementedError()
