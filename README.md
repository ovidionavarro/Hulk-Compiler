# Hulk-Compiler

## Autores:
- Ovidio Navarro
- Juan José Muñoz
- Jesus Armando Padrón


## Project Structure

    
    lexer/: Implements the lexer for tokenizing HULK code.
        - lexer.py: Implements a lexer's generator
        - regex.py: Regular expressions for HULK Grammar
    
    parser/: Implements the parser
        - parserLR1.py: Implements a parser LR1 generator

    semantic_checker/: Implements the semantic checker for performing semantic analysis. 
        - ast.py: Contains nodes of AST
        - types.py: Contains types, Context and Scope implementation
        - type_checker.py: Implements initial semantic analysis


## Getting Started

Clone the Repository:

```bash
git clone https://github.com/ovidionavarro/Hulk-Compiler.git
```

Navigate to the Project Directory:

```bash
cd hulk-compiler
```

```bash
python main.py test#.py
```