"""Pairs of knots to 10 crossings with equal Jones polynomial (up to mirror): Alexander equality, signatures,
determinant and Fox colouring ranks."""
import spherogram, numpy as np, knotlib as K, pickle, itertools, sympy as sp
t = sp.symbols("t")
A, Jn = pickle.load(open("tables.pkl", "rb"))
def norm_jones(J, mirror=False):
    d = {(-k if mirror else k): int(v) for k, v in dict(J).items() if v != 0}
    lo = min(d); return tuple(d.get(k, 0) for k in range(lo, max(d) + 1))
names = [f"{n}_{k}" for n, cnt in ((3,1),(4,1),(5,2),(6,3),(7,7),(8,21),(9,49),(10,165)) for k in range(1, cnt+1)]
data = {}
for nm in names:
    L = spherogram.Link(nm); pd = [tuple(x) for x in L.PD_code()]; signs = K.signs_from_pd(pd)
    if nm in Jn: j = Jn[nm]
    else:
        J = K.jones(pd, sum(signs)); j = (norm_jones(J), norm_jones(J, True))
    V = np.array(L.seifert_matrix(), float); ev = np.linalg.eigvalsh(V + V.T); sig = int((ev > 1e-9).sum() - (ev < -1e-9).sum())
    det = K.determinant(pd)
    cols = {p: K.colorings(pd, p) for p in (3, 5, 7) if det % p == 0}
    data[nm] = dict(j=j, sig=sig, det=det, cols=cols, A=A[nm])
    print(nm, flush=True) if nm.endswith("_1") else None
pickle.dump(data, open("tables_jones.pkl", "wb"))
cl = {}
for nm, d in data.items(): cl.setdefault(min(d["j"]), []).append(nm)
print("Jones collision classes to 10 crossings:")
for key, v in cl.items():
    if len(v) > 1:
        print(v, "| Alexander equal:", len(set(data[x]["A"] for x in v)) == 1, "| signatures", [data[x]["sig"] for x in v], "| det", [data[x]["det"] for x in v], "| colourings", [data[x]["cols"] for x in v])
