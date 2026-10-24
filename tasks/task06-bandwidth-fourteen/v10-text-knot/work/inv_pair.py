import sys, spherogram, sympy as sp, knotlib as K
t = sp.symbols("t")
def norm_alex(expr):
    P = sp.Poly(sp.expand(expr), t); c = P.all_coeffs()
    while c and c[-1] == 0: c.pop()
    if c[0] < 0: c = [-x for x in c]
    return tuple(int(x) for x in c)
def gauss_from_pd(pd):
    n = len(pd); ev = {}
    for cid, (a, b, c, d) in enumerate(pd):
        s = K.crossing_sign_from_pd((a, b, c, d), 2 * n)
        ev[a] = (cid, "U", s)
        over_in = d if s == 1 else b     # over strand runs over_in -> over_out
        ev[over_in] = (cid, "O", s)
    return [ev[e] for e in range(2 * n)]
for nm in ("5_1", "10_132"):
    L = spherogram.Link(nm); pd = [tuple(x) for x in L.PD_code()]
    signs = K.signs_from_pd(pd); wr = sum(signs)
    al = K.alexander(pd, signs); J = K.jones(pd, wr)
    print(nm, "writhe", wr, "signs", signs)
    print("  alexander", norm_alex(al.as_expr() if hasattr(al, "as_expr") else al), "det", K.determinant(pd), "5-col", K.colorings(pd, 5), "3-col", K.colorings(pd, 3))
    print("  jones", K.jones_str(J))
    g = gauss_from_pd(pd); print("  gauss", " ".join(f"{c+1}{o}{'+' if s>0 else '-'}" for c, o, s in g))
    try: print("  faces", len(L.faces()), [len(f) for f in L.faces()])
    except Exception as e: print("  faces fail", e)
