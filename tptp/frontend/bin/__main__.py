import argparse
import sys
from typing import List

from .toolEncoder import CliToolEncoder
from .toolSystemOnTPTP import CliToolSystemOnTPTP
from .toolLocalSolver import CliToolLocalSolver
from .toolCompetition import CliToolCompetition
from .toolBase import CliToolBase


def parse_args(tools:List[CliToolBase]):
    topLevelParser = argparse.ArgumentParser()
    topLevelSubParsers = topLevelParser.add_subparsers()

    actionList = {}
    for t in tools:
        instance = t.getInstance()
        toolParser = topLevelSubParsers.add_parser(instance.name())
        toolParser.set_defaults(tool=instance.name())
        instance.parseArgs(toolParser)
        actionList[instance.name()] = instance.run

    args = topLevelParser.parse_args()
    if not 'tool' in args: # check if the attribute 'tool' is available in args; otherwise an exception would be raised
        topLevelParser.print_help()
        sys.exit(1)
    return (args, actionList)


def main():
    activatedTools = [CliToolSystemOnTPTP, CliToolCompetition, CliToolLocalSolver, CliToolEncoder]
    args, actionList = parse_args(activatedTools)
    actionList[args.tool](args)


if __name__ == '__main__':
   main()
