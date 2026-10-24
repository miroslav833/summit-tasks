"""11-crossing knots whose Alexander polynomial equals that of a knot with at most 10 crossings; signatures."""
import spherogram, numpy as np, knotlib as K, sympy as sp, pickle
t = sp.symbols("t")
def norm_alex(expr):
    P = sp.Poly(sp.expand(expr), t); c = P.all_coeffs()
    while c and c[-1] == 0: c.pop()
    if c[0] < 0: c = [-x for x in c]
    return tuple(int(x) for x in c)
A, Jn = pickle.load(open("tables.pkl", "rb")); byA = {}
for nm, a in A.items(): byA.setdefault(a, []).append(nm)
sigs = {}
def sig_of(L):
    V = np.array(L.seifert_matrix(), float); ev = np.linalg.eigvalsh(V + V.T); return int((ev > 1e-9).sum() - (ev < -1e-9).sum())
hits = []
for nm in [f"K11a{k}" for k in range(1, 368)] + [f"K11n{k}" for k in range(1, 186)]:
    L = spherogram.Link(nm); pd = [tuple(x) for x in L.PD_code()]; a = norm_alex(K.alexander(pd, K.signs_from_pd(pd)).as_expr())
    if a in byA:
        s = sig_of(L); partners = byA[a]; ps = [(p, sig_of(spherogram.Link(p))) for p in partners]
        print(nm, "alexander", a, "det", abs(sum(c * (-1) ** i for i, c in enumerate(a))), "sigma", s, "| partners", ps, flush=True)
        hits.append((nm, pd, a, s, ps))
pickle.dump(hits, open("scan11b.pkl", "wb")); print("done", len(hits))
