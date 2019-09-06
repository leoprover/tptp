class Solver():
    def __init__(self, solverName:str, solverCommand:str):
        self.name = solverName
        self.command = solverCommand

    def __repr__(self):
        return ','.join([self.name, self.command])

    def getName(self):
        return self.name

    def getCommand(self):
        return self.command
