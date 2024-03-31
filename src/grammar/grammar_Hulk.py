from cmp.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
let_var, def_func, print_stat, arg_list = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list>')
expr, term, factor, atom = G.NonTerminals('<expr> <term> <factor> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')

let, defx, printx = G.Terminals('let def print')
semi, comma, opar, cpar, arrow = G.Terminals('; , ( ) ->')
equal, plus, minus, star, div = G.Terminals('= + - * /')
idx, num = G.Terminals('id int')

program %= stat_list

stat_list %= stat + semi
stat_list %= stat + semi + stat_list

stat %= let_var
stat %= def_func
stat %= print_stat

let_var %= let + idx + equal + expr

def_func %= defx + idx + opar + arg_list + cpar + arrow + expr

print_stat %= printx + expr

arg_list %=idx
arg_list %= idx + comma + arg_list

expr %= expr + plus + term
expr %= expr + minus + term
expr %= term

term %= term + star + factor
term %= term + div + factor
term %= factor

factor %= atom
factor %= opar + expr + cpar

atom %= num
atom %= idx
atom %= func_call

func_call %= idx + opar + expr_list + cpar

expr_list %= expr
expr_list %= expr + comma + expr_list

print(G)