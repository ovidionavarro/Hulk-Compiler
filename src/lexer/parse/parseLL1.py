from itertools import islice
from src.cmp.utils import ContainerSet
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()
    else:
        first_alpha.update(firsts[alpha._symbols[0]])

        i = 0
        xi = alpha._symbols[i]
        while firsts[xi].contains_epsilon:
            if i == len(alpha._symbols):
                first_alpha.set_epsilon()
                break
            i += 1
            xi = alpha._symbols[i]
            if not firsts[xi].contains_epsilon:
                first_alpha.update(firsts[xi])
                break
    # First(alpha)
    return first_alpha
def compute_firsts(G):
    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            first_X = firsts[X]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    return firsts
def compute_follows(G, firsts):
    follows = {}
    change = True

    local_firsts = {}

    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            follow_X = follows[X]

            if alpha.IsEpsilon:
                continue

            n = len(alpha._symbols) - 1
            for i in range(n):
                Y = alpha._symbols[i]
                beta = alpha._symbols[i + 1]
                if Y.IsNonTerminal:
                    change |= follows[Y].update(firsts[beta])
                    if firsts[beta].contains_epsilon:
                        change |= follows[Y].update(follow_X)
                if i == n - 1 and beta.IsNonTerminal:
                    change |= follows[beta].update(follow_X)

    # Follow(Vn)
    return follows


def build_parsing_table(G, firsts, follows):
    # init parsing table
    M = {}
    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        # working with symbols on First(alpha) ...
        for terminal in G.terminals:
            if terminal in firsts[alpha].set:
                M[X, terminal] = [production]

        # working with epsilon...
        if firsts[alpha].contains_epsilon:
            for terminal in G.terminals:
                if terminal in follows[X].set:
                    M[X, terminal] = [production]
            if G.EOF in follows[X].set:
                M[X, G.EOF] = [production]

    # parsing table is ready!!!
    return M


def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    # parser construction...
    def parser(w):
        # w ends with $ (G.EOF)
        # init:
        stack = [G.startSymbol]
        cursor = 0
        output = []
        # parsing w...
        while True:
            if not stack:
                break
            top = stack.pop()
            a = w[cursor]

            if top.IsTerminal:
                if top == a:
                    cursor += 1
            else:
                production = M[top, a][0]
                output.append(production)

                _, sentenceToInsert = production
                if sentenceToInsert.IsEpsilon:
                    continue
                n = len(sentenceToInsert._symbols)
                for i in range(n):
                    stack.append(sentenceToInsert._symbols[n - i - 1])
                    ###################################################
        # left parse is ready!!!
        return output
    # parser is ready!!!
    return parser

deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated
##TEST##
# from src.cmp.pycompiler import Grammar,EOF,Epsilon,Sentence,Production
# from src.cmp.utils import pprint
# G = Grammar()
# E = G.NonTerminal('E', True)
# T,F,X,Y = G.NonTerminals('T F X Y')
# plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')
#
# E %= T + X
# X %= plus + T + X | minus + T + X | G.Epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.Epsilon
# F %= num | opar + E + cpar
#
# from src.cmp.languages import BasicHulk
# hulk =BasicHulk(G)
#
# firsts=compute_firsts(G)
# follows = compute_follows(G, firsts)
# M = build_parsing_table(G, firsts, follows)
#
# parser = metodo_predictivo_no_recursivo(G, M)
# left_parse = parser([num, star, num, star, num, plus, num, star, num, plus, num, plus, num, G.EOF])
#
# assert left_parse == [
#    Production(E, Sentence(T, X)),
#    Production(T, Sentence(F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, Sentence(star, F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, Sentence(star, F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, G.Epsilon),
#    Production(X, Sentence(plus, T, X)),
#    Production(T, Sentence(F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, Sentence(star, F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, G.Epsilon),
#    Production(X, Sentence(plus, T, X)),
#    Production(T, Sentence(F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, G.Epsilon),
#    Production(X, Sentence(plus, T, X)),
#    Production(T, Sentence(F, Y)),
#    Production(F, Sentence(num)),
#    Production(Y, G.Epsilon),
#    Production(X, G.Epsilon),
# ]

###TEST2
# G = Grammar()
# S = G.NonTerminal('S', True)
# A,B = G.NonTerminals('A B')
# a,b = G.Terminals('a b')
#
# S %= A + B
# A %= a + A | a
# B %= b + B | b
#
# firsts = compute_firsts(G)
# pprint(firsts)
#
# # print(inspect(firsts))
# assert firsts == {
#    a: ContainerSet(a , contains_epsilon=False),
#    b: ContainerSet(b , contains_epsilon=False),
#    S: ContainerSet(a , contains_epsilon=False),
#    A: ContainerSet(a , contains_epsilon=False),
#    B: ContainerSet(b , contains_epsilon=False),
#    Sentence(A, B): ContainerSet(a , contains_epsilon=False),
#    Sentence(a, A): ContainerSet(a , contains_epsilon=False),
#    Sentence(a): ContainerSet(a , contains_epsilon=False),
#    Sentence(b, B): ContainerSet(b , contains_epsilon=False),
#    Sentence(b): ContainerSet(b , contains_epsilon=False)
# }
# print('ok')