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
        scope.current_type=self.context.get_type(node.name)
        for param in node.constructor:
            param_type=self.context.get_type(param.type)
            scope.define_variable(param.name,param_type)

        for corp in node.corpus:
            self.visit(corp,scope)

    @visitor.when(TypeAttributeNode)
    def visit(self,node:TypeAttributeNode,scope):
        self.visit(node.value,scope)
        var_type=self.context.get_type(node.var.type)
        if var_type==AnyType():
            node.var.type=node.value.type_value
            scope.current_type.get_attribute(node.var.name).type=node.value.type_value
            print(scope.current_type.get_attribute(node.var.name).name,scope.current_type.get_attribute(node.var.name).type)
            node.type_value=node.value.type_value
            return

        node.var.type=var_type
        node.type_value=node.value.type_value
        if not node.value.type_value.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.value.type_value,var_type))
            node.type_value=self.context.get_type('<error>')

    @visitor.when(SelfVaraiableNode)
    def visit(self,node:SelfVaraiableNode,scope):
        if scope.current_type:
            try:
                if scope.current_type.get_attribute(node.name):
                    node.type_value=scope.current_type.get_attribute(node.name).type
                    return
            except SemanticError as ex:
                self.errors.append(ex.text)
        else:
            self.errors.append(f'Current {scope.current_type} type not exist')

    @visitor.when(SelfDesctructiveExpression)
    def visit(self,node:SelfDesctructiveExpression,scope):
        try:
            self.visit(node.var,scope)
            self.visit(node.expression,scope)
            if(isinstance(node.expression,VariableNode)):
                if(scope.find_variable(node.expression.name).type==AnyType()):
                    scope.find_variable(node.expression.name).type=node.var.type_value
                    node.expression.type_value=node.var.type_value
                    node.type_value=node.var.type_value
                else:
                   
                    if node.expression.type_value.conforms_to(node.var.type_value):
                        node.var.type_value=node.expression.type_value
                        node.type_value=node.expression.type_value
                    else:
                        self.errors.append(INCOMPATIBLE_TYPES % (node.var.type_value,node.expression.type_value))
                        node.var.type_value=self.context.get_type('<error>')
                        node.type_value= self.context.get_type('<error>')

                return
            if node.expression.type_value.conforms_to(node.var.type_value):
                node.var.type_value=node.expression.type_value
                node.type_value=node.expression.type_value
            else:
                self.errors.append(INCOMPATIBLE_TYPES % (node.var.type_value,node.expression.type_value))
                node.var.type_value=self.context.get_type('<error>') 
                node.type_value= self.context.get_type('<error>')  
                return
        except SemanticError as ex:
            self.errors.append(ex.text)
            node.var.type_value=self.context.get_type('<error>')

    @visitor.when(FunctionNode)
    def visit(self,node:FunctionNode,scope):
        aux=False
        if scope.current_type:
            if scope.current_type.get_method(node.name):

                aux=True
                
        if aux:
            self.current_method=scope.current_type.get_method(node.name)

            for param_n,param_t in zip(self.current_method.param_names,self.current_method.param_types):
                if not scope.find_variable(param_n):
                    scope.define_variable(param_n,param_t)
                else:
                    self.errors.append(LOCAL_ALREADY_DEFINED % (param_n,self.current_method.name))
                    return    
            self.visit(node.corpus,scope)
            ####redefinir typos de los parametros
            for param_n , param_t in zip(self.current_method.param_names,self.current_method.param_types):
                if(param_t==AnyType()):
                    param_t=scope.find_variable(param_n).type

            for param in self.current_method.param_names:
                x=scope.find_variable(param)
                index=scope.locals.index(x)
                del scope.locals[index]
            if self.current_method.return_type==AnyType():
                self.current_method.return_type=node.corpus.type_value
                node.type=node.corpus.type_value
            else:
               if not node.corpus.type_value.conforms_to(self.current_method.return_type):
                    self.errors.append(INCOMPATIBLE_TYPES % (self.current_method.return_type,node.corpus.type_value))
                    self.current_method.return_type=self.context.get_type('<error>')
            return


        self.current_method=self.context.func[node.name]
        # print(self.current_method.return_type)
        for param in self.current_method.params:
            scope.define_variable(param.name,param.type)
        self.visit(node.corpus,scope)
        ####redefinir typos de los parametros
        for param in self.current_method.params:
            if(param.type==AnyType()):
                param.type=scope.find_variable(param.name).type

        if self.current_method.return_type==AnyType():
            self.current_method.return_type=node.corpus.type_value
            return
        if(not node.corpus.type_value.conforms_to(self.current_method.return_type)):
            self.errors.append(INCOMPATIBLE_TYPES % (self.current_method.return_type,node.corpus.type_value))
           
    @visitor.when(NewNode)
    def visit(self,node:NewNode,scope):
        if self.context.get_type(node.name):
            node.type_value=self.context.get_type(node.name)
            if(node.type_value.parent!=ObjectType()):
                self.context.get_type(node.name).parameters=node.type_value.parent.parameters
            #redefiniendo los parametros
            node.type_value=self.context.get_type(node.name)  

            if(len(node.arguments)!=len(node.type_value.parameters)):
                self.errors.append(NUMBER_ARGUMENT % (node.name,len(node.type_value.parameters)))
                node.type_value=self.context.get_type('<error>')
                return
            for arg in node.arguments:
                self.visit(arg,scope)
            for arg,param in zip(node.arguments,node.type_value.parameters):
                if not arg.type_value.conforms_to(param.type) and param.type!=AnyType():
                    self.errors.append(INCOMPATIBLE_TYPES % (arg.type_value,param.type))
                    node.type_value=self.context.get_type('<error>')
                    return

        else:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.type,'here'))
            node.type_value=self.context.get_type('<error>')

#=============CALLNODES================#
    @visitor.when(TypeFunctionCallNode)
    def visit(self,node:TypeFunctionCallNode,scope):
        if scope.find_variable(node.class_.name):
            var=scope.find_variable(node.class_.name)
            type_=var.type
            if type_.get_method(node.funct):
                function=type_.get_method(node.funct)
                if len(node.arguments)!=len(function.param_names):
                    self.errors.append(NUMBER_ARGUMENT % (node.funct,len(function.param_names)))
                    node.type_value=self.context.get_type('<error>')

                    return
                for arg, param in zip(node.arguments,function.param_types):
                    self.visit(arg,scope)
                    
                    if not arg.type_value.conforms_to(param) and param!=AnyType():
                        self.errors.append(INCOMPATIBLE_TYPES % (arg.type_value,param))
                        node.type_value=self.context.get_type('<error>')
                        return
                node.type_value=function.return_type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED % (node.funct,type_.name))
                node.type_value=self.context.get_type('<error>')

        else:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.class_.name,'here'))
            node.type_value=self.context.get_type('<error>')


    @visitor.when(LetNode)
    def visit(self,node:LetNode,scope):
        for var_param,var_value in zip(node.vars,node.values):
            var_param_type=self.context.get_type(var_param.type)
            self.visit(var_value,scope)
            if(var_param_type==AnyType()):
                var_param_type=var_value.type_value
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
            self.errors.append(VARIABLE_NOT_DEFINED % (node.funct,'here'))
            node.type_value=self.context.get_type('<error>')
            return
        if len(node.arguments)!=len(function.params):
            self.errors.append(NUMBER_ARGUMENT % (node.funct,len(function.params)))
            return
        for arg, param in zip(node.arguments,function.params):
            self.visit(arg,scope)
            if(arg.type_value==AnyType()):
                arg.type_value=param.type
            if(param.type==AnyType()):
                param.type=arg.type_value
            if not arg.type_value.conforms_to(param.type) :
                self.errors.append(INCOMPATIBLE_TYPES % (arg.type_value,param.type))
                node.type_value=self.context.get_type('<error>')
                return
        node.type_value=function.return_type
    
    @visitor.when(ExpressionBlockNode)
    def visit(self,node:ExpressionBlockNode,scope):
        for exp in node.expressions:
            self.visit(exp,scope)
            node.type_value=exp.type_value
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
        node.type_value=self.parent_nearby(list_type)
        print(node.type_value)

    

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

    @visitor.when(AsNode)
    def visit(self,node:AsNode,scope):
        self.visit(node.expression,scope)
        if(self.context.get_type(node.type)  or self.context.get_protocol(node.name)):
            node.type_value=self.context.get_type(node.type)
        else:
            self.errors.append(f'Type {node.type} not found')
            node.type_value=self.context.get_type("<error>")

    @visitor.when(IsExpression)
    def visit(self,node:IsExpression,scope):
        if(self.context.get_type(node.name) or self.context.get_protocol(node.name)):
            node.type_value=self.context.get_type("Boolean")
        else:
            self.errors.append(f'Type {node.name} not found')
            node.type_value=self.context.get_type("<error>")
        
        

#===========Operations================#
    @visitor.when(DesctructiveExpression)
    def visit(self,node:DesctructiveExpression,scope):
        if not scope.is_defined(node.name):
            self.errors.append(VARIABLE_NOT_DEFINED % (node.name,'Global'))
            node.type_value=self.context.get_type('<error>')
            return
        self.visit(node.expression,scope)
        node.type_value=node.expression.type_value
        var=scope.find_variable(node.name)
        if var.type==AnyType():
            var.type=node.expression.type_value
        else:
            if not node.expression.type_value.conforms_to(var.type):
                self.errors.append(INCOMPATIBLE_TYPES % (node.expression.type_value,var.type))
                node.type_value=self.context.get_type('<error>')
        node.type_value=var.type
        var2=scope.find_variable(node.name)
        print(var2.type)
    @visitor.when(AritmethicExpression)
    def visit(self,node:AritmethicExpression,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        if(isinstance(node.left,VariableNode)):
            if(scope.find_variable(node.left.name).type==AnyType()):
                scope.find_variable(node.left.name).type=self.context.get_type('Number')
                node.left.type_value=self.context.get_type('Number')
            else:node.left.type_value=scope.find_variable(node.left.name).type

        if(isinstance(node.right,VariableNode)):
            if(scope.find_variable(node.right.name).type==AnyType()):
                scope.find_variable(node.right.name).type=self.context.get_type('Number')
                node.right.type_value=self.context.get_type('Number')
            else:node.right.type_value=scope.find_variable(node.right.name).type
        if(node.left.type_value!=NumType() or node.right.type_value!=NumType()):
            self.errors.append(INVALID_OPERATION % (node.operation,node.right.type_value,node.left.type_value))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Number')


    @visitor.when(OrAndExpression)
    def visit(self,node:OrAndExpression,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        
        if(isinstance(node.left,VariableNode)):
            if(scope.find_variable(node.left.name).type==AnyType()):
                scope.find_variable(node.left.name).type=self.context.get_type('Boolean')
                node.left.type_value=self.context.get_type('Boolean')
            else:node.left.type_value=scope.find_variable(node.left.name).type

        if(isinstance(node.right,VariableNode)):
            if(scope.find_variable(node.right.name).type==AnyType()):
                scope.find_variable(node.right.name).type=self.context.get_type('Boolean')
                node.right.type_value=self.context.get_type('Boolean')
            else:node.right.type_value=scope.find_variable(node.right.name).type
        

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

        if(isinstance(node.expression,VariableNode)):
            if(scope.find_variable(node.expression.name).type==AnyType()):
                scope.find_variable(node.expression.name).type=self.context.get_type('Boolean')
                node.expression.type_value=self.context.get_type('Boolean')
            else:node.expression.type_value=scope.find_variable(node.expression.name).type


        if(node.expression.type_value!=BoolType()):
            self.errors.append(INVALID_OPERATION % ('!',node.expression.type_value,BoolType()))
            node.type_value=self.context.get_type('<error>')
        else:
            node.type_value=self.context.get_type('Boolean')

    @visitor.when(StringConcatenationNode)
    def visit(self,node:StringConcatenationNode,scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)

        if(isinstance(node.left,VariableNode)):
            if(scope.find_variable(node.left.name).type==AnyType()):
                scope.find_variable(node.left.name).type=self.context.get_type('String')
                node.left.type_value=self.context.get_type('String')
            else:node.left.type_value=scope.find_variable(node.left.name).type

        if(isinstance(node.right,VariableNode)):
            if(scope.find_variable(node.right.name).type==AnyType()):
                scope.find_variable(node.right.name).type=self.context.get_type('String')
                node.right.type_value=self.context.get_type('String')
            else:node.right.type_value=scope.find_variable(node.right.name).type

        if(isinstance(node.left,SelfVaraiableNode)):
            if(scope.find_variable(node.left.name).type==AnyType()):
                scope.find_variable(node.left.name).type=self.context.get_type('String')
                node.left.type_value=self.context.get_type('String')
            else:node.left.type_value=scope.find_variable(node.left.name).type

        if(isinstance(node.right,SelfVaraiableNode)):
            if(scope.find_variable(node.right.name).type==AnyType()):
                scope.find_variable(node.right.name).type=self.context.get_type('String')
                node.right.type_value=self.context.get_type('String')
            else:node.right.type_value=scope.find_variable(node.right.name).type

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
    