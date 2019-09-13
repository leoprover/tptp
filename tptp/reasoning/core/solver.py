from ...core import Problem


class Solver():
    def __init__(self, name:str, *,
        command:str,
        version:str= None, 
        prettyName:str= None,
    ):
        self._name = name
        self._prettyName = prettyName
        self._command = command
        self._version = version

    def __hash__(self):
        return hash(self._name + str(self._version))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return ', '.join([self._name, self._prettyName, self._version, self._command])

    def __str__(self):
        return '{name}{version}'.format(
            name=self._prettyName if self._prettyName else self._name,
            version=" "+str(self._version) if self._version else '',
        )

    @property
    def name(self):
        return self._name

    @property
    def command(self):
        return self._command

    @property
    def version(self):
        return self._version

    @property
    def prettyName(self):
        return self._prettyName

    @property
    def call(self, problem:Problem, *, timeout):
        raise NotImplementedError()
