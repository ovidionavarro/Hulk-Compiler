from src.cmp.pycompiler import Grammar
from src.lexer.lexer_ast import UnionNode,ConcatNode,ClosureNode,SymbolNode,EpsilonNode


G=Grammar()
E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# > PRODUCTIONS???
# Your code here!!!

E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0],s[2])
X %= G.Epsilon, lambda h,s: h[0]

T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]

Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0],s[1])
Y %= G.Epsilon, lambda h,s: h[0]

F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

Z %= star, lambda h,s: ClosureNode(h[0]), None
Z %= G.Epsilon, lambda h,s: h[0]

A %= symbol, lambda h,s: SymbolNode(s[1]), None
A %= epsilon, lambda h,s: EpsilonNode(s[1]), None
A %= opar + E + cpar, lambda h,s: s[2], None, None, None

# print(G)