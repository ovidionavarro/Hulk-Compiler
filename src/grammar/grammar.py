
import math

from src.cmp.pycompiler import Grammar


G = Grammar()


# No Terminals
init_ = G.NonTerminal("<init>", startSymbol=True)
program = G.NonTerminal("<program>")
simple_expression = G.NonTerminal("<expression>")
statement = G.NonTerminal("<statement>")
parameters, parameter_list, variable = G.NonTerminals("<parameters> <parameter_list> <variable>")
function_style = G.NonTerminal("<function_style>")
type_def = G.NonTerminal("<type_def>")
protocol_declare, protocol_body = G.NonTerminals("<protocol_declare> <protocol_body>")
simple_expression = G.NonTerminal("<simple_expression>")
expression_block = G.NonTerminal("<expression_block>")
class_block, class_body, class_declaration = G.NonTerminals("<class_block> <class_body> <class_declaration>")
arguments, argument_list = G.NonTerminals("<arguments> <argument_list>")
typed_parameters, typed_parameter_list = G.NonTerminals("<typed_parameters> <typed_parameter_list>")
declaration = G.NonTerminal("<declaration>")
if_block = G.NonTerminal("<if_block>")
else_block = G.NonTerminal("<else_block>")
disjunction, conjunction = G.NonTerminals("<disjunction> <conjunction>")
literal, proposition, boolean = G.NonTerminals("<literal> <proposition> <boolean>")
concatenation = G.NonTerminal("<concatenation>")
arithmetic_expression = G.NonTerminal("<arithmetic_expression>")
module, product, monomial, pow_ = G.NonTerminals("<module> <product> <monomial> <pow>")
high_hierarchy_object, object_exp = G.NonTerminals("<high_hierarchy_object> <object_exp>")
list_, explicit_list_, main_expression, function_stack = G.NonTerminals("<list> <explicit_list> <main_expression> <function_stack>")
not_sc_expression, else_block_not_sc, simple_program = G.NonTerminals("<not_sc_expression> <else_block_not_sc> <simple_program>")


# Terminals
string, identifier, number = G.Terminals("<string> <id> <number>")
plus, minus, star, divide, int_divide = G.Terminals("+ - * / //")
equal, dequal, lesst, greatt, lequal, gequal, notequal = G.Terminals("= == < > <= >= !=")
lparen, rparen, lbrack, rbrack, lbrace, rbrace = G.Terminals("( ) [ ] { }")
comma, period, colon, semicolon = G.Terminals(", . : ;")
arrow, darrow = G.Terminals("-> =>")
and_, or_, not_ = G.Terminals("& | !")

modulus, power, power_asterisk = G.Terminals("% ^ **")
destruct, concat = G.Terminals(":= @")
list_comprehension = G.Terminal("||")

for_, let, if_, else_, elif_ = G.Terminals("for let if else elif")
while_, function, pi, e, print_ = G.Terminals("while function pi e print")
new, inherits, protocol, type_, in_, range_, extends = G.Terminals("new inherits protocol type in range extends")
true, false = G.Terminals("true false")

rand = G.Terminal("rand")
sin, cos, sqrt, exp, log, tan, base = G.Terminals("sin cos sqrt exp log tan base")
as_, is_ = G.Terminals("as is")

init_ %= program, lambda h, s: s[1]

program%=simple_program
program %= simple_program+program#, lambda h, s: ProgramNode([], s[1])
# program %= statement + program#, lambda h, s: ProgramNode([s[1]] + s[2].STATEMENTS, s[2].EXPRESSION)
simple_program %= main_expression#, lambda h, s: s[1]
simple_program %= function + identifier + parameters + function_style#, lambda h, s: FunctionNode(s[2].Lemma, s[3], s[4][1], s[4][0])
simple_program %= type_ + identifier + type_def#, lambda h, s: TypeNode(s[2].Lemma, s[3][3], s[3][0], s[3][1], s[3][2])
simple_program %= protocol_declare#, lambda h, s: s[1]
# statement %= function + identifier + parameters + function_style#, lambda h, s: FunctionNode(s[2].Lemma, s[3], s[4][1], s[4][0])
# statement %= type_ + identifier + type_def#, lambda h, s: TypeNode(s[2].Lemma, s[3][3], s[3][0], s[3][1], s[3][2])
# statement %= protocol_declare#, lambda h, s: s[1]
#
function_style %= darrow + simple_expression + semicolon#, lambda h, s: ("Object", s[2])
function_style %= colon + identifier + darrow + simple_expression + semicolon#, lambda h, s: (s[2].Lemma, s[4])
function_style %= lbrace + expression_block + rbrace#, lambda h, s: ("Object", s[2])
function_style %= colon + identifier + lbrace + expression_block + rbrace#, lambda h, s: (s[2].Lemma, s[4])
#
parameters %= lparen + rparen#, lambda h, s: []
parameters %= lparen + parameter_list + rparen#, lambda h, s: s[2]
#
parameter_list %= variable#, lambda h, s: [s[1]]
parameter_list %= variable + comma + parameter_list#, lambda h, s: [s[1]] + s[3]
#
variable %= identifier#, lambda h, s: ParameterNode(s[1].Lemma)
variable %= identifier + colon + identifier#, lambda h, s: ParameterNode(s[1].Lemma, s[3].Lemma)
#
type_def %= class_block#, lambda h, s: ([], 'Object', [], s[1])
type_def %= inherits + identifier + class_block#, lambda h, s: ([], s[2].Lemma, [], s[3])
type_def %= lparen + parameter_list + rparen + class_block#, lambda h, s: (s[2], 'Object', [], s[4])
type_def %= lparen + parameter_list + rparen + inherits + identifier + class_block#, lambda h, s: (s[2], s[5].Lemma, [], s[6])
type_def %= lparen + parameter_list + rparen + inherits + identifier + lparen + argument_list + rparen + class_block#, lambda h, s: (s[2], s[5].Lemma, s[7], s[9])
type_def %= inherits + identifier + lparen + argument_list + rparen + class_block#, lambda h, s: ([], s[2].Lemma, s[4], s[6])
#
class_block %= lbrace + rbrace#, lambda h, s: []
class_block %= lbrace + class_body + rbrace#, lambda h, s: s[2]
#
class_body %= class_declaration#, lambda h, s: [s[1]]
class_body %= class_declaration + class_body#, lambda h, s: [s[1]] + s[2]
#
class_declaration %= variable + equal + main_expression#, lambda h, s: TypeAtributeNode(s[1], s[3])
class_declaration %= identifier + parameters + function_style#, lambda h, s: FunctionNode(s[1].Lemma, s[2], s[3][1], s[3][0])
#
protocol_declare %= protocol + identifier + lbrace + protocol_body + rbrace#, lambda h, s: ProtocolNode(s[2].Lemma, s[4])
protocol_declare %= protocol + identifier + extends + identifier + lbrace + protocol_body + rbrace#, lambda h, s: ProtocolNode(s[2].Lemma, s[6], s[4].Lemma)
#
protocol_body %= identifier + typed_parameters + colon + identifier + semicolon#, lambda h, s: [ProtocolMethodNode(s[1].Lemma, s[2], s[4].Lemma)]
protocol_body %= identifier + typed_parameters + colon + identifier + semicolon + protocol_body#, lambda h, s: [ProtocolMethodNode(s[1].Lemma, s[2], s[4].Lemma)] + s[6]
#
typed_parameters %= lparen + rparen#, lambda h, s: []
typed_parameters %= lparen + typed_parameter_list + rparen#, lambda h, s: s[2]
#
typed_parameter_list %= identifier + colon + identifier#, lambda h, s: [ParameterNode(s[1].Lemma, s[3].Lemma)]
typed_parameter_list %= identifier + colon + identifier + typed_parameter_list#, lambda h, s: [ParameterNode(s[1].Lemma, s[3].Lemma)] + s[4]
#

#----------------#

main_expression %= simple_expression + semicolon#, lambda h, s: s[1]
main_expression %= not_sc_expression#, lambda h, s: s[1]

# simple_expression %= simple_expression#, lambda h, s: s[1]


expression_block %= main_expression#, lambda h, s: ExpressionBlockNode([s[1]])
expression_block %= expression_block + main_expression#, lambda h, s: ExpressionBlockNode([s[2]] + s[1].EXPRESSIONS)

not_sc_expression %= let + declaration + in_ + not_sc_expression#, lambda h, s: LetNode(s[2][0], s[2][1], s[4])
not_sc_expression %= identifier + destruct + not_sc_expression#, lambda h, s: DestructiveExpression(s[1].Lemma, s[3])
not_sc_expression %= identifier + period + identifier + destruct + not_sc_expression#, lambda h, s: SelfDestructiveExpression(SelfVariableNode(s[1].Lemma == 'self', s[3].Lemma), s[5])
not_sc_expression %= if_ + lparen + disjunction + rparen + simple_expression + else_block_not_sc#, lambda h, s: IfElseExpression([s[3]] + s[6][0], [s[5]] + s[6][1])
not_sc_expression %= while_ + lparen + disjunction + rparen + not_sc_expression#, lambda h, s: WhileNode(s[3], s[5])
not_sc_expression %= for_ + lparen + identifier + in_ + simple_expression + rparen + not_sc_expression#, lambda h, s: ForNode(s[3].Lemma, s[5], s[7])
not_sc_expression %= lbrace + expression_block + rbrace#, lambda h, s: s[2]

else_block_not_sc %= else_ + not_sc_expression#, lambda h, s: ([], [s[2]])
else_block_not_sc %= elif_ + lparen + disjunction + rparen + simple_expression + else_block_not_sc#, lambda h, s: ([s[3]] + s[6][0], [s[5]] + s[6][1])

simple_expression %= let + declaration + in_ + simple_expression#, lambda h, s: LetNode(s[2][0], s[2][1], s[4])
simple_expression %= identifier + destruct + simple_expression#, lambda h, s: DestructiveExpression(s[1].Lemma, s[3])
simple_expression %= identifier + period + identifier + destruct + simple_expression#, lambda h, s: SelfDestructiveExpression(SelfVariableNode(s[1].Lemma == 'self', s[3].Lemma), s[5])
simple_expression %= if_ + lparen + disjunction + rparen + simple_expression + else_block#, lambda h, s: IfElseExpression([s[3]] + s[6][0], [s[5]] + s[6][1])
simple_expression %= while_ + lparen + disjunction + rparen + simple_expression#, lambda h, s: WhileNode(s[3], s[5])
simple_expression %= for_ + lparen + identifier + in_ + simple_expression + rparen + simple_expression#, lambda h, s: ForNode(s[3].Lemma, s[5], s[7])
simple_expression %= new + identifier + arguments#, lambda h, s: NewNode(s[2].Lemma, s[3])
simple_expression %= lbrace + expression_block + rbrace#, lambda h, s: s[2]

simple_expression %= disjunction#, lambda h, s: s[1]


declaration %= variable + equal + simple_expression#, lambda h, s: ([s[1]], [s[3]])
declaration %= variable + equal + simple_expression + comma + declaration#, lambda h, s: ([s[1]] + s[5][0], [s[3]]+s[5][1])

else_block %= else_ + simple_expression#, lambda h, s: ([], [s[2]])
else_block %= elif_ + lparen + disjunction + rparen + simple_expression + else_block#, lambda h, s: ([s[3]] + s[6][0], [s[5]] + s[6][1])

arguments %= lparen + rparen#, lambda h, s: []
arguments %= lparen + argument_list + rparen#, lambda h, s: s[2]
#
argument_list %= simple_expression#, lambda h, s: [s[1]]
argument_list %= simple_expression + comma + argument_list#, lambda h, s: [s[1]] + s[3]

disjunction %= conjunction#, lambda h, s: s[1]
disjunction %= conjunction + or_ + disjunction#, lambda h, s: OrAndExpression('|', s[1], s[3])

#
conjunction %= literal#, lambda h, s: s[1]
conjunction %= literal + and_ + conjunction#, lambda h, s: OrAndExpression('&', s[1], s[3])
#
literal %= proposition#, lambda h, s: s[1]
literal %= not_ + literal#, lambda h, s: NotExpression(s[2])
#
proposition %= boolean#, lambda h, s: s[1]
proposition %= proposition + is_ + identifier#, lambda h, s: IsExpression(s[1], s[3].Lemma)
#
boolean %= concatenation#, lambda h, s: s[1]
boolean %= boolean + dequal + concatenation#, lambda h, s: ComparationExpression('==', s[1], s[3])
boolean %= boolean + notequal + concatenation#, lambda h, s: ComparationExpression('!=', s[1], s[3])
boolean %= boolean + lequal + concatenation#, lambda h, s: ComparationExpression('<=', s[1], s[3])
boolean %= boolean + gequal + concatenation#, lambda h, s: ComparationExpression('>=', s[1], s[3])
boolean %= boolean + lesst + concatenation#, lambda h, s: ComparationExpression('<', s[1], s[3])
boolean %= boolean + greatt + concatenation#, lambda h, s: ComparationExpression('>', s[1], s[3])
#
concatenation %= arithmetic_expression#, lambda h, s: s[1]
concatenation %= arithmetic_expression + concat + concatenation#, lambda h, s: StringConcatenationNode(s[1], s[3])
concatenation %= arithmetic_expression + concat + concat + concatenation#, lambda h, s: StringConcatenationNode(s[1], s[4], True)
#
arithmetic_expression %= module#, lambda h, s: s[1]
arithmetic_expression %= arithmetic_expression + plus + module#, lambda h, s: ArithmeticExpression('+', s[1], s[3])
arithmetic_expression %= arithmetic_expression + minus + module#, lambda h, s: ArithmeticExpression('-', s[1], s[3])

module %= product#, lambda h, s: s[1]
module %= module + modulus + product#, lambda h, s: ArithmeticExpression('%', s[1], s[3])
#
product %= monomial#, lambda h, s: s[1]
product %= product + star + monomial#, lambda h, s: ArithmeticExpression('*', s[1], s[3])
product %= product + divide + monomial#, lambda h, s: ArithmeticExpression('/', s[1], s[3])
product %= product + int_divide + monomial#, lambda h, s: ArithmeticExpression('//', s[1], s[3])
#
monomial %= pow_#, lambda h, s: s[1]
monomial %= minus + monomial#, lambda h, s: ArithmeticExpression('-', NumberNode(0), s[2])
#
pow_ %= high_hierarchy_object#, lambda h, s: s[1]
pow_ %= pow_ + power_asterisk + high_hierarchy_object#, lambda h, s: ArithmeticExpression('**', s[1], s[3])
pow_ %= pow_ + power + high_hierarchy_object#, lambda h, s: ArithmeticExpression('^', s[1], s[3])
#
high_hierarchy_object %= object_exp#, lambda h, s: s[1]
high_hierarchy_object %= high_hierarchy_object + as_ + identifier#, lambda h, s: AsNode(s[1], s[3].Lemma)
#
function_stack %= identifier + period + identifier + arguments#, lambda h, s: TypeFunctionCallNode(VariableNode(s[1].Lemma), s[3].Lemma, s[4])
function_stack %= function_stack + period + identifier + arguments#, lambda h, s: TypeFunctionCallNode(s[1], s[3].Lemma, s[4])
function_stack %= identifier + arguments#, lambda h, s: FunctionCallNode(s[1].Lemma, s[2])
function_stack %= print_ + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('print', [s[3]])
function_stack %= sin + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('sin', [s[3]])
function_stack %= cos + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('cos', [s[3]])
function_stack %= tan + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('tan', [s[3]])
function_stack %= sqrt + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('sqrt', [s[3]])
function_stack %= exp + lparen + simple_expression + rparen#, lambda h, s: FunctionCallNode('exp', [s[3]])
function_stack %= log + lparen + simple_expression + comma + simple_expression + rparen#, lambda h, s: FunctionCallNode('log', [s[3]] + [s[5]]) # duda
function_stack %= rand + lparen + rparen#, lambda h, s: FunctionCallNode('rand', [])
function_stack %= range_ + lparen + simple_expression + comma + simple_expression + rparen#, lambda h, s: FunctionCallNode('range', [s[3]] + [s[5]])
function_stack %= base + lparen + rparen#, lambda h, s: FunctionCallNode('base', [])
function_stack %= identifier + period + identifier#, lambda h, s: SelfVariableNode(s[1].Lemma == 'self', s[3].Lemma)
function_stack %= lparen + simple_expression + rparen#, lambda h, s: s[2]
function_stack %= number#, lambda h, s: NumberNode(float(s[1].Lemma))
function_stack %= pi#, lambda h, s: NumberNode(math.pi)
function_stack %= e#, lambda h, s: NumberNode(math.e)
function_stack %= string#, lambda h, s: StringNode(s[1].Lemma)
function_stack %= true#, lambda h, s: BooleanNode(True)
function_stack %= false#, lambda h, s: BooleanNode(False)
function_stack %= lbrack + list_ + rbrack#, lambda h, s: s[2]
function_stack %= object_exp + lbrack + simple_expression + rbrack#, lambda h, s: IndexingNode(s[1], s[3])

object_exp %= identifier#, lambda h, s: VariableNode(s[1].Lemma)
object_exp %= function_stack#, lambda h, s: s[1]
#
list_ %= explicit_list_#, lambda h, s: ListNode(s[1])
list_ %= simple_expression + list_comprehension + identifier + in_ + simple_expression#, lambda h, s: ImplicitListNode(s[1], s[3].Lemma, s[5])

explicit_list_ %= simple_expression#, lambda h, s: [s[1]]
explicit_list_ %= simple_expression + comma + explicit_list_#, lambda h, s: [s[1]] + s[3]


def GetKeywords():
    return [for_, let, if_, else_, elif_, while_, function, pi, e, print_,
            new, inherits, protocol, type_, in_, range_, true, false, extends, as_,
            rand, sin, cos, sqrt, exp, log, is_, tan, base]

# from parserLr1 import LR1Parser
# parse=LR1Parser(G,verbose=True)
#
# derivarion=parse([let,identifier,equal,number,in_,print_,lparen,minus,identifier,rparen,semicolon,G.EOF])

