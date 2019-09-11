from pathlib import Path

from ...core.problem import Problem
from ...reasoning.localSolver import LocalSolver, LocalSolverCall
from .toolBase import CliToolBase
from ...reasoning import solvers

class CliToolLocalSolver(CliToolBase):
    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def getInstance(cls):
        return cls('local')

    def run(self, args):
        if args.task == 'list-solvers':
            print(solvers.getLocalSolvers())
        elif args.task == 'run':
            path = Path(args.problem)
            problem = Problem.readFromFile(path)
            solver = solvers.getLocalSolver(
                name=args.solver_name,
            )
            call = solver.call(problem, timeout=args.timeout)
            result = call.run()
            print('CALL', call)
            print('RESULT', result)
        elif args.task == 'request':
            path = Path(args.problem)
            problem = Problem.readFromFile(path)
            solver = LocalSolver(
                name=args.solver_name, 
                command=args.solver_command,
            )
            call = solver.call(problem, timeout=args.timeout)
            result = call.run()
            print('CALL', call)
            print('RESULT', result)

    def parseArgs(self, toolParser):
        toolSubParsers = toolParser.add_subparsers()
        requestparser = toolSubParsers.add_parser('request')
        requestparser.set_defaults(task='request')
        requestparser.add_argument('--solver-name', help='name of the solver', required=True)
        requestparser.add_argument('--solver-command', help='command of the solver', required=True)
        requestparser.add_argument('--problem', help='path to problem file', required=True)
        requestparser.add_argument('--timeout', help='timeout in seconds (default is 60)', type=int)
        requestparser.set_defaults(timeout=60)


        requestparser = toolSubParsers.add_parser('run')
        requestparser.set_defaults(task='run')
        requestparser.add_argument('--solver-name', help='name of the solver', required=True)
        requestparser.add_argument('--problem', help='path to problem file', required=True)
        requestparser.add_argument('--timeout', help='timeout in seconds (default is 60)', type=int)
        requestparser.set_defaults(timeout=60)

        listParser = toolSubParsers.add_parser('list-solvers')
        listParser.set_defaults(task='list-solvers')

