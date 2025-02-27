from cmp.pycompiler import Grammar
from cmp.pycompiler import Item
from cmp.utils import ContainerSet
from cmp.tools.parsing import compute_firsts, compute_local_first
from cmp.automata import State, multiline_formatter
from pandas import DataFrame
from src.grammar.aux_grammar import *


# clausura del conjunto de items
def expand(item, G):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    # Your code here!!! (Compute lookahead for child items)
    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # Your code here!!! (Build and return child items)
    output = []
    for production in G.Productions:
        if production.Left == next_symbol:
            output.append(Item(production, 0, lookaheads))
    return output


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
def closure_lr1(items, G):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        # Your code here!!!
        for item in closure:
            for new_item in expand(item, G):
                new_items.add(new_item)

        changed = closure.update(new_items)
        # print(changed)

    return compress(closure)


# GOTO
def goto_lr1(items, symbol, G, just_kernel=False):
    # assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, G)


# Construyendo el autómata LR(1)
def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    # firsts = compute_firsts(G)
    # firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, G)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            next_items = frozenset(goto_lr1(current_state.state, symbol, G))
            if not next_items:
                continue
            try:
                next_state = visited[next_items]
            except KeyError:
                visited[next_items] = State(next_items, True)
                pending.append(next_items)
                next_state = visited[next_items]

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

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_operations=True):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        while True:
            state = stack[-1]
            if cursor < len(w):
                lookahead = w[cursor]
            else:
                break
            if self.verbose: print(stack, '<---||--->', w[cursor:])

            # Your code here!!! (Detect error)

            action, tag = self.action[state, lookahead]
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
            return output, operations
        return output


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
                # - Fill `self.Action` and `self.Goto` according to `item`)
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


parser = LR1Parser(G, verbose=True)


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
print(table_to_dataframe(parser.action))
print(table_to_dataframe(parser.goto))

###TEST
# derivation = parser([number, plus, number, equal, number, plus, number, G.EOF])
derivation, operations = parser([defx, idx, opar, idx, comma, idx, cpar, arrow, num, plus, num, semi])
# derivation, operations = parser([defx, idx, opar, idx,cpar, arrow, ])

# assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'
print(derivation)
