from src.utils.automatas import NFA,DFA,nfa_to_dfa
from src.cmp.utils import  DisjointSet
from copy import copy
def automata_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

    for (origin, symbol), destinations in a2.map.items():
        # Your code here
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]

    ## Add transitions from start state ...
    transitions[start, ''] = [d1, d2]

    ## Add transitions to final state ...
    transitions[d2 - 1, ''] = [final]
    transitions[final - 1, ''] = [final]

    states = a1.states + a2.states + 2
    finals = {final}

    return NFA(states, finals, transitions, start)
def automata_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[origin, symbol] = destinations

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]

    ## Add transitions to final state ...
    transitions[d2 - 1, ''] = [d2]
    transitions[final - 1, ''] = [final]

    states = a1.states + a2.states + 1
    finals = {final}

    return NFA(states, finals, transitions, start)
def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        # Your code here
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

        ## Add transitions from start state ...
    # Your code here
    transitions[start, ''] = [d1]

    ## Add transitions to final state and to start state ...
    # Your code here
    transitions[final - 1, ''] = [final]
    transitions[final, ''] = [start]

    states = a1.states + 2
    finals = {start, final}

    return NFA(states, finals, transitions, start)


def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        state = member.value

        # Your code here
        destinations = []
        for char in vocabulary:
            destinations.append(partition[automaton.transitions[state][char][0]].representative)
        destinations = tuple(destinations)

        try:
            split[destinations].append(state)
        except KeyError:
            split[destinations] = [state]

    return [group for group in split.values()]


def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))

    ## partition = { NON-FINALS | FINALS }
    finals = automaton.finals
    non_finals = [state for state in range(automaton.states) if state not in finals]

    partition.merge(finals)
    partition.merge(non_finals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))

        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        # Your code here
        for group in partition.groups:
            new_groups = distinguish_states(group, automaton, partition)

            for new_group in new_groups:
                new_partition.merge(new_group)

        if len(new_partition) == len(partition):
            break

        partition = new_partition

    return partition


def automata_minimization(automaton):
    partition = state_minimization(automaton)

    states = [s.value for s in partition.representatives]

    transitions = {}
    for i, state in enumerate(states):
        ## origin = ???
        # Your code here
        origin = state

        for symbol, destinations in automaton.transitions[origin].items():
            # Your code here
            destination = destinations[0]
            new_destination = partition[destination].representative.value
            new_destination = states.index(new_destination)

            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                # Your code here
                transitions[i, symbol] = new_destination

    ## finals = ???
    ## start  = ???
    # Your code here
    finals = [states.index(state) for state in states if state in automaton.finals]
    for group in partition.groups:
        for member in group:
            if automaton.start == member.value:
                start = states.index(partition[member.value].representative.value)
                break
                # start = [states.index(group[0].value) for group in partition.groups if automaton.start in group][0]

    return DFA(len(states), finals, transitions, start)

def automata_complement(a1):
    complement = copy(a1)
    complement.finals = [i for i in range(a1.states) if i not in a1.finals]
    return complement


# automaton = DFA(states=5, finals=[4], transitions={
#     (0,'a'): 1,
#     (0,'b'): 2,
#     (1,'a'): 1,
#     (1,'b'): 3,
#     (2,'a'): 1,
#     (2,'b'): 2,
#     (3,'a'): 1,
#     (3,'b'): 4,
#     (4,'a'): 1,
#     (4,'b'): 2,
# })
# print(automaton.transitions[4]['b'][0])
# states = state_minimization(automaton)
# print(states)
#
# for members in states.groups:
#     all_in_finals = all(m.value in automaton.finals for m in members)
#     none_in_finals = all(m.value not in automaton.finals for m in members)
#     assert all_in_finals or none_in_finals
#
# assert len(states) == 4
# assert states[0].representative == states[2].representative
# assert states[1].representative == states[1]
# assert states[3].representative == states[3]
# assert states[4].representative == states[4]
#
#
# mini = automata_minimization(automaton)
#
# assert mini.states == 4
#
# assert mini.recognize('abb')
# assert mini.recognize('ababbaabb')
#
# assert not mini.recognize('')
# assert not mini.recognize('ab')
# assert not mini.recognize('aaaaa')
# assert not mini.recognize('bbbbb')
# assert not mini.recognize('abbabababa')


# automaton = DFA(states=2, finals=[1], transitions={(0,'a'):  0, (0,'b'):  1, (1,'a'):  0, (1,'b'):  1,})
#
# complement = automata_complement(automaton)
# recognize = nfa_to_dfa(complement).recognize
#
# assert not recognize('b')
# assert not recognize('abbb')
# assert not recognize('abaaababab')
#
# assert recognize('')
# assert recognize('a')
# assert recognize('abbbbaa')