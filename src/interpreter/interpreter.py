import src.cmp.visitor as visitor
from src.semantic_checker.ast import *


class Interpreter_Visitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs
        statements = '\n'.join(self.visit(child) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(FunctionNode)
    def visit(self, node, tabs=0, is_class=False):
        p = [x.name for x in node.parameters]
        if is_class:
            ans = '\t' * tabs + f'def {node.name}(self,{','.join(p)}):' if p else '\t' * tabs + f'def {node.name}({','.join(p)}):'
        else:
            ans = '\t' * tabs + f'def {node.name}({','.join(p)}):'
        expression = self.visit(node.corpus, tabs + 1)
        return f'{ans}\n{expression}'

    @visitor.when(TypeAttributeNode)
    def visit(self, node, tabs=0):
        value = self.visit(node.value)
        ans = '\t' * tabs + f'self.{node.var.name} = {value}'
        return f'{ans}'

    @visitor.when(ParameterNode)
    def visit(self, node, tabs=0):
        return f'{node.name}'

    # @visitor.when(TypeAttributeNode)
    # def visit(self, node, tabs=0):
    #     ans = '\t' * tabs + f'\\TypeAttributeNode'
    #     value = self.visit(node.value, tabs + 1)
    #     return f'{ans} {value}'

    @visitor.when(ProtocolMethodNode)
    def visit(self, node, tabs=0):
        parameters = [self.visit(child) for child in node.parameters]
        if parameters:
            ans = '\t' * tabs + f'def {node.name}(self,{','.join(parameters)}):\n{'\t' * (tabs + 1)}pass '
        else:
            ans = '\t' * tabs + f'def {node.name}(self):\n{'\t' * (tabs + 1)}pass '
        return f'{ans}'

    @visitor.when(ProtocolNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'class {node.name}:'
        methods = [self.visit(child, tabs + 1) for child in node.corpus]
        parameters = '\n'.join(methods) if methods else '\tpass'
        return f'{ans}\n{parameters}'

    # TODO--Done
    @visitor.when(TypeNode)
    def visit(self, node, tabs=0):
        corpus = [self.visit(child, tabs + 1) for child in node.corpus if not isinstance(child, TypeAttributeNode)]
        ans = '\t' * tabs + f'class {node.name}:' if node.inherits == 'Object' else '\t' * tabs + f'class {node.name}({node.inherits}):'
        attrs = [self.visit(x) for x in node.corpus if isinstance(x, TypeAttributeNode)]
        t = '\n' + '\t' * 2
        if (node.inherits == 'Object'):
            parameters = [self.visit(param, tabs) for param in node.constructor]
            init = f'\tdef __init__(self,{','.join(parameters)})' if parameters else ""
            for i in attrs:
                init += t + i
            ans += '\n' + init
        return f'{ans}\n{'\n'.join(corpus)}'

    @visitor.when(ExpressionBlockNode)
    def visit(self, node, tabs=0):
        ans = ''
        expressions = '\n'.join(self.visit(child) for child in node.expressions)
        return f'{ans}\n{expressions}'

    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = ""
        name = [self.visit(child) for child in node.vars]
        vals = [self.visit(child) for child in node.values]
        expression = str(self.visit(node.expression, tabs))
        for name, vals in zip(name, vals):
            ans += f'\n{name} = {vals}'

        return f'{ans}\n{expression}\n'

    # TODO - Done
    @visitor.when(IfElseExpression)
    def visit(self, node, tabs=0):
        condition = [self.visit(child) for child in node.condition]
        cases = [self.visit(child, tabs + 1) for child in node.cases]
        res = ''
        for i in range(0, len(condition)):
            _type = 'if' if i == 0 else 'elif'
            res += '\t' * tabs + f'{_type} {condition[i]}:'
            _cases = cases[i].replace('\t', '').split('\n')
            for c in _cases:
                res += '\t' * (tabs + 1) + c + '\n'
            res += '\n'

        if len(cases) > 1:
            res += '\t' * tabs + f'else:\n'
            res += '\t' * tabs + cases[len(cases) - 1]

        return res

    @visitor.when(DesctructiveExpression)
    def visit(self, node, tabs=0):
        exp = self.visit(node.expression)
        ans = '\t' * tabs + f'{node.name} = {exp}'
        return ans

    @visitor.when(SelfVaraiableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'self.{node.name}'
        return f'{ans}'

    @visitor.when(SelfDesctructiveExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'='
        return f'{ans} {self.visit(node.var, tabs + 1)} {self.visit(node.expression, tabs + 1)}'

    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'while {self.visit(node.condition)}:'
        return f'{ans}\n{self.visit(node.expression, tabs + 1)}'

    # TODO
    @visitor.when(ForNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'for {node.name} in {self.visit(node.collection)}:'
        return f'{ans}\n{self.visit(node.expression, tabs + 1)}'

    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        args = [self.visit(child) for child in node.arguments]
        ans = '\t' * tabs + f'{node.name}({','.join(args)})'
        return f'{ans}'

    @visitor.when(NumberNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'{node.value}'
        return f'{ans}'

    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'{node.value}'
        return f'{ans}'

    @visitor.when(BooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'{node.value}'
        return f'{ans}'

    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'{node.name}'
        return f'{ans}'

    @visitor.when(FunctionCallNode)
    def visit(self, node, tabs=0):
        arguments = [self.visit(child) for child in node.arguments]
        ans = '\t' * tabs + f'{node.funct}({','.join(arguments)})'
        return f'{ans}'

    # TODO - Done
    @visitor.when(TypeFunctionCallNode)
    def visit(self, node, tabs=0):
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        ans = '\t' * tabs + f'{node.funct}({','.join(arguments)})'
        return f'{node.class_.name}.{ans}'

    # TODO-Done
    @visitor.when(ListNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs
        elements = ','.join(self.visit(child, tabs + 1) for child in node.elements)
        elements = f'[{elements.replace('\t', '')}]'
        return f'{ans}{elements}'

    # TODO-Done
    @visitor.when(ImplicitListNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ImplicitListNode'
        iterator = self.visit(node.iterator, tabs + 1)
        collection = self.visit(node.collection, tabs + 1)
        return f'{ans}\niterator:\n{iterator}\ncollection:\n{collection}'

    @visitor.when(IndexingNode)
    def visit(self, node, tabs=0):
        exp = self.visit(node.collection)
        index = self.visit(node.index)
        ans = '\t' * tabs + f'{exp}[{index}]'
        return f'{ans}'

    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        exp = self.visit(node.expression)
        ans = '\t' * tabs + f'{node.type}({exp})'
        return f'{ans}'

    @visitor.when(OrAndExpression)
    def visit(self, node, tabs=0):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = 'and' if node.operation == '&' else 'or'
        ans = '\t' * tabs + f'{left} {op} {right}'
        return f'{ans}'

    @visitor.when(NotExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'!'
        return f'{ans} {self.visit(node.expression, tabs + 1)}'

    @visitor.when(ComparationExpression)
    def visit(self, node, tabs=0):
        left = self.visit(node.left)
        right = self.visit(node.right)
        ans = '\t' * tabs + f'{left} {node.operation} {right}'
        return f'{ans}'

    @visitor.when(IsExpression)
    def visit(self, node, tabs=0):
        exp = self.visit(node.left)
        ans = '\t' * tabs + f'isinstance({node.name}, {exp})'
        return f'{ans}'

    @visitor.when(AritmethicExpression)
    def visit(self, node, tabs=0):
        left = self.visit(node.left, tabs)
        right = self.visit(node.right)
        op = node.operation
        return f'{left} {op} {right}'

    # TODO - Done
    @visitor.when(StringConcatenationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs
        if node.double:
            return f'{ans}{self.visit(node.left, tabs)}+" "+{self.visit(node.right, tabs)}'
        else:
            return f'{ans}{self.visit(node.left, tabs)} + {self.visit(node.right, tabs)}'
