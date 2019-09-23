from typing import List, Dict, Callable, Type


class Action:
    """
    An Action is a defined task some describing exactly one task that some tool can do.
    This is a singleton class, not intended for user-instantiation.
    """
    _nextIdentifier = 0
    _name = {}

    @staticmethod
    def _generateIdentifier():
        Action._nextIdentifier += 1
        return Action._nextIdentifier - 1

    def __init__(self, name):  ###
        self._identifier = Action._generateIdentifier()
        self.name = name
        Action._name[name] = self

    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return self._identifier == other._identifier

    def __hash__(self):
        return self._identifier

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

Action.THEOREM_PROVING = Action('theorem proving')
Action.MODEL_FINDING = Action('model finding')
Action.ENCODING = Action('encoding')
Action.TYPE_CHECKING = Action('type checking')
Action.SYNTAX_CHECKING = Action('syntax checking')


class CapabilityInsufficientError(Exception):
    """
    Thrown if a capability applied for an ineligible input or output type
    """
    pass

class Capability:
    """
    A capability wraps a single action of a tool, its kinds of inputs and
    hooks inputs of different kinds to different kinds of outputs.
    The apply method of a Capability instance executes the tool for a specific input and output format.
    """
    _nextIdentifier = 0
    _name = {}

    @staticmethod
    def _generateIdentifier():
        Capability._nextIdentifier += 1
        return Capability._nextIdentifier - 1

    def __init__(self, name:str, description:str, action:Action, actionMap:Dict[Type, Dict[Type, Callable]], exceptions=None):  ###
        self.exceptions = exceptions
        self.action = action
        self.description = description
        self.name = name
        self._actionMap = actionMap
        self._identifier = Capability._generateIdentifier()
        Capability._name[name] = self

    def __eq__(self, other):
        if not isinstance(other, Capability):
            return False
        return self._identifier == other._identifier

    def __hash__(self):
        return self._identifier

    def __repr__(self):
        sb = []
        for inputType in self._actionMap:
            sb.append(str(inputType) + ' -> ' + str(list(map(lambda kv: str(kv[0]) + ' (' + kv[1].__name__ + ' )', self._actionMap[inputType].items()))))
        return '\n'.join([self.name] + sb)

    def __str__(self):
        return self.name

    def apply(self, input, outputType:Type):
        inputType = type(input)
        if not inputType in self._actionMap:
            raise CapabilityInsufficientError(str(inputType) + " is not a valid input type for capability " + self.name)
        if not outputType in self._actionMap[inputType]:
            raise CapabilityInsufficientError(str(inputType) + " is not a valid output type for capability " + self.name)
        self._actionMap[inputType][outputType](input)


