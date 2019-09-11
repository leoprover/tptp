import sys
from importlib._bootstrap_external import SourceFileLoader
from pathlib import Path

from .toolBase import CliToolBase
from ...competition import casc


class CliToolCompetition(CliToolBase):
    # keys: COMPETITION_TYPE as declared in the configuration file
    # values: competition class that inherits from class Competition
    AVAILABLE_COMPETITIONS = {
        "CASC": casc.CASC
    }

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def getInstance(cls):
        return cls('competition')

    def run(self, args):
        configurationModulePath = Path(args.configuration)
        configuration = SourceFileLoader('configuration', str(configurationModulePath)).load_module()
        if not configuration.COMPETITION_TYPE in CliToolCompetition.AVAILABLE_COMPETITIONS:
            print("Competition type " + configuration.COMPETITION_TYPE + " is not supported. Please choose from " + str(sorted(CliToolCompetition.AVAILABLE_COMPETITIONS.keys())) + ".")
            sys.exit(1)
        competitionClass = CliToolCompetition.AVAILABLE_COMPETITIONS.get(configuration.COMPETITION_TYPE)
        print(competitionClass)
        competitionInstance = competitionClass.configure(configurationModulePath)
        competitionInstance.run()

    def parseArgs(self, toolSubParser):
        toolSubParser.add_argument('configuration', help='configuration file of the competition')
