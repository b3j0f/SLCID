from core import MagicBox

class Primitive(MagicBox):
    """
    Primitive class which uses both language value and literal value.
    """
    LITERAL_VALUE = 'LITERAL'
    VALUE = 'value'
    GET_VALUE = 'GET_VALUE'
    SET_VALUE = 'SET_VALUE'
    def __init__(self, literalValue='', value=None):
        self._literalValue = literalValue
        if value == None:
            self._value = self.getValue(literalValue)
        else:
            self._value = value
    def getValue(self, literalValue=None):
        """ 
        Get a value from a literalValue
        """
        # get interceptor container for getvalue evaluation
        interceptorContainer = self._interceptorContainer(Primitive.GET_VALUE)
        params = mb(literalValue=literalValue)
        args = Eval._args(self, self, Primitive.GET_VALUE, params)
        result = interceptorContainer(args)
        return result
    def setLiteralValue(self, value=None):
        """
        change self value
        """
        self._value = value

class Number(Primitive):
    """
    Primitive class dedicated to embed a number value
    """
    def __init__(self, value=0):
        Primitive.__init__(self, value=value)
    def getValue(self, literalValue=None):
        result = float(0)
        if literalValue != None:
            result = float(literalValue)
        return result
    def setValue(self, literalValue=None):
        
def n(value=0):
    result = Number(value)
    return result

class Boolean(Primitive):
    """
    Primitive class dedicated to embed a boolean value
    """
    def __init__(self, value=False):
        Primitive.__init__(self, value=value)
    def getValue(self, literalValue):
        return bool(literalValue)

def b(value=False):
    result = Boolean(value)
    return result

class String(Primitive):
    """
    Primitive class dedicated to embed a string value
    """
    def __init__(self, value=''):
        Primitive.__init__(self, value=value)
    def getValue(self, literalValue):
        return literalValue

class Null(Primitive):
    """
    Primitive class dedicated to embed a null value
    """
    def __init__(self, value=None):
        Primitive.__init__(self)
    def getValue(self, literalValue):
        return None
