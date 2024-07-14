from src.cmp.utils import Token
from src.cmp.automata import State
from src.lexer.regex import Regex
from src.lexer.symbol_table import symbol_table

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
            automaton = Regex(regex).automaton
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (token_type, n)
            regexs.append(automaton)
        return regexs

    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:
            # Your code here!!!
            try:
                state = state[symbol][0]
                lex = lex + symbol
            except TypeError:
                break

        final = state
        final.tag = (None, float('inf'))
        for state in final.state:
            if state.final and state.tag[1] < final.tag[1]:
                final.tag = state.tag
        final_lex = lex

        return final, final_lex

    def _tokenize(self, text: str):
        # Your code here!!!
        remaining_text = text
        while True:
            final_state, final_lex = self._walk(remaining_text)

            if final_lex == '':
                yield text.rsplit(remaining_text)[0], final_state.tag[0]
                return

            yield final_lex, final_state.tag[0]
            remaining_text = remaining_text.replace(final_lex, '', 1)
            if remaining_text == '':
                break

        yield '$', self.eof

    def __call__(self, text):
        tokens= [Token(lex, ttype) for lex, ttype in self._tokenize(text)]
        aux= [token for token in tokens if token.token_type not in ['space']]
        count_col=1
        count_fil=1
        for token in aux:
            if token.lex=='~':
                count_fil+=1
                count_col=0
            token.fil=count_fil
            token.col=count_col
            count_col+=1
        return[token for token in aux if token.token_type not in ['jump']]


# lexer=Lexer(symbol_table,'eof')
# lexer = Lexer([
#     ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
#     ('for' , 'for'),
#     ('foreach' , 'foreach'),
#     ('space', '  *'),
#     ('open_parent','\\('),
#     ('id', f'({letters})({letters}|0|{nonzero_digits})*')
# ], 'eof')

# text = ('{x = 1;y = 0;}')
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
# assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']
#
# text = '4forense forforeach for4foreach foreach 4for'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
# assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']