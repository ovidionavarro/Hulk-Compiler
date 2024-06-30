import sys
import os
from src.lexer.lexer import Lexer
from src.lexer.symbol_table import  symbol_table




lexer=Lexer(symbol_table,'eof')
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
        print(f'\n>>> Tokenizando: "{text}"')
        tokens = lexer(text)
        print(tokens)


    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
    except Exception as e:
        print(f"Error: {e}")