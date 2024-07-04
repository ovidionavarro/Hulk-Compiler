from typing import List ,Union

class Node:
    """basic node"""
    pass
#NODE
class StatementNode(Node):
    """type,expression,function,protocol"""
    pass
class ExpressionNode(StatementNode):
    def __init__(self):
        self.type_value='Object'
class ProgramNode:
    def __init__(self, statements: List[StatementNode]):
        self.statements = statements
class ParameterNode(Node):
    def __init__(self,name:str,type:str='Object'):
        self.name=name
        self.type=type
class FunctionNode(StatementNode):
    def __init__(self,name:str,parameters:List[ParameterNode],corpus:ExpressionNode,type:str='Object'):
        self.name=name
        self.parameters=parameters
        self.corpus=corpus
        self.type=type
class TypeAttributeNode(Node):
    def __init__(self,param:ParameterNode,value=ExpressionNode):
        self.var=param
        self.value=value
class ProtocolMethodNode(Node):
    def __init__(self,name:str,parameters:List[ParameterNode],type:str):
        self.name=name
        self.parameters=parameters
        self.type=type

class TypeNode(StatementNode):
    def __init__(self,name:str,corpus:List[Union[FunctionNode,TypeAttributeNode]],
                 parameters:List[ParameterNode],inherits:str='Object',
                 arguments:List[ExpressionNode]=[]):
        self.name=name
        self.corpus=corpus
        self.constructor=parameters
        self.inherits=inherits
        self.arguments=arguments

class ProtocolNode(StatementNode):
    def __init__(self,name:str,corpus:List[ProtocolMethodNode],extends:str=''):
        self.name=name
        self.corpus=corpus
        self.extends=extends


#EXPRESSION_NODE
class ExpressionBlockNode(ExpressionNode):
    def __init__(self,expressions:List[ExpressionNode]):
        self.expressions=expressions
        self.type_value='Object'

    #LOW PRIORITY
class LetNode(ExpressionNode):
    def __init__(self,variable_names:List[ParameterNode],
                 variable_values:List[ExpressionNode],expression:ExpressionNode):
        self.vars=variable_names
        self.values=variable_values
        self.expression=expression
        self.value_type='Object'
class IfElseExpression(ExpressionNode):
    def __init__(self,condition:List[ExpressionNode],expressions:List[ExpressionNode]):
        self.condition=condition
        self.cases=expressions
        self.type_value='Object'
class DesctructiveExpression(ExpressionNode):
    def __init__(self,name:str,expression:ExpressionNode):
        self.name=name
        self.expression=expression
        self.type_value='Object'
class SelfVaraiableNode(ExpressionNode):
    def __init__(self,is_self:bool,name:str):
        self.is_self=is_self
        self.name=name
        self.type_value='Object'
class SelfDesctructiveExpression(ExpressionNode):
    def __init__(self,var:SelfVaraiableNode,expression:ExpressionNode):
        self.var=var
        self.expression=expression
        self.value='Object'
class WhileNode(ExpressionNode):
    def __init__(self,condition:ExpressionNode,expression:ExpressionNode):
        self.condition=condition
        self.expression=expression
        self.type_value='Object'

class ForNode(ExpressionNode):
    def __init__(self,name:str,collection:ExpressionNode,expression:ExpressionNode):
        self.name=name
        self.collection=collection
        self.expression=expression
        self.type_value='Object'
class NewNode(ExpressionNode):
    def __init__(self,name:str,arguments:List[ExpressionNode]):
        self.name=name
        self.arguments=arguments
        self.type_value='Object'

    #HIGH PRIORITY

class NumberNode(ExpressionNode):
    def __init__(self, value):
        self.value = value
        self.type_value = 'Object'

class StringNode(ExpressionNode):
    def __init__(self, value):
        self.value = value
        self.type_value = 'Object'

class BooleanNode(ExpressionNode):
    def __init__(self, value):
        self.value = value
        self.type_value = 'Object'

class VariableNode(ExpressionNode):
    def __init__(self, name: str):
        self.name = name
        self.type_value = 'Object'


class FunctionCallNode(ExpressionNode):
    def __init__(self, name: str, arguments: List[ExpressionNode]):
        self.funct = name
        self.arguments = arguments
        self.type_value = 'Object'

class TypeFunctionCallNode(ExpressionNode):
    def __init__(self, class_calling: ExpressionNode, name: str, arguments: List[ExpressionNode]):
        self.class_ = class_calling
        self.funct = name
        self.arguments = arguments
        self.type_value = 'Object'
class ListNode(ExpressionNode):
    def __init__(self, expressions: List[ExpressionNode]):
        self.elements = expressions
        self.type_value = 'Object'
class ImplicitListNode(ExpressionNode):
    def __init__(self, operator: ExpressionNode, iterator: str, collection: ExpressionNode):
        self.operation = operator
        self.iteration = iterator
        self.collection = collection
        self.type_value = 'Object'

class IndexingNode(ExpressionNode):
    def __init__(self, collection: ExpressionNode, index: ExpressionNode):
        self.collection = collection
        self.index = index
        self.type_value = 'Object'

class AsNode(ExpressionNode):
    def __init__(self,left:ExpressionNode,right:str):
        self.expression=left
        self.type=right
        self.type_value='Object'




    #OPERATIONS

class OrAndExpression(ExpressionNode):
    def __init__(self,operation:str,left:ExpressionNode,right:ExpressionNode):
        self.operation=operation
        self.left=left
        self.right=right
        self.type_value='Object'
class NotExpression(ExpressionNode):
    def __init__(self,expression:ExpressionNode):
        self.expression=expression
        self.type_value='Object'
class ComparationExpression(ExpressionNode):
    def __init__(self,operation:str,left:ExpressionNode,right:ExpressionNode=None):
        self.operation = operation
        self.left = left
        self.right = right
        self.type_value = 'Object'
class IsExpression(ExpressionNode):
    def __init__(self,left:ExpressionNode,name:str):
        self.left=left
        self.name=name
        self.type_value='Object'
class AritmethicExpression(ExpressionNode):
    def __init__(self,operation:str,left:ExpressionNode,right:ExpressionNode):
        self.operation = operation
        self.left = left
        self.right = right
        self.type_value = 'Object'
class StringConcatenationNode(ExpressionNode):
    def __init__(self,left:ExpressionNode,right:ExpressionNode,double:bool=False):
        self.left = left
        self.right = right
        self.double=double
        self.type_value = 'Object'
