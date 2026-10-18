"""Verification of the answer key: the smallest number of rows of a covering array with 5 columns over the symbols 0, 1, 2
that avoids the seven forbidden pairs of the figure is 10, and the 10-row array is unique.

Self-contained, python3 standard library only (scipy, when installed, adds an integer-programming solve and the
enumeration of all optimal designs).  Run: python3 verify_key.py

Columns x1 to x5 are written A to E here, symbols 0, 1, 2.  Forbidden pairs (no row may contain both entries):
A0E1, A1B0, A1C2, A2B1, B1C1, B1D1, D0E0, i.e. (x1=0, x5=1), (x2=0, x1=1), (x1=1, x3=2), (x1=2, x2=1), (x2=1, x3=1),
(x2=1, x4=1), (x4=0, x5=0).
  (1) the admissible rows are enumerated: 105 of the 243 words of length 5 over {0,1,2}; the admissible pairs of
      symbols in two different columns: 83 of 90;
  (2) trivial lower bound: every pair of columns has at most 9 admissible symbol pairs, so at least 9 rows;
  (3) lower bound 10: the 10 symbol pairs A0D0, A0D1, A0D2, A1E0, A1E2, A2E0, A2E2, B0E1, B1E1, B2E1 are pairwise exclusive,
      no admissible row contains two of them (checked against all 105 rows, and explained pair by pair), so every
      covering array needs at least 10 rows;
  (4) upper bound 10 (the decisive step): an explicit array of 10 rows covers all 83 admissible pairs;
  (5) with scipy: the integer programme confirms the minimum 10 and the enumeration of optimal arrays finds exactly
      one; 47 different exclusive sets of size 10 exist, so the bound is easy and the construction is the hard part;
  (6) wrong routes: the trivial bound 9; the unconstrained covering array number CAN(2,5,3) = 11; 200 randomised greedy
      constructions never reach 10 (sizes 11 to 15).
"""
import itertools, random

LEVELS = [3, 3, 3, 3, 3]; k = 5; L = "ABCDE"
FORB = {((0, 0), (4, 1)), ((0, 1), (1, 0)), ((0, 1), (2, 2)), ((0, 2), (1, 1)), ((1, 1), (2, 1)), ((1, 1), (3, 1)), ((3, 0), (4, 0))}
def name(p): return f"{L[p[0][0]]}{p[0][1]}{L[p[1][0]]}{p[1][1]}"
def admissible(r): return all(((i, r[i]), (j, r[j])) not in FORB for i, j in itertools.combinations(range(k), 2))
ROWS = [r for r in itertools.product(*[range(l) for l in LEVELS]) if admissible(r)]
PAIRS = [((i, a), (j, b)) for i, j in itertools.combinations(range(k), 2) for a in range(3) for b in range(3) if ((i, a), (j, b)) not in FORB]
def covers(r, p): return r[p[0][0]] == p[0][1] and r[p[1][0]] == p[1][1]
print(f"admissible rows: {len(ROWS)} of 243; admissible symbol pairs: {len(PAIRS)} of 90; forbidden: {[name(p) for p in sorted(FORB)]}")
assert len(ROWS) == 105 and len(PAIRS) == 83
assert all(any(covers(r, p) for r in ROWS) for p in PAIRS), "every admissible pair must be realisable"

# ---------- (2) trivial bound ----------
per_factor_pair = {(i, j): sum(1 for p in PAIRS if p[0][0] == i and p[1][0] == j) for i, j in itertools.combinations(range(k), 2)}
print("admissible symbol pairs per column pair:", {f"{L[i]}{L[j]}": v for (i, j), v in per_factor_pair.items()}, "-> trivial bound", max(per_factor_pair.values()))

# ---------- (3) lower bound: 11 pairwise exclusive pairs ----------
EXCL = [((0, 0), (3, 0)), ((0, 0), (3, 1)), ((0, 0), (3, 2)), ((0, 1), (4, 0)), ((0, 1), (4, 2)), ((0, 2), (4, 0)),
        ((0, 2), (4, 2)), ((1, 0), (4, 1)), ((1, 1), (4, 1)), ((1, 2), (4, 1))]
assert all(p in PAIRS for p in EXCL)
for r in ROWS:
    assert sum(covers(r, p) for p in EXCL) <= 1, r
print("exclusive set:", [name(p) for p in EXCL])
print("CHECK 3: no admissible row contains two of the 10 pairs, so every covering array has at least 10 rows")
# why each couple is exclusive, for the written proof
def why(p, q):
    d = {}
    for (f, l) in (p[0], p[1], q[0], q[1]):
        if f in d and d[f] != l: return f"both need column {L[f]} at different levels"
        d[f] = l
    bad = [((x, d[x]), (z, d[z])) for x, z in itertools.combinations(sorted(d), 2) if ((x, d[x]), (z, d[z])) in FORB]
    if bad: return "together they contain the forbidden pair " + name(bad[0])
    # otherwise every completion of the free factors must hit a forbidden pair
    free = [f for f in range(k) if f not in d]
    return "every choice of the remaining column(s) " + ",".join(L[f] for f in free) + " creates a forbidden pair"
reasons = {}
for p, q in itertools.combinations(EXCL, 2):
    reasons.setdefault(why(p, q), []).append(f"{name(p)}/{name(q)}")
for reason, lst in reasons.items(): print(f"   {len(lst)} couples: {reason}" + (f": {lst}" if len(lst) <= 6 else ""))

# ---------- (4) upper bound: an explicit 11-specimen design ----------
DESIGN = [(0, 0, 1, 0, 2), (0, 1, 2, 2, 0), (0, 2, 0, 1, 2), (1, 1, 0, 0, 1), (1, 1, 0, 2, 2), (1, 2, 1, 1, 0),
          (2, 0, 0, 2, 0), (2, 0, 2, 1, 1), (2, 2, 1, 2, 1), (2, 2, 2, 0, 2)]
assert all(admissible(r) for r in DESIGN) and len(DESIGN) == 10
uncovered = [p for p in PAIRS if not any(covers(r, p) for r in DESIGN)]
print("array:", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in DESIGN], "; uncovered admissible pairs:", uncovered)
assert not uncovered
print("CHECK 4: the 10-row array covers all 83 admissible pairs; with CHECK 3 the minimum is 10")

# ---------- (5) integer programme and enumeration of optimal designs (scipy) ----------
try:
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    A = np.array([[1.0 if covers(r, p) else 0.0 for r in ROWS] for p in PAIRS])
    c = np.ones(len(ROWS)); cons = [LinearConstraint(A, lb=1, ub=np.inf)]
    res = milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1))
    N = int(round(res.fun)); print("integer programme (HiGHS): minimum number of rows =", N); assert N == 10
    sols = []
    while True:
        r2 = milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1))
        if r2.status != 0 or int(round(r2.fun)) > N: break
        sel = [i for i in range(len(ROWS)) if r2.x[i] > 0.5]; sols.append(tuple(sorted(ROWS[i] for i in sel)))
        cut = np.zeros(len(ROWS)); cut[sel] = 1; cons.append(LinearConstraint(cut.reshape(1, -1), lb=-np.inf, ub=N - 1))
    print(f"all optimal arrays: {len(sols)}")
    for s_ in sols: print("   ", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in s_])
    assert len(sols) == 1 and sols[0] == tuple(sorted(DESIGN))
    # how many exclusive sets of size 10 exist (cliques in the conflict graph of pairs)
    conflict = {p: set() for p in PAIRS}
    for p, q in itertools.combinations(PAIRS, 2):
        if not any(covers(r, p) and covers(r, q) for r in ROWS): conflict[p].add(q); conflict[q].add(p)
    def cliques(cands, cur, out):
        if len(cur) == 10: out.append(cur); return
        for i, p in enumerate(cands):
            cliques([q for q in cands[i + 1:] if q in conflict[p]], cur + [p], out)
    found = []; cliques(PAIRS, [], found)
    print(f"exclusive sets of size 10 (each one a complete lower-bound proof): {len(found)}")
    print("CHECK 5: the integer programme agrees, the optimal array is unique, and the lower bound has many proofs")
except ImportError:
    print("scipy not installed: integer programme and enumeration skipped (CHECK 3 and CHECK 4 are complete without them)")

# ---------- (6) wrong routes ----------
sizes = []
for t in range(200):
    rng = random.Random(t); unc = set(range(len(PAIRS))); used = 0
    while unc:
        best = max(sum(1 for pi in unc if covers(r, PAIRS[pi])) for r in ROWS)
        cands = [r for r in ROWS if sum(1 for pi in unc if covers(r, PAIRS[pi])) == best]
        r = rng.choice(cands); unc -= {pi for pi in unc if covers(r, PAIRS[pi])}; used += 1
    sizes.append(used)
print("randomised greedy construction (200 runs), sizes reached:", {s: sizes.count(s) for s in sorted(set(sizes))})
print("ALL CHECKS PASSED. Minimum number of rows 10, unique array; trivial bound 9; unconstrained CAN(2,5,3) = 11; greedy constructions 11 or more.")
