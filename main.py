from src.lexer import Lexer
from src.lexer import lexer_table
lexer = Lexer(lexer_table,'eof')


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
