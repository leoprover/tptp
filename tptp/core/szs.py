"""
  * SZS Success status values, as given by the following ontology diagram:
  * {{{
  *                                 Success
  *                                   SUC
  *         ___________________________|_______________________________
  *        |         |    |                                  |         |
  *     UnsatPre  SatPre  |                             CtrSatPre CtrUnsatPre
  *       UNP       SAP   |                                 CSP       CUP
  *        |_______/ |    |                                  | \_______|
  *        |         |    |                                  |         |
  *     EquSat       | FiniteThm                             |     EquCtrSat
  *       ESA        |   FTH                                 |        ECS
  *        |         |   /                                   |         |
  *     Sat'ble   Theorem                                 CtrThm     CtrSat
  *       SAT       THM                                     CTH       CSA
  *      / | \______.|._____________________________________.|.______/ | \
  *     /  |         |                   |                   |         |  \
  * FinSat |         |                NoConq                 |  FinUns | FinCtrSat
  *  FSA   |         |                  NOC                  |     FUN |   FCS
  *        |         |_______________________________________|       | |
  *        |         |                   |                   |       | |
  *        |     SatAxThm             CtraAx              SatAxCth   | |
  *        |        STH                 CAX                 SCT      : |
  *       _|_________|_              ____|____              _|_________|_
  *      |      |      |            |         |            |      |  :   |
  *   Eqvlnt  TautC  WeakC      SatConCA   SatCCoCA      WkCC  UnsCon|CtrEqu
  *     EQV    TAC    WEC          SCA       SCC          WCC    UNC |  CEQ
  *    __|__   _|_   __|__        __|___   ___|__        __|__   _|_ |__|__
  *   |     | /   \ |     |      |      \ /      |      |     | /   \|     |
  *Equiv  Taut-  Weaker Weaker TauCon   WCon  UnsCon Weaker Weaker Unsat Equiv
  * Thm   ology  TautCo  Thm   CtraAx  CtraAx CtraAx CtrThm UnsCon -able CtrTh
  * ETH    TAU    WTC    WTH    TCA     WCA     UCA    WCT    WUC    UNS  ECT
  * }}}
  * taken from [[https://github.com/leoprover/Leo-III/blob/master/src/main/scala/leo/modules/output/StatusSZS.scala]].
  * taken from [[http://www.cs.miami.edu/~tptp/cgi-bin/SeeTPTP?Category=Documents&File=SZSOntology]].
"""

"""
  * Unsuccessful result status, as given by the NoSuccess ontology:
  * {{{
  *                                            NoSuccess
  *                                               NOS
  *                            ____________________|___________________
  *                           |                    |                   |
  *                         Open                Unknown             Assumed
  *                          OPN                  UNK             ASS(UNK,SUC)
  *                               _________________|_________________
  *                              |                 |                 |
  *                           Stopped         InProgress         NotTried
  *                             STP               INP               NTT
  *          ____________________|________________               ____|____
  *         |                    |                |             |         |
  *       Error               Forced           GaveUp           |    NotTriedYet
  *        ERR                  FOR              GUP            |        NTY
  *     ____|____            ____|____   _________|__________   |
  *    |         |          |         | |         |     |    |  |
  * OSError   InputEr      User   ResourceOut  Incompl  |  Inappro
  *   OSE       INE        USR        RSO        INC    |    IAP
  *           ___|___              ___|___             v
  *          |   |   |            |       |           to
  *      UseEr SynEr SemEr    Timeout MemyOut        ERR
  *         USE SYE SEE         TMO     MMO
  *                  |
  *              TypeError
  *                 TYE
  * }}}
  *
  * taken from [[https://github.com/leoprover/Leo-III/blob/master/src/main/scala/leo/modules/output/StatusSZS.scala]].
  * taken from [[http://www.cs.miami.edu/~tptp/cgi-bin/SeeTPTP?Category=Documents&File=SZSOntology]].
"""

class UnknownSZSStatusError(Exception):
    """
    Thrown if an SZS status could not be parsed from a string
    """
    pass

class SZSStatusMatch():
    _nextIdentifier = 0

    @staticmethod
    def _generateIdentifier():
        SZSStatusMatch._nextIdentifier += 1
        return SZSStatusMatch._nextIdentifier - 1

    def __init__(self, name, correct, sound):
        self._identifier = SZSStatusMatch._generateIdentifier()
        self._name = name
        self._correct = correct
        self._sound = sound

    def __eq__(self, other):
        if not isinstance(other, SZSStatusMatch):
            return False
        return self._identifier == other._identifier
    
    def __hash__(self):
        return self._identifier
    
    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def isCorrect(self):
        return self._correct

    def isSound(self):
        return self._sound

UNSOUND = SZSStatusMatch("unsound", correct=False, sound=False)
NO_SUCCESS = SZSStatusMatch("no success", correct=False, sound=True)
CORRECT = SZSStatusMatch("correct", correct=True, sound=True)

class SZSStatus():
    _nextIdentifier = 0
    _shortNames = {}
    _longNames = {}
    _children = []
    _parents = []

    @staticmethod
    def _generateIdentifier():
        SZSStatus._nextIdentifier += 1
        return SZSStatus._nextIdentifier - 1

    def __init__(self, shortName, longName, children=[]): ###
        self._identifier = SZSStatus._generateIdentifier()
        self._shortName = shortName
        self._longName = longName
        self._children = children

        SZSStatus._shortNames[shortName] = self
        SZSStatus._longNames[longName] = self
        
    def __eq__(self, other):
        if not isinstance(other, SZSStatus):
            return False
        return self._identifier == other._identifier
    
    def __hash__(self):
        return self._identifier
    
    def __repr__(self):
        return self._longName

    def __str__(self):
        return self._longName

    def _isAncestor(self, other):
        if self == other:
            return True
        for c in other._children:
            if self._isAncestor(c):
                return True
        return False

    def matches(self, other):
        if self == SUC and not (other == SUC):
            return UNSOUND
        if self._isAncestor(NOS):
            return NO_SUCCESS
        if self._isAncestor(other):
            return CORRECT
        if other._isAncestor(self):
            return CORRECT
        return UNSOUND
    
    @staticmethod
    def get(status:str):
        """
        Returns the enumeration item for a short or long status (e.g. THM or Theorem)
        :param status:
        :return:
        """
        if status in SZSStatus._shortNames:
            return SZSStatus._shortNames[status]
        if status in SZSStatus._longNames:
            return SZSStatus._longNames[status]
        raise UnknownSZSStatusError('\"' + status + '\" is not a valid SZS status.')

# SUCCESS
# layer 7
ETH = SZSStatus("ETH", "EquivalentTheorem",)
TAU = SZSStatus("TAU", "Tautology",)
WTC = SZSStatus("WTC", "WeakerTautologousConclusion",)
WTH = SZSStatus("WTH", "WeakerTheorem",)
TCA = SZSStatus("TCA", "TautologousConclusionContradictoryAxioms",)
WCA = SZSStatus("WCA", "WeakerConclusionContradictoryAxioms",)
UCA = SZSStatus("UCA", "UnsatisfiableConclusionContradictoryAxioms",)
WCT = SZSStatus("WCT", "WeakerCounterTheorem",)
WUC = SZSStatus("WUC", "WeakerUnsatisfiableConclusion",)
UNS = SZSStatus("UNS", "Unsatisfiable",)
ECT = SZSStatus("ECT", "EquivalentCounterTheorem",)
# layer 6
EQV = SZSStatus("EQV", "Equivalent", [ETH, TAU])
TAC = SZSStatus("TAC", "TautologousConclusion", [TAU, WTC])
WEC = SZSStatus("WEC", "WeakerConclusion", [WTC, WTH])
SCA = SZSStatus("SCA", "SatisfiableConclusionContradictoryAxioms", [TCA, WCA])
SCC = SZSStatus("SCC", "SatisfiableCounterConclusionContradictoryAxioms", [WCA, UCA])
WCC = SZSStatus("WCC", "WeakerCounterConclusion", [WCT, WUC])
UNC = SZSStatus("UNC", "UnsatisfiableConclusion", [WUC, UNS])
CEQ = SZSStatus("CEQ", "CounterEquivalent", [UNS, ECT])
# layer 5
STH = SZSStatus("STH", "SatisfiableTheorem", [EQV, TAC, WEC])
CAX = SZSStatus("CAX", "ContradictoryAxioms", [SCA, SCC])
SCT = SZSStatus("SCT", "SatisfiableCounterTheorem", [WCC, UNC, CEQ])
# layer 4
FSA = SZSStatus("FSA", "FinitelySatisfiable",)
NOC = SZSStatus("NOC", "NoConsequence",)
FUN = SZSStatus("FUN", "FinitelyUnsatisfiable", [UNS])
FCS = SZSStatus("FCS", "FinitelyCounterSatisfiable",)
# layer 3
SAT = SZSStatus("SAT", "Satisfiable", [FSA, NOC])
THM = SZSStatus("THM", "Theorem", [STH])
CTH = SZSStatus("CTH", "CounterTheorem", [SCT])
CSA = SZSStatus("CSA", "CounterSatisfiable", [NOC, FUN, FCS])
# layer 2
ESA = SZSStatus("ESA", "EquiSatisfiable", [SAT])
FTH = SZSStatus("FTH", "FiniteTheorem", [THM])
ECS = SZSStatus("ECS", "EquiCounterSatisfiable", [CSA])
# layer 1
UNP = SZSStatus("UNP", "UnsatisfiabilityPreserving", [ESA])
SAP = SZSStatus("SAP", "SatisfiabilityPreserving", [ESA, THM])
CSP = SZSStatus("CSP", "CounterSatisfiabilityPreserving", [CTH, ECS])
CUP = SZSStatus("CUP", "CounterUnsatisfiabilityPreserving", [ECS])
# layer 0
SUC = SZSStatus("SUC", "Success", [UNP, SAP, FTH, CSP, CUP])

# NOSUCCESS
# layer 6
TYE = SZSStatus("TYE", "TypeError",)
# layer 5
USE = SZSStatus("USE", "UsageError",)
SYE = SZSStatus("SYE", "SyntaxError",)
SEE = SZSStatus("SEE", "SemanticError", [TYE])
TMO = SZSStatus("TMO", "Timeout",)
MMO = SZSStatus("MMO", "MemoryOut",)
# layer 4
OSE = SZSStatus("OSE", "OSError",)
INE = SZSStatus("INE", "InputError", [USE, SYE, SEE])
USR = SZSStatus("USR", "User",)
RSO = SZSStatus("RSO", "ResourceOut", [TMO, MMO])
INC = SZSStatus("INC", "Incomplete",)
IAP = SZSStatus("IAP", "Inappropriate",)
# layer 3
ERR = SZSStatus("ERR", "Error", [OSE, INE])
FOR = SZSStatus("FOR", "Forced", [USR, RSO])
GUP = SZSStatus("GUP", "GaveUp", [RSO, INC, ERR, IAP])
NTY = SZSStatus("NTY", "NotTriedYet", )
# layer 2
STP = SZSStatus("STP", "Stopped", [ERR, FOR, GUP])
INP = SZSStatus("INP", "InProgress",)
NTT = SZSStatus("NTT", "NotTried", [IAP, NTY])
# layer 1
OPN = SZSStatus("OPN", "Open",)
UNK = SZSStatus("UNK", "Unknown", [STP, INP, NTT])
ASS = SZSStatus("ASS", "Assumed",)
# layer 0
NOS = SZSStatus("NOS", "NoSuccess", [OPN, UNK, ASS])
