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

    def isUnsound(self):
        return not self._sound

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
        if self == self.SUC and not (other == self.SUC):
            return UNSOUND
        if self._isAncestor(self.NOS):
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

    @staticmethod
    def getOrUnknown(status:str):
        try:
            return SZSStatus.get(status)
        except:
            return SZSStatus.UNK

# SUCCESS
# layer 7
SZSStatus.ETH = SZSStatus.EquivalentTheorem                               = SZSStatus("ETH", "EquivalentTheorem",)
SZSStatus.TAU = SZSStatus.Tautology                                       = SZSStatus("TAU", "Tautology",)
SZSStatus.WTC = SZSStatus.WeakerTautologousConclusion                     = SZSStatus("WTC", "WeakerTautologousConclusion",)
SZSStatus.WTH = SZSStatus.WeakerTheorem                                   = SZSStatus("WTH", "WeakerTheorem",)
SZSStatus.TCA = SZSStatus.TautologousConclusionContradictoryAxioms        = SZSStatus("TCA", "TautologousConclusionContradictoryAxioms",)
SZSStatus.WCA = SZSStatus.WeakerConclusionContradictoryAxioms             = SZSStatus("WCA", "WeakerConclusionContradictoryAxioms",)
SZSStatus.UCA = SZSStatus.UnsatisfiableConclusionContradictoryAxioms      = SZSStatus("UCA", "UnsatisfiableConclusionContradictoryAxioms",)
SZSStatus.WCT = SZSStatus.WeakerCounterTheorem                            = SZSStatus("WCT", "WeakerCounterTheorem",)
SZSStatus.WUC = SZSStatus.WeakerUnsatisfiableConclusion                   = SZSStatus("WUC", "WeakerUnsatisfiableConclusion",)
SZSStatus.UNS = SZSStatus.Unsatisfiable                                   = SZSStatus("UNS", "Unsatisfiable",)
SZSStatus.ECT = SZSStatus.EquivalentCounterTheorem                        = SZSStatus("ECT", "EquivalentCounterTheorem",)
# layer 6
SZSStatus.EQV = SZSStatus.Equivalent                                      = SZSStatus("EQV", "Equivalent", [SZSStatus.ETH, SZSStatus.TAU])
SZSStatus.TAC = SZSStatus.TautologousConclusion                           = SZSStatus("TAC", "TautologousConclusion", [SZSStatus.TAU, SZSStatus.WTC])
SZSStatus.WEC = SZSStatus.WeakerConclusion                                = SZSStatus("WEC", "WeakerConclusion", [SZSStatus.WTC, SZSStatus.WTH])
SZSStatus.SCA = SZSStatus.SatisfiableConclusionContradictoryAxioms        = SZSStatus("SCA", "SatisfiableConclusionContradictoryAxioms", [SZSStatus.TCA, SZSStatus.WCA])
SZSStatus.SCC = SZSStatus.SatisfiableCounterConclusionContradictoryAxioms = SZSStatus("SCC", "SatisfiableCounterConclusionContradictoryAxioms", [SZSStatus.WCA, SZSStatus.UCA])
SZSStatus.WCC = SZSStatus.WeakerCounterConclusion                         = SZSStatus("WCC", "WeakerCounterConclusion", [SZSStatus.WCT, SZSStatus.WUC])
SZSStatus.UNC = SZSStatus.UnsatisfiableConclusion                         = SZSStatus("UNC", "UnsatisfiableConclusion", [SZSStatus.WUC, SZSStatus.UNS])
SZSStatus.CEQ = SZSStatus.CounterEquivalent                               = SZSStatus("CEQ", "CounterEquivalent", [SZSStatus.UNS, SZSStatus.ECT])
# layer 5
SZSStatus.STH = SZSStatus.SatisfiableTheorem                              = SZSStatus("STH", "SatisfiableTheorem", [SZSStatus.EQV, SZSStatus.TAC, SZSStatus.WEC])
SZSStatus.CAX = SZSStatus.ContradictoryAxioms                             = SZSStatus("CAX", "ContradictoryAxioms", [SZSStatus.SCA, SZSStatus.SCC])
SZSStatus.SCT = SZSStatus.SatisfiableCounterTheorem                       = SZSStatus("SCT", "SatisfiableCounterTheorem", [SZSStatus.WCC, SZSStatus.UNC, SZSStatus.CEQ])
# layer 4
SZSStatus.FSA = SZSStatus.FinitelySatisfiable                             = SZSStatus("FSA", "FinitelySatisfiable",)
SZSStatus.NOC = SZSStatus.NoConsequence                                   = SZSStatus("NOC", "NoConsequence",)
SZSStatus.FUN = SZSStatus.FinitelyUnsatisfiable                           = SZSStatus("FUN", "FinitelyUnsatisfiable", [SZSStatus.UNS])
SZSStatus.FCS = SZSStatus.FinitelyCounterSatisfiable                      = SZSStatus("FCS", "FinitelyCounterSatisfiable",)
# layer 3
SZSStatus.SAT = SZSStatus.Satisfiable                                     = SZSStatus("SAT", "Satisfiable", [SZSStatus.FSA, SZSStatus.NOC])
SZSStatus.THM = SZSStatus.Theorem                                         = SZSStatus("THM", "Theorem", [SZSStatus.STH])
SZSStatus.CTH = SZSStatus.CounterTheorem                                  = SZSStatus("CTH", "CounterTheorem", [SZSStatus.SCT])
SZSStatus.CSA = SZSStatus.CounterSatisfiable                              = SZSStatus("CSA", "CounterSatisfiable", [SZSStatus.NOC, SZSStatus.FUN, SZSStatus.FCS])
# layer 2
SZSStatus.ESA = SZSStatus.EquiSatisfiable                                 = SZSStatus("ESA", "EquiSatisfiable", [SZSStatus.SAT])
SZSStatus.FTH = SZSStatus.FiniteTheorem                                   = SZSStatus("FTH", "FiniteTheorem", [SZSStatus.THM])
SZSStatus.ECS = SZSStatus.EquiCounterSatisfiable                          = SZSStatus("ECS", "EquiCounterSatisfiable", [SZSStatus.CSA])
# layer 1
SZSStatus.UNP = SZSStatus.UnsatisfiabilityPreserving                      = SZSStatus("UNP", "UnsatisfiabilityPreserving", [SZSStatus.ESA])
SZSStatus.SAP = SZSStatus.SatisfiabilityPreserving                        = SZSStatus("SAP", "SatisfiabilityPreserving", [SZSStatus.ESA, SZSStatus.THM])
SZSStatus.CSP = SZSStatus.CounterSatisfiabilityPreserving                 = SZSStatus("CSP", "CounterSatisfiabilityPreserving", [SZSStatus.CTH, SZSStatus.ECS])
SZSStatus.CUP = SZSStatus.CounterUnsatisfiabilityPreserving               = SZSStatus("CUP", "CounterUnsatisfiabilityPreserving", [SZSStatus.ECS])
# layer 0
SZSStatus.SUC = SZSStatus.Success                                         = SZSStatus("SUC", "Success", [SZSStatus.UNP, SZSStatus.SAP, SZSStatus.FTH, SZSStatus.CSP, SZSStatus.CUP])

# NOSUCCESS
# layer 6
SZSStatus.TYE = SZSStatus.TypeError     = SZSStatus("TYE", "TypeError",)
# layer 5
SZSStatus.USE = SZSStatus.UsageError    = SZSStatus("USE", "UsageError",)
SZSStatus.SYE = SZSStatus.SyntaxError   = SZSStatus("SYE", "SyntaxError",)
SZSStatus.SEE = SZSStatus.SemanticError = SZSStatus("SEE", "SemanticError", [SZSStatus.TYE])
SZSStatus.TMO = SZSStatus.Timeout       = SZSStatus("TMO", "Timeout",)
SZSStatus.MMO = SZSStatus.MemoryOut     = SZSStatus("MMO", "MemoryOut",)
# layer 4
SZSStatus.OSE = SZSStatus.OSError       = SZSStatus("OSE", "OSError",)
SZSStatus.INE = SZSStatus.InputError    = SZSStatus("INE", "InputError", [SZSStatus.USE, SZSStatus.SYE, SZSStatus.SEE])
SZSStatus.USR = SZSStatus.User          = SZSStatus("USR", "User",)
SZSStatus.RSO = SZSStatus.ResourceOut   = SZSStatus("RSO", "ResourceOut", [SZSStatus.TMO, SZSStatus.MMO])
SZSStatus.INC = SZSStatus.Incomplete    = SZSStatus("INC", "Incomplete",)
SZSStatus.IAP = SZSStatus.Inappropriate = SZSStatus("IAP", "Inappropriate",)
# layer 3
SZSStatus.ERR = SZSStatus.Error         = SZSStatus("ERR", "Error", [SZSStatus.OSE, SZSStatus.INE])
SZSStatus.FOR = SZSStatus.Forced        = SZSStatus("FOR", "Forced", [SZSStatus.USR, SZSStatus.RSO])
SZSStatus.GUP = SZSStatus.GaveUp        = SZSStatus("GUP", "GaveUp", [SZSStatus.RSO, SZSStatus.INC, SZSStatus.ERR, SZSStatus.IAP])
SZSStatus.NTY = SZSStatus.NotTriedYet   = SZSStatus("NTY", "NotTriedYet", )
# layer 2
SZSStatus.STP = SZSStatus.Stopped       = SZSStatus("STP", "Stopped", [SZSStatus.ERR, SZSStatus.FOR, SZSStatus.GUP])
SZSStatus.INP = SZSStatus.InProgress    = SZSStatus("INP", "InProgress",)
SZSStatus.NTT = SZSStatus.NotTried      = SZSStatus("NTT", "NotTried", [SZSStatus.IAP, SZSStatus.NTY])
# layer 1
SZSStatus.OPN = SZSStatus.Open          = SZSStatus("OPN", "Open",)
SZSStatus.UNK = SZSStatus.Unknown       = SZSStatus("UNK", "Unknown", [SZSStatus.STP, SZSStatus.INP, SZSStatus.NTT])
SZSStatus.ASS = SZSStatus.Assumed       = SZSStatus("ASS", "Assumed",)
# layer 0
SZSStatus.NOS = SZSStatus.NoSuccess     = SZSStatus("NOS", "NoSuccess", [SZSStatus.OPN, SZSStatus.UNK, SZSStatus.ASS])
