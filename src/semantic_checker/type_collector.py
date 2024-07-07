import src.cmp.visitor as visitor
from src.semantic_checker.ast import *
from src.semantic_checker.utils.context import *
from src.semantic_checker.utils.types import *

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