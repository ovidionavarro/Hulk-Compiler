import cmp.visitor as visitor
import itertools as itl


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements


class StatementNode(Node):
    pass


class ExpressionNode(Node):
    pass


class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body


class PrintNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class ConstantNumNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class CallNode(AtomicNode):
    def __init__(self, idx, args):
        AtomicNode.__init__(self, idx)
        self.args = args


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(PrintNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PrintNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CallNode: {node.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'


class VariableInfo:
    def __init__(self, name):
        self.name = name


class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params


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
        self.local_funcs = []  # Changed from local_vars
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)

    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname):
        if self.is_local_var(vname):
            return False
        self.local_vars.append(VariableInfo(vname))
        return True

    def define_function(self, fname, params):
        if self.is_local_func(fname, len(params)):
            return False
        self.local_funcs.append(FunctionInfo(fname, params))  # Fixed appending to local_funcs
        return True

    def is_var_defined(self, vname):
        if self.is_local_var(vname):
            return True
        if self.parent is not None and self.var_index_at_parent < len(self.parent.local_vars):
            return self.parent.is_var_defined(vname)
        return False

    def is_func_defined(self, fname, n):
        if self.is_local_func(fname, n):
            return True
        if self.parent is not None and self.func_index_at_parent < len(self.parent.local_funcs):
            return self.parent.is_func_defined(fname, n)
        return False

    def is_local_var(self, vname):
        return any(var_info.name == vname for var_info in self.local_vars)

    def is_local_func(self, fname, n):
        return any(func_info.name == fname and len(func_info.params) == n for func_info in self.local_funcs)

    def get_local_variable_info(self, vname):
        for var_info in self.local_vars:
            if var_info.name == vname:
                return var_info
        return None

    def get_local_function_info(self, fname, n):
        for func_info in self.local_funcs:
            if func_info.name == fname and len(func_info.params) == n:
                return func_info
        return None





class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        # Your code here!!!
        if scope is None:
            scope = Scope()
        for statement_node in node.statements:
            self.visit(statement_node, scope)
        return self.errors

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        # Your code here!!!
        self.visit(node.expr, scope)
        if not scope.define_variable(node.id):
            self.errors.append(f'Variable {node.id} is already defined in current scope.')

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        # Your code here!!!
        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(
                    f'Function {node.id} is invalid, its arguments have to be different from each other.')
        self.visit(node.body, inner_scope)
        if not scope.define_function(node.id, node.params):
            self.errors.append(f'Function {node.id} is already defined with {len(node.params)} arguments.')

    @visitor.when(PrintNode)
    def visit(self, node, scope):
        # Your code here!!!
        self.visit(node.expr, scope)

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        # Your code here!!!
        pass

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        # Your code here!!!
        if not scope.is_var_defined(node.lex):
            self.errors.append(f'Variable {node.lex} is not defined.')

    @visitor.when(CallNode)
    def visit(self, node, scope):
        # Your code here!!!
        for argument_node in node.args:
            self.visit(argument_node, scope)
        if not scope.is_func_defined(node.lex, len(node.args)):
            self.errors.append(f'Function {node.lex} is not defined with {len(node.args)} arguments.')

    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        # Your code here!!!
        self.visit(node.left, scope)
        self.visit(node.right, scope)
