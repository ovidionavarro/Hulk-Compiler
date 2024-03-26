from cmp.automata import State
from cmp.tools.regex import Regex
from cmp.utils import Token

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            # Your code here!!!
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            automaton,states=State.from_nfa(Regex(regex).automaton,get_states=True)
            for state in states:
                if state.final:
                    state.tag=(n,token_type)
            regexs.append(automaton)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for state in self.regexs:
            start.add_epsilon_transition(state)

        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        lex = ""

        for symbol in string:
            # Your code here!!!
            if state.has_transition(symbol):
                lex += symbol
                state = state[symbol][0]

                if state.final:
                    final = state
                    final.lex = lex
            else:
                break

        if final:
            return final, final.lex

        return None, None
    
    def _tokenize(self, text):
        while text:
            final, lex = self._walk(text)
            if final is None:
                yield 'Error', text
                break

            text = text[len(lex):]
            final=[state.tag for state in final.state if state.tag ]
            final.sort()

            yield lex, final[0][1]
        
        yield '$', self.eof
    
    def __call__(self, text):
            return [Token(lex, ttype) for lex, ttype in self._tokenize(text)]





nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

print('Non-zero digits:', nonzero_digits)
print('Letters:', letters)

lexer = Lexer([
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('for' , 'for'),
    ('foreach' , 'foreach'),
    ('space', '  *'),
    ('id', f'({letters})({letters}|0|{nonzero_digits})*')
], 'eof')



#test
text = '5465 for 45foreach fore'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)
assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

text = '4forense forforeach for4foreach foreach 4for'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)
assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']