from cmp.evaluation import evaluate_reverse_parse
from src.grammar.aux_grammar import *
from src.parserLR1 import LR1Parser
from cmp.utils import Token

tokens = [
    Token('print', printx),
    Token('1', num),
    Token('-', minus),
    Token('1', num),
    Token('-', minus),
    Token('1', num),
    Token(';', semi),
    Token('let', let),
    Token('x', idx),
    Token('=', equal),
    Token('58', num),
    Token(';', semi),
    Token('let', let),
    Token('z', idx),
    Token('=', equal),
    Token('58', num),
    Token(';', semi),
    Token('def', defx),
    Token('f', idx),
    Token('(', opar),
    Token('a', idx),
    Token(',', comma),
    Token('b', idx),
    Token(')', cpar),
    Token('->', arrow),
    Token('5', num),
    Token('+', plus),
    Token('6', num),
    Token(';', semi),
    Token('print', printx),
    Token('f', idx),
    Token('(', opar),
    Token('5', num),
    Token('+', plus),
    Token('x', idx),
    Token(',', comma),
    Token('7', num),
    Token('+', plus),
    Token('y', idx),
    Token('+', plus),
    Token('z', idx),
    Token(')', cpar),
    Token(';', semi),
    Token('$', G.EOF),
]
parser = LR1Parser(G)

derivation, operations = parser([t.token_type for t in tokens],
                                get_operations=True)

ast = evaluate_reverse_parse(derivation, operations, tokens)
print(ast)

formatter = FormatVisitor()
print(formatter.visit(ast))

semantic_checker = SemanticCheckerVisitor()
errors = semantic_checker.visit(ast)
for i, error in enumerate(errors, 1):
    print(f'{i}.', error)
