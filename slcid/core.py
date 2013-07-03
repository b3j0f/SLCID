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

    GET_ITERATOR = '_iterator' # ITERATOR on labels

    INTERCEPTORS = '_interceptors' # interceptors
    GET_INTERCEPTOR_CONTAINER = '_getInterceptorContainer' # get interception container

    def __init__(self, sources=None, typeName=None, interceptors=None, *contents, **contentsWithLabels):
        """ 
        DEFAULT CONSTRUCTOR. Could be parameterized with couples of key string and magic box.
        """
        # content is a dictionary
        self._content = dict()
        # self type string
        if typeName == None:
            # default type name is python class name
            self._typeName = type(self).__name__
        else:
            self._typeName = typeName
        # default content
        content = self._defaultContent()
        # put all content which are not given by the input contentsWithLabels
        for label in content:
            self._content[label] = content[label]
        # sources
        if sources!=None:
            if isinstance(sources, MB):
                labels = source.labels()
                if labels != None:
                    for label in labels:
                        self._content[label] = content[label]
            elif isinstance(sources, list):
                for source in sources:
                    labels = source.labels()
                    if labels != None:
                        for label in labels:
                            self._content[label] = content[label]
        # put dictionary
        for label in contentsWithLabels:
            self._content[label] = contentsWithLabels[label]
        # put contents
        for content in contents:
            self += content
        # put interceptors
        if interceptors != None:
            _interceptors = MB()
            _interceptors += interceptors
            self._content[MagicBox.INTERCEPTORS] = _interceptors
    def _defaultContent(self):
        """
        Get default content whith keys which are python type values
        """
        result = {
            MagicBox.GET: Get,
            MagicBox.PUT: Put,
            MagicBox.NEW_LABEL: NewLabel,
            MagicBox.LABELS: Labels,
            MagicBox.POP: Pop,
            MagicBox.POP_ITEM: PopItem,
            MagicBox.CLEAR: Clear,
            MagicBox.EVAL: Eval,
            MagicBox.HAS: Has,
            MagicBox.LEN: Len,
            MagicBox.GET_ITERATOR: GetIterator,
            MagicBox.INTERCEPTORS: Interceptors,
            MagicBox.GET_INTERCEPTOR_CONTAINER: GetInterceptorContainer,
        }
        return result
    # public methods
    def eval(self, params=None, *contents, **dictionary):
        """
        SELF EVALUATION
        """
        if params==None:
            params = MB()
        params+=contents
        params+=dictionary
        result = self._evalContent(MagicBox.EVAL, params)
        return result
    def get(self, label, default=None):
        """
        return specific python content
        """
        params = MB()
        params._content[Get.LABEL] = label
        params._content[Get.DEFAULT] = default
        result = self._evalContent(MagicBox.GET, params)
        return result
    def has(self, label):
        params = MB()
        params._content[Get.LABEL] = label
        result = self._evalContent(MagicBox.HAS, params)
        return result
    def put(self, value, label=None):
        """
        change content, and return the previous one
        """
        if label==None:
            label = self.newLabel()
        params = MB()
        params._content[Put.VALUE] = value
        params._content[Put.LABEL] = label
        result = self._evalContent(MagicBox.PUT, params)
        return result
    def newLabel(self, context = None):
        """
        Get an available label in the context of an input mb context
        """
        params = MB()
        params._content[NewLabel.CONTEXT] = context
        result = self._evalContent(MagicBox.LABEL, params)
        return result
    def labels(self, lowerBound = None, upperBound = None):
        """
        get a new magic box which contains self labels
        """
        params = MB()
        params._content[Labels.LOWER_BOUND] = lowerBound
        params._content[Labels.UPPER_BOUND] = upperBound
        result = self._evalContent(MagicBox.LABELS, params)
        return result
    def pop(self, label):
        """
        Remove an item from content which corresponds to the input label
        """
        params = MB()
        params._content[Pop.LABEL] = label
        result = self._evalContent(MagicBox.POP, params)
        return result
    def popItem(self, item):
        """
        Remove the input item
        """
        params = MB()
        params._content[PopItem.ITEM] = item
        result = self._evalContent(MagicBox.POP_ITEM, params)
        return result
    def clear(self):
        """
        Clear content
        """
        result = self._evalContent(MagicBox.CLEAR)
        return result
    def len(self):
        """
        Return number of content
        """
        result = self._evalContent(MagicBox.LEN)
        return result
    def getInterceptorContainer(self, label=None):
        """
        Used in self eval method. Return the first interceptor stack to evaluate.
        """
        params = MB()
        if label != None:
            params._content[Eval.EVAL_LABEL] = label
        result = self._evalContent(MagicBox.GET_INTERCEPTOR_CONTAINER, params)
        return result
    # private operations
    def _evalContent(self, label=EVAL, params=None):
        """
        Eval content with an input label, default type to create if content doesn't exist and evaluation parameters.
        """
        result = None
        # get content or raise an error
        content = self._getContent(label)
        # get default interceptor container
        getInterceptorContainer = self._getContent(MagicBox.GET_INTERCEPTOR_CONTAINER)
        
        interceptorContainer = self.getInterceptorContainer(label)
        # initialize meta values which may be given by the execution engine
        args = MB()
        args._content[Eval.PARAMS] = params
        args._content[Eval.CALLER] = self
        args._content[Eval.EVAL_LABEL] = label
        # evaluate the interceptor container
        result = interceptorContainer(args)
        return result
    def _getContent(self, label=EVAL):
        """
        Get content and initialize it before get it if not already initialized
        """
        # get content or raise an error
        result = self._content[label]
        # if content is a type, then it is initialized with its instantiation
        if isinstance(result, type):
            # then it is initialized with its instantiation
            result = result()
            # and update value in content
            self._content[label] = result
        return result
    def _eval(self, args):
        """
        Private Evaluation to override in order to specialize self evaluation if no evaluation content exists.
        """
        return self
    # python operators
    def __getattr__(self, label):
        """
        Fired when an accessor doesn't exist. Return content with input label.
        """
        return self.get(label)
    def __getitem__(self, label):
        """
        Override python __getitem__ method
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
    def __contains__(self, label):
        return self.has(label)
    def __len__(self):
        return self._content.len()
    def __sizeof__(self):
        return self._content.len()
    def __add__(self, other):
        result = MB(self)
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
        result = MB(self)
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
        result = MB(contents=(self._content & other._content))
        return result
    def __iand__(self, other):
        self._content &= other._content
        return self
    def __or__(self, other):
        result = MB(contents=(self._content | other._content))
        return result
    def __ior__(self, other):
        self._content |= other._content
    def __xor__(self, other):
        result = MB(contents=(self._content ^ other._content))
        return result
    def __ixor__(self, other):
        self._content ^= other._content

# Shortcut for MagicBox construction
MB = MagicBox

class Empty(MagicBox, object):
    """
    Empty box which does not accept content
    """
    pass

class Eval(MagicBox):
    """
    Class dedicated to evaluate a MagicBox
    """
    CALLER = 'CALLER'
    EVAL_LABEL = 'EVAL_LABEL'
    PARAMS = 'PARAMS'
    def _defaultContent(self):
        result = MagicBox._defaultContent(self)
        result[MagicBox.EVAL] = self
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
        result = MB()
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
        result = MB(keys)
        return result

class Len(Get):
    """
    Evaluation for Len operation
    """
    def _eval(self, args):
        caller = self._param(args, Eval.CALLER)
        result = caller._content.len()
        return result

class GetIterator(Get):
    """
    Evaluation for GetIterator operation
    """
    def _eval(self, args):
        caller = self._param(args, Eval.CALLER)
        result = caller._content.iterator()
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
    UPDATE = 'update'
    def _defaultContent(self):
        result = MagicBox._defaultContent(self)
        result[MagicBox.GET_INTERCEPTOR_CONTAINER] = self
        return result
    def eval(self, args):
        caller = self.param(args, Eval.CALLER)
        eval_label = self.param(args, Eval.EVAL_LABEL)
        update = self.param(args, GetInterceptorContainer.UPDATE)
        # default result is empty
        result = Empty
        # first, try to get a default content if content does not exists
        content = caller._evalContent(eval_label, update)
        # if content exists
        if content != Empty:
            # by default, the result is a default interceptor container
            result = InterceptorContainer(content)
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
                                result = InterceptorContainer(interceptor, result)
                # dynamic interceptors
                dynamicInterceptors = interceptors._content[Interceptors.DYNAMIC]
                if dynamicInterceptors != None:
                    for _label in dynamicInterceptors:
                        interceptor = dynamicInterceptors[_label]
                        result = InterceptorContainer(interceptor, result)
                # global interceptors
                globalInterceptors = interceptors._content[Interceptors.ALL]
                if globalInterceptors != None:
                    for _label in globalInterceptors:
                        interceptor = globalInterceptors[_label]
                        result = InterceptorContainer(interceptor, result)
        return result

class Interceptor(MagicBox):
    """
    Interceptor used to evaluate a magicbox
    """
    def _eval(self, args):
        callee = args._content[InterceptorContainer.NEXT]
        result = callee.eval(args)
        return result

class InterceptorContainer(Interceptor):
    """
    In charge of evaluate an interceptor or a magic box
    """
    NEXT = 'NEXT'
    INTERCEPTOR = 'INTERCEPTOR'
    def __init__(self, interceptor, next=None):
        MagicBox.__init__(self)
        self._content[InterceptorContainer.INTERCEPTOR] = interceptor
        if next!=None:
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
            # if next exists in args, delete it
            if InterceptorContainer.NEXT in args._content:
                del args._content[InterceptorContainer.NEXT]
            # if evaluation doesn't exist or evaluation equals to interceptor
            if MagicBox.EVAL not in interceptor._content or interceptor._content[MagicBox.EVAL]==interceptor:
                # evaluate private evaluation
                result = interceptor._eval(args)
            else:
                # evaluate public evaluation
                result = interceptor.eval(args)
        return result

class MBConf:
    """
    MB configurator annotation
    """
    def __init__(self, sources=None, typeName=None, interceptors=None, *contents, **contentsWithLabels):
        self.sources = sources
        self.typeName = typeName
        self.interceptors = interceptors
        self.contents = contents
        self.contentsWithLabels = contentsWithLabels
    def __call__(self, t):
        def configureMB(sources=None, typeName=None, interceptors=None, *contents, **contentsWithLabels):
            _sources = self.sources
            _typeName = self.typeName
            _interceptors = self.interceptors
            _contents = self.contents
            _contentsWithLabels = self.contentsWithLabels
            result = t(_sources, _typeName, _interceptors, _contents, _contentsWithLabels)
            if sources != None:
                result |= sources
            return result
        return configureMB

def list2mb(l):
    """
    Get a MB from a list
    """
    result = MB()
    result += l
    return result

def dict2mb(d):
    """
    Get a MB from a dictionary
    """
    result = MB()
    result += d
    return result

Empty = Empty()
