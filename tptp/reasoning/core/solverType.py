class SolverType: # TODO singleton # TODO where to put this?
    def __init__(self,type):
        self.type = type
    def __repr__(self):
        return self.type