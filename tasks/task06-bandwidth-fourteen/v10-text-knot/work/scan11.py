"""11- and 12-crossing knots with the Alexander polynomial of 5_1: signature, Jones, determinant."""
import sys, spherogram, numpy as np, knotlib as K, sympy as sp, pickle
t = sp.symbols("t")
def norm_alex(expr):
    P = sp.Poly(sp.expand(expr), t); c = P.all_coeffs()
    while c and c[-1] == 0: c.pop()
    if c[0] < 0: c = [-x for x in c]
    return tuple(int(x) for x in c)
target = (1, -1, 1, -1, 1); hits = []
names = [f"K11a{k}" for k in range(1, 368)] + [f"K11n{k}" for k in range(1, 186)]
if len(sys.argv) > 1: names = [f"K12a{k}" for k in range(1, 1289)] + [f"K12n{k}" for k in range(1, 889)]
for nm in names:
    try: L = spherogram.Link(nm)
    except Exception as e: print("skip", nm, e, flush=True); continue
    pd = [tuple(x) for x in L.PD_code()]; signs = K.signs_from_pd(pd)
    A = norm_alex(K.alexander(pd, signs).as_expr())
    if A != target: continue
    V = np.array(L.seifert_matrix(), float); ev = np.linalg.eigvalsh(V + V.T); sig = int((ev > 1e-9).sum() - (ev < -1e-9).sum())
    J = K.jones_str(K.jones(pd, sum(signs)))
    print(nm, "crossings", len(pd), "signature", sig, "det", K.determinant(pd), "jones", J, flush=True)
    hits.append((nm, pd, sig, J))
pickle.dump(hits, open("scan11.pkl" if len(sys.argv) == 1 else "scan12.pkl", "wb"))
print("done", len(hits))
