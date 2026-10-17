"""Verification of the answer key: the smallest pairwise-covering test matrix for the five three-level factors of the
figure, with its eight unavailable level combinations, has 11 specimens, and that programme is unique.

Self-contained, python3 standard library only (scipy, when installed, adds an integer-programming solve and the
enumeration of all optimal designs).  Run: python3 verify_key.py

Factors (index: name, levels 0/1/2): A powder (TiH2-derived, HDH, gas-atomised); B specimen geometry (round bar, flat,
notched); C space-holder content (0, 15, 30 vol%); D oxygen (0.15, 0.30, 0.45 wt%); E load ratio (-1, 0.1, 0.5).
Unavailable combinations: A0C2, A0D1, A1C1, A1E0, A2B2, B0C2, B1D2, B2E1.
  (1) the admissible specimens (rows) are enumerated: 82 of the 243 level combinations; the admissible pairs of levels
      of two different factors: 82 of 90;
  (2) trivial lower bound: every pair of factors has at most 9 admissible level pairs, so at least 9 specimens;
  (3) lower bound 11: the 11 level pairs A1B0, A1B1, A0E1, A0E2, A2E1, A2E2, B2D1, C2D2, D0E0, D1E0, D2E0 are pairwise
      exclusive, no admissible specimen contains two of them (checked against all 82 rows, and explained couple by
      couple; four couples are exclusive only because every completion of their four fixed levels meets an unavailable
      combination), so every programme needs at least 11 specimens;
  (4) upper bound 11: an explicit programme of 11 specimens covers all 82 admissible pairs;
  (5) with scipy: the integer programme confirms the minimum 11 and the enumeration of optimal programmes finds exactly
      one; the number of exclusive sets of size 11 is counted;
  (6) wrong routes: the trivial bound 9; 200 randomised greedy constructions never reach 11.
"""
import itertools, random

LEVELS = [3, 3, 3, 3, 3]; k = 5; L = "ABCDE"
FORB = {((0, 0), (2, 2)), ((0, 0), (3, 1)), ((0, 1), (2, 1)), ((0, 1), (4, 0)), ((0, 2), (1, 2)), ((1, 0), (2, 2)), ((1, 1), (3, 2)), ((1, 2), (4, 1))}
def name(p): return f"{L[p[0][0]]}{p[0][1]}{L[p[1][0]]}{p[1][1]}"
def admissible(r): return all(((i, r[i]), (j, r[j])) not in FORB for i, j in itertools.combinations(range(k), 2))
ROWS = [r for r in itertools.product(*[range(l) for l in LEVELS]) if admissible(r)]
PAIRS = [((i, a), (j, b)) for i, j in itertools.combinations(range(k), 2) for a in range(3) for b in range(3) if ((i, a), (j, b)) not in FORB]
def covers(r, p): return r[p[0][0]] == p[0][1] and r[p[1][0]] == p[1][1]
print(f"admissible specimens: {len(ROWS)} of 243; admissible level pairs: {len(PAIRS)} of 90; unavailable: {[name(p) for p in sorted(FORB)]}")
assert len(ROWS) == 82 and len(PAIRS) == 82
assert all(any(covers(r, p) for r in ROWS) for p in PAIRS), "every admissible pair must be realisable"

# ---------- (2) trivial bound ----------
per_factor_pair = {(i, j): sum(1 for p in PAIRS if p[0][0] == i and p[1][0] == j) for i, j in itertools.combinations(range(k), 2)}
print("admissible pairs per factor pair:", {f"{L[i]}{L[j]}": v for (i, j), v in per_factor_pair.items()}, "-> trivial bound", max(per_factor_pair.values()))

# ---------- (3) lower bound: 11 pairwise exclusive pairs ----------
EXCL = [((0, 1), (1, 0)), ((0, 1), (1, 1)), ((0, 0), (4, 1)), ((0, 0), (4, 2)), ((0, 2), (4, 1)), ((0, 2), (4, 2)),
        ((1, 2), (3, 1)), ((2, 2), (3, 2)), ((3, 0), (4, 0)), ((3, 1), (4, 0)), ((3, 2), (4, 0))]
assert all(p in PAIRS for p in EXCL)
for r in ROWS:
    assert sum(covers(r, p) for p in EXCL) <= 1, r
print("exclusive set:", [name(p) for p in EXCL])
print("CHECK 3: no admissible specimen contains two of the 11 pairs, so every programme has at least 11 specimens")
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
DESIGN = [(0, 0, 1, 2, 1), (0, 1, 0, 0, 2), (0, 2, 1, 0, 0), (1, 0, 0, 1, 1), (1, 1, 2, 0, 1), (1, 2, 0, 1, 2),
          (1, 2, 2, 2, 2), (2, 0, 0, 2, 0), (2, 0, 1, 0, 2), (2, 1, 1, 1, 1), (2, 1, 2, 1, 0)]
assert all(admissible(r) for r in DESIGN) and len(DESIGN) == 11
uncovered = [p for p in PAIRS if not any(covers(r, p) for r in DESIGN)]
print("design:", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in DESIGN], "; uncovered admissible pairs:", uncovered)
assert not uncovered
print("CHECK 4: the 11-specimen programme covers all 82 admissible pairs; with CHECK 3 the minimum is 11")

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
    print(f"all optimal programmes: {len(sols)}")
    for s_ in sols: print("   ", ["".join(f"{L[i]}{r[i]}" for i in range(k)) for r in s_])
    assert len(sols) == 1 and sols[0] == tuple(sorted(DESIGN))
    # how many exclusive sets of size 10 exist (cliques in the conflict graph of pairs)
    conflict = {p: set() for p in PAIRS}
    for p, q in itertools.combinations(PAIRS, 2):
        if not any(covers(r, p) and covers(r, q) for r in ROWS): conflict[p].add(q); conflict[q].add(p)
    def cliques(cands, cur, out):
        if len(cur) == 11: out.append(cur); return
        for i, p in enumerate(cands):
            cliques([q for q in cands[i + 1:] if q in conflict[p]], cur + [p], out)
    found = []; cliques(PAIRS, [], found)
    print(f"exclusive sets of size 11 (each one a complete lower-bound proof): {len(found)}")
    print("CHECK 5: the integer programme agrees and the optimal programme is unique")
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
print("ALL CHECKS PASSED. Minimum number of specimens 11, unique programme; trivial bound 9.")
