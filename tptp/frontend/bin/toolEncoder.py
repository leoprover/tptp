from pathlib import Path

from ...encoding.encodingChooser import getEncoder
from ...core.problem import Problem
from .toolBase import CliToolBase

class CliToolEncoder(CliToolBase):
    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def getInstance(cls):
        return cls('encode')

    def run(self, args):
        # dimacs to tptp cnf only for now
        inputProblem = Problem.readFromFile(Path(args.input_file))
        encoder = getEncoder(inputProblem, args.output_encoding)
        encodingResult = encoder.encode(inputProblem)
        outPath = Path(args.output_file)
        outPath.write_text(encodingResult.newProblem.problem())


    def parseArgs(self, toolParser):
        toolParser.add_argument('--input-file', help='input file', required=True)
        toolParser.add_argument('--output-file', help='output file', required=True)
        toolParser.add_argument('--output-encoding', help='output encoding', required=True, choices=['tptp-cnf'])

