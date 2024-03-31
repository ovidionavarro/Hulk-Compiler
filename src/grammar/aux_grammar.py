from cmp.pycompiler import Grammar
from src.ast.nodes_class import *

G = Grammar()


# Non Terminals
program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
let_var, def_func, print_stat, arg_list = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list>')
expr, term, factor, atom = G.NonTerminals('<expr> <term> <factor> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')

let, defx, printx = G.Terminals('let def print')
semi, comma, opar, cpar, arrow = G.Terminals('; , ( ) ->')
equal, plus, minus, star, div = G.Terminals('= + - * /')
idx, num = G.Terminals('id int')

program %= stat_list, lambda h,s: ProgramNode(s[1])

stat_list %= stat + semi, lambda h,s: [s[1]] # Your code here!!! (add rule)
stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

stat %= let_var, lambda h,s: s[1] # Your code here!!! (add rule)
stat %= def_func, lambda h,s: s[1] # Your code here!!! (add rule)
stat %= print_stat, lambda h,s: s[1] # Your code here!!! (add rule)

let_var %= let + idx + equal + expr, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)

def_func %= defx + idx + opar + arg_list + cpar + arrow + expr, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)

print_stat %= printx + expr, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)

arg_list %= idx, lambda h,s: [s[1]] # Your code here!!! (add rule)
arg_list %= idx + comma + arg_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

expr %= expr + plus + term, lambda h,s: PlusNode(s[1],s[3]) # Your code here!!! (add rule)
expr %= expr + minus + term, lambda h,s: MinusNode(s[1],s[3]) # Your code here!!! (add rule)
expr %= term, lambda h,s: s[1] # Your code here!!! (add rule)

term %= term + star + factor, lambda h,s: StarNode(s[1],s[3]) # Your code here!!! (add rule)
term %= term + div + factor, lambda h,s: DivNode(s[1],s[3]) # Your code here!!! (add rule)
term %= factor, lambda h,s: s[1] # Your code here!!! (add rule)

factor %= atom, lambda h,s: s[1] # Your code here!!! (add rule)
factor %= opar + expr + cpar, lambda h,s: s[2] # Your code here!!! (add rule)

atom %= num, lambda h,s: ConstantNumNode(s[1]) # Your code here!!! (add rule)
atom %= idx, lambda h,s: VariableNode(s[1]) # Your code here!!! (add rule)
atom %= func_call, lambda h,s: s[1] # Your code here!!! (add rule)

func_call %= idx + opar + expr_list + cpar, lambda h,s: CallNode(s[1], s[3]) # Your code here!!! (add rule)

expr_list %= expr, lambda h,s: [s[1]] # Your code here!!! (add rule)
expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

# print(G)