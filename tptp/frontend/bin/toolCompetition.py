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
        competitionInstance = competitionClass.configure(configurationModulePath, 
            verbose=args.verbose,
            silent=args.silent,
            colored=args.colored,
            outputDir=Path(args.output) if args.output else None
        )
        competitionInstance.run()

    def parseArgs(self, toolSubParser):
        toolSubParser.add_argument('configuration', 
            help='configuration file of the competition'
        )
        toolSubParser.add_argument('--verbose',
            help='generates a more verbose output',
            action='store_const', default=False, const=True,
        )
        toolSubParser.add_argument('--silent',
            help='does not output stdout or stderr of the underlaying prover, even in error cases',
            action='store_const', default=False, const=True,
        )
        toolSubParser.add_argument('--colored',
            help='prints with color',
            action='store_const', default=False, const=True,
        )
        toolSubParser.add_argument('--output', 
            help='dictionary where the output of the competition and all solvers should be stored',
            required=False,
        )
