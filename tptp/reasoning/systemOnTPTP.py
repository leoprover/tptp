from typing import List
from lxml import html
import argparse
from pathlib import Path
import requests
import re

from .core.solverResult import SolverResult
from .core.solverCall import SolverCall
from .core.solverType import SolverType
from ..core.problem import Problem
from ..core.tptpInputLanguages import TPTPInputLanguage
from ..core.szs import SZSStatus
from ..reasoning.core.solver import Solver
from ..util.concurrent.httpRequest import AsyncPostRequest

class SystemOnTPTPSolver(Solver):
    def __init__(self, name: str, command: str, inputLanguages: List[TPTPInputLanguage],
                 applications: List[SolverType]):
        super().__init__(name, command)
        self._inputLanguages = inputLanguages
        self._applications = applications

    def __repr__(self):
        return ','.join([self._name, self._command, ' '.join(map(lambda x: str(x),self._inputLanguages)), ' '.join(map(lambda x: str(x),self._applications))])

    def name(self):
        return self._name

    def command(self):
        return self._command

    def inputLanguages(self):
        return self._inputLanguages

    def applications(self):
        return self._applications

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
        solverApplications.append(apps)
        try:
            formats = applicationText.split(', for ',1)[1].split(' ')
        except:
            formats = applicationText.split('For ',1)[1].split(' ')
        solverFormats.append(list(map(lambda f: TPTPInputLanguage(f), filter(lambda a: len(a) != 0, formats))))

    ret = []
    for name, command, formats, applications in zip(solverNames,solverCommands,solverFormats,solverApplications):
        ret.append(SystemOnTPTPSolver(name,command,formats,applications))
    return ret

class SystemOnTPTPSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float):
        super().__init__(call, szs, cpu, wc)

class SystemOnTPTPSolverCall(SolverCall):
    def __init__(self, solver:SystemOnTPTPSolver, problem:Problem, timeout):
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
        URL_SYSTEM_ON_TPTP_FORM = 'http://www.tptp.org/cgi-bin/SystemOnTPTPFormReply'
        if hasattr(self._timeout, '__call__'):
            self._calculatedTimeout = self._timeout()
        elif isinstance(self._timeout, int):
            self._calculatedTimeout = self._timeout
        payload = {
            'TPTPProblem': '',
            'ProblemSource': 'FORMULAE',
            'FORMULAEProblem': self._problem.problem(),
            'QuietFlag': '-q01',  # for output mode System
            # 'QuietFlag':'-q3', #for output mode Result
            'SubmitButton': 'RunSelectedSystems',
            'System___' + self._solver.name(): self._solver.name(),
            'TimeLimit___' + self._solver.name(): str(self._calculatedTimeout),
            'Command___' + self._solver.name(): self._solver.command(),
        }
        self._request = AsyncPostRequest(URL_SYSTEM_ON_TPTP_FORM, payload, self._calculatedTimeout)
        self._request.start()

    def result(self) -> SystemOnTPTPSolverResult:
        if not self._started:
            raise Exception("Reasoning call has not been started.")
        if self._request.cancelled():
            raise Exception("Reasoning call has been cancelled.")
        if not self._request.done():
            raise Exception("Reasoning call has not been finished.")
        # % RESULT: SOT_WZbJQt - Leo-III---1.4 says Theorem - CPU = 0.00 WC = 0.04
        self._response = self._request.result()
        results = re.findall('^% RESULT:.*', self._response.text , re.M)
        if results == []: # TODO better error reporting
            raise Exception("Response not interpretable: Could not find RESULT token.\n" + self._response.text)
        elif len(results) > 1:
            raise Exception("Response not interpretable: More than one RESULT token.\n" + self._response.text)
        szs = re.search('(?:.*says )(.*)(?: - CPU.*)', results[0], re.I).group(1)
        cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', results[0], re.I).group(1))
        wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', results[0], re.I).group(1))
        return SystemOnTPTPSolverResult(self, SZSStatus.get(szs), cpu, wc)

    def wait(self) -> None:
        self._request.wait()

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    requestparser = subparsers.add_parser('request')
    requestparser.set_defaults(task='request')
    requestparser.add_argument('--solver-name', help='name of the solver', required=True)
    requestparser.add_argument('--solver-command', help='command of the solver', required=True)
    requestparser.add_argument('--problem', help='path to problem file', required=True)
    requestparser.add_argument('--timeout', help='timeout in seconds (default is 60)', type=int)
    requestparser.set_defaults(timeout=60)

    listParser = subparsers.add_parser('list-solvers')
    listParser.set_defaults(task='list-solvers')

    args = parser.parse_args()
    return(args)

def main():
    # example arguments: request --solver-name "Leo-III---1.4" --solver-command "run_Leo-III %s %d" --problem "/home/tg/true.p" --timeout 60
    args = parse_args()
    if args.task == 'list-solvers':
        print(getSolvers())
    elif args.task == 'request':
        path = Path(args.problem)
        problem = Problem.readFromFile(path)
        solver = SystemOnTPTPSolver(args.solver_name, args.solver_command, [], [])
        call = SystemOnTPTPSolverCall(solver, problem, args.timeout)
        call.start()
        call.wait()
        result = call.result()
        print('CALL',call)
        print('RESULT',result)

if __name__ == '__main__':
   main()





