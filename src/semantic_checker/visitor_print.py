import src.cmp.visitor as visitor
from src.semantic_checker.ast import *
class PrintVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
       ans='\t'*tabs+f'\\ProgramNode'
       statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
       return f'{ans}\n{statements}'

