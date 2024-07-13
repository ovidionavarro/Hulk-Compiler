import src.cmp.visitor as visitor
from src.cmp.semantic import Scope
from src.semantic_checker.ast import *
from src.semantic_checker.utils.types import *

#errors
NUMBER_ARGUMENT='Method "%s" have "%s" arguments'
WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation"%s" is not defined between "%s" and "%s".'

class TypeChecker:
    def __init__(self,context,errors):
        self.context=context
        self.errors=errors
        self.current_type=None
        self.current_method=None 

    @visitor.on('node')
    def visit(self,node,scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node,scope=None):
        scope=Scope()
        for statement in node.statements:
            self.visit(statement,scope.create_child())
        return scope                
#=============Typos================#    
    @visitor.when(TypeNode)
    def visit(self,node:TypeNode,scope):
        self.current_type=self.context.get_type(node.name)
        for param in node.constructor:
            param_type=self.context.get_type(param.type)
            scope.define_variable(param.name,param_type)

        for corp in node.corpus:
            self.visit(corp,scope)
    
    @visitor.when(FunctionNode)
    def visit(self,node:FunctionNode,scope):

        self.current_method=self.context.func[node.name]
        # print(self.current_method.return_type)
        for param in self.current_method.params:
            scope.define_variable(param.name,param.type)
        self.visit(node.corpus,scope)
        print(node.corpus.type_value,'->',self.current_method.return_type)
        print(node.corpus.type_value.conforms_to(self.current_method.return_type))
        if(not node.corpus.type_value.conforms_to(self.current_method.return_type)):
            self.errors.append(INCOMPATIBLE_TYPES % (self.current_method.return_type,node.corpus.type_value))
           


    @visitor.when(TypeAttributeNode)
    def visit(self,node:TypeAttributeNode,scope):
        self.visit(node.value,scope)
        var_type=self.context.get_type(node.var.type)
        print()
        if not var_type.conforms_to(node.value.type_value):
            self.errors.append(INCOMPATIBLE_TYPES % (node.value.type_value,var_type))

#=============CALLNODES================#
    @visitor.when(LetNode)
    def visit(self,node:LetNode,scope):
        for var_param,var_value in zip(node.vars,node.values):
            var_param_type=self.context.get_type(var_param.type)
            self.visit(var_value,scope)
            if not var_value.type_value.conforms_to(var_param_type):
                self.errors.append(INCOMPATIBLE_TYPES % (var_value.type_value,var_param_type))
                node.type_value=self.context.get_type('<error>')
                return
            else:
                scope.define_variable(var_param.name,var_value.type_value)
        self.visit(node.expression,scope)
        node.type_value=node.expression.type_value


    @visitor.when(FunctionCallNode)
    def visit(self,node:FunctionCallNode,scope):

        if node.funct in self.context.func.keys():
            function=self.context.func[node.funct]
        else:
            print('no hay na')
            self.errors.append(VARIABLE_NOT_DEFINED % (node.funct,'here'))
            node.type_value=self.context.get_type('<error>')
            return
        if len(node.arguments)!=len(function.params):
            self.errors.append(NUMBER_ARGUMENT % (node.funct,len(function.params)))
            return
        for arg, param in zip(node.arguments,function.params):
            self.visit(arg,scope)
            if not arg.type_value.conforms_to(param.type):
                self.errors.append(INCOMPATIBLE_TYPES % (arg.type_value,param.type))
                node.type_value=self.context.get_type('<error>')
                return
        node.type_value=function.return_type
    
    @visitor.when(ExpressionBlockNode)
    def visit(self,node:ExpressionBlockNode,scope):
        for exp in node.expressions:
            self.visit(exp,scope)
            node.expressions=exp.type_value
    @visitor.when(IfElseExpression)
    def visit(self,node:IfElseExpression,scope):
        list_type=[]
        for exp in node.condition:
            self.visit(exp,scope)
            if exp.type_value!=BoolType():
                self.errors.append(INCOMPATIBLE_TYPES % (exp.type_value,BoolType()))
                node.type_value=self.context.get_type('<error>')
        for cas in node.cases:
            self.visit(cas,scope)
            list_type.append(cas.type_value)
        print(list_type)
        node.type_value=self.parent_nearby(list_type)
        print(node.type_value)

    def parent_nearby(self,list_type):
        for typ1 in list_type:
            temp=True
            for typ2 in list_type:
                if not typ2.conforms_to(typ1):
                    temp=False
                    break
            if temp:
                return typ1
        x=list_type[0]

        while True:
            parent=x.parent
            if(parent.name=='Object'):
                return parent
            for typ in list_type:
                temp=True
                if not typ.conforms_to(parent):
                    temp=False
                    x=parent
                    break
            if temp:
                return parent
            



    @visitor.when(WhileNode)
    def visit(self,node:WhileNode,scope):
        self.visit(node.condition,scope)
        self.visit(node.expression,scope)
        node.type_value=node.expression.type_value
    @visitor.when(ForNode)
    def visit(self,node:ForNode,scope):
        ##la coolection tiene k ser tipo iterable
        ##meter el name en el scope con el tipo de valor del collection
        self.visit(node.collection,scope)
        self.visit(node.expression,scope)
        node.type_value=node.expression.type_value

#===========Operations================#

    @visitor.when(AritmethicExpression)
    def visit(self,node:AritmethicExpression,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        if(node.left.type_value!=NumType() or node.right.type_value!=NumType()):
            self.errors.append(INVALID_OPERATION % (node.operation,node.right.type_value,node.left.type_value))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Number')


    @visitor.when(OrAndExpression)
    def visit(self,node:OrAndExpression,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        if(node.left.type_value!=BoolType() or node.right.type_value!=BoolType()):
            self.errors.append(INVALID_OPERATION % (node.operation,node.right.type_value,node.left.type_value))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Boolean')

    @visitor.when(ComparationExpression)
    def visit(self,node:ComparationExpression,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        if (not node.left.type_value.conforms_to(node.right.type_value) and not node.right.type_value.conforms_to(node.left.type_value) ):
            self.errors.append(INVALID_OPERATION % (node.operation,node.right.type_value,node.left.type_value))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Boolean')

    @visitor.when(NotExpression)
    def visit(self,node:NotExpression,scope):
        self.visit(node.expression,scope)
        if(node.expression.type_value!=BoolType()):
            self.errors.append(INVALID_OPERATION % ('!',node.expression.type_value,BoolType()))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Boolean')

    @visitor.when(StringConcatenationNode)
    def visit(self,node:StringConcatenationNode,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)

        type_num=self.context.get_type('Number')
        type_str=self.context.get_type('String')
        
        if(not node.left.type_value in[type_num,type_str] or not node.right.type_value in[type_num,type_str]):
            op="@"
            if node.double:
                op="@@"
            self.errors.append(INVALID_OPERATION % (op,node.left.type_value,node.right.type_value))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('String')


    @visitor.when(VariableNode)
    def visit(self, node:VariableNode,scope:Scope):
        if scope.is_defined(node.name):
            var=scope.find_variable(node.name)
            node.type_value=var.type
        else:
            self.errors.append(VARIABLE_NOT_DEFINED%(node.name,'Here'))
            node.type_value=self.context.get_type('<error>')
    

    ###basic_type
    @visitor.when(NumberNode)
    def visit(self,node:NumberNode,scope):
        node.type_value=self.context.get_type('Number')

    @visitor.when(StringNode)
    def visit(self,node:StringNode,scope):
        node.type_value=self.context.get_type('String')

    @visitor.when(BooleanNode)
    def visit(self,node:BooleanNode,scope):
        node.type_value=self.context.get_type('Boolean')