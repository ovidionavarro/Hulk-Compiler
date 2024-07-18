import random
import src.cmp.visitor as visitor
from src.semantic_checker.ast import *
import math


def base_method(self_obj, method_name, *args):
    base_class = type(self_obj).__bases__[0]
    print(base_class)
    func = getattr(base_class, method_name)
    return func(self_obj, *args)


class Scope:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
        self.initialize_builtins()

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable {name} not found")

    def initialize_builtins(self):
        self.set_variable('print', print)
        self.set_variable('sin', math.sin)
        self.set_variable('cos', math.cos)
        self.set_variable('tan', math.tan)
        self.set_variable('log', math.log)
        self.set_variable('sqrt', math.sqrt)
        self.set_variable('exp', math.sin)
        self.set_variable('rand', random.randint(0, 1))
        self.set_variable('PI', math.pi)


class InterpreterVisitor:
    def __init__(self):
        self.global_scope = Scope()

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        if scope is None:
            scope = self.global_scope
        for child in node.statements:
            self.visit(child, scope)

    @visitor.when(FunctionNode)
    def visit(self, node, scope):
        def func(*args):
            local_scope = Scope(scope)
            for param, arg in zip(node.parameters, args):
                local_scope.set_variable(param.name, arg)
            return self.visit(node.corpus, local_scope)

        scope.set_variable(node.name, func)
        return func

    @visitor.when(TypeAttributeNode)
    def visit(self, node, scope):
        value = self.visit(node.value, scope)
        scope.set_variable(f'self.{node.var.name}', value)

    @visitor.when(ParameterNode)
    def visit(self, node, scope):
        return node.name

    @visitor.when(ProtocolMethodNode)
    def visit(self, node, scope):
        def method(self_obj, *args):
            local_scope = Scope(scope)
            local_scope.set_variable('self', self_obj)
            for param, arg in zip(node.parameters, args):
                local_scope.set_variable(param.name, arg)
            return self.visit(node.body, local_scope)

        return method

    @visitor.when(ProtocolNode)
    def visit(self, node, scope):
        methods = {}
        for method in node.corpus:
            methods[method.name] = self.visit(method, scope)
        cls = type(node.name, (object,), methods)
        scope.set_variable(node.name, cls)
        return cls

    @visitor.when(TypeNode)
    def visit(self, node, scope):
        def init(self_obj, *args):
            local_scope = Scope(scope)
            local_scope.set_variable('self', self_obj)
            for param, arg in zip(node.constructor, args):
                local_scope.set_variable(param.name, arg)
                setattr(self_obj, param.name, arg)

            if node.inherits != 'Object':
                base_cls = scope.get_variable(node.inherits)
                base_cls.__init__(self_obj, *args)

            for attr in node.corpus:
                if isinstance(attr, TypeAttributeNode):
                    value = self.visit(attr.value, local_scope)
                    setattr(self_obj, attr.var.name, value)
                    local_scope.set_variable(f'self.{attr.var.name}', value)

            for method in node.corpus:
                if isinstance(method, FunctionNode):
                    method_func = self.visit(method, local_scope)
                    setattr(self_obj, method.name, method_func)

        bases = (object,)
        if node.inherits != 'Object':
            bases = (scope.get_variable(node.inherits),)

        cls = type(node.name, bases, {})

        cls.__init__ = init
        scope.set_variable(node.name, cls)
        return cls

    @visitor.when(ExpressionBlockNode)
    def visit(self, node, scope):
        result = None
        expressions = reversed(list(node.expressions))
        for expr in expressions:
            result = self.visit(expr, scope)
        return result

    @visitor.when(LetNode)
    def visit(self, node, scope):
        local_scope = Scope(scope)
        for var, val in zip(node.vars, node.values):
            local_scope.set_variable(var.name, self.visit(val, local_scope))
        return self.visit(node.expression, local_scope)

    @visitor.when(IfElseExpression)
    def visit(self, node, scope):
        for condition, case in zip(node.condition, node.cases):
            if self.visit(condition, scope):
                return self.visit(case, scope)
        n_cases = len(node.cases)
        return self.visit(node.cases[n_cases - 1], scope)

    @visitor.when(DesctructiveExpression)
    def visit(self, node, scope):
        value = self.visit(node.expression, scope)
        scope.set_variable(node.name, value)
        return value

    @visitor.when(SelfVaraiableNode)
    def visit(self, node, scope):
        return scope.get_variable(f'self.{node.name}')

    @visitor.when(SelfDesctructiveExpression)
    def visit(self, node, scope):
        expr_value = self.visit(node.expression, scope)
        if scope.parent:
            scope.parent.set_variable(f'self.{node.var.name}', expr_value)
        else:
            scope.set_variable(f'self.{node.var.name}', expr_value)

        return expr_value

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        while self.visit(node.condition, scope):
            self.visit(node.expression, scope)

    @visitor.when(ForNode)
    def visit(self, node, scope):
        collection = self.visit(node.collection, scope)
        for item in collection:
            local_scope = Scope(scope)
            local_scope.set_variable(node.name, item)
            self.visit(node.expression, local_scope)

    @visitor.when(NewNode)
    def visit(self, node, scope):
        cls = scope.get_variable(node.name)
        args = [self.visit(arg, scope) for arg in node.arguments]
        instance = cls(*args)
        return instance

    @visitor.when(NumberNode)
    def visit(self, node, scope):
        return node.value

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return node.value

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        return node.value

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        return scope.get_variable(node.name)

    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):

        if node.funct == 'base':
            self_obj = scope.parent.get_variable('self')
            func_name = None
            for m in scope.parent.variables:
                if callable(scope.parent.get_variable(m)):
                    func_name = m
            args = [self.visit(arg, scope) for arg in node.arguments]
            base_class = super(self_obj.__class__, self_obj)
            if hasattr(base_class, func_name):
                func = getattr(base_class, func_name)
                result = func(*args)
                return result
            else:
                raise Exception(f"function {func_name} not found in {base_class}")

        else:
            func = scope.get_variable(node.funct)
            args = [self.visit(arg, scope) for arg in node.arguments]
            return func(*args)

    @visitor.when(TypeFunctionCallNode)
    def visit(self, node, scope):
        instance = self.visit(node.class_, scope)
        method = getattr(instance, node.funct)
        args = [self.visit(arg, scope) for arg in node.arguments]
        return method(*args)

    @visitor.when(ListNode)
    def visit(self, node, scope):
        return [self.visit(element, scope) for element in node.elements]

    @visitor.when(ImplicitListNode)
    def visit(self, node, scope):
        iterator = self.visit(node.iterator, scope)
        collection = self.visit(node.collection, scope)
        return [self.visit(iterator, Scope(scope, {iterator.name: item})) for item in collection]

    @visitor.when(IndexingNode)
    def visit(self, node, scope):
        collection = self.visit(node.collection, scope)
        index = self.visit(node.index, scope)
        return collection[index]

    @visitor.when(AsNode)
    def visit(self, node, scope):
        expr = self.visit(node.expression, scope)
        return expr if isinstance(expr, node.type) else None

    @visitor.when(OrAndExpression)
    def visit(self, node, scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if node.operation == '&':
            return left and right
        elif node.operation == '|':
            return left or right

    @visitor.when(NotExpression)
    def visit(self, node, scope):
        return not self.visit(node.expression, scope)

    @visitor.when(ComparationExpression)
    def visit(self, node, scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if node.operation == '==':
            return left == right
        elif node.operation == '!=':
            return left != right
        elif node.operation == '<':
            return left < right
        elif node.operation == '>':
            return left > right
        elif node.operation == '<=':
            return left <= right
        elif node.operation == '>=':
            return left >= right

    @visitor.when(IsExpression)
    def visit(self, node, scope):
        expr = self.visit(node.left, scope)
        return isinstance(expr, scope.get_variable(node.name))

    @visitor.when(AritmethicExpression)
    def visit(self, node, scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        operator = node.operation
        if operator == '+':
            return left + right
        if operator == '-':
            return left - right
        if operator == '*':
            return left * right
        if operator == '/':
            return left / right
        if operator == '^':
            return left ** right

    @visitor.when(StringConcatenationNode)
    def visit(self, node, scope):
        left = str(self.visit(node.left, scope))
        left = left.replace('"', '')
        right = str(self.visit(node.right, scope))
        right = right.replace('"', '')
        if node.double:
            return left + " " + right
        else:
            return left + right
