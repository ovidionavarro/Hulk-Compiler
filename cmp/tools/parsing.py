import zlib, base64
from itertools import islice
from cmp.utils import ContainerSet


def compute_local_first(firsts, alpha):
    f = firsts
    p = alpha
    D = ContainerSet()
    try:
        P = p.IsEpsilon
    except:
        P = False
    if P:
        D.set_epsilon()
    else:
        for G in p:
            M = f[G]
            D.update(M)
            if not M.contains_epsilon:
                break
        else:
            D.set_epsilon()
    return D


def compute_firsts(G):
    f = {}
    E = True
    for b in G.terminals:
        f[b] = ContainerSet(b)
    for t in G.nonTerminals:
        f[t] = ContainerSet()
    while E:
        E = False
        for O in G.Productions:
            X = O.Left
            p = O.Right
            A = f[X]
            try:
                D = f[p]
            except:
                D = f[p] = ContainerSet()
            J = compute_local_first(f, p)
            E |= D.hard_update(J)
            E |= A.hard_update(J)
    return f


def compute_follows(G, firsts):
    f = firsts
    q = {}
    E = True
    e = {}
    for t in G.nonTerminals:
        q[t] = ContainerSet()
    q[G.startSymbol] = ContainerSet(G.EOF)
    while E:
        E = False
        for O in G.Productions:
            X = O.Left
            p = O.Right
            R = q[X]
            for i, sy in enumerate(p):
                if sy.IsNonTerminal:
                    Q = q[sy]
                    try:
                        fb = e[p, i]
                    except:
                        fb = e[p, i] = compute_local_first(f, islice(p, i + 1, None))
                    E |= Q.update(fb)
                    if fb.contains_epsilon:
                        E |= Q.update(R)
    return q


def build_parsing_table(G, firsts, follows):
    f = firsts
    ff = follows
    M = {}
    for a in G.Productions:
        X = a.Left
        P = a.Right
        for e in f[P]:
            try:
                M[X, e].append(a)
            except:
                M[X, e] = [a]
        if f[P].contains_epsilon:
            for e in ff[X]:
                try:
                    M[X, e].append(a)
                except:
                    M[X, e] = [a]
    return M


def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    fi = firsts
    fo = follows
    if M is None:
        if fi is None:
            fi = compute_firsts(G)
        if fo is None:
            fo = compute_follows(G, fi)
        M = build_parsing_table(G, fi, fo)

    def m(w):
        V = [G.EOF, G.startSymbol]
        mm = 0
        z = []
        while True:
            g = V.pop()
            a = w[mm]
            if g.IsTerminal:
                if g == a:
                    if g == G.EOF:
                        break
                    else:
                        mm += 1
                else:
                    print("Error. Aborting...")
                    return None
            else:
                try:
                    P = M[g, a][0]
                    for i in range(len(P.Right) - 1, -1, -1):
                        V.append(P.Right[i])
                    z.append(P)
                except:
                    print("Error. Aborting...")
                    return None
        return z

    return m


deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo


def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)

    def updated(tokens):
        return parser([t.token_type for t in tokens])

    return updated


exec(zlib.decompress(base64.b64decode(
    'eJx9U8GO2jAQvfMVZi9JtCFarqiuVLUsRUilWranCEUmGcBaY0e2s3TV7b/X9iQhpaiXxJ4Zv3nzZqYUzBiyOfK9fYKqKeE70wb0bEQ2X5ePzzQKv2hEnuZffnye0wj/zrBe0Wi9cocK9qQouOS2KGIDYp8u0lfQO2WAPjJhIHFoxDuyBV10xy6i/XdmVlquJP31uzMclFWDa7FruKiK2rHk8lBYthMQJy2JWz7/KhDQjBsg35RdnmoBJ5AWqrnWSvfPi5IJ0dVwTg9gC+OFKXRQZliMZeULzR+27lw22ihNH9xRNbZuLM29WdWgma/F4P185ALIs27AA3gECzTg5JOpDyBCqRd2BFbRc46gwcz3fwk2qzWXNg4v0+jDZDJ5f3efj1HavZptE3wXhyRpj5tIZQmXQ6EDF4KQ/4QnA+ddkCojn3ZKW6dulmV36NdgGy2dsNI3kSBuatmBDvLkV9hdZW27MTSMGjK6qJexugZZxZcITBsEuKd5D+lTBti2I/d06m8grtPgBP83D4ZgImxq53ZJ0BxS7lT1Rp0pWPZKE/N22inhRdbgGmagin1MgtmQdFarOkYQ4pYPtB3aHcmA0RV5PSUkLES/Gq2wvaa9LoGfj9jeVmG9mo1uUbrJKOxu5mzabi7s2lABEsfRRU6HI4HK+Tb7wbteJ8fJQIwx6aUPCdI1uCbt1s5/llB7dxwt5SsTvGqLGY/HUTL6AyImjec=')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

exec(zlib.decompress(base64.b64decode(
    'eJyFVltP4zoQfu+v8D41OcfHWl6RLJ0KekEgqLg+dKtiGrf1ktiR7RS6iP9+ZuykSYE9ywOKLzPzzTffjLuypiDLomSVV7kjqiiN9eTEaC+UlvZG+t6queKNyR0rhXVKr5urS1OUlZeLlbLOO9osc7MUedxsHZQ7PFa5tI31mZdFL5MrIl9LobMkozo97pEdz9ilfPU3u+LJ5D2iVmRHlCOXRktiLNHGkx07c7C+lbZQWuRgRaz0ldWzeY/c824KSdojKzAbEqVJxqZWbpV8STASeeZfQE40HYINuWdVmQkvk2dYCeckQMbY92wZ3buFLJ3Kje41wTGjpLQmo9/pfYpRcYGBdwy/qqVXRrt5yBpDW+lcMkAsOX97j0DD/QHCWwETJ1J7aTEJ4u0OdyG/fLaCPIG3pSw9OZe7obXGhkM84vfcxcTbJDKWG/MsNlJkLm0AvwXArx1sFBbGUTR/TkMGr/QZAeVMwV2XpO8RfG5cZYE3e5QMYt0mh7T/NYAwV/zWVrJHXjZQeHKFCK/4SOQO9oj4VKc2/0lIRjDQgQRpdBSSBh+TJi+xT6YldJIGjGvjTQ1wSqNEOYqI/qycXzxLq2UewSD8usKdMxRbNEP5YemDdf8xbj6SAu6SJ4lF3qpMZijVx0/OH/s9MuDQB7+kRl6jugPzaVtvtO3qnvNpm1k47SKT4PdDDSKotG04UXlTCC+adrvxwBctqhyaHThfQGw4BnEFsp4qlWeLi+ujRW1ndDLu8JJLWDPnha0BdgWdcn5E+2MrikLYPS2iWheo3gwI0PxwVoBv2JyN2fBqND/UQdiD0zP+23iz7yB/wwOHZ9BrrbR5NKcoE98hfWbmKUq0y5kHNQHFPBCTtHcnKUXVwtmWzzxE2vA3f2zfGxlvUZsXfAudUgbV3vHN7GJey3eK5RwzX48m9/eY6XZSuaDrQxwXAQcha75X7AQU2xVSjYegDlCI6+CG4CBSGhusnQ7kBdCsEc2X8+FD7HUdu7b6Hy7gb8tEWWI7rsP6joksW3grtFNYlmTKLkUh6QuyysC6lVjyhexaeds/PDM3G7Xy1xKqL6dwAopd5iBLAmqN6+TTDVQuynoRdV07XHjxlMvkIQz/MX9gYzZoRFqrN2nStfzrlqjLrOgpFlrqqpAWOQshQ4Ee2FbaJ+PkcWmV9omi/R++D//0D0/67KdROnHeJq9xvqKbU1S6lyle6gdyT5nKXrmqo4VYsYCShyP83E+P2jwWOAySMxfZwBaJ26SE16TtobgHd0t2IVeeHzZbbQKpLKxcK4clfGAiPhGJpLFHKexdnVOcimlUSBhMjfG+G7pvT3P4W9fT4PZ6eHp3MqRl7bfjdvrh5wEJnXPK1qDWKMC04SfkNwUuur8T/hz7ZnI2uqXrr1I6NMR2rc2wI/7FIqhlIf3GZLX89rdHFIgKEqkH6nloZGBnhO/MaHY+5/yS9oOS/4nFw4P41WxAw69ytfTfvn2DoRqtLnv/ATLgLos=')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
