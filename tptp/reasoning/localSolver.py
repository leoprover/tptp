from tptp.core.szs import SZSStatus
from tptp.reasoning import SolverResult

from tptp.utils.process import Process

class LocalSolver(Solver):
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

    def call(*, problem_file, timeout):
        c0 = self._command
        c1 = c0.replace('%s', problem_file)
        c2 = c1.replace('%d', timeout)

        return c2

class LocalSolverResult(SolverResult):
    def __init__(self, call, szs: SZSStatus, cpu: float, wc: float, stdout:str, stderr:str, returnCode:int):
        super().__init__(call, szs, cpu, wc)
        self._stdout = stdout
        self._stderr = stderr
        self._returnCode = returnCode

    def stdout(self):
        return self._stdout

    def stderr(self):
        return self._stderr

    def returnCode(self):
        return self._returnCode

class LocalSolverCall(SolverCall):
    def __init__(self, solver:LocalSolver, problem:Problem, timeout):
        self._problem = problem
        self._process = Process(
            timeout=timeout, 
            call=lambda t: solver.call(problem=problem, timeout=t)
        )

    def isStarted(self) -> bool:
        """
        Indicates whether the reasoning call has already started.
        A suspended call is considered started.
        :return:
        """
        self._process.isStarted()

    def isRunning(self) -> bool:
        self._process.isRunning()

    def done(self) -> bool:
        """
        Checks whether the reasoning call is finished and the reasoning result is available.
        :return:
        """
        self._process.isDone()       

    def run(self):
        stdout, stderr = self._process.run()
        call = self._process.calculatedCall()

        szs = re.search('(?:.*says )(.*)(?: - CPU.*)', stdout, re.I).group(1)
        cpu = float(re.search('(?:.*CPU = )(.*)(?: WC.*)', stdout, re.I).group(1))
        wc = float(re.search('(?:.*WC = )(\S*)(?: .*)', stdout, re.I).group(1))

        return LocalSolverResult(
            call=call,
            szs=szs,
            cpu=cpu,
            wc=wc,
            stdout=stdout,
            stderr=stderr,
            returnCode=0,
        )

    def terminate(self) -> None:
        """
        Cancels the reasoning call asking the recipient (CLI tool, etc.) of the reasoning call to terminate.
        # If the reasoning call has not been started this method will throw an exception.
        If the reasoning call has not been started the start will be prevented.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        """
        self._process.terminate()

    def kill(self) -> None:
        """
        Cancels the reasoning call without asking the the recipient (CLI tool, etc.) of the reasoning call to terminate.
        # If the reasoning call has not been started this method will throw an exception.
        If the reasoning call has not been started the start will be prevented.
        If the reasoning call is already finished this method doesnot have any effect.
        :return:
        """
        self._process.kill()

    def calculatedTimeout(self) -> float:
        """
        Returns calculated the timeout.
        If the reasoning call has not been started this method will throw an exception.
        Since a timeout can be a float or a callable object the timeout is evaluated when the method start is invoked.
        :return:
        """
        self._process.calculatedTimeout()

    def timeout(self):
        """
        Returns the timeout if it is a float or the callable object that calculates the timeout during the start method.
        :return:
        """
        self._process.timeout()

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
        solver = LocalSolver(args.solver_name, args.solver_command, [], [])
        call = LocalSolverCall(solver, problem, args.timeout)
        result = call.run()
        print('CALL',call)
        print('RESULT',result)

if __name__ == '__main__':
    main()
