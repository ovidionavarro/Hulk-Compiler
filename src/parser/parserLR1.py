from src.cmp.pycompiler import Item
from src.cmp.utils import ContainerSet
from src.parser.utils_parse import compute_firsts, compute_local_first
from src.cmp.automata import State, multiline_formatter
from pandas import DataFrame
from src.grammar.grammar import *

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # Your code here!!! (Compute lookahead for child items)
    for preview in item.Preview():
        lookaheads.hard_update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # Your code here!!! (Build and return child items)
    # output = []
    # for production in G.Productions:
    #     if production.Left == next_symbol:
    #         output.append(Item(production,0,lookaheads))
    # return output
    return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}


# clausura del conjunto de items lr1
def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False
        new_items = ContainerSet()
        # Your code here!!!
        for item in closure:
            new_items.extend(expand(item, firsts))
        changed = closure.update(new_items)

    return compress(closure)


# GOTO
def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert (
            just_kernel or firsts is not None
    ), '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


# Construyendo el autómata LR(1)
def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            items = current_state.state
            kernel = goto_lr1(items, symbol, just_kernel=True)
            if not kernel:
                continue
            try:
                next_state = visited[kernel]
            except KeyError:
                closure = goto_lr1(items, symbol, firsts)
                next_state = visited[kernel] = State(frozenset(closure), True)
                pending.append(kernel)
            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton


class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    # def _build_parsing_table(self):
    #    raise NotImplementedError()

    def __call__(self, w, get_operations=True):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        error=[]

        while True:
            state = stack[-1]
            if cursor < len(w):
                lookahead = w[cursor]
            else:
                break
            if self.verbose: print(stack, '<---||--->', w[cursor:])

            # Your code here!!! (Detect error)

            try:
                action, tag = self.action[state, lookahead]
            except KeyError as ex:
                error.append(cursor)
                break

            # Your code here!!! (Shift case)
            match action:
                case self.SHIFT:
                    operations.append((self.SHIFT))
                    stack.append(lookahead)
                    stack.append(tag)
                    cursor += 1
                # Your code here!!! (Reduce case)
                case self.REDUCE:
                    operations.append((self.REDUCE))
                    production = self.G.Productions[tag]
                    X, beta = production
                    for i in range(2 * len(beta)):
                        stack.pop()
                    l = stack[-1]
                    stack.append(X.Name)
                    stack.append(self.goto[l, X])
                    output.append(production)
                # Your code here!!! (OK case)
                case self.OK:
                    break
                # Your code here!!! (Invalid case)
                case _:
                    raise Exception
        if (get_operations):
            return output, operations,error
        return output,error


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`
                # - Feel free to use `self._register(...)`)
                X = item.production.Left
                symbol = item.NextSymbol
                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0))
                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:
                        self._register(self.action, (idx, s), (self.REDUCE, k))
                elif symbol.IsTerminal:
                    self._register(self.action, (idx, symbol), (self.SHIFT, node.transitions[symbol.Name][0].idx))
                else:
                    self._register(self.goto, (idx, symbol), node.transitions[symbol.Name][0].idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value


# Utilizando pandas generar tabla
def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action == ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value


def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = {symbol: value}

    return DataFrame.from_dict(d, orient='index', dtype=str)


# ver tabla
# print(table_to_dataframe(parser.action))
# print(table_to_dataframe(parser.goto))

###TEST
# from src.cmp.utils import Token
# parser = LR1Parser(G, verbose=True)
# tokens= [
#     Token('let',let ),
# Token('a', identifier),
# Token('=', equal),
# Token('55', number),
# Token('==', dequal),
# Token('55', number),
# Token('+', plus),
# Token('55', number),
#
# Token('|', or_),
# Token('55', number),
# Token('!=',notequal ),
# Token('55', number),



# Token(',', comma),
# Token('b', identifier),
# Token('=', equal),
# Token('55', number),
# Token('*', times),
# Token('a',identifier),
# Token('in', in_),
# Token('print',print_),
# Token('(', lparen),
# Token('a', identifier),

# Token('5',number),
# Token('^',power),
# Token('5',number),
# Token('as',as_),
# Token('b',identifier),
# Token(')', rparen),
# Token(';',semicolon),
# Token('$', G.EOF),
# ]
# tokens=[
#     Token('let', let),
#     Token('x', idx),
#     Token('=', equal),
#     Token('58', num),
#     Token(';', semi),
#     Token('def', defx),
#     Token('f', idx),
#     Token('(', opar),
#     Token('a', idx),
#     Token(',', comma),
#     Token('b', idx),
#     Token(')', cpar),
#     Token('->', arrow),
#     Token('5', num),
#     Token('+', plus),
#     Token('6', num),
#     Token(';', semi),
#     Token('print', printx),
#     Token('f', idx),
#     Token('(', opar),
#     Token('5', num),
#     Token('+', plus),
#     Token('x', idx),
#     Token(',', comma),
#     Token('7', num),
#     Token('+', plus),
#     Token('y', idx),
#     Token(')', cpar),
#     Token(';', semi),
#     Token('$', G.EOF),
# ]

# parse, operations = parser([t.token_type for t in tokens],get_operations=True)

# assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'
# derivation,operations = parser([number,minus,number])
# print(operations)
# derivation