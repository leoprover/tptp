import re

from .encodingResult import EncodingResult
from .encodingUtils import modifyProblemSourceTemporary
from ..core import Problem
from .encoder import Encoder


class DimacsEncoder(Encoder):
    def __init__(self, outputEncoding):
        self.outputEncoding = outputEncoding

    CLAUSE_PATTERN = re.compile('-[1-9]+|[1-9+]')
    def encode(self, problem:Problem, tempSource:bool=False):
        if self.outputEncoding != 'tptp-cnf':
            raise Exception(self.outputEncoding + " is not a valid output encoding from a dimacs file.")

        # only cnf for now
        # TODO explore this format
        contentLines = problem.problem().splitlines(keepends=False)
        counter = 0
        cnfSentences = []
        for l in contentLines:
            # empty lines
            if len(l.strip()) == 0:
                continue
            # comments
            elif l.startswith('c'):
                cnfSentences.append('%' + l[1:])
            # c
            elif l.startswith('p'):
                cnfSentences.append('% ' + l)
            # clause
            else:
                literals = re.findall(DimacsEncoder.CLAUSE_PATTERN, l)
                newLiterals = []
                for literal in literals:
                    # literal is negated
                    if literal.startswith('-'):
                        newLiterals.append('~l' + literal[1:])
                    # literal is not negated
                    else:
                        newLiterals.append('l' + literal)
                cnfSentences.append('cnf(' + str(counter) + ', axiom, ' + '|'.join(newLiterals) + ').')
                counter += 1
        encodedProblem = Problem(problem.name, problem, '\n'.join(cnfSentences))
        if tempSource:
            modifyProblemSourceTemporary(encodedProblem)
        return EncodingResult(problem, encodedProblem)
