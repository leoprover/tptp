class CliToolBase:
    """
    A tool can be invoked on the command line in the root directory by executing python3 -m tptp.frontend.bin.bin my-tool-name <optional_args>
    my-tool-name has to be defined through the constructor.
    <optional_args> are defined in the method parseArgs
    """
    def __init__(self, name:str):
        self._name = name

    def __repr__(self):
        return self._name

    def name(self):
        """
        The name as reflected in the arguments of the binary
        :return:
        """
        return self._name

    @classmethod
    def getInstance(cls):
        """
        Returns an instance of a class that inherits CliToolBase.
        :return:
        """
        raise NotImplementedError()

    def run(self, args):
        """

        :param args:
        :return:
        """
        raise NotImplementedError()

    def parseArgs(self, toolSubParser):
        """
        Adds a custom parser to the binary.

        myNewParser = toolSubParser.add_parser('mySubcommandName')
        myNewParser.set_defaults(myDefaultArgument='someValue')
        myNewParser.add_argument('--some-argument', help='myHelp')
        :param toolSubParser: a subparser from the library argparse
        :return:
        """
        raise NotImplementedError()
