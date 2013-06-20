import core.MagicBox

class Eval(MagicBox):
    """
    Class dedicated to evaluate a MagicBox
    """
    CALLER = 'CALLER'
    EVAL_LABEL = 'EVAL_LABEL'
    PARAMS = 'PARAMS'
    def _eval(self, args):
        caller = _param(args, Eval.CALLER)
        result = caller(args)
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
        create arguments from a caller, evaluation name and parameters
        """
        result = mb()
        result[Eval.CALLER] = caller
        result[Eval.PARAMS] = params
        result[Eval.EVAL_LABEL] = evaluationLabel
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
    LOWER = 'lower'
    UPPER = 'upper'
    def _eval(self, args):
        result = []
        # get caller
        caller = self._param(args, Eval.CALLER)
        lower = self._param(args, Labels.LOWER, 0)
        upper = self._param(args, Labels.UPPER, -1)
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
