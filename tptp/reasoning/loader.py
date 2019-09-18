import pathlib
import os
from importlib.machinery import SourceFileLoader

from .localSolver import LocalSolver
from .systemOnTPTP import SystemOnTPTPSolver
from .dockerSolver import DockerSolver

HERE = pathlib.Path(__file__).parent

DEFAULT_SOLVER_PATH = os.path.abspath(HERE / ".." / ".." / "config" / "solvers.py")

class Solvers():
    """
    TODO speed this all up by lazy loading of config files.
    """
    def __init__(self):
        self._localSolvers = None
        self._systemOnTptpSolvers = None
        self._dockerSolvers = None
        self._isInit = False

    def init(self):
        if self._isInit:
            return
        self.loadDefaultSolvers()

    def loadDefaultSolvers(self):
        solvers = SourceFileLoader('solvers', DEFAULT_SOLVER_PATH).load_module()
        self._localSolvers, self._systemOnTptpSolvers, self._dockerSolvers = loadSolversAsDict(solvers.SOLVERS)
        
    def getLocalSolver(self, name):
        return self._localSolvers.get(name, None)

    def getSystemOnTptpSolver(self, name):
        return self._systemOnTptpSolvers.get(name, None)

    def getDockerSolver(self, name):
        return self._dockerSolvers.get(name, None)

"""
Singelton pattern
"""
_solvers__singelton = Solvers()
def _solvers():
    _solvers__singelton.init()
    return _solvers__singelton

def loadSolversAsDict(solverDefinitions):
    _localSolvers = {}
    _systemOnTptpSolvers = {}
    _dockerSolvers = {}

    for s in solverDefinitions:
        if s['type'] == 'local':
            name = s['name']
            _localSolvers[name] = LocalSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                version = s.get('version', None),
                command = s['command'],
            )
        elif s['type'] == 'system-on-tptp':
            name = s['name']
            _systemOnTptpSolvers[name] = SystemOnTPTPSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                systemOnTPTPName = s['system-on-tptp-name'],
                version = s.get('version', None),
                command = s['command'],
            )
        else:
            name = s['name']
            _dockerSolvers[name] = DockerSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                version = s.get('version', None),
                dockerConfig = s['docker-config'],
            )

    return _localSolvers, _systemOnTptpSolvers, _dockerSolvers

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
        elif s['type'] == 'system-on-tptp':
            name = s['name']
            _solvers.append(SystemOnTPTPSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                systemOnTPTPName = s['system-on-tptp-name'],
                version = s.get('version', None),
                command = s['command'],
            ))
        else:
            name = s['name']
            _solvers.append(DockerSolver(
                name = name, 
                prettyName = s.get('pretty-name', None),
                version = s.get('version', None),
                dockerConfig = s['docker-config'],
            ))

    return _solvers

def getLocalSolvers():
    return _solvers()._localSolver

def getDockerSolvers():
    return _solvers()._dockerSolvers

def getSystemOnTptpSolvers():
    return _solvers()._systemOnTptpSolver

def getLocalSolver(name):
    return _solvers().getLocalSolver(name)

def getSystemOnTptpSolver(name):
    return _solvers().getSystemOnTptpSolver(name)

def getDockerSolver(name):
    return _solvers().getDockerSolver(name)
