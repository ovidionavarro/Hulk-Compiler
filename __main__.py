import sys
import os
from src.lexer.lexer import Lexer
from src.lexer.symbol_table import  symbol_table
from src.parser.parserLR1 import LR1Parser,G
from src.grammar.jagrammar import *




lexer=Lexer(symbol_table,G.EOF)
parser=LR1Parser(G,verbose=True)

def read_file_as_string(filename):
    with open(filename, "r") as file:
        content = file.read()
    return content


if __name__ == "__main__":
    # Comprueba que se haya pasado un argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <nombre_del_archivo>")
        sys.exit(1)

    # Obtiene el nombre del archivo del primer argumento
    filename = sys.argv[1]
    try:
    #obtener ruta completa
        file_path = os.path.join("test", filename)
        text = read_file_as_string(file_path)
        text = text.replace('\n', '')
    #TOKENIZAR
        print(f'\n>>> Tokenizando: "{text}"')
        tokens = lexer(text)
        print(tokens)
    #PARSER
        print('Parseando')
        parser,operations=parser([t.token_type for t in tokens])


    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
    except Exception as e:
        print(f"Error: {e}")