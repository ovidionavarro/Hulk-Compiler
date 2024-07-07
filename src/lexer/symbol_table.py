
from src.grammar.grammar import  *

regular_chars = ("abcdefghijklmnopqrstuvwxyzABCD"
                 "EFGHIJKLMNOPQRSTUVWXYZ#$%&@^_"
                 "<>=,:;-+/0123456789{}")
join_reg_chars='|'.join(str(n) for n in regular_chars)
# +'|' + '\\('+ '|' +'\\)' + '|'+'\\*'+'|'+ '\\|'
nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters_minus = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters_mayus = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
letters='_'+'|'+letters_mayus+'|'+letters_minus

symbol_table=[
    (for_, "for"),
    (let, "let"),
    (if_, "if"),
    (else_, "else"),
    (elif_, "elif"),
    (while_, "while"),
    (function, "function"),
    # (print_, "print"),
    (pi, "pi"),
    (e, "e"),
    (new, "new"),
    (inherits, "inherits"),
    (protocol, "protocol"),
    (type_, "type"),
    (in_, "in"),
    (range_, "range"),
    (true, "true"),
    (false, "false"),
    (extends, "extends"),
    # (sin, "sin"),
    # (cos, "cos"),
    # (tan, "tan"),
    # (sqrt, "sqrt"),
    # (exp, "exp"),
    # (log, "log"),
    # (rand, "rand"),
    # (base, "base"),
    (plus, "+"),
    (star, "\\*"),
    (minus, "-"),
    (divide, "/"),
    (equal, "="),
    (dequal, "=="),
    (notequal, "!="),
    (lesst, "<"),
    (greatt, ">"),
    (lequal, "<="),
    (gequal, ">="),
    (lparen, "\\("),
    (rparen, "\\)"),
    (lbrack, "["),
    (rbrack, "]"),
    (lbrace, "{"),
    (rbrace, "}"),
    (comma, ","),
    (period, "."),
    (colon, ":"),
    (semicolon, ";"),
    (arrow, "->"),
    (darrow, "=>"),
    (and_, "&"),
    (or_, "\\|"),
    ('space',"\\ *"),
    # ('list_comprehension', "\|\|"),
    (not_, "!"),
    (modulus, "%"),
    (power, "^"),
    (destruct, ":="),
    (concat, "@"),
    (is_, "is"),
    (as_, "as"),
    (number, f'(0|({nonzero_digits})(0|{nonzero_digits})*)|((0|({nonzero_digits})(0|{nonzero_digits})*).(0|{nonzero_digits})*)'),
    (identifier, f'({letters})({letters}|0|{nonzero_digits})*'),
    (string,f'"({join_reg_chars}| |\\(|\\)|\\*|\\|)*"'),
]
