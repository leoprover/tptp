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

class SZSStatus():
    _nextIdentifier = 0
    _shortNames = {}
    _longNames = {}

    @staticmethod
    def _generateIdentifier():
        SZSStatus._nextIdentifier += 1
        return SZSStatus._nextIdentifier - 1

    def __init__(self, shortName, longName): ###
        self._identifier = SZSStatus._generateIdentifier()
        self._shortName = shortName
        self._longName = longName
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

    @staticmethod
    def get(status:str):
        """
        Returns the enumeration item for a short or long status (e.g. THM or Theorem)
        :param status:
        :return:
        """
        if status in SZSStatus._shortNames.keys():
            return SZSStatus._shortNames[status]
        if status in SZSStatus._longNames.keys():
            return SZSStatus._longNames[status]
        raise UnknownSZSStatusError('\"' + status + '\" is not a valid SZS status.')

# SUCCESS
SUC = SZSStatus("SUC","Success",)
# layer 1
UNP = SZSStatus("UNP", "UnsatisfiabilityPreserving",)
SAP = SZSStatus("SAP", "SatisfiabilityPreserving",)
CSP = SZSStatus("CSP", "CounterSatisfiabilityPreserving",)
CUP = SZSStatus("CUP", "CounterUnsatisfiabilityPreserving",)
# layer 2
ESA = SZSStatus("ESA", "EquiSatisfiable",)
FTH = SZSStatus("FTH", "FiniteTheorem",)
ECS = SZSStatus("ECS", "EquiCounterSatisfiable",)
# layer 3
SAT = SZSStatus("SAT", "Satisfiable",)
THM = SZSStatus("THM", "Theorem",)
CTH = SZSStatus("CTH", "CounterTheorem",)
CSA = SZSStatus("CSA", "CounterSatisfiable",)
# layer 4
FSA = SZSStatus("FSA", "FinitelySatisfiable",)
NOC = SZSStatus("NOC", "NoConsequence",)
FUN = SZSStatus("FUN", "FinitelyUnsatisfiable",)
FCS = SZSStatus("FCS", "FinitelyCounterSatisfiable",)
# layer 5
STH = SZSStatus("STH", "SatisfiableTheorem",)
CAX = SZSStatus("CAX", "ContradictoryAxioms",)
SCT = SZSStatus("SCT", "SatisfiableCounterTheorem",)
# layer 6
EQV = SZSStatus("EQV", "Equivalent",)
TAC = SZSStatus("TAC", "TautologousConclusion",)
WEC = SZSStatus("WEC", "WeakerConclusion",)
SCA = SZSStatus("SCA", "SatisfiableConclusionContradictoryAxioms",)
SCC = SZSStatus("SCC", "SatisfiableCounterConclusionContradictoryAxioms",)
WCC = SZSStatus("WCC", "WeakerCounterConclusion",)
UNC = SZSStatus("UNC", "UnsatisfiableConclusion",)
CEQ = SZSStatus("CEQ", "CounterEquivalent",)
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

# NOSUCCESS
NOS = SZSStatus("NOS", "NoSuccess",)
# layer 1
OPN = SZSStatus("OPN", "Open",)
UNK = SZSStatus("UNK", "Unknown",)
ASS = SZSStatus("ASS", "Assumed",)
# layer 2
STP = SZSStatus("STP", "Stopped",)
INP = SZSStatus("INP", "InProgress",)
NTT = SZSStatus("NTT", "NotTried",)
# layer 3
ERR = SZSStatus("ERR", "Error",)
FOR = SZSStatus("FOR", "Forced",)
GUP = SZSStatus("GUP", "GaveUp",)
NTY = SZSStatus("NTY", "NotTriedYet",)
# layer 4
OSE = SZSStatus("OSE", "OSError",)
INE = SZSStatus("INE", "InputError",)
USR = SZSStatus("USR", "User",)
RSO = SZSStatus("RSO", "ResourceOut",)
INC = SZSStatus("INC", "Incomplete",)
IAP = SZSStatus("IAP", "Inappropriate",)
# layer 5
USE = SZSStatus("USE", "UsageError",)
SYE = SZSStatus("SYE", "SyntaxError",)
SEE = SZSStatus("SEE", "SemanticError",)
TMO = SZSStatus("TMO", "Timeout",)
MMO = SZSStatus("MMO", "MemoryOut",)
# layer 6
TYE = SZSStatus("TYE", "TypeError",)


