from core import MB, Eval

class Instantiator(MB):
    """
    Class in charge of instantiate magic boxes when evaluated
    """

# scope elements
class Scope(MB):
    pass

class ScopedElement(MB):
    pass

class ParameterType(ScopedElement):
    pass

class Operation(Scope):
    pass

class Type(Scope):
    pass

class TypeDefinition(Eval):
    pass
