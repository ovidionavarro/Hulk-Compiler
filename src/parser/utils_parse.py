from  src.cmp.utils import ContainerSet
def compute_firsts(grammar):
    """
    Computes the firsts sets for the given grammar

    :param grammar: Grammar
    :return: dict
    """
    firsts = {}
    change = True

    for terminal in grammar.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for non_terminal in grammar.nonTerminals:
        firsts[non_terminal] = ContainerSet()

    while change:
        change = False

        for production in grammar.Productions:
            x = production.Left
            alpha = production.Right

            first_x = firsts[x]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_x.hard_update(local_first)

    return firsts

def compute_local_first(firsts, alpha):
    """
    Computes the local firsts for a given alpha

    :param firsts:
    :param alpha:
    :return: ContainerSet
    """
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha