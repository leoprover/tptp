'''
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
'''

'''
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
'''

class SZSStatus:
    def __init__(self,szs): # TODO make this unusable. people should use SZSStatus.get(...)
      self.szs = szs
    def __repr__(self):
      return self.szs
    @staticmethod
    def get(status:str):
      '''
      Returns the enumeration item for a short or long status (e.g. THM or Theorem)
      :param status:
      :return:
      '''
      return SZSStatus(status)


    SUCCESS = [ ("SUC", "Success")
    # layer 1
      , ("UNP", "UnsatisfiabilityPreserving")
      , ("SAP", "SatisfiabilityPreserving")
      , ("CSP", "CounterSatisfiabilityPreserving")
      , ("CUP", "CounterUnsatisfiabilityPreserving")
    # layer 2
      , ("ESA", "EquiSatisfiable")
      , ("FTH", "FiniteTheorem")
      , ("ECS", "EquiCounterSatisfiable")
    # layer 3
      , ("SAT", "Satisfiable")
      , ("THM", "Theorem")
      , ("CTH", "CounterTheorem")
      , ("CSA", "CounterSatisfiable")
    # layer 4
      , ("FSA", "FinitelySatisfiable")
      , ("NOC", "NoConsequence")
      , ("FUN", "FinitelyUnsatisfiable")
      , ("FCS", "FinitelyCounterSatisfiable")
    # layer 5
      , ("STH", "SatisfiableTheorem")
      , ("CAX", "ContradictoryAxioms")
      , ("SCT", "SatisfiableCounterTheorem")
    # layer 6
      , ("EQV", "Equivalent")
      , ("TAC", "TautologousConclusion")
      , ("WEC", "WeakerConclusion")
      , ("SCA", "SatisfiableConclusionContradictoryAxioms")
      , ("SCC", "SatisfiableCounterConclusionContradictoryAxioms")
      , ("WCC", "WeakerCounterConclusion")
      , ("UNC", "UnsatisfiableConclusion")
      , ("CEQ", "CounterEquivalent")
    # layer 7
      , ("ETH", "EquivalentTheorem")
      , ("TAU", "Tautology")
      , ("WTC", "WeakerTautologousConclusion")
      , ("WTH", "WeakerTheorem")
      , ("TCA", "TautologousConclusionContradictoryAxioms")
      , ("WCA", "WeakerConclusionContradictoryAxioms")
      , ("UCA", "UnsatisfiableConclusionContradictoryAxioms")
      , ("WCT", "WeakerCounterTheorem")
      , ("WUC", "WeakerUnsatisfiableConclusion")
      , ("UNS", "Unsatisfiable")
      , ("ECT", "EquivalentCounterTheorem")
    ]
    SUCCESS_SHORT = list(map(lambda v: v[0], SUCCESS))
    SUCCESS_LONG = list(map(lambda v: v[1], SUCCESS))

    NOSUCCESS = [ ("NOS", "NoSuccess")
    # layer 1
      , ("OPN", "Open")
      , ("UNK", "Unknown")
      , ("ASS", "Assumed")
    # layer 2
      , ("STP", "Stopped")
      , ("INP", "InProgress")
      , ("NTT", "NotTried")
    # layer 3
      , ("ERR", "Error")
      , ("FOR", "Forced")
      , ("GUP", "GaveUp")
      , ("NTY", "NotTriedYet")
    # layer 4
      , ("OSE", "OSError")
      , ("INE", "InputError")
      , ("USR", "User")
      , ("RSO", "ResourceOut")
      , ("INC", "Incomplete")
      , ("IAP", "Inappropriate")
    # layer 5
      , ("USE", "UsageError")
      , ("SYE", "SyntaxError")
      , ("SEE", "SemanticError")
      , ("TMO", "Timeout")
      , ("MMO", "MemoryOut")
    # layer 6
      , ("TYE", "TypeError")
      ]
    NOSUCCESS_SHORT = list(map(lambda v: v[0], NOSUCCESS))
    NOSUCCESS_LONG = list(map(lambda v: v[1], NOSUCCESS))

    @classmethod
    def isSuccess(cls, state):
        return state in cls.SUCCESS_LONG