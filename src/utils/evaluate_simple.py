from src.cmp.pycompiler import EOF
def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result


def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes

    # Insert your code here ...
    if body.IsEpsilon:
        n = 1
    else:
        n = len(body._symbols) + 1
    synteticed = [None for i in range(n)]
    inherited = [None for i in range(n)]
    # Anything to do with inherited_value?
    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            if attributes[i]:
                inherited[i] = attributes[i](inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])

    synteticed[0] = attributes[0](inherited, synteticed)
    return synteticed[0]