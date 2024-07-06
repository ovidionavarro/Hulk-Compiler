import src.cmp.visitor as visitor
from src.semantic_checker.ast import *
class PrintVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'
    
    @visitor.when(FunctionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FunctionNode'
        expression=self.visit(node.corpus,tabs+1)
        return f'{ans}\n{expression}'

    @visitor.when(TypeAttributeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\TypeAttributeNode'
        value=self.visit(node.value,tabs+1)
        return f'{ans}\n{value}'
    
    @visitor.when(ParameterNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ParameterNode'
        return f'{ans} {node.name}:{node.type}'

    @visitor.when(TypeAttributeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\TypeAttributeNode'
        value=self.visit(node.value,tabs+1)
        return f'{ans} {value}'
    
    @visitor.when(ProtocolMethodNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ProtocolMethodNode {node.type}'
        parameters = '\n'.join(self.visit(child, tabs + 1) for child in node.parameters)
        return f'{ans}\n{parameters}'
    
    @visitor.when(TypeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\TypeNode'
        parameters = '\n'.join(self.visit(child, tabs + 1) for child in node.corpus)
        return f'{ans}\n{parameters}'
    
    @visitor.when(ProtocolNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ProtocolNode'
        parameters = '\n'.join(self.visit(child, tabs + 1) for child in node.corpus)
        return f'{ans}\n{parameters}'
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ExpressionBlockNode'
        expressions = '\n'.join(self.visit(child, tabs + 1) for child in node.expressions)
        return f'{ans}\n{expressions}'
    
    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\LetNode'
        names = '\n'.join(self.visit(child, tabs + 1) for child in node.vars)
        values= '\n'.join((self.visit(child, tabs + 1) for child in node.values))
        expression=str(self.visit(node.expression,tabs+1)) 
        return f'{ans}\n{names}\n{expression}\n{values}'
    
    @visitor.when(IfElseExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\IfElseExpression'
        condition = '\n'.join(self.visit(child, tabs + 1) for child in node.condition)
        cases = '\n'.join(self.visit(child, tabs + 1) for child in node.cases)

        return f'{ans}\n{condition}\n{cases}'
    @visitor.when(DesctructiveExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\DesctructiveExpression'
        return f'{ans} {node.name} {self.visit(node.expression,tabs+1)}'
    
    @visitor.when(SelfVaraiableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\SelfVaraiableNode {node.name}'
        return f'{ans}'
    
    @visitor.when(SelfDesctructiveExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\SelfDesctructiveExpression '
        return f'{ans} {self.visit(node.var,tabs+1)} {self.visit(node.expression,tabs+1)}'
    
    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\WhileNode'
        return f'{ans}\n{self.visit(node.condition,tabs+1)}\n{self.visit(node.expression,tabs+1)}'
    @visitor.when(ForNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ForNode {node.name}'
        return f'{ans}\n{self.visit(node.collection,tabs+1)}\n{self.visit(node.expression,tabs+1)}'
    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\NewNode'
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        return f'{ans} {node.name}\n {arguments}'
    @visitor.when(NumberNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\NumberNode {node.value}'
        return f'{ans}'
    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\StringNode {node.value}'
        return f'{ans}'
    
    @visitor.when(BooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\BooleanNode {node.value}'
        return f'{ans}'
    
    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\VariableNode {node.name}'
        return f'{ans}'
    
    @visitor.when(FunctionCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\FunctionCallNode {node.funct}'
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        return f'{ans}\n{arguments}'
    
    @visitor.when(TypeFunctionCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\TypeFunctionCallNode {node.name}'
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        return f'{ans}\n{arguments}'
        
    @visitor.when(ListNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ListNode'
        elements = '\n'.join(self.visit(child, tabs + 1) for child in node.elements)
        return f'{ans}\nelemenets:\n{elements}'
    @visitor.when(ImplicitListNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ImplicitListNode'
        iterator=self.visit(node.iterator,tabs+1)
        collection=self.visit(node.collection,tabs+1)
        return f'{ans}\niterator:\n{iterator}\ncollection:\n{collection}'
    
    @visitor.when(IndexingNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\IndexingNode'
        return f'{ans}\n{self.visit(node.collection,tabs+1)}\n{self.visit(node.index,tabs+1)}'
    
    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\AsNode {node.type}'
        return f'{ans}\n{self.visit(node.expression,tabs+1)}'
    
    @visitor.when(OrAndExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\OrAndExpression {node.operation}'
        return f'{ans}\n{self.visit(node.left,tabs+1)}\n{self.visit(node.right,tabs+1)}'
    
    @visitor.when(NotExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\NotExpression'
        return f'{ans}\n{self.visit(node.expression,tabs+1)}'
    @visitor.when(ComparationExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\ComparationExpression {node.operation}'
        return f'{ans}\n{self.visit(node.left,tabs+1)}\n{self.visit(node.right,tabs+1)}'
    
    @visitor.when(IsExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\IsExpression {node.name}'
        return f'{ans}\n{self.visit(node.left,tabs+1)}'
    
    @visitor.when(AritmethicExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\AritmethicExpression {node.operation}'
        return f'{ans}\n{self.visit(node.left,tabs+1)}\n{self.visit(node.right,tabs+1)}'
    @visitor.when(StringConcatenationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\StringConcatenationNode'
        return f'{ans}\n{self.visit(node.left,tabs+1)}\n{self.visit(node.right,tabs+1)}'    
