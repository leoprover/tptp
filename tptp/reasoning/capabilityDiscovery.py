from typing import Callable, List

from tptp.core.tptpInputLanguages import TPTPLanguageFeature
from .capability import Capability, Action
from ..core import TPTPDialect


def discoverCapabilites(action:Callable) -> List[Capability]:
    for testName, test in _testCases.items():
        for problemString in test:
            action(problemString)
    pass


# InputSet -> InputType -> OutputType -> Action -> TestCase
_testCases = {}

# TPTP dialect, language feature,
_th0TestCases = {}
_th0TestCases[TPTPLanguageFeature.TRUE] = [
    '''
    thf(0,conjecture,$true).
    ''',
]
_th0TestCases[TPTPLanguageFeature.FALSE] = [
    '''
    thf(0,conjecture,~$false).
    ''',
]
_th0TestCases[TPTPLanguageFeature.NEGATION] = [
    '''
    thf(0,conjecture,~$false).
    ''',
]
_th0TestCases[TPTPLanguageFeature.DISJUNCTION]= [
    '''
    thf(0,type,a:$o).
    thf(0,conjecture, a|~a).
    ''',
]
#TPTPLanguageFeature.JOINT_DENIAL,
#TPTPLanguageFeature.CONJUNCTION,
#TPTPLanguageFeature.ALTERNATIVE_DENIAL,
#TPTPLanguageFeature.IMPLICATION,
#TPTPLanguageFeature.CONVERSE_IMPLICATION,
#TPTPLanguageFeature.BICONDITIONAL,
#TPTPLanguageFeature.XOR,
#TPTPLanguageFeature.EQUALITY,
#TPTPLanguageFeature.INEQUALITY,
#TPTPLanguageFeature.FORALL_BINDER,
#TPTPLanguageFeature.EXISTS_BINDER,
#TPTPLanguageFeature.LAMBDA_BINDER,
#TPTPLanguageFeature.INDEFINITE_DESCRIPTION_BINDER,
#TPTPLanguageFeature.DEFINITE_DESCRIPTION_BINDER,
#TPTPLanguageFeature.SORT,
