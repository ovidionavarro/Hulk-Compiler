from src.cmp.pycompiler import Grammar

G = Grammar()




#terminals
string, identifier, number = G.Terminals('string identifier number')
equal,doble_equal,less,great,less_equal,great_equal,not_equal = G.Terminals('= == < > <= >= !=')
plus,minus,mult,div,int_div = G.Terminals('+ - * / //')
destruct,concat= G.Terminals(':= @')
oparent, cparent, obrack, cbrack, okey, ckey = G.Terminals('( ) [ ] { }')
comma,point,doble_point,semicolon = G.Terminals(', . : ;')
arrow,darrow=G.Terminals('-> =>')
and_,or_,not_=G.Terminals('& | !')
for_,while_=G.Terminals('for while')
if_,else_,elif_=G.Terminals('if else elif')
function_,print_,let_=G.Terminals('function print let')
sin,cos,sqrt,exp,log,tan,base=G.Terminals('sin cos sqrt exp log tan base')
pi,e=G.Terminals('pi e')
as_,is_,random_=G.Terminals('as is rand')
true,false=G.Terminals('true false')   
new,inherit,protocol,type_,in_,range_,extend=G.Terminals('new inherit protocol type in range extend')   



# no Terminals
init = G.NonTerminal("<init>", startSymbol=True)
program ,expression, statement, simple_program = G.NonTerminals("<program> <expression> <statement> <simple_program")
dec_func, dec_type, dec_protocol = G.NonTerminals("<dec_func> <dec_type> <dec_protocol>")
parameters, doubt, variable=G.NonTerminals("<parameters> <doubt> <variable>")
expression_block,simple_expression=G.NonTerminals("<expression_block> <simple_expression>")
boolean,concatenation=G.NonTerminals("<boolean> <concatenation>")


init%=program

program %= simple_program + program
program %= statement + program

statement %= dec_func
statement %= dec_type
statement %= dec_protocol

dec_func %= function_ + identifier + oparent + parameters + cparent+ darrow + simple_expression+semicolon
dec_func %= function_ + identifier + oparent + parameters + cparent+ doble_point+identifier+darrow + simple_expression+semicolon
dec_func %=function_ + identifier + oparent + parameters+ cparent + expression_block + doubt
dec_func %=function_ + identifier + oparent + parameters+ cparent + okey + doble_point + ckey +identifier+ expression_block + doubt

doubt%= semicolon
doubt%= G.Epsilon

parameters %= variable
parameters %= variable + comma + parameters

variable%=identifier
variable %= identifier + doble_point + identifier



boolean%=concatenation
boolean%=boolean + or_ + concatenation
boolean%=boolean + and_ + concatenation
boolean%=boolean +  + concatenation
boolean%=boolean + and_ + concatenation
boolean%=boolean + and_ + concatenation
boolean%=boolean + and_ + concatenation

