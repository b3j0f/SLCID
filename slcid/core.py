class MagicBox:
    """
    BASE ELEMENT. Contains language specific values and MagicBox contents.
    """
    GET = 'get' # get value from label
    PUT = 'put' # put label, value
    NEW_LABEL = 'availableLabel' # get available label
    LABELS = 'labels' # get labels
    POP = 'pop' # remove content
    POP_ITEM = 'popItem' # remove the first item which corresponds to an input item
    CLEAR = 'clear' # clear content
    EVAL = 'eval' # evaluation
    HAS = 'has' # has label
    LEN = 'len' # Number of values

    GET_ITERATOR = 'iterator' # ITERATOR on labels

    INTERCEPTORS = 'interceptors' # interceptors
    GET_INTERCEPTOR_CONTAINER = 'getInterceptorContainer' # get interception container

    def __init__(self, source=None, type=None, *contents, **dictionary):
        """ 
        DEFAULT CONSTRUCTOR. Could be parameterized with couples of key string and magic box.
        """
        # content
        self._content = dict()
        # self type string
        self._type = type
        # default content
        content = self._defaultContent()
        # put all content which are not given by the input dictionary
        for label in content:
            self._content[label] = content[label]
        # source
        if source!=None:
            labels = source.labels()
            if labels!= None:
                for label in labels:
                    self._content[label] = content[label]
        # put dictionary
        if dictionary!=None:
            for label in dictionary:
                self._content[label] = dictionary[label]
        # put contents
        for content in contents:
            self+=content
    def _defaultContent(self):
        """
        Get default content whith keys which have no values
        """
        result = {
            MagicBox.GET: None,
            MagicBox.PUT: None,
            MagicBox.NEW_LABEL: None,
            MagicBox.LABELS: None,
            MagicBox.POP: None,
            MagicBox.POP_ITEM: None,
            MagicBox.CLEAR: None,
            MagicBox.EVAL: None,
            MagicBox.HAS: None,
            MagicBox.LEN: None,
            MagicBox.GET_ITERATOR: None,
            MagicBox.INTERCEPTORS: None,
            MagicBox.GET_INTERCEPTOR_CONTAINER: None,
        }
        return result
    def eval(self, params=None, *contents, **dictionary):
        """
        SELF EVALUATION
        """
        if params==None:
            params = mb()
        if contents!=None:
            params+=contents
        if dictionary!=None:
            params+=dictionary
        result = self._evalContent(MagicBox.EVAL, Eval, params)
        return result
    def get(self, label, default=None):
        """
        return specific python content
        """
        params = mb()
        params._content[Get.LABEL] = label
        params._content[Get.DEFAULT] = default
        result = self._evalContent(MagicBox.GET, Get, params)
        return result
    def has(self, label):
        params = mb()
        params._content[Get.LABEL] = label
        result = self._evalContent(MagicBox.HAS, Has, params)
        return result
    def put(self, value, label=None):
        """
        change content, and return the previous one
        """
        if label==None:
            label = self.newLabel()
        params = mb()
        params._content[Put.VALUE] = value
        params._content[Put.LABEL] = label
        result = self._evalContent(MagicBox.PUT, Put, params)
        return result
    def newLabel(self, context=None):
        """
        Get an available label in the context of an input mb context
        """
        params = mb()
        params._content[NewLabel.CONTEXT] = context
        result = self._evalContent(MagicBox.LABEL, Label, params)
        return result
    def labels(self, lowerBound = None, upperBound = None):
        """
        get a new magic box which contains self labels
        """
        params = mb()
        params._content[Labels.LOWER_BOUND] = lowerBound
        params._content[Labels.UPPER_BOUND] = upperBound
        result = self._evalContent(MagicBox.LABELS, Labels, params)
        return result
    def pop(self, label):
        """
        Remove an item from content which corresponds to the input label
        """
        params = mb()
        params._content[Pop.LABEL] = label
        result = self._evalContent(MagicBox.POP, Pop, params)
        return result
    def popItem(self, item):
        """
        Remove the input item
        """
        params = mb()
        params._content[PopItem.ITEM] = item
        result = self._evalContent(MagicBox.POP_ITEM, PopItem, params)
        return result
    def clear(self):
        """
        Clear content
        """
        result = self._evalContent(MagicBox.CLEAR, Clear)
        return result
    def len(self):
        """
        Return number of content
        """
        result = self._evalContent(MagicBox.LEN, Len)
        return result
    def getInterceptorContainer(self, label=None, mbtype=None, update=True):
        """
        Used in self eval method. Return the first interceptor stack to evaluate.
        """
        params = mb()
        params._content[Eval.EVAL_LABEL] = label
        params._content[GetInterceptorContainer.MB_TYPE] = mbtype
        params._content[GetInterceptorContainer.UPDATE] = update
        result = self._evalContent(MagicBox.GET_INTERCEPTOR_CONTAINER, GetInterceptorContainer, params)
        return result
    # private operations
    def _evalContent(self, label=None, type=None, params=None):
        """
        Eval content with an input label, default type to create if content doesn't exist and evaluation parameters.
        """
        result = Empty
        # get content
        content = self._getContent(label, type)
        # create args
        args = mb()
        args._content[Eval.CALLER] = self # may be a stack of callers
        args._content[Eval.PARAMS] = params
        args._content[Eval.EVAL_LABEL] = label
        # result is content private meta evaluation
        result = content._meval(args)
        return result
    def _meval(self, args):
        """
        Meta evaluation which processes meta information and parameters.
        """
        # create parameters
        params = mb()
        if Eval.PARAMS in args:
            params = args[Eval.PARAMS]
        result = self._eval(params)
        return result
    def _eval(self, params):
        """
        Private Evaluation to override in order to specialize self evaluation.
        """
        return self
    def _getContent(self, label=None, type=None, update=True):
        """
        get content or create a new type
        """
        result = Empty
        # update result only if label is in self._content
        if label in self._content:
            # first, get a default interceptor which evaluates self
            result = self._content[label]
            # if content does not exist, but if type is not null
            if result == None and type != None:
                # content is a new instance of type
                result = type()
                # if update, associate new content to label
                if update:
                    self._content[label] = result
            else:
                raise TypeError
        else:
            raise KeyError
        return result
    # python operators
    def __getattr__(self, label):
        """
        fired when an attribute lookup has not found the attribute in the usual place
        """
        return self.get(label)
    def __getitem__(self, label):
        """
        override python __getitem__ method
        """
        return self.get(label)
    def __setattribute__(self, label, value):
        """
        override python __setattribute__ method
        """
        return self.put(value, label)
    def __setitem__(self, label, value):
        """
        override python __setitem__ method
        """
        return self.put(value, label)
    def __delattr__(self, label):
        """
        override python delete method
        """
        return self.rem(label)
    def __delitem__(self, label):
        return self.rem(label)
    def __call__(self, params=None, *contents, **dictionary):
        return self.eval(params=params, *contents, **dictionary)
    def __iter__(self):
        return self._content.__iter__()
    def __contains__(self, item):
        return self.has(item)
    def __iter__(self):
        return self._content.__iter__()
    def __contains__(self, label):
        return self.has(label)
    def __len__(self):
        return self._content.len()
    def __sizeof__(self):
        return self._content.len()
    def __add__(self, other):
        result = mb(self)
        if isinstance(other, tuple) and len(other)==2:
            result.put(other[1], other[0])
        elif isinstance(other, MagicBox):
            result.put(other)
        return result
    def __iadd__(self, other):
        if isinstance(other, dict):
            for key in other:
                self.put(other[key], key)
        elif isinstance(other, list):
            for item in list:
                self.put(item)
        elif isinstance(other, tuple) and len(other)==2:
            self.put(other[1], other[0])
        elif isinstance(other, MagicBox):
            self.put(other)
        return self
    def __sub__(self, other):
        result = mb(self)
        if isinstance(other, MagicBox):
            result.popItem(other)
        elif isinstance(other, str):
            result.pop(other)
        return result
    def __isub__(self, other):
        if isinstance(other, MagicBox):
            self.popItem(other)
        elif isinstance(other, str):
            self.pop(other)
        return self
    def __and__(self, other):
        result = mb(contents=(self._content & other._content))
        return result
    def __iand__(self, other):
        self._content &= other._content
        return self
        

# Shortcut for MagicBox construction
mb = MagicBox

class Empty(MagicBox, object):
    """
    Empty box which does not accept content
    """
    pass

Empty = Empty()

class Eval(MagicBox):
    """
    Class dedicated to evaluate a MagicBox
    """
    CALLER = 'CALLER'
    EVAL_LABEL = 'EVAL_LABEL'
    PARAMS = 'PARAMS'
    
    def __init__(self, source=None, type=None, *contents, **dictionary):
        MagicBox.__init__(source, type, *contents, **dictionary)
        # evaluation eval content is self
        self[MagicBox.EVAL] = self
    def _meval(self, args):
        """
        Recall caller mevaluation.
        """
        caller = _param(args, Eval.CALLER)
        result = caller._meval(args)
        return result
    def _param(self, args, param, default=None):
        """
        Get parameters from args, or default value
        """
        result = default
        if args.contains(param):
            result = args[param]
        return result
    def _args(self, caller, evaluationLabel, params):
        """
        Create arguments from a caller, evaluation name and parameters
        """
        result = mb()
        result[Eval.CALLER] = caller
        result[Eval.PARAMS] = params
        result[Eval.EVAL_LABEL] = evaluationLabel
        return result

class InterceptedEval(Eval):
    """
    Intercepted evaluation which allows to intercept calls.
    """
    def _meval(self, args):
        result = Empty
        # get interceptor container for label evaluation only in first call
        interceptorContainer = self._getContent(MagicBox.GET_INTERCEPTOR_CONTAINER, GetInterceptorContainer)
        # if interceptorContainer exists
        if interceptorContainer != Empty:
            # evaluate get content
            result = interceptorContainer(params=args)
        return result

class Get(Eval):
    """
    Evaluation for Get operation
    """
    LABEL = 'LABEL'
    DEFAULT = 'DEFAULT'
    def _eval(self, args):
        caller = self._param(args, Eval.CALLER)
        label = self._param(args, Eval.LABEL)
        result = caller._content[label]
        return result

class Has(Get):
    """
    Evaluation for has operation
    """
    def _eval(self, args):
        caller = self._param(params, Eval.CALLER)
        label = self._param(params, Get.LABEL)
        result = label in caller._content.keys()
        return result

class Put(Get):
    """
    Evaluation for put operation
    """
    VALUE = 'VALUE'
    def _eval(self, args):
        caller = self._param(args, Eval.CALLER)
        label = self._param(args, Get.LABEL)
        result = caller[label]
        value = self._param(args, Put.VALUE)
        caller._content[label] = value
        return result

class Pop(Get):
    """
    Evaluation for pop operation
    """
    def _eval(self, args):
        label = self._param(args, Get.LABEL)
        caller = self._param(args, Eval.CALLER)
        result = caller._content
        del caller._content[label]

class PopItem(Pop):
    """
    Evaluation for PopItem
    """
    ITEM = 'item'
    def _eval(self, args):
        item = self._param(args, PopItem.ITEM)
        caller = self._param(args, Eval.CALLER)
        if item == None:
            caller._content.clear()
        for label, value in enumerate(caller._content):
            if value==item:
                del caller._content[label]
                break

class Clear(Pop):
    """
    Evaluation for clear operation
    """
    def _eval(self, args):
        self._content.clear()
        return self

class NewLabel(Get):
    """
    Evaluation for Available Label operation.
    """
    CONTEXT = 'context'
    def _eval(self, args):
        context = self._param(args, NewLabel.CONTEXT)
        caller = self._param(args, Eval.CALLER)
        try:
            caller._newLabel += 1
        except:
            caller._newLabel = 0
        result = caller._newLabel
        return result

class Labels(Get):
    """
    Evaluation for labels operation
    """
    LOWER_BOUND = 'lower'
    UPPER_BOUND = 'upper'
    def _eval(self, args):
        result = []
        # get caller
        caller = self._param(args, Eval.CALLER)
        lower = self._param(args, Labels.LOWER_BOUND, 0)
        upper = self._param(args, Labels.UPPER_BOUND, -1)
        # new magicbox initialized with all caller keys
        keys = caller._content.keys()[lower:upper]
        result = mb(keys)
        return result

class Len(Get):
    """
    Evaluation for Len operation
    """
    def _eval(self, args):
        caller = self._param(args, Eval.CALLER)
        result = caller._content.len()
        return result

# Interceptors
class Interceptors(MagicBox):
    """
    Class used to managed magic box interceptors. Labels correspond to magic box labels to intercept, and values are magic box of interceptors.
    """
    ALL = '*'
    DYNAMIC = 'DYNAMIC'

class GetInterceptorContainer(Eval):
    """
    Stack of Interceptors
    """
    MB_TYPE = 'type'
    UPDATE = 'update'
    def _eval(self, args):
        caller = self.param(args, Eval.CALLER)
        eval_label = self.param(args, Eval.EVAL_LABEL)
        mbtype = self.param(args, GetStackOfInterceptors.MB_TYPE)
        update = self.param(args, GetStackOfInterceptors.UPDATE)
        # default result is empty
        result = Empty
        # first, try to get a default content if content does not exists
        content = caller._getContent(eval_label, mbtype, update)
        # if content exists
        if content != Empty:
            # by default, the result is a default interceptor container
            result = StackOfInterceptors(content)
            # get self interceptors
            interceptors = caller.evalInterceptor(MagicBox.INTERCEPTORS, Inters)
            if interceptors != Empty:
                # get specific interceptors if label exists
                if label != None:
                    specificInters = interceptors._content[label]
                    if specificIntercs != None:
                        for _label in specificInterceptors:
                            interceptor = specificInterceptors[_label]
                            if interceptor.check(args):
                                result = StackOfInterceptors(interceptor, result)
                # dynamic interceptors
                dynamicInterceptors = interceptors._content[Interceptors.DYNAMIC]
                if dynamicInterceptors != None:
                    for _label in dynamicInterceptors:
                        interceptor = dynamicInterceptors[_label]
                        result = StackOfInterceptors(interceptor, result)
                # global interceptors
                globalInterceptors = interceptors._content[Interceptors.ALL]
                if globalInterceptors != None:
                    for _label in globalInterceptors:
                        interceptor = globalInterceptors[_label]
                        result = StackOfInterceptors(interceptor, result)
        return result

class Interceptor(MagicBox):
    """
    Interceptor used to evaluate a magicbox
    """
    def _eval(self, args):
        callee = args._content[InterceptorContainer.NEXT]
        result = callee._eval(args)
        return result
    def _evalInterceptor(self, label=None, type=None, params=None):
        return self._eval(params)

class InterceptorContainer(Interceptor):
    """
    In charge of evaluate an interceptor
    """
    NEXT = 'NEXT'
    INTERCEPTOR = 'INTERCEPTOR'
    def __init__(self, interceptor, next=Empty):
        MagicBox.__init__(self)
        self._content[InterceptorContainer.INTERCEPTOR] = interceptor
        if next!=Empty:
            self._content[InterceptorContainer.NEXT] = next
    def _eval(self, args):
        # get interceptor
        interceptor = self._content[InterceptorContainer.INTERCEPTOR]
        # add the next InterceptorContainer to evaluate
        if InterceptorContainer.NEXT in self._content:
            args._content[InterceptorContainer.NEXT] = self._content[InterceptorContainer.NEXT]
            # evaluate the interceptor with args
            result = interceptor(args)        
        else:
            if InterceptorContainer.NEXT in args._content:
                del args._content[InterceptorContainer.NEXT]
            result = interceptor._eval(args)
        return result
    
