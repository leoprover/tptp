import pathlib
import os
from importlib.machinery import SourceFileLoader

from .localSolver import LocalSolver
from .systemOnTPTP import SystemOnTPTPSolver

HERE = pathlib.Path(__file__).parent

DEFAULT_SOLVER_PATH = os.path.abspath(HERE / ".." / ".." / "config" / "solvers.py")

class Solvers():
    """
    TODO speed this all up by lazy loading of config files.
    """
    def __init__(self):
        self._localSolver = None
        self._systemOnTptpSolver = None
        self._isInit = False

    def init(self):
        if self._isInit:
            return
        self.loadDefaultSolvers()

    def loadDefaultSolvers(self):
        solvers = SourceFileLoader('solvers', DEFAULT_SOLVER_PATH).load_module()
        self._localSolver, self._systemOnTptpSolver = loadSolversAsDict(solvers.SOLVERS)
        
    def getLocalSolver(self, name):
        return self._localSolver.get(name, None)

    def getSystemOnTptpSolver(self, name):
        return self._systemOnTptpSolver.get(name, None)

"""
Singelton pattern
"""
_solvers__singelton = Solvers()
def _solvers():
    _solvers__singelton.init()
    return _solvers__singelton

def loadSolversAsDict(solverDefinitions):
    _localSolver = {}
    _systemOnTptpSolver = {}

    for s in solverDefinitions:
        if s['type'] == 'local':
            name = s['name']
            _localSolver[name] = LocalSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                version = s.get('version', None),
                command = s['command'],
            )
        else:
            name = s['name']
            _systemOnTptpSolver[name] = SystemOnTPTPSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                systemOnTPTPName = s['system-on-tptp-name'],
                version = s.get('version', None),
                command = s['command'],
            )

    return _localSolver, _systemOnTptpSolver

def loadSolvers(solverDefinitions, split=False):
    _solvers = []

    for s in solverDefinitions:
        if s['type'] == 'local':
            name = s['name']
            _solvers.append(LocalSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                version = s.get('version', None),
                command = s['command'],
                encoding = s.get('encoding', None),
            ))
        else:
            name = s['name']
            _solvers.append(SystemOnTPTPSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                systemOnTPTPName = s['system-on-tptp-name'],
                version = s.get('version', None),
                command = s['command'],
            ))

    return _solvers

def getLocalSolvers():
    return _solvers()._localSolver

def getSystemOnTptpSolvers():
    return _solvers()._systemOnTptpSolver

def getLocalSolver(name):
    return _solvers().getLocalSolver(name)

def getSystemOnTptpSolver(name):
    return _solvers().getSystemOnTptpSolver(name)
