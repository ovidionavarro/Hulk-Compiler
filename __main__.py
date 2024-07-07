import sys
import os

from src.lexer.lexer import Lexer
from src.lexer.symbol_table import  symbol_table
from src.parser.parserLR1 import LR1Parser
from src.grammar.grammar import *
from src.cmp.evaluation import evaluate_reverse_parse
from src.semantic_checker.visitor_print import *
from src.semantic_checker.type_collector import *
import dill


def read_file_as_string(filename):
    with open(filename, "r") as file:
        content = file.read()
    return content

def load_src():
    route = os.getcwd()
    route = os.path.join(route, 'models')

    try:
        with open(os.path.join(route, 'lexer.pkl'), 'rb') as lexer_file:
            lexer = dill.load(lexer_file)

        with open(os.path.join(route, 'parser.pkl'), 'rb') as parser_file:
            parser = dill.load(parser_file)

        return lexer, parser
    except:
        lexer=Lexer(symbol_table,G.EOF)
        parser=LR1Parser(G,verbose=True)        

        with open(os.path.join(route, 'lexer.pkl'), 'wb') as lexer_file:
            dill.dump(lexer, lexer_file)

        with open(os.path.join(route, 'parser.pkl'), 'wb') as parser_file:
            dill.dump(parser, parser_file)

        return lexer, parser




if __name__ == "__main__":
    # Comprueba que se haya pasado un argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <nombre_del_archivo>")
        sys.exit(1)

    # Obtiene el nombre del archivo del primer argumento
    filename = sys.argv[1]
    try:
        lexer=Lexer(symbol_table,G.EOF)
        parser=LR1Parser(G,verbose=True)   
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
        parse,operations=parser([t.token_type for t in tokens])
        print(tokens)
    # AST
        ast=evaluate_reverse_parse(parse,operations,tokens)
        print(ast)
        formater=PrintVisitor()
        print(formater.visit(ast))
    #Type Collector
        collector = TypeCollector()
        collector.visit(ast)

        context = collector.context

        
        print('Context:')
        print(context)
        print('Errors:', collector.errors)


    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
    except Exception as e:
        print(f"Error: {e}")