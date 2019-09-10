import argparse
from typing import List

from .toolSystemOnTPTP import CliToolSystemOnTPTP
from .toolLocalSolver import CliToolLocalSolver
from .toolBase import CliToolBase


def parse_args(tools:List[CliToolBase]):
    topLevelParser = argparse.ArgumentParser()
    topLevelSubParsers = topLevelParser.add_subparsers()

    actionList = {}
    for t in tools:
        instance = t.getInstance()
        toolParser = topLevelSubParsers.add_parser(instance.name())
        toolParser.set_defaults(tool=instance.name())
        toolSubParser = toolParser.add_subparsers()
        instance.parseArgs(toolSubParser)
        actionList[instance.name()] = instance.run

    args = topLevelParser.parse_args()
    return (args, actionList)


def main():
    activatedTools = [CliToolSystemOnTPTP, CliToolLocalSolver]
    args, actionList = parse_args(activatedTools)
    actionList[args.tool](args)


if __name__ == '__main__':
   main()
