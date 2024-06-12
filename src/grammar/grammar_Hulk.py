from cmp.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
decl_let, decl_func, print_stat, arg_list,expr,simple_expr = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list> <expr> <simple-expr>')
neg_term,pw_ ,expr_arith, term, factor, atom ,expr_object= G.NonTerminals('<pw> <expr_arith> <term> <factor> <atom> <expr_object>')
func_call, expr_list = G.NonTerminals('<func-call> <expr_arith-list>')

destruct, concat = G.Terminals(":= @")
sqrt,sin,cos,exp,log,rand=G.Terminals('sqrt sin cos exp log rand')
let, defx, printx = G.Terminals('let def print')
semi, comma, opar, cpar,point, arrow = G.Terminals('; , ( ) . ->')
equal, plus, minus, star, div,pow = G.Terminals('= + - * / ^')
idx, num ,string= G.Terminals('id int string')
true,false = G.Terminals('true false')
pi,e = G.Terminals('pi e')

program %= stat_list

stat_list %= stat + semi
stat_list %= stat + semi + stat_list

stat %= decl_let
stat %= decl_func
stat %= print_stat
stat%= expr_arith

decl_let %= let + idx + equal + expr_arith
decl_func %= defx + idx + opar + arg_list + cpar + arrow + expr_arith
print_stat %= printx + expr_arith

arg_list %=idx
arg_list %= idx + comma + arg_list

expr_arith %= expr_arith + plus + term
expr_arith %= expr_arith + minus + term
expr_arith %= term

term %= term + star + neg_term
term %= term + div + neg_term
term %= neg_term

neg_term %= minus+neg_term
neg_term %= pw_

pw_%=pw_+pow+expr_object
pw_%=expr_object

expr_object%=idx
expr_object%=func_call

func_call%=exp+opar+expr+cpar
func_call%=log+opar+expr+cpar
func_call%=sin+opar+expr+cpar
func_call%=cos+opar+expr+cpar
func_call%=sqrt+opar+expr+cpar
func_call%=rand+opar+cpar
func_call%=true
func_call%=false
func_call%=string 
func_call%=num
func_call%=idx
func_call%=pi 
func_call%=e




#pw_%=factor + pow+ factor
#pw_%=factor
#
#factor %= atom
#factor %= opar + expr_arith + cpar
#
#atom %= num
#atom %= idx
#atom %= func_call



#func_call %= idx + opar + expr_list + cpar
#
#
#
#expr_list %= expr_arith
#expr_list %= expr_arith + comma + expr_list

print(G)