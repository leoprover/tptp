import re
from pathlib import Path
from .szs import SZSStatus

class InvalidSourceError(Exception):
    pass

class Problem:
    def __init__(self, name:str, source, problem:str):
        self._name = name
        self._source = source
        self._problem = problem

    def __repr__(self):
        return self._name

    def problem(self):
        if not self._problem:
            try:
                path = Path(self._source)
                self._problem = path.read_text()
            except Exception as e:
                raise InvalidSourceError(e)
        return self._problem

    @property
    def name(self):
        return self._name

    @property
    def source(self):
        return self._source

    @classmethod
    def readFromFile(cls,path:Path):
        fileContent = path.read_text()
        return cls(str(path.name), path.absolute(), fileContent)

class ProblemWithStatus(Problem):
    def __init__(self, name: str, source, problem: str, szs:SZSStatus):
        super().__init__(name, source, problem)
        self._szs = szs

    def __repr__(self):
        return self._name + " " + str(self._szs)

    def __str__(self):
        return '{name} expecting {szs}'.format(
            name=self._name,
            szs=self._szs,
        )

    def szs(self):
        """
        @depricated use szsStatus
        """
        return self._szs

    @property
    def szsStatus(self):
        return self._szs

class TPTPProblem(ProblemWithStatus):
    def __init__(self, name:str, source, problem:str, szs:SZSStatus):
        super().__init__(name, source, problem, szs)

    # A TPTP header
    """
    %--------------------------------------------------------------------------
    % File     : PLA003-1 : TPTP v7.0.0. Released v1.0.0.
    % Domain   : Planning
    % Problem  : Monkey and Bananas Problem
    % Version  : Especial.
    % English  :
    
    % Refs     :
    % Source   : [SPRFN]
    % Names    :
    
    % Status   : Unsatisfiable
    % Rating   : 0.00 v5.3.0, 0.05 v5.2.0, 0.00 v2.2.1, 0.11 v2.1.0, 0.00 v2.0.0
    % Syntax   : Number of clauses     :   11 (   0 non-Horn;   2 unit;   8 RR)
    %            Number of atoms       :   20 (   0 equality)
    %            Maximal clause size   :    2 (   2 average)
    %            Number of predicates  :    1 (   0 propositional; 3-3 arity)
    %            Number of functors    :   11 (   8 constant; 0-3 arity)
    %            Number of variables   :   31 (   7 singleton)
    %            Maximal term depth    :    2 (   2 average)
    % SPC      : CNF_UNS_RFO_NEQ_HRN
    
    % Comments : Formulated as a state space.
    %--------------------------------------------------------------------------
    """
    #TODO everything else here
    _regexFile = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexDomain = re.compile('% Domain(\s*):(\s*)(.*)') # ok
    @staticmethod
    def _parseDomain(content) -> str:
        return TPTPProblem._regexDomain.search(content).group(3).strip()
    _regexProblem = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexVersion = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexEnglish = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexRefs = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexSource = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexNames = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexStatus = re.compile('% Status(\s*):(\s*)(.*)')
    @staticmethod
    def _parseStatus(content) -> SZSStatus:
        return SZSStatus.get(TPTPProblem._regexStatus.search(content).group(3).strip())
    _regexRating = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexSPC = re.compile('% Domain(\s*):(\s*)(.*)')
    _regexComments = re.compile('% Domain(\s*):(\s*)(.*)')

    @classmethod
    def readFromFile(cls,path:Path):
        content = path.read_text()
        szs = cls._parseStatus(content)
        return cls(path.name, path.absolute(), content, szs)