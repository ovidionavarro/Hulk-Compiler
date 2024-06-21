from src.cmp.utils import Token
from src.lexer.grammar_regex import G
from src.lexer.parse.parseLL1 import metodo_predictivo_no_recursivo
from src.utils.evaluate_simple import evaluate_parse
from src.lexer.lexer_ast import AtomicNode,UnaryNode,BinaryNode
from src.cmp.ast import get_printer
from src.utils.automatas import nfa_to_dfa
from src.utils.automata_operation import automata_minimization

printer=get_printer(AtomicNode=AtomicNode,UnaryNode=UnaryNode,BinaryNode=BinaryNode)
def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    # > fixed_tokens = ???
    fixed_tokens = {lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split()}
    special_char = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif special_char:
            token = Token(char, G['symbol'])
            special_char = False
        elif char == '\\':
            special_char = True
            continue
        else:
            try:
                token = fixed_tokens[char]
            except:
                token = Token(char, G['symbol'])
        tokens.append(token)

    tokens.append(Token('$', G.EOF))
    return tokens


class Regex:
    def __init__(self,regex,skip_whitespaces=False):
        self.regex=regex
        self.automaton = self.regex_automaton(regex, skip_whitespaces)

    @staticmethod
    def regex_automaton(regex, skip_whitespaces):
        tokens = regex_tokenizer(regex, G, skip_whitespaces)
        parser = metodo_predictivo_no_recursivo(G)
        left_parser = parser(tokens)
        ast = evaluate_parse(left_parser, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        return automata_minimization(dfa)

    def __call__(self, text):
        return self.automaton.recognize(text)


# m=Regex('"(a|b|\\|)*"',False)
# print(m('"||a|"'))
##test
# tokens = regex_tokenizer('\\(* | ε',G)
# print(tokens)
# parser = metodo_predictivo_no_recursivo(G)
# left_parse = parser(tokens)
# print(left_parse)
# ast = evaluate_parse(left_parse, tokens)
# print(printer(ast))
# nfa=ast.evaluate()
# print(nfa)
# dfa=nfa_to_dfa(nfa)

# assert dfa.recognize('(')
# assert dfa.recognize('(((')
# assert not dfa.recognize('()')
# dfa=Regex('\\(')
# assert dfa.recognize('bbbcd')
# assert dfa.recognize('aaaaacd')
# assert dfa.recognize('bbbbbcd')
# assert dfa.recognize('bbabababcd')
# assert dfa.recognize('aaabbabababcd')
#
# assert not dfa.recognize('cdacd')
# assert not dfa.recognize('aaaaa')
# assert not dfa.recognize('bbbbb')
# assert not dfa.recognize('ababba')
# assert not dfa.recognize('cdbaba')
# assert not dfa.recognize('cababad')
# assert not dfa.recognize('bababacc')
#
# mini = automata_minimization(dfa)
# assert mini.recognize('aaaaacd')
# assert mini.recognize('bbbbbcd')
# assert mini.recognize('bbabababcd')
# assert mini.recognize('aaabbabababcd')
#
# assert not mini.recognize('cda')
# assert not mini.recognize('aaaaa')
# assert not mini.recognize('bbbbb')
# assert not mini.recognize('ababba')
# assert not mini.recognize('cdbaba')
# assert not mini.recognize('cababad')
# assert not mini.recognize('bababacc')

