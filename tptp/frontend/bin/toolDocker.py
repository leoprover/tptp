from pathlib import Path
import subprocess

from ...core.problem import Problem
from ...reasoning import getDockerSolver, getDockerSolvers
from ...reasoning.dockerSolver import DockerSolver, DockerSolverCall
from .toolBase import CliToolBase

class CliToolDocker(CliToolBase):
    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def getInstance(cls):
        return cls('docker')

    def run(self, args):
        if args.task == 'list-solvers':
            for s in getDockerSolvers():
                print(s)
        elif args.task == 'build':
            solver = getDockerSolver(args.solver_name)

            cmd = 'cd {config}; docker build --rm -t tptp-solver/{name}:{version} .'.format(
                name=solver.name,
                config=solver.dockerConfig,
                version=solver.version,
            )
            subprocess.run(cmd,
                shell=True,
            )
        elif args.task == 'run':
            path = Path(args.problem)
            problem = Problem.readFromFile(path)
            solver = getDockerSolver(
                name=args.solver_name,
            )
            call = solver.call(problem, timeout=args.timeout)
            
            print('% SZS status Started for {}'.format(call))
            result = call.run()
            print(result.command)
            print('% SZS status {result}'.format(
                result=result,
            ))
            if result.exception:
                print(result.exception)
            if args.verbose:
                print(result.output)
                print(result.stderr)

    def parseArgs(self, toolParser):
        toolSubParsers = toolParser.add_subparsers()
        buildparser = toolSubParsers.add_parser('build')
        buildparser.set_defaults(task='build')
        buildparser.add_argument('--solver-name', help='name of the solver', required=True)

        requestparser = toolSubParsers.add_parser('run')
        requestparser.set_defaults(task='run')
        requestparser.add_argument('--solver-name', help='name of the solver', required=True)
        requestparser.add_argument('--problem', help='path to problem file', required=True)
        requestparser.add_argument('--timeout', help='timeout in seconds (default is 60)', type=int)
        requestparser.add_argument('--verbose',
            help='generates a more verbose output',
            action='store_const', default=False, const=True,
        )
        requestparser.set_defaults(timeout=60)

        listParser = toolSubParsers.add_parser('list-solvers')
        listParser.set_defaults(task='list-solvers')
