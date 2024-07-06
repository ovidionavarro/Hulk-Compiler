import pydot
from src.cmp.utils import ContainerSet

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass


class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        # Your code here
        try:
            self.current = self.transitions[self.current][symbol][0]
        except KeyError:
            self.current = None
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        # Your code here
        self._reset()
        for symbol in string:
            self._move(symbol)
        return self.current in self.finals

def move(automaton, states, symbol):
    moves = set()
    for state in states:
        # Your code here
        try:
            moves.update(automaton.map[(state,symbol)])
        except KeyError:
            pass
    return moves


def epsilon_closure(automaton, states):
    pending = [s for s in states]  # equivalente a list(states) pero me gusta así :p
    closure = {s for s in states}  # equivalente a  set(states) pero me gusta así :p
    while pending:
        state = pending.pop()
        try:
            new_states = automaton.map[(state, '')]
            closure.update(new_states)
            closure.update(epsilon_closure(automaton, new_states).set)
        except KeyError:
            pass
    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [start]
    state_sets = [start.set]

    pending = [start]
    index = 0
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            # Your code here
            next_state_set = epsilon_closure(automaton, move(automaton, list(state.set), symbol)).set

            if not next_state_set:  # Para obtener un automata completamente especificado
                continue  # comentar estas dos lineas

            try:
                i = state_sets.index(next_state_set)
                next_state = states[i]
            except ValueError:
                next_state = ContainerSet(*next_state_set)
                index += 1
                next_state.id = index
                next_state.is_final = any(s in automaton.finals for s in next_state)

                states.append(next_state)
                state_sets.append(next_state_set)
                pending.append(next_state)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                transitions[state.id, symbol] = next_state.id

    finals = [state.id for state in states if state.is_final]
    dfa = DFA(len(states), finals, transitions)
    return dfa


def nfa_recognize(automaton: NFA, string: str):
    states = epsilon_closure(automaton, [automaton.start]).set

    while states and string:
        symbol = string[0]

        states = epsilon_closure(automaton, move(automaton, states, symbol)).set

        string = string[1:]

    return len(states.intersection(automaton.finals)) > 0


##test
# automaton = NFA(states=5, finals=[4], transitions={
#     (0,'a'): [ 0, 1 ],
#     (0,'b'): [ 0, 2 ],
#     (0,'c'): [ 0, 3 ],
#     (1,'a'): [ 1, 4 ],
#     (1,'b'): [ 1 ],
#     (1,'c'): [ 1 ],
#     (2,'a'): [ 2 ],
#     (2,'b'): [ 2, 4 ],
#     (2,'c'): [ 2 ],
#     (3,'a'): [ 3 ],
#     (3,'b'): [ 3 ],
#     (3,'c'): [ 3, 4 ],
# })
#
# assert nfa_recognize(automaton,'abccac')
# assert nfa_recognize(automaton,'bbbbbbbbaa')
# assert nfa_recognize(automaton,'cac')
#
# assert not nfa_recognize(automaton,'abbbbc')
# assert not nfa_recognize(automaton,'a')
# assert not nfa_recognize(automaton,'')
# assert not nfa_recognize(automaton,'acacacaccab')