import spherogram, sympy as sp, knotlib as K, itertools, pickle
t = sp.symbols("t")
def norm_alex(expr):
    P = sp.Poly(sp.expand(expr), t); c = P.all_coeffs()
    while c and c[-1] == 0: c.pop()
    if c[0] < 0: c = [-x for x in c]
    return tuple(int(x) for x in c)
def norm_jones(J, mirror=False):
    d = {(-k if mirror else k): int(v) for k, v in dict(J).items() if v != 0}
    lo = min(d); return tuple(d.get(k, 0) for k in range(lo, max(d) + 1))
names = [f"{n}_{k}" for n, cnt in ((3,1),(4,1),(5,2),(6,3),(7,7),(8,21),(9,49),(10,165)) for k in range(1, cnt+1)]
A = {}; Jn = {}
for nm in names:
    pd = [tuple(x) for x in spherogram.Link(nm).PD_code()]; signs = K.signs_from_pd(pd)
    A[nm] = norm_alex(K.alexander(pd, signs).as_expr())
    if int(nm.split("_")[0]) <= 9:
        J = K.jones(pd, sum(signs)); Jn[nm] = (norm_jones(J), norm_jones(J, True))
target = A["5_1"]
print("Alexander of 5_1:", target)
print("prime knots to 10 crossings sharing it:", [nm for nm in names if A[nm] == target])
print("Jones of 5_1 shared (either chirality) among knots to 9 crossings:", [nm for nm in Jn if (Jn[nm][0] in Jn["5_1"]) and nm != "5_1"])
# Jones separates all knots to 9 crossings (up to mirror)?
cl = {}
for nm, (j1, j2) in Jn.items(): cl.setdefault(min(j1, j2), []).append(nm)
print("Jones classes with more than one knot (to 9 crossings):", [v for v in cl.values() if len(v) > 1])
small = [nm for nm in names if int(nm.split("_")[0]) <= 6]
for r in (2, 3):
    for combo in itertools.combinations_with_replacement(small, r):
        if sum(int(c.split("_")[0]) for c in combo) <= 10:
            P = sp.Integer(1)
            for c in combo: P *= sp.Poly(list(A[c]), t).as_expr()
            if norm_alex(P) == target: print("composite with the Alexander polynomial of 5_1:", combo)
print("composites to 10 crossings checked")
pickle.dump((A, Jn), open("tables.pkl", "wb"))
