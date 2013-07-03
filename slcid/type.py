from core import MB, Eval

class Instantiator(MB):
    """
    Class in charge of instantiate magic boxes when evaluated
    """

class ParameterType(Instantiator):
    pass

class Operation(Instantiator):
    pass

class Type(Instantiator):
    pass

class TypeDefinition(Eval):
    
