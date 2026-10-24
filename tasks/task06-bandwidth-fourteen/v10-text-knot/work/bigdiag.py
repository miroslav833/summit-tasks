"""Non-minimal diagrams of 10_132 by random Reidemeister moves (spherogram backtrack), with checks."""
import sys, random, spherogram, knotlib as K, glsig, numpy as np, pickle
sys.setrecursionlimit(10000)
def norm_alex(expr):
    import sympy as sp; t = sp.symbols("t"); P = sp.Poly(sp.expand(expr), t); c = P.all_coeffs()
    while c and c[-1] == 0: c.pop()
    if c[0] < 0: c = [-x for x in c]
    return tuple(int(x) for x in c)
def gauss_from_pd(pd):
    n = len(pd); ev = {}
    for cid, (a, b, c, d) in enumerate(pd):
        s = K.crossing_sign_from_pd((a, b, c, d), 2 * n); ev[a] = (cid, "U", s); ev[d if s == 1 else b] = (cid, "O", s)
    return [ev[e] for e in range(2 * n)]
def r1r2(g):
    """count visible Reidemeister-1 (same crossing at consecutive positions) and R2 pairs (two crossings adjacent twice, same over/under)."""
    n2 = len(g); r1 = sum(1 for k in range(n2) if g[k][0] == g[(k + 1) % n2][0])
    pairs = {}
    for k in range(n2):
        a, b = g[k], g[(k + 1) % n2]
        if a[0] != b[0]: pairs.setdefault(frozenset((a[0], b[0])), []).append((a[1], b[1]))
    r2 = sum(1 for v in pairs.values() if len(v) == 2 and all(x[0] == x[1] for x in v))
    return r1, r2
want = int(sys.argv[1]); out = []
for seed in range(int(sys.argv[2]), int(sys.argv[3])):
    random.seed(seed); L = spherogram.Link("10_132"); L.backtrack(steps=int(sys.argv[4]), prob_type_1=0.25, prob_type_2=0.5)
    pd = [tuple(x) for x in L.PD_code()]; n = len(pd)
    if not (want - 1 <= n <= want + 1): continue
    signs = K.signs_from_pd(pd); g = gauss_from_pd(pd); r1, r2 = r1r2(g)
    al = norm_alex(K.alexander(pd, signs).as_expr()); det = K.determinant(pd)
    sig = glsig.gl_signature(pd, 0)[0]; sig1 = glsig.gl_signature(pd, 1)[0]
    J = K.jones_str(K.jones(pd, sum(signs)))
    print(f"seed {seed}: n={n} writhe={sum(signs)} R1={r1} R2={r2} alexander={al} det={det} sigma={sig},{sig1} jones={J}", flush=True)
    out.append(dict(seed=seed, pd=pd, gauss=g, signs=signs, r1=r1, r2=r2, sigma=sig))
pickle.dump(out, open(f"bigdiag_{want}.pkl", "wb"))
