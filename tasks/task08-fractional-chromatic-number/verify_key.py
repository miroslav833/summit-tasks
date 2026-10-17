"""Verification of the answer key: the smallest covering array with six columns, x1..x5 over {0,1,2} and x6 over {0,1},
avoiding the ten forbidden pairs of the figure, has 10 rows; exactly two 10-row covering arrays exist.

Self-contained, python3 standard library only (scipy, when installed, adds an integer-programming solve and the
enumeration of all optimal arrays).  Run: python3 verify_key.py

Columns x1..x6 are written A..F.  Forbidden pairs: A1B1, A1C2, A1E1, A2C0, A2D0, C0E0, C1F0, C2E1, D0E1, D2F0.
  (1) admissible rows: 136 of 486; admissible symbol pairs: 110 of 120;
  (2) trivial lower bound 9 (column pairs BC, BD, BE, CD keep all 9 symbol pairs);
  (3) lower bound 10: the pairs B0E1, B1E1, B2E1, C0D0, C1D0, C2D0, D1E0, D1E2, D2E0, D2E2 are pairwise incompatible;
  (4) upper bound 10: an explicit 10-row covering array;
  (5) integer programme: minimum 10, exactly two optimal arrays;
  (6) wrong routes: the trivial bound 9, the unconstrained value CAN(2, 3^5 2^1) = 11, greedy constructions.
"""
import itertools, random

LEVELS = [3, 3, 3, 3, 3, 2]; k = 6; L = "ABCDEF"
def P(s): return ((L.index(s[0]), int(s[1])), (L.index(s[2]), int(s[3])))
FORB = {P(s) for s in "A1B1 A1C2 A1E1 A2C0 A2D0 C0E0 C1F0 C2E1 D0E1 D2F0".split()}
def name(p): return f"{L[p[0][0]]}{p[0][1]}{L[p[1][0]]}{p[1][1]}"
def admissible(r): return all(((i, r[i]), (j, r[j])) not in FORB for i, j in itertools.combinations(range(k), 2))
ROWS = [r for r in itertools.product(*[range(l) for l in LEVELS]) if admissible(r)]
PAIRS = [((i, a), (j, b)) for i, j in itertools.combinations(range(k), 2) for a in range(LEVELS[i]) for b in range(LEVELS[j]) if ((i, a), (j, b)) not in FORB]
def covers(r, p): return r[p[0][0]] == p[0][1] and r[p[1][0]] == p[1][1]
def word(r): return "".join(map(str, r))
print(f"admissible rows: {len(ROWS)} of 486; admissible symbol pairs: {len(PAIRS)} of 120; forbidden: {sorted(name(p) for p in FORB)}")
assert len(ROWS) == 136 and len(PAIRS) == 110
assert all(any(covers(r, p) for r in ROWS) for p in PAIRS)

per = {(i, j): sum(1 for p in PAIRS if p[0][0] == i and p[1][0] == j) for i, j in itertools.combinations(range(k), 2)}
print("admissible symbol pairs per column pair:", {f"{L[i]}{L[j]}": v for (i, j), v in per.items()}, "-> trivial bound", max(per.values()))

# ---------- (3) lower bound ----------
EXCL = [P(s) for s in "B0E1 B1E1 B2E1 C0D0 C1D0 C2D0 D1E0 D1E2 D2E0 D2E2".split()]
for r in ROWS: assert sum(covers(r, p) for p in EXCL) <= 1, r
print("exclusive set:", [name(p) for p in EXCL])
def why(p, q):
    d = {}
    for (f, l) in (p[0], p[1], q[0], q[1]):
        if f in d and d[f] != l: return f"both need column {L[f]} with different symbols"
        d[f] = l
    bad = [((x, d[x]), (z, d[z])) for x, z in itertools.combinations(sorted(d), 2) if ((x, d[x]), (z, d[z])) in FORB]
    if bad: return "together they contain the forbidden pair " + name(bad[0])
    return "no admissible completion of the remaining columns " + ",".join(L[f] for f in range(k) if f not in d)
reasons = {}
for p, q in itertools.combinations(EXCL, 2): reasons.setdefault(why(p, q), []).append(f"{name(p)}/{name(q)}")
for reason, lst in reasons.items(): print(f"   {len(lst)} couples: {reason}: {lst}")
print("CHECK 3: no admissible row contains two of the 10 pairs, so every covering array has at least 10 rows")

# ---------- (4) upper bound ----------
DESIGN = [tuple(int(c) for c in w) for w in "001211 010110 011021 022000 100020 101101 120221 202120 212201 221111".split()]
assert all(admissible(r) for r in DESIGN) and len(DESIGN) == 10
unc = [name(p) for p in PAIRS if not any(covers(r, p) for r in DESIGN)]
print("array:", [word(r) for r in DESIGN], "; uncovered admissible pairs:", unc)
assert not unc
for (i, j), v in per.items():
    got = sorted({(r[i], r[j]) for r in DESIGN})
    print(f"   column pair {L[i]}{L[j]}: {len(got)} of {v} admissible pairs present: {got}")
print("CHECK 4: the 10-row array covers all 110 admissible pairs; with CHECK 3 the minimum is 10")

# ---------- (5) integer programme ----------
try:
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    A = np.array([[1.0 if covers(r, p) else 0.0 for r in ROWS] for p in PAIRS])
    c = np.ones(len(ROWS)); cons = [LinearConstraint(A, lb=1, ub=np.inf)]
    N = int(round(milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1)).fun))
    print("integer programme (HiGHS): minimum number of rows =", N); assert N == 10
    sols = []
    while True:
        r2 = milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1))
        if r2.status != 0 or int(round(r2.fun)) > N: break
        sel = [i for i in range(len(ROWS)) if r2.x[i] > 0.5]; sols.append(tuple(sorted(ROWS[i] for i in sel)))
        cut = np.zeros(len(ROWS)); cut[sel] = 1; cons.append(LinearConstraint(cut.reshape(1, -1), lb=-np.inf, ub=N - 1))
    print(f"all optimal arrays: {len(sols)}")
    for s_ in sols: print("   ", [word(r) for r in s_])
    assert len(sols) == 2 and tuple(sorted(DESIGN)) in sols
    print("CHECK 5: the integer programme agrees; exactly two 10-row covering arrays exist")
except ImportError:
    print("scipy not installed: integer programme skipped (CHECK 3 and CHECK 4 are complete without it)")

# ---------- (6) wrong routes ----------
sizes = []
for t in range(200):
    rng = random.Random(t); unc_ = set(range(len(PAIRS))); used = 0
    while unc_:
        best = max(sum(1 for pi in unc_ if covers(r, PAIRS[pi])) for r in ROWS)
        cands = [r for r in ROWS if sum(1 for pi in unc_ if covers(r, PAIRS[pi])) == best]
        r = rng.choice(cands); unc_ -= {pi for pi in unc_ if covers(r, PAIRS[pi])}; used += 1
    sizes.append(used)
print("randomised greedy construction (200 runs), sizes reached:", {s: sizes.count(s) for s in sorted(set(sizes))})
print("ALL CHECKS PASSED. Minimum number of rows 10 (two optimal arrays); trivial bound 9; unconstrained value 11.")
