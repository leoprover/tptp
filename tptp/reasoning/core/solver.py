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

    def __repr__(self):
        return ', '.join([self._name, self._prettyName, self._version, self._command])

    def name(self):
        return self._name

    def command(self):
        return self._command

    def version(self):
        return self._version

    def prettyName(self):
        return self._prettyName
