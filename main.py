from src.lexer import Lexer

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
zero = '|'.join(str(n) for n in range(0, 10))
letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
cap_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letters = cap_letters + '|' + letters
print('Non-zero digits:', nonzero_digits)
print('Zero Dig', zero)
print('Letters:', letters)

lexer = Lexer([
    ('num', f'({nonzero_digits})*|({nonzero_digits})*(.)({zero})*|(0)*(.)({zero})'),
    ('for', 'for'),
    ('foreach', 'foreach'),
    ('space', ' *'),
    ('equal', '='),
    ('let', 'let'),
    ('in', 'in'),
    ('plus', '+'),
    ('f_print', 'print'),
    ('semicolon', ';'),
    ('open_paran', '\\('),
    ('close_paran', '\\)'),
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
    for j in i:
        tokens.append(j)

print(tokens)

