from src.cmp.semantic import Type,Context,SemanticError,Method
from src.semantic_checker.utils.types import *
from src.semantic_checker.utils.statements import *

class Hulk_Context(Context):
    def __init__(self):
        Context.__init__(self)
        self.func = {}
        self.protocol={}
    def create_func(self, name, params, return_type):
        if name in self.func:
            raise SemanticError(f'Function with the same name ({name}) already in context.')
        for _param in params:
            if _param.type is None:
                _param.type=NoneType()
            else:
                _param.type=self.get_type(_param.type)
        typex = self.func[name] = Func(name,params,return_type)
        return typex

    def get_func(self, name:str):
        try:
            return self.func[name]
        except KeyError:
            raise SemanticError(f'Function "{name}" is not defined.')
        
    def create_protocol(self,name,methods,parents=None):
        if name in self.protocol:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.')
        typex = self.protocol[name] = Protocol(name,methods,parents)
        return typex
    def get_protocol(self,name:str):
        try:
            return self.protocol[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.')

        
    def __str__(self):
        types_str='Types: {\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'
        func_str='Functions: {\n\t' + '\n\t'.join(y for x in self.func.values() for y in str(x).split('\n')) + '\n}'
        protocol_str='Protocol: {\n\t' + '\n\t'.join(y for x in self.protocol.values() for y in str(x).split('\n')) + '\n}'
        return types_str+'\n'+func_str +'\n'+protocol_str
    
