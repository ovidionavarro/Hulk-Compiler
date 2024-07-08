import src.cmp.visitor as visitor
from src.semantic_checker.ast import *
from src.semantic_checker.utils.context import *
from src.semantic_checker.utils.types import *

def check_methods(node,parent):
    if parent is None:
        return False
    this_type = parent.name
    if node.name == this_type:
        return False
    for n in node.methods:
        for p in parent.methods:
            if n.name == p.name:
                if len(n.param_names) != len(p.param_names):
                    return True
    return check_methods(node,parent.parent)

def check_parents(initial_type,parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
       return check_parents(initial_type,parent.parent)
    else: return False
class TypeCollector(object):
    def __init__(self,errors=[]) :
        self.context=None
        self.errors=errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context=Hulk_Context()
        self.context.types['Number']=NumType()
        self.context.types['String']=StringType()
        self.context.types['Boolean']=BoolType()
        self.context.types['None']=NoneType()   
        self.context.types['Object']=ObjectType()   
        self.context.types['<error>']=ErrorType()
        self.context.func['sin']=Func('sin',[ParameterNode('angle','Number')],NumType())
        self.context.func['cos']=Func('cos',[ParameterNode('angle','Number')],NumType())
        self.context.func['tan']=Func('tan',[ParameterNode('angle','Number')],NumType())
        self.context.func['print']=Func('print',[ParameterNode('value','Object')],NoneType())
        self.context.func['log']=Func('log',[ParameterNode('base','Number'),ParameterNode('value','Number')],NumType())
        self.context.func['sqrt']=Func('sqrt',[ParameterNode('value','Number')],NumType())
        self.context.func['exp']=Func('exp',[ParameterNode('value','Number')],NumType())
        self.context.func['rand']=Func('rand',[],NoneType())
        self.context.create_protocol('iterable')
        self.context.protocol['iterable'].define_method('next',[],BoolType())
        self.context.protocol['iterable'].define_method('current',[],ObjectType())
        for statement in node.statements:
            if isinstance(statement,TypeNode) or isinstance(statement,ProtocolNode) or isinstance(statement,FunctionNode):
                self.visit(statement)

    @visitor.when(TypeNode)
    def visit(self,node):
        try:
            self.context.create_type(node.name)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FunctionNode)
    def visit(self,node):
        try:
            self.context.create_func(node.name,node.parameters,node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtocolNode)
    def visit(self,node):
        try:    
            self.context.create_protocol(node.name)
        except SemanticError as ex:
            self.errors.append(ex.text)


class TypeBuilder:
    def __init__(self,context,error=[]):
        self.context=context
        self.current_type=None
        self.errors=error

    @visitor.on('node')
    def visit(self,node):
        pass

####Verificar primero los typos y protocolos que heredan de object o no lo hacen
    @visitor.when(ProgramNode)
    def visit(self,node):
        for statement in node.statements:
            if isinstance(statement,TypeNode):
                if statement.inherits=='Object':
                    self.visit(statement)
            if isinstance(statement,ProtocolNode):
                if statement.extends=='':
                    self.visit(statement)
        for statement in node.statements:
            if isinstance(statement,TypeNode):
                if statement.inherits!='Object':
                    self.visit(statement)
            if isinstance(statement,ProtocolNode):
                if statement.extends!='':
                    self.visit(statement)
            # if isinstance(statement,FunctionNode):
            #     self.visit(statement)        

    @visitor.when(TypeNode)
    def visit(self,node):
        self.current_type=self.context.get_type(node.name)
        
        if node.inherits:
            try:
                if node.inherits in ['Number','Boolean','String']:
                    error= SemanticError('cannot be inherited from Number, Boolean or String')
                    self.errors.append(error.text)
                parent_type=self.context.get_type(node.inherits)
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
            except SemanticError as ex:
                self.errors.append(ex.text)
            if check_parents(self.current_type.name,self.current_type.parent):
                error= SemanticError("Cyclic inheritance is not allowed.")
                self.errors.append(error.text)
        for corp in node.corpus:
            self.visit(corp)
        
        if check_methods(self.current_type,self.current_type.parent):
                error= SemanticError("Using the same method name with different arguments is not allowed.")
                self.errors.append(error.text)
    
    @visitor.when(FunctionNode)
    def visit(self,node):
        params_names=[]
        params_types=[]
        for params in node.parameters:
            params_names.append(params.name)
            try:
                param_type=self.context.get_type(params.type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                param_type=ErrorType()
            params_types.append(param_type)  
        try:
            type=self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type=ErrorType()     
        
        try:
            self.current_type.define_method(node.name,params_names,params_types,type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(TypeAttributeNode)
    def visit(self,node):
        try:
            att_type=self.context.get_type(node.var.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            att_type=ErrorType()
        try:
            self.current_type.define_attribute(node.var.name,att_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
    
    @visitor.when(ProtocolNode)
    def visit(self,node):
        self.current_protocol=self.context.get_protocol(node.name)

        if node.extends!='':
            try:
                parent_protocol=self.context.get_protocol(node.extends)
                try:
                    self.current_protocol.set_parent(parent_protocol)
                except SemanticError as ex:
                    self.errors.append(ex.text)
            except SemanticError as ex:
                self.errors.append(ex.text)
            if check_parents(self.current_protocol.name,self.current_protocol.parent):
                error= SemanticError("Cyclic extends is not allowed.")
                self.errors.append(error.text)
        for corp in node.corpus:
            self.visit(corp)

    @visitor.when(ProtocolMethodNode)
    def visit(self,node):
       
        # params_names=[]
        # params_types=[]
        for params in node.parameters:
            # params_names.append(params.name)
            try:
                params.type=self.context.get_type(params.type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                param_type=ErrorType()
            # params_types.append(param_type)  
        try:
            type=self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type=ErrorType()
             
        
        try:
            self.current_protocol.define_method(node.name,node.parameters,type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    def update_globals_function(self):
        for func in self.context.func.values():
            
            if func.name in ['sin','cos','tan','log','sqrt','exp','rand','print']:
                continue
            try:
                func.return_type=self.context.get_type(func.return_type)
            except SemanticError as ex:
                func.return_type=ErrorType()
                self.errors.append(ex.text)
            for param in func.params:
                try:
                    param.type=self.context.get_type(param.type)
                except SemanticError as ex:
                    param.type=ErrorType()
                    self.errors.append(ex.text)