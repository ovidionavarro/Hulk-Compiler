import cmp.visitor as visitor
from semantic_checker.ast import *
from src.semantic_checker.utils.types import *


def check_parents(initial_type,parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
       return check_parents(initial_type,parent.parent)
    else: return False

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
            


class Collector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):

        self.context = Hulk_Context()
        self.context.types['Number'] = NumType() 
        self.context.types['String'] = StringType()        
        self.context.types['Boolean'] = BoolType()
        self.context.types['None'] = NoneType()   
        self.context.types['Object'] = ObjectType()    
        self.context.types['<error>'] = ErrorType()
        self.context.func['sin']= self.context.create_func('sin',[VarDefNode('angle','Number')],NumType())
        self.context.func['cos']= self.context.create_func('cos',[VarDefNode('angle','Number')],NumType())
        self.context.func['print']= self.context.create_func('print',[VarDefNode('value','Object')],NoneType())
        self.context.func['log']= self.context.create_func('log',[VarDefNode('base','Number'),VarDefNode('value','Number')],NumType())
        self.context.func['sqrt']= self.context.create_func('sqrt',[VarDefNode('value','Number')],NumType())
        self.context.func['exp']= self.context.create_func('exp',[VarDefNode('value','Number')],NumType())
        self.context.func['rand']= self.context.create_func('rand',[],NumType())
        for class_declaration in node.decl_list:
            self.visit(class_declaration)
        
    @visitor.when(TypeDeclNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)   
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtDeclNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.id,node.parents)   
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FuncDeclNode)
    def visit(self, node: FuncDeclNode):
        try:
            if node.return_type == None:
                type = self.context.get_type('None') 
                self.context.create_func(node.id,node.args,type) 
            else:
                type = self.context.get_type(node.return_type) 
                self.context.create_func(node.id,node.args,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_declaration in node.decl_list:
            self.visit(class_declaration)

    @visitor.when(TypeDeclNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        if node.parent:            
            try:
                parent_type = self.context.get_type(node.parent)
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
            except SemanticError as ex:
                self.errors.append(ex.text)
            if check_parents(self.current_type.name,self.current_type.parent):
                error= SemanticError("Cyclic inheritance is not allowed.")
                self.errors.append(error)
        for feature in node.features:
            self.visit(feature)

        if node.parent: 
            if check_methods(self.current_type,self.current_type.parent):
                error= SemanticError("Using the same method name with different arguments is not allowed.")
                self.errors.append(error)

    @visitor.when(ProtDeclNode)
    def visit(self, node:ProtDeclNode):
        self.current_type = self.context.get_type(node.id)
        if node.parents:  
            for parent in node.parents:        
                try:
                    parent_type = self.context.get_type(parent)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                if check_parents(self.current_type.name,parent_type):
                    error= SemanticError("Cyclic inheritance is not allowed.")
                    self.errors.append(error)
        for feature in node.methods:
            self.visit(feature)

    @visitor.when(ProtMethodNode)
    def visit(self, node:ProtMethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)
                
        try:
            type = self.context.get_type(node.return_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id,param_names,param_types,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node:MethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)
                
        try:
            type = self.context.get_type('None')
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id,param_names,param_types,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(AssignNode)
    def visit(self,node:AssignNode):
        try:
            if node.var.type is None:
                type = self.context.get_type('None')
            else:
                type = self.context.get_type(node.var.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_attribute(node.var.id,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)   

