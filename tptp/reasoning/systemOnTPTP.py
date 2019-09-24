from typing import List
from lxml import html
import requests
import re

from ..core import UnknownSZSStatusError
from ..encoding.encodingChooser import getEncoder
from ..core import Problem, TPTPDialect, SZSStatus
from .core import Solver, SolverCall, SolverType, SolverResult

from ..utils.concurrent.httpRequest import AsyncPostRequest

class SystemOnTPTPSolver(Solver):
    def __init__(self, name: str, *,
                 systemOnTPTPName: str,
                 command: str,
                 version: str= None,
                 prettyName: str= None,
                 encoding: str=None,
                 inputLanguages: List[TPTPDialect]= [],
                 applications: List[SolverType]= [],
                 ):
        super().__init__(
            name=name,
            prettyName=prettyName,
            command=command, 
            version=version,
        )
        self._encoding=encoding
        self._systemOnTPTPName = systemOnTPTPName
        self._inputLanguages = inputLanguages
        self._applications = applications

    def __repr__(self):
        return ', '.join([
            str(self._name), 
            str(self._prettyName),
            str(self._systemOnTPTPName),
            str(self._version),
            str(self._command), 
            ' '.join(map(lambda x: str(x),self._inputLanguages)), 
            ' '.join(map(lambda x: str(x),self._applications))],
        )

    @property
    def name(self):
        return self._name

    @property
    def systemOnTPTPName(self):
        return self._systemOnTPTPName

    @property
    def command(self):
        return self._command

    @property
    def inputLanguages(self):
        return self._inputLanguages

    @property
    def applications(self):
        return self._applications

    def call(self, problem:Problem, *, timeout):
        return SystemOnTPTPSolverCall(
            problem=problem, 
            solver=self, 
            timeout=timeout
        )

class SystemOnTPTPMalfunctionError(Exception):
    pass

def getSolvers() -> List[SystemOnTPTPSolver]:
    URL_SYSTEM_ON_TPTP = 'http://www.tptp.org/cgi-bin/SystemOnTPTP' # TODO put this into a config
    site = requests.get(URL_SYSTEM_ON_TPTP)
    tree = html.fromstring(site.text)
    listOfInputElements = tree.xpath('//input')

    solverNames = []
    solverCommands = []
    solverFormats = []
    solverApplications = []

    for inputElement in listOfInputElements:
        if inputElement.name.startswith('System___'):
            solverNames.append((inputElement.xpath('@value'))[0])
        elif inputElement.name.startswith('Command___'):
            solverCommands.append((inputElement.xpath('@value'))[0])
        else:
            continue

    solverApplicationElements = tree.xpath('//font[@size="-1"]/text()')
    for applicationText in solverApplicationElements:
        apps = []
        if 'prover' in applicationText.lower():
            apps.append(SolverType('prover'))
        if 'finder' in applicationText.lower():
            apps.append(SolverType('model finder'))
        # solverApplications.append(apps) # TODO when top-level capability architecture is fixed
        solverApplications.append(None)
        try:
            formats = applicationText.split(', for ',1)[1].split(' ')
        except:
            formats = applicationText.split('For ',1)[1].split(' ')
        # solverFormats.append(list(map(lambda f: TPTPDialect(f), filter(lambda a: len(a) != 0, formats)))) # TODO when top-level capability architecture is fixed
        solverFormats.append(None)

    ret = []
    for name, command, formats, applications in zip(solverNames,solverCommands,solverFormats,solverApplications):
        ret.append(SystemOnTPTPSolver(
            name=name,
            systemOnTPTPName=name,
            command=command,
            inputLanguages=formats,
            applications=applications
        ))
    return ret

class SystemOnTPTPSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, response):
        super().__init__(call, szs, cpu, wc)

        self._response = response

    def output(self):
        return self._response

class SystemOnTPTPSolverCall(SolverCall):
    def __init__(self, problem:Problem, *, solver:SystemOnTPTPSolver, timeout):
        self._solver = solver
        self._problem = problem
        self._timeout = timeout
        self._calculatedTimeout = None
        self._result = None
        self._started = False

    def __repr__(self):
        return str(self._solver) + str(self._calculatedTimeout)

    def start(self):
        self._started = True
        if self._solver._encoding:
            problem = getEncoder(self._problem, self._solver._encoding).encode(self._problem).newProblem
        else:
            problem = self._problem.problem()
        URL_SYSTEM_ON_TPTP_FORM = 'http://www.tptp.org/cgi-bin/SystemOnTPTPFormReply'
        if hasattr(self._timeout, '__call__'):
            self._calculatedTimeout = self._timeout()
        elif isinstance(self._timeout, int):
            self._calculatedTimeout = self._timeout
        payload = {
            'TPTPProblem': '',
            'ProblemSource': 'FORMULAE',
            'FORMULAEProblem': problem,
            'QuietFlag': '-q01',  # for output mode System
            # 'QuietFlag':'-q3', #for output mode Result
            'SubmitButton': 'RunSelectedSystems',
            'System___' + self._solver.systemOnTPTPName: self._solver.systemOnTPTPName,
            'TimeLimit___' + self._solver.systemOnTPTPName: str(self._calculatedTimeout),
            'Command___' + self._solver.systemOnTPTPName: self._solver.command,
        }
        self._request = AsyncPostRequest(URL_SYSTEM_ON_TPTP_FORM, payload, self._calculatedTimeout)
        self._request.start()

    SYSTEM_ON_TPTP_RESULT_PATTERN = re.compile(r'^% RESULT:.*says\s+(\S+)\s+-\s+CPU\s+=\s+(\d+\.\d+)\s+WC\s+=\s+(\d+\.\d+).*', re.MULTILINE)
    def result(self) -> SystemOnTPTPSolverResult:
        if not self._started:
            raise Exception('Reasoning call has not been started.')
        if self._request.cancelled():
            raise Exception('Reasoning call has been cancelled.')
        if not self._request.done():
            raise Exception('Reasoning call has not been finished.')
        # % RESULT: SOT_WZbJQt - Leo-III---1.4 says Theorem - CPU = 0.00 WC = 0.04
        response = self._request.result()
        print(response.text)
        try:
            szs, cpu, wc = re.search(SystemOnTPTPSolverCall.SYSTEM_ON_TPTP_RESULT_PATTERN, response.text).groups()
        except:
            raise SystemOnTPTPMalfunctionError('Response not interpretable: Could not match RESULT line.\n' + response.text)
        try:
            szsSingleton = SZSStatus.get(szs)
        except UnknownSZSStatusError:
            raise SystemOnTPTPMalfunctionError('Response not interpretable: SZS status ' + szs + ' is not interpretable.\n' + response.text)

        return SystemOnTPTPSolverResult(self, 
            szs=szsSingleton,
            cpu=cpu, 
            wc=wc,
            response=response,
        )

    def wait(self) -> None:
        self._request.wait()

    def run(self) -> SystemOnTPTPSolverResult:
        self.start()
        self.wait()
        return self.result()

    def estimatedTimeout(self):
        if self._calculatedTimeout:
            return self._calculatedTimeout
        if hasattr(self._timeout, '__call__'):
            return self._timeout()
        return self._timeout
