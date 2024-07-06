import itertools as itl

class VariableInfo:
    def __init__(self, name):
        self.name = name

class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Scope:
    def __init__(self, parent=None):
        self.local_vars = []
        self.local_funcs = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
    # create child scope
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    # define variable
    def define_variable(self, vname):
        # Your code here!!!
        if self.is_local_var(vname):
            return False
        self.local_vars.append(VariableInfo(vname))
        return True
    
    def define_function(self, fname, params):
        # Your code here!!!
        if self.is_local_func(fname,len(params)):
            return False
        self.local_funcs.append(FunctionInfo(fname,params))
        return True

    def is_var_defined(self, vname):   # ARREGLAR: BUSCAR EN PARENT SOLO HASTA VAR_INDEX_AT_PARENT
        # Your code here!!!
        return self.is_local_var(vname) or (self.parent.is_var_defined(vname) if self.parent is not None else False)    
    
    def is_func_defined(self, fname, n):     # ARREGLAR: BUSCAR EN PARENT SOLO HASTA FUNC_INDEX_AT_PARENT
        # Your code here!!!
        return self.is_local_func(fname,n) or (self.parent.is_func_defined(fname,n) if self.parent is not None else False)

    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname):
        # Your code here!!!
        for var_info in self.local_vars:
            if vname == var_info.name:
                return var_info
        return None
    
    def get_local_function_info(self, fname, n):
        # Your code here!!!
        for func_info in self.local_funcs:
            if fname == func_info.name and n == len(func_info.params):
                return func_info
        return None       
    
    
scope = Scope()