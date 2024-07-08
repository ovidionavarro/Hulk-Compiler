from src.cmp.semantic import SemanticError,Method

class Func:
    def __init__(self,name,args=[],return_type='Object') :
        self.name = name
        self.params = args
        self.return_type = return_type

    def __str__(self):
        output = self.name
        output += ' ('
        params = ', '.join(f'{n.name}:{n.type}' for n in self.params)
        output += params
        output += ') :'
        output += str(self.return_type)
        return output

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type #and \
            #other.param_types == self.param_types   
    
class Protocol:
    def __init__(self,name:str):
        self.name=name
        self.parent = None
        self.methods=[]
    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def define_method(self, name:str, params:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        params_names=[]
        params_types=[]
        for met in params:
            params_names.append(met.name)
            params_types.append(met.type)
            
        method = Method(name, params_names,params_types, return_type)
        self.methods.append(method)
        return method
        
    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            
    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else ' : '+self.parent.name
        output +=': '+ parent
        output += ' {'
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output
    
