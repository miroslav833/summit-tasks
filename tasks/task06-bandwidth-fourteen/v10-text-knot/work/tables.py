"""Collision check: which knots share the Alexander or Jones polynomial of 5_1? Uses spherogram's tables."""
import spherogram, snappy, itertools
def inv(name):
    L = spherogram.Link(name); return L.alexander_polynomial(), L.jones_polynomial(), L.signature(), L.PD_code()
a51, j51, s51, pd51 = inv("5_1"); print("5_1:", a51, "|", j51, "| signature", s51); print("PD 5_1", pd51)
a, j, s, pd = inv("10_132"); print("10_132:", a, "|", j, "| signature", s); print("PD 10_132", pd)
print("same alexander", a == a51, "same jones", j == j51)
names = [f"{n}_{k}" for n, cnt in ((3,1),(4,1),(5,2),(6,3),(7,7),(8,21),(9,49),(10,165)) for k in range(1, cnt+1)]
hitsA = []; hitsJ = []
polys = {}
for nm in names:
    try: L = spherogram.Link(nm)
    except Exception as e: print("skip", nm, e); continue
    A = L.alexander_polynomial(); polys[nm] = A
    if A == a51 or A == a51.subs({A.parent().gen(): 1/A.parent().gen()}) if False else A == a51: hitsA.append(nm)
    if L.jones_polynomial() == j51: hitsJ.append(nm)
print("prime knots to 10 crossings with Alexander of 5_1:", hitsA)
print("prime knots to 10 crossings with Jones of 5_1:", hitsJ)
# composites up to 9 crossings
primes = [nm for nm in names if int(nm.split("_")[0]) <= 6]
for r in (2, 3):
    for combo in itertools.combinations_with_replacement(primes, r):
        if sum(int(c.split("_")[0]) for c in combo) <= 9:
            P = 1
            for c in combo: P = P * polys[c]
            if P == a51: print("composite hit", combo)
print("composites checked")
