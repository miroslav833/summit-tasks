"""12-crossing diagrams of 10_132 with no Reidemeister I or II move visible in the Gauss code (a type III move is
needed first). Built from the minimal diagram by random moves; kept when spherogram's basic simplify (R1/R2 only)
cannot reduce it while the global simplify returns to 10 crossings."""
import sys, random, spherogram, knotlib as K, glsig, pickle
sys.setrecursionlimit(10000)
def gauss_from_pd(pd):
    n = len(pd); ev = {}
    for cid, (a, b, c, d) in enumerate(pd):
        s = K.crossing_sign_from_pd((a, b, c, d), 2 * n); ev[a] = (cid, "U", s); ev[d if s == 1 else b] = (cid, "O", s)
    return [ev[e] for e in range(2 * n)]
def visible(g):
    n2 = len(g); r1 = sum(1 for k in range(n2) if g[k][0] == g[(k + 1) % n2][0]); pairs = {}
    for k in range(n2):
        a, b = g[k], g[(k + 1) % n2]
        if a[0] != b[0]: pairs.setdefault(frozenset((a[0], b[0])), []).append((a[1], b[1]))
    r2 = sum(1 for v in pairs.values() if len(v) >= 2 and all(x[0] == x[1] for x in v))
    return r1, r2
out = []
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    random.seed(seed); L = spherogram.Link(sys.argv[4] if len(sys.argv) > 4 else "10_132"); L.backtrack(steps=int(sys.argv[3]), prob_type_1=0.0, prob_type_2=0.4)
    pd = [tuple(x) for x in L.PD_code()]; n = len(pd)
    if n not in (int(sys.argv[5]), int(sys.argv[5]) + 1) if len(sys.argv) > 5 else n not in (12, 13): continue
    g = gauss_from_pd(pd); r1, r2 = visible(g)
    if r1 or r2: continue
    Lb = L.copy(); Lb.simplify("basic"); Lg = L.copy(); Lg.simplify("global")
    nb, ng = len(Lb.crossings), len(Lg.crossings)
    sig = glsig.gl_signature(pd, 0)[0]; det = K.determinant(pd); al = K.alexander(pd, K.signs_from_pd(pd)).as_expr()
    print(f"seed {seed}: n={n} basic->{nb} global->{ng} writhe={sum(K.signs_from_pd(pd))} sigma={sig} det={det} alexander={al}", flush=True)
    out.append(dict(seed=seed, pd=pd, n=n, nb=nb, ng=ng))
pickle.dump(out, open(sys.argv[6] if len(sys.argv) > 6 else "hidden.pkl", "wb"))
