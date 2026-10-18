"""Verification of the answer key: the smallest pairwise-covering test matrix for the six three-level factors of the
figure, with its ten unavailable level combinations, has 11 specimens.

Self-contained, python3 standard library only (scipy, when installed, adds an integer-programming solve and the
enumeration of all optimal programmes).  Run: python3 verify_key.py

Factors (index: name, levels 0/1/2): A powder (TiH2-derived, HDH, gas-atomised); B specimen geometry (round bar, flat,
notched); C space-holder content (0, 15, 30 vol%); D oxygen (0.15, 0.30, 0.45 wt%); E load ratio (-1, 0.1, 0.5);
F environment (laboratory air, Ringer's solution, Ringer's with hydrogen charging).
Unavailable combinations: A0B0, A0C0, A0D2, A0F1, A1B2, B1E0, C0D0, C1E2, D1F0, D2F1.
  (1) the admissible specimens (rows) are enumerated: 223 of the 729 level combinations; the admissible pairs of levels
      of two different factors: 125 of 135;
  (2) trivial lower bound: every pair of factors has at most 9 admissible level pairs, so at least 9 specimens; the best
      set of pairwise incompatible pairs has 10 members, so that route gives only 10;
  (3) lower bound 11 (the decisive step on the proof side): a weighting of 16 admissible level pairs with weights 1/2 and
      1 and total 21/2 under which every admissible specimen carries total weight at most 1 (checked against all 223
      rows), so every programme has at least 21/2, that is at least 11, specimens;
  (4) upper bound 11 (the decisive step on the construction side): an explicit programme of 11 specimens covers all 125
      admissible pairs;
  (5) with scipy: the integer programme confirms the minimum 11 and the enumeration of optimal programmes finds 4, which
      differ only in the environment of one or two specimens (2 programmes up to that choice);
  (6) wrong routes: the trivial bound 9; the best incompatible-pair bound 10; 200 randomised greedy constructions never
      reach 11 (sizes 13 to 17).
"""
import itertools, random
from fractions import Fraction as F

LEVELS = [3] * 6; k = 6; L = "ABCDEF"
FORB = {((0, 0), (1, 0)), ((0, 0), (2, 0)), ((0, 0), (3, 2)), ((0, 0), (5, 1)), ((0, 1), (1, 2)), ((1, 1), (4, 0)),
        ((2, 0), (3, 0)), ((2, 1), (4, 2)), ((3, 1), (5, 0)), ((3, 2), (5, 1))}
def name(p): return f"{L[p[0][0]]}{p[0][1]}{L[p[1][0]]}{p[1][1]}"
def admissible(r): return all(((i, r[i]), (j, r[j])) not in FORB for i, j in itertools.combinations(range(k), 2))
ROWS = [r for r in itertools.product(*[range(l) for l in LEVELS]) if admissible(r)]
PAIRS = [((i, a), (j, b)) for i, j in itertools.combinations(range(k), 2) for a in range(3) for b in range(3) if ((i, a), (j, b)) not in FORB]
def covers(r, p): return r[p[0][0]] == p[0][1] and r[p[1][0]] == p[1][1]
print(f"admissible specimens: {len(ROWS)} of 729; admissible level pairs: {len(PAIRS)} of 135; unavailable: {[name(p) for p in sorted(FORB)]}")
assert len(ROWS) == 223 and len(PAIRS) == 125
assert all(any(covers(r, p) for r in ROWS) for p in PAIRS), "every admissible pair must be realisable"

# ---------- (2) trivial bound and the best incompatible-pair bound ----------
per_factor_pair = {(i, j): sum(1 for p in PAIRS if p[0][0] == i and p[1][0] == j) for i, j in itertools.combinations(range(k), 2)}
print("admissible pairs per factor pair:", {f"{L[i]}{L[j]}": v for (i, j), v in per_factor_pair.items()}, "-> trivial bound", max(per_factor_pair.values()))
conflict = {p: set() for p in PAIRS}
for p, q in itertools.combinations(PAIRS, 2):
    if not any(covers(r, p) and covers(r, q) for r in ROWS): conflict[p].add(q); conflict[q].add(p)
best = [0]
def grow(cands, cur):
    if len(cur) + len(cands) <= best[0]: return
    if not cands: best[0] = max(best[0], len(cur)); return
    for i, p in enumerate(cands):
        grow([q for q in cands[i + 1:] if q in conflict[p]], cur + [p])
grow(PAIRS, [])
print(f"largest set of pairwise incompatible pairs: {best[0]} (so that route proves only {best[0]})")
assert best[0] == 10

# ---------- (3) lower bound 11: a half-integral weighting ----------
W = {((0, 1), (3, 0)): F(1, 2), ((0, 2), (3, 0)): F(1, 2), ((0, 0), (4, 0)): F(1, 2), ((0, 0), (4, 1)): F(1, 2), ((0, 0), (4, 2)): F(1, 2),
     ((2, 1), (3, 1)): F(1, 2), ((2, 1), (3, 2)): F(1), ((2, 2), (3, 1)): F(1, 2), ((2, 2), (3, 2)): F(1),
     ((2, 0), (5, 0)): F(1), ((2, 0), (5, 1)): F(1), ((2, 0), (5, 2)): F(1), ((2, 1), (5, 1)): F(1, 2), ((2, 2), (5, 1)): F(1, 2),
     ((3, 0), (5, 0)): F(1, 2), ((3, 0), (5, 2)): F(1, 2)}
assert all(p in PAIRS for p in W)
total = sum(W.values())
def weight(r): return sum(w for p, w in W.items() if covers(r, p))
worst = max(weight(r) for r in ROWS)
print("weighting (pair: weight):", {name(p): str(w) for p, w in W.items()}, "; total", total)
print(f"largest total weight carried by one admissible specimen: {worst}; number of specimens of weight 1: {sum(1 for r in ROWS if weight(r) == 1)}")
assert total == F(21, 2) and worst == 1
print("CHECK 3: every programme covers each weighted pair at least once and no specimen carries more than weight 1, so it has at least 21/2 specimens, hence at least 11")
print("weight of every admissible specimen:", [("".join(f"{L[i]}{r[i]}" for i in range(k)), str(weight(r))) for r in ROWS])

# ---------- (4) upper bound: an explicit 11-specimen programme ----------
DESIGN = [(0, 1, 2, 0, 2, 2), (0, 2, 1, 0, 0, 0), (0, 2, 2, 1, 1, 2), (1, 0, 0, 1, 0, 2), (1, 0, 1, 0, 1, 2), (1, 0, 2, 2, 2, 0),
          (1, 1, 1, 1, 1, 1), (2, 0, 2, 0, 0, 1), (2, 1, 0, 2, 1, 0), (2, 2, 0, 1, 2, 1), (2, 2, 1, 2, 0, 2)]
assert all(admissible(r) for r in DESIGN) and len(DESIGN) == 11
uncovered = [p for p in PAIRS if not any(covers(r, p) for r in DESIGN)]
print("programme:", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in DESIGN], "; uncovered admissible pairs:", uncovered)
assert not uncovered
print("CHECK 4: the 11-specimen programme covers all 125 admissible pairs; with CHECK 3 the minimum is 11")

# ---------- (5) integer programme and enumeration of optimal programmes (scipy) ----------
try:
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    A = np.array([[1.0 if covers(r, p) else 0.0 for r in ROWS] for p in PAIRS])
    c = np.ones(len(ROWS)); cons = [LinearConstraint(A, lb=1, ub=np.inf)]
    res = milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1))
    N = int(round(res.fun)); print("integer programme (HiGHS): minimum number of specimens =", N); assert N == 11
    sols = []
    while True:
        r2 = milp(c, constraints=cons, integrality=np.ones(len(ROWS)), bounds=Bounds(0, 1))
        if r2.status != 0 or int(round(r2.fun)) > N: break
        sel = [i for i in range(len(ROWS)) if r2.x[i] > 0.5]; sols.append(tuple(sorted(ROWS[i] for i in sel)))
        cut = np.zeros(len(ROWS)); cut[sel] = 1; cons.append(LinearConstraint(cut.reshape(1, -1), lb=-np.inf, ub=N - 1))
    print(f"all optimal programmes: {len(sols)}")
    for s_ in sols: print("   ", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in s_])
    assert len(sols) == 4 and tuple(sorted(DESIGN)) in sols
    print("CHECK 5: the integer programme agrees; four optimal programmes exist, differing only in the environment of one or two specimens")
except ImportError:
    print("scipy not installed: integer programme and enumeration skipped (CHECK 3 and CHECK 4 are complete without them)")

# ---------- (6) wrong routes ----------
sizes = []
for t in range(200):
    rng = random.Random(t); unc = set(range(len(PAIRS))); used = 0
    while unc:
        bestc = max(sum(1 for pi in unc if covers(r, PAIRS[pi])) for r in ROWS)
        cands = [r for r in ROWS if sum(1 for pi in unc if covers(r, PAIRS[pi])) == bestc]
        r = rng.choice(cands); unc -= {pi for pi in unc if covers(r, PAIRS[pi])}; used += 1
    sizes.append(used)
print("randomised greedy construction (200 runs), sizes reached:", {s: sizes.count(s) for s in sorted(set(sizes))})
print("ALL CHECKS PASSED. Minimum number of specimens 11; trivial bound 9; incompatible-pair bound 10; greedy constructions 13 or more.")
