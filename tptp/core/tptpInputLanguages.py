class InputLanguage():
    pass

class UnknownTPTPDialectError(Exception):
    """
    Thrown if a TPTPDialect could not be parsed from a string
    """
    pass

class UnknownTPTPLanguageFeatureError(Exception):
    """
    Thrown if an TPTPDialect status could not be parsed from a string
    """
    pass

class TPTPLanguageFeature:
    _shortNames = {}
    _longNames = {}
    _symbols = {}

    _nextIdentifier = 0

    @staticmethod
    def _generateIdentifier():
        TPTPDialect._nextIdentifier += 1
        return TPTPDialect._nextIdentifier - 1

    def __init__(self,longName: str, symbol:str):
        self._identifier = TPTPDialect._generateIdentifier()
        self.longName = longName
        self.symbol = symbol
        TPTPLanguageFeature._longNames[longName] = self
        TPTPLanguageFeature._symbols[symbol] = self

    def __hash__(self):
        return self._identifier

    def __eq__(self, other):
        if not isinstance(other, TPTPLanguageFeature):
            return False
        return self._identifier == other._identifier

    def __repr__(self):
        return self.longName

    def __str__(self):
        return self.longName

    @staticmethod
    def get(languageFeature: str):
        if languageFeature in TPTPLanguageFeature._longNames:
            return TPTPDialect._longNames[languageFeature]
        raise UnknownTPTPLanguageFeatureError('\"' + languageFeature + '\" is not a valid TPTP language feature.')


class TPTPDialect(InputLanguage):
    _shortNames = {}
    _longNames = {}

    _nextIdentifier = 0
    @staticmethod
    def _generateIdentifier():
        TPTPDialect._nextIdentifier += 1
        return TPTPDialect._nextIdentifier - 1

    def __init__(self, shortName:str, longName:str, children:set, languageFeatures:set):
        self._identifier = TPTPDialect._generateIdentifier()
        self.shortName = shortName
        self.longName = longName
        self.children = children
        self.languageFeatures = languageFeatures
        TPTPDialect._shortNames[shortName] = self
        TPTPDialect._longNames[longName] = self

    def __hash__(self):
        return self._identifier

    def __eq__(self, other):
        if not isinstance(other, TPTPDialect):
            return False
        return self._identifier == other._identifier

    def __repr__(self):
        return self.shortName

    def __str__(self):
        return self.shortName

    @staticmethod
    def get(dialect: str):
        if dialect in TPTPDialect._shortNames:
            return TPTPDialect._shortNames[dialect]
        if dialect in TPTPDialect._longNames:
            return TPTPDialect._longNames[dialect]
        raise UnknownTPTPDialectError('\"' + dialect + '\" is not a valid TPTP dialect.')

# defined functors
TPTPLanguageFeature.TRUE = TPTPLanguageFeature('true', '$true') # $true
TPTPLanguageFeature.FALSE = TPTPLanguageFeature('false', '$false') # $false

# connectives
TPTPLanguageFeature.NEGATION = TPTPLanguageFeature('negation', '~') # ~
TPTPLanguageFeature.DISJUNCTION = TPTPLanguageFeature('disjunction', '|') # |
TPTPLanguageFeature.JOINT_DENIAL = TPTPLanguageFeature('joint denial', '~|') # ~|
TPTPLanguageFeature.CONJUNCTION = TPTPLanguageFeature('conjunction', '&') # &
TPTPLanguageFeature.ALTERNATIVE_DENIAL = TPTPLanguageFeature('alternative denial', '~&') # ~&
TPTPLanguageFeature.IMPLICATION = TPTPLanguageFeature('implication', '=>') # =>
TPTPLanguageFeature.CONVERSE_IMPLICATION = TPTPLanguageFeature('converse implication', '<=') # <=
TPTPLanguageFeature.BICONDITIONAL = TPTPLanguageFeature('biconditional', '<=>') # <=>
TPTPLanguageFeature.XOR = TPTPLanguageFeature('exclusive disjunction', '<~>') # <~>
TPTPLanguageFeature.EQUALITY = TPTPLanguageFeature('equality', '=') # =
TPTPLanguageFeature.INEQUALITY = TPTPLanguageFeature('inequality', '!=') # !=

# binders
TPTPLanguageFeature.FORALL_BINDER = TPTPLanguageFeature('forall binder', '!') # ! forall binder
TPTPLanguageFeature.EXISTS_BINDER = TPTPLanguageFeature('exists binder', '?') # ? exists binder
TPTPLanguageFeature.LAMBDA_BINDER = TPTPLanguageFeature('lambda binder', '^') # ^ lambda binder
TPTPLanguageFeature.INDEFINITE_DESCRIPTION_BINDER = TPTPLanguageFeature('indefinite description binder', '@+') # @+ indefinite description (choice)
TPTPLanguageFeature.DEFINITE_DESCRIPTION_BINDER = TPTPLanguageFeature('definite_description_binder', '@-') # @- definite description
TPTPLanguageFeature.TYPE_BINDER = TPTPLanguageFeature('type binder', '!>') # !> rank 1 polymorphism

# polymorphic constants
TPTPLanguageFeature.FORALL_POLYMORPHIC = TPTPLanguageFeature('forall polymorphic constant', '!!') # !! forall polymorphic constant
TPTPLanguageFeature.EXISTS_POLYMORPHIC = TPTPLanguageFeature('exists polymorphic constant', '??') # ?? exists polymorphic constant
TPTPLanguageFeature.INDEFINITE_DESCRIPTION_POLYMORPHIC = TPTPLanguageFeature('indefinite description polymorphic constant', '@@+') # @@+ indefinite description (choice) polymorphic constant
TPTPLanguageFeature.DEFINITE_DESCRIPTION_POLYMORPHIC = TPTPLanguageFeature('definite description polymorphic constant', '@@-') # @@- definite description polymorphic constant
TPTPLanguageFeature.EQUALITY_POLYMORPHIC = TPTPLanguageFeature('equality polymorphic constant', '@=') # @= equality polymorphic constant

# misc
TPTPLanguageFeature.SORT = TPTPLanguageFeature('new sort', 'mytype: $tType') # introduce a new sort (type)
#TPTPLanguageFeature.PROPOSITION = TPTPLanguageFeature('proposition', 'mybooleanconstant') # supports propositions

# missing:
# prod and mapping types
# subtypes
# ?*
# numbers
# arithmetic
# $tType
# conditional expressions $ite, $let
# *
# other defined functors

TPTPDialect.CNF = TPTPDialect('CNF',
                              'clause normal form',
                              set(),
                              {
                                  TPTPLanguageFeature.NEGATION,
                                  TPTPLanguageFeature.DISJUNCTION,
                              })
TPTPDialect.FOF = TPTPDialect('FOF', 'first-order form',
                              set(),
                              {
                                  TPTPLanguageFeature.TRUE,
                                  TPTPLanguageFeature.FALSE,
                                  TPTPLanguageFeature.NEGATION,
                                  TPTPLanguageFeature.DISJUNCTION,
                                  TPTPLanguageFeature.JOINT_DENIAL,
                                  TPTPLanguageFeature.CONJUNCTION,
                                  TPTPLanguageFeature.ALTERNATIVE_DENIAL,
                                  TPTPLanguageFeature.IMPLICATION,
                                  TPTPLanguageFeature.CONVERSE_IMPLICATION,
                                  TPTPLanguageFeature.BICONDITIONAL,
                                  TPTPLanguageFeature.XOR,
                                  TPTPLanguageFeature.EQUALITY,
                                  TPTPLanguageFeature.INEQUALITY,
                                  TPTPLanguageFeature.FORALL_BINDER,
                                  TPTPLanguageFeature.EXISTS_BINDER,
                              })

TPTPDialect.TF0 = TPTPDialect('TF0',
                              'monomorphic typed first-order form',
                              set(),
                              set(), # TODO
                              )
TPTPDialect.TF1 = TPTPDialect('TF1',
                              'polymorphic typed first-order form',
                              set(),
                              TPTPDialect.TF0.languageFeatures.union({
                                  # TODO
                              }))
TPTPDialect.TFF = TPTPDialect('TFF',
                              'typed first-order form',
                              {TPTPDialect.TF0, TPTPDialect.TF1},
                              TPTPDialect.TF1.languageFeatures
                              )
TPTPDialect.TFX = TPTPDialect('TFX',
                              'extended typed first-order form',
                              set(), # TODO
                              set() # TODO
                              )
TPTPDialect.TH0 = TPTPDialect('TH0',
                              'monomorphic typed higher-order form',
                              set(),
                              {
                                  TPTPLanguageFeature.TRUE,
                                  TPTPLanguageFeature.FALSE,
                                  TPTPLanguageFeature.NEGATION,
                                  TPTPLanguageFeature.DISJUNCTION,
                                  TPTPLanguageFeature.JOINT_DENIAL,
                                  TPTPLanguageFeature.CONJUNCTION,
                                  TPTPLanguageFeature.ALTERNATIVE_DENIAL,
                                  TPTPLanguageFeature.IMPLICATION,
                                  TPTPLanguageFeature.CONVERSE_IMPLICATION,
                                  TPTPLanguageFeature.BICONDITIONAL,
                                  TPTPLanguageFeature.XOR,
                                  TPTPLanguageFeature.EQUALITY,
                                  TPTPLanguageFeature.INEQUALITY,
                                  TPTPLanguageFeature.FORALL_BINDER,
                                  TPTPLanguageFeature.EXISTS_BINDER,
                                  TPTPLanguageFeature.LAMBDA_BINDER,
                                  TPTPLanguageFeature.INDEFINITE_DESCRIPTION_BINDER,
                                  TPTPLanguageFeature.DEFINITE_DESCRIPTION_BINDER,
                                  TPTPLanguageFeature.SORT,
                              })
TPTPDialect.TH1 = TPTPDialect('TH1',
                              'polymorphic typed higher-order form',
                              set(),
                              TPTPDialect.TH0.languageFeatures.union({
                                  TPTPLanguageFeature.TYPE_BINDER,
                                  TPTPLanguageFeature.FORALL_POLYMORPHIC,
                                  TPTPLanguageFeature.EXISTS_POLYMORPHIC,
                                  TPTPLanguageFeature.INDEFINITE_DESCRIPTION_POLYMORPHIC,
                                  TPTPLanguageFeature.DEFINITE_DESCRIPTION_POLYMORPHIC,
                                  TPTPLanguageFeature.EQUALITY_POLYMORPHIC,
                              }))
TPTPDialect.THF = TPTPDialect('THF',
                              'typed higher-order form',
                              {TPTPDialect.TH0, TPTPDialect.TH1},
                              TPTPDialect.TH1.languageFeatures
                              )
