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
    def __init__(self, solverName:str, solverCommand:str, inputLanguages:List[TPTPInputLanguage], applications:List[SolverType]):
        self.name = solverName
        self.command = solverCommand
        self.inputLanguages = inputLanguages
        self.applications = applications

    def __repr__(self):
        return ','.join([self.name, self.command, ' '.join(map(lambda x: str(x),self.inputLanguages)), ' '.join(map(lambda x: str(x),self.applications))])

    def getSolverName(self):
        return self.name

    def getSolverCommand(self):
        return self.command

    def getInputLanguages(self):
        return self.inputLanguages

    def getApplications(self):
        return self.applications

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
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, configuration=None):
        super().__init__(call, szs, cpu, wc, configuration)

class SystemOnTPTPSolverCall(SolverCall):
    def __init__(self, solver:SystemOnTPTPSolver, problem:Problem, timeout):
        self.solver = solver
        self.problem = problem
        self.timeout = timeout
        self.calculatedTimeout = None
        self.result = None
        self.started = False

    def __repr__(self):
        return str(self.solver) + str(self.calculatedTimeout)

    def start(self):
        self.started = True
        URL_SYSTEM_ON_TPTP_FORM = 'http://www.tptp.org/cgi-bin/SystemOnTPTPFormReply'
        if hasattr(self.timeout, '__call__'):
            self.calculatedTimeout = self.timeout()
        elif isinstance(self.timeout, int):
            self.calculatedTimeout = self.timeout
        payload = {
            'TPTPProblem': '',
            'ProblemSource': 'FORMULAE',
            'FORMULAEProblem': self.problem.getProblem(),
            'QuietFlag': '-q01',  # for output mode System
            # 'QuietFlag':'-q3', #for output mode Result
            'SubmitButton': 'RunSelectedSystems',
            'System___' + self.solver.getSolverName(): self.solver.getSolverName(),
            'TimeLimit___' + self.solver.getSolverName(): str(self.calculatedTimeout),
            'Command___' + self.solver.getSolverName(): self.solver.getSolverCommand(),
        }
        self.request = AsyncPostRequest(URL_SYSTEM_ON_TPTP_FORM, payload, self.calculatedTimeout)
        self.request.start()

    def result(self) -> SystemOnTPTPSolverResult:
        if not self.started:
            raise Exception("Reasoning call has not been started.")
        if self.request.cancelled():
            raise Exception("Reasoning call has been cancelled.")
        if not self.request.finished():
            raise Exception("Reasoning call has not been finished.")
        # % RESULT: SOT_WZbJQt - Leo-III---1.4 says Theorem - CPU = 0.00 WC = 0.04
        self.response = self.request.result()
        results = re.findall('^% RESULT:.*', self.response.text , re.M)
        if results == []: # TODO better error reporting
            raise Exception("Response not interpretable: Could not find RESULT token.\n" + self.response.text)
        elif len(results) > 1:
            raise Exception("Response not interpretable: More than one RESULT token.\n" + self.response.text)
        szs = re.search('(?:.*says )(.*)(?: - CPU.*)', results[0], re.I).group(1)
        cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', results[0], re.I).group(1))
        wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', results[0], re.I).group(1))
        return SystemOnTPTPSolverResult(self, SZSStatus.get(szs), cpu, wc)

    def wait(self) -> None:
        self.request.wait()

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





