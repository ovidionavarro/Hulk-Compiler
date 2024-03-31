from src.lexer import Lexer
nonzero_digits = '|'.join(str(n) for n in range(1, 10))
digits = '|'.join(str(n) for n in range(0, 10))
letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
cap_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letters = cap_letters + '|' + letters

no_first_zero = f'({nonzero_digits})*|(({nonzero_digits})(0)*)'
lexer = Lexer([
    ('num', f'{no_first_zero}|(({no_first_zero})*|(0))(.)({digits})*'),
    ('_for', 'for'),
    ('_foreach', 'foreach'),
    ('_while', 'while'),
    ('_range', 'range'),
    ('_if', 'if'),
    ('_else', 'else'),
    ('_elif', 'elif'),
    ('space', ' *'),

    ('asig', '='),
    ('des_operator', ':='),
    ('mult', '\\*'),
    ('div', '/'),
    ('pow', '^'),
    ('add', '+'),
    ('sub', '-'),
    ('lt', '<'),
    ('le', '<='),
    ('gt', '>'),
    ('ge', '>='),
    ('eq', '=='),
    ('not_eq', '!='),
    ('_and', '&'),
    ('_or', '\\|'),
    ('_not', '!'),
    ('concatenation', '@'),
    ('l_op', '\\||'),
    ('exp', '\\**'),
    ('_sqrt', 'sqrt'),
    ('_sin', 'sin'),
    ('_cos', 'cos'),
    ('_exp', 'exp'),
    ('_log', 'log'),
    ('_rand', 'rand'),

    ('Number', 'Number'),
    ('Object', 'Object'),
    ('Boolean', 'Boolean'),
    ('let', 'let'),
    ('in', 'in'),
    ('_print', 'print'),
    ('_size', 'size'),
    ('_function', 'function'),
    ('new', 'new'),
    ('_type', 'type'),
    ('_self', 'self'),
    ('inherits','inherits'),
    ('protocol', 'protocol'),
    ('_extends', 'extends'),
    ('_as', 'as'),
    ('_is', 'is'),
    ('arrow', '=>'),
    ('colon', ':'),
    ('semicolon', ';'),
    ('comma', ','),
    ('d_quotes', '"'),
    #('esc_quotes', str("\"")),
    # ('eol', str("\n")),
    # ('tab', str("\t")),
    ('o_parent', '\\('),
    ('c_parent', '\\)'),
    ('o_curly_brakes', '{'),
    ('c_curly_brakes', '}'),
    ('o_sq_bracket', '['),
    ('c_sq_bracket', ']'),
    ('id', f'({letters})({letters}|0|{nonzero_digits})*')
], 'eof')



# test

with open("test.hulk") as file:
    content = file.read()
    file.close()

print("Contenido:\n", content)

text_list = content.split('\n')
tokens_l = []
tokens = []
for i in text_list:
    tokens_l.append(lexer(i))

for i in tokens_l:
    print(i)
    for j in i:
        tokens.append(j)
