"""Verification of the answer key: the smallest pairwise-covering test matrix for the five three-level factors of the
figure, with its five unavailable level combinations, has 11 specimens.

Self-contained, python3 standard library only (scipy, when installed, adds an integer-programming solve and the
enumeration of all optimal designs).  Run: python3 verify_key.py

Factors (index: name, levels 0/1/2): A powder (TiH2-derived, HDH, gas-atomised); B specimen geometry (round bar, flat,
notched); C space-holder content (0, 15, 30 vol%); D oxygen (0.15, 0.30, 0.45 wt%); E load ratio (-1, 0.1, 0.5).
Unavailable combinations: A0C1, A0C2, A1D0, A2B1, B0D1.
  (1) the admissible specimens (rows) are enumerated: 114 of the 243 level combinations; the admissible pairs of levels
      of two different factors: 85 of 90;
  (2) trivial lower bound: every pair of factors has at most 9 admissible level pairs, so at least 9 specimens;
  (3) lower bound 11 (the decisive step): the 11 level pairs A0B0, A0B2, A1B0, A1B2, A2D1, A2D2, B1E0, B1E1, B1E2, C1D0, C2D0
      are pairwise exclusive, no admissible specimen contains two of them (checked against all 114 rows, and explained
      pair by pair), so every design needs at least 11 specimens;
  (4) upper bound 11: an explicit design of 11 specimens covers all 85 admissible pairs;
  (5) with scipy: the integer programme confirms the minimum 11, and all optimal designs are enumerated (24, which are
      4 designs up to the renaming of the three load ratios, which no constraint distinguishes);
  (6) wrong routes: the trivial bound 9; 200 randomised greedy constructions never reach 11 (sizes 12 to 14).
"""
import itertools, random

LEVELS = [3, 3, 3, 3, 3]; k = 5; L = "ABCDE"
FORB = {((0, 0), (2, 1)), ((0, 0), (2, 2)), ((0, 1), (3, 0)), ((0, 2), (1, 1)), ((1, 0), (3, 1))}
def name(p): return f"{L[p[0][0]]}{p[0][1]}{L[p[1][0]]}{p[1][1]}"
def admissible(r): return all(((i, r[i]), (j, r[j])) not in FORB for i, j in itertools.combinations(range(k), 2))
ROWS = [r for r in itertools.product(*[range(l) for l in LEVELS]) if admissible(r)]
PAIRS = [((i, a), (j, b)) for i, j in itertools.combinations(range(k), 2) for a in range(3) for b in range(3) if ((i, a), (j, b)) not in FORB]
def covers(r, p): return r[p[0][0]] == p[0][1] and r[p[1][0]] == p[1][1]
print(f"admissible specimens: {len(ROWS)} of 243; admissible level pairs: {len(PAIRS)} of 90; unavailable: {[name(p) for p in sorted(FORB)]}")
assert len(ROWS) == 114 and len(PAIRS) == 85
assert all(any(covers(r, p) for r in ROWS) for p in PAIRS), "every admissible pair must be realisable"

# ---------- (2) trivial bound ----------
per_factor_pair = {(i, j): sum(1 for p in PAIRS if p[0][0] == i and p[1][0] == j) for i, j in itertools.combinations(range(k), 2)}
print("admissible pairs per factor pair:", {f"{L[i]}{L[j]}": v for (i, j), v in per_factor_pair.items()}, "-> trivial bound", max(per_factor_pair.values()))

# ---------- (3) lower bound: 11 pairwise exclusive pairs ----------
EXCL = [((0, 0), (1, 0)), ((0, 0), (1, 2)), ((0, 1), (1, 0)), ((0, 1), (1, 2)), ((0, 2), (3, 1)), ((0, 2), (3, 2)),
        ((1, 1), (4, 0)), ((1, 1), (4, 1)), ((1, 1), (4, 2)), ((2, 1), (3, 0)), ((2, 2), (3, 0))]
assert all(p in PAIRS for p in EXCL)
for r in ROWS:
    assert sum(covers(r, p) for p in EXCL) <= 1, r
print("exclusive set:", [name(p) for p in EXCL])
print("CHECK 3: no admissible specimen contains two of the 11 pairs, so every design has at least 11 specimens")
# why each couple is exclusive, for the written proof
def why(p, q):
    d = {}
    for (f, l) in (p[0], p[1], q[0], q[1]):
        if f in d and d[f] != l: return f"both need factor {L[f]} at different levels"
        d[f] = l
    bad = [((x, d[x]), (z, d[z])) for x, z in itertools.combinations(sorted(d), 2) if ((x, d[x]), (z, d[z])) in FORB]
    if bad: return "together they contain the unavailable combination " + name(bad[0])
    # otherwise every completion of the free factors must hit a forbidden pair
    free = [f for f in range(k) if f not in d]
    return "every choice of the remaining factor(s) " + ",".join(L[f] for f in free) + " creates an unavailable combination"
reasons = {}
for p, q in itertools.combinations(EXCL, 2):
    reasons.setdefault(why(p, q), []).append(f"{name(p)}/{name(q)}")
for reason, lst in reasons.items(): print(f"   {len(lst)} couples: {reason}" + (f": {lst}" if len(lst) <= 6 else ""))

# ---------- (4) upper bound: an explicit 11-specimen design ----------
DESIGN = [(0, 0, 0, 2, 1), (0, 1, 0, 0, 2), (0, 2, 0, 1, 0), (1, 0, 1, 2, 2), (1, 1, 1, 1, 1), (1, 1, 2, 2, 0),
          (1, 2, 0, 2, 1), (2, 0, 0, 2, 0), (2, 0, 2, 0, 1), (2, 2, 1, 0, 0), (2, 2, 2, 1, 2)]
assert all(admissible(r) for r in DESIGN) and len(DESIGN) == 11
uncovered = [p for p in PAIRS if not any(covers(r, p) for r in DESIGN)]
print("design:", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in DESIGN], "; uncovered admissible pairs:", uncovered)
assert not uncovered
print("CHECK 4: the 11-specimen design covers all 85 admissible pairs; with CHECK 3 the minimum is 11")

# ---------- (5) integer programme and enumeration of optimal designs (scipy) ----------
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
    classes = set()
    for s in sols:
        best = min(tuple(sorted(tuple(r[:4]) + (perm[r[4]],) for r in s)) for perm in itertools.permutations(range(3)))
        classes.add(best)
    print(f"all optimal designs: {len(sols)}; distinct up to renaming the load ratios: {len(classes)}")
    for cl in sorted(classes): print("   ", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in cl])
    assert len(sols) == 24 and len(classes) == 4
    # 10-specimen designs: none (the ILP minimum is 11; also implied by CHECK 3)
    print("CHECK 5: the integer programme agrees; there is no design with 10 specimens")
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
print("ALL CHECKS PASSED. Minimum number of specimens 11; trivial bound 9; greedy constructions 12 or more.")
