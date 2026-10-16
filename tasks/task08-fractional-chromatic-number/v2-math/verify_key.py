"""Verification of the answer key: the fractional chromatic number of the 20-vertex 4-regular planar graph in the
figure is 35/11.

Self-contained, python3 standard library only (numpy and scipy are used for two optional extra checks when they
are installed, and skipped otherwise).  Run: python3 verify_key.py

  (1) every independent set of the graph is enumerated (backtracking over vertices, bitmasks): 2456 independent
      sets including the empty set, 212 maximal, independence number 7, clique number 3 (twelve triangles, no K4),
      so n/alpha = 20/7 and omega = 3;
  (2) the chromatic number is 4 (no proper 3-colouring, an explicit 4-colouring);
  (3) lower-bound certificate: the vertex weighting w with w = 1/11 on vertices 2, 3, 4, 17, 20 and w = 2/11 on the
      other fifteen vertices has total 35/11, and every independent set has weight at most 1, so every fractional
      colouring has weight at least 35/11 (weak LP duality, written out in the notes);
  (4) upper-bound certificate: seventeen independent sets with weights k/11 cover every vertex with total weight
      at least 1 and have total weight 35/11; equivalently a 35:11-colouring is written out;
  (5) the linear programme is solved twice more: the dual (maximum weight of a fractional clique) by an exact
      rational tableau simplex written here with the standard library, and the primal numerically by scipy's
      HiGHS solver when scipy is installed; both give 35/11;
  (6) the wrong routes: n/alpha = 20/7, omega = 3, chi = 4; the best ratio |S|/alpha(G[S]) over all induced
      subgraphs is 19/6 (delete vertex 2 or vertex 3; computed exactly over all 2^20 subsets with numpy when
      numpy is installed, and over all subsets of size at least 17 or at most 6 otherwise); the smallest 2-fold
      colouring uses 7 colours (weight 7/2), by a direct k:d-colouring search.
"""
import itertools
from fractions import Fraction as F

EDGES = [(1, 2), (1, 3), (1, 5), (1, 6), (2, 4), (2, 6), (2, 9), (3, 4), (3, 11), (3, 15), (4, 17), (4, 20), (5, 6),
         (5, 7), (5, 8), (6, 10), (7, 8), (7, 11), (7, 12), (8, 12), (8, 18), (9, 10), (9, 16), (9, 17), (10, 16),
         (10, 18), (11, 12), (11, 13), (12, 13), (13, 14), (13, 18), (14, 15), (14, 18), (14, 19), (15, 19), (15, 20),
         (16, 17), (16, 19), (17, 20), (19, 20)]
V = list(range(1, 21)); n = 20
adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
assert len(EDGES) == 40 and all(len(adj[v]) == 4 for v in V)
print("vertices:", n, "edges:", len(EDGES), "4-regular:", all(len(adj[v]) == 4 for v in V))

# ---------- (1) independent sets ----------
bit = {v: 1 << (v - 1) for v in V}
nbmask = {v: sum(bit[u] for u in adj[v]) for v in V}
IND = []
def enum(i, cur, blocked):
    if i == n + 1: IND.append(cur); return
    v = V[i - 1]
    enum(i + 1, cur, blocked)
    if not (blocked & bit[v]): enum(i + 1, cur | bit[v], blocked | nbmask[v])
enum(1, 0, 0)
def members(mask): return [v for v in V if mask & bit[v]]
def is_maximal(mask):
    cover = mask
    for v in members(mask): cover |= nbmask[v]
    return cover == (1 << n) - 1
MAXIMAL = [m for m in IND if is_maximal(m)]
alpha = max(bin(m).count("1") for m in IND)
triangles = [c for c in itertools.combinations(V, 3) if all(b in adj[a] for a, b in itertools.combinations(c, 2))]
k4 = [c for c in itertools.combinations(V, 4) if all(b in adj[a] for a, b in itertools.combinations(c, 2))]
print(f"independent sets (with the empty set): {len(IND)}, maximal: {len(MAXIMAL)}, alpha = {alpha}, n/alpha = {F(n, alpha)}")
print("triangles:", [list(t) for t in triangles], "; K4 subgraphs:", len(k4), "; omega = 3")
assert len(IND) == 2456 and len(MAXIMAL) == 212 and alpha == 7 and len(triangles) == 12 and not k4
print("maximal independent sets:", [members(m) for m in MAXIMAL])

# ---------- (2) chromatic number ----------
def colourable(k):
    col = {}
    order = sorted(V, key=lambda v: -len(adj[v]))
    def rec(i):
        if i == len(order): return True
        v = order[i]
        for c in range(k):
            if all(col.get(u) != c for u in adj[v]):
                col[v] = c
                if rec(i + 1): return True
                del col[v]
        return False
    return rec(0), dict(col)
ok3, _ = colourable(3); ok4, col4 = colourable(4)
print("proper 3-colouring exists:", ok3, "; 4-colouring:", {v: col4[v] + 1 for v in V})
assert not ok3 and ok4

# ---------- (3) lower bound: fractional clique ----------
w = {v: F(2, 11) for v in V}
for v in (2, 3, 4, 17, 20): w[v] = F(1, 11)
total_w = sum(w.values())
def weight(mask): return sum(w[v] for v in members(mask))
worst = max(weight(m) for m in IND)
print(f"fractional clique: total weight {total_w}, largest weight of an independent set {worst}")
assert total_w == F(35, 11) and worst == 1
tight = [members(m) for m in MAXIMAL if weight(m) == 1]
print(f"weight of every maximal independent set (set: weight):", [(members(m), str(weight(m))) for m in MAXIMAL])
print(f"{len(tight)} maximal independent sets have weight exactly 1")
print("CHECK 3: every fractional colouring has weight at least 35/11")

# ---------- (4) upper bound: fractional colouring ----------
COLOURING = [([1, 7, 10, 13, 15, 17], F(5, 11)), ([1, 8, 10, 13, 17, 19], F(2, 11)), ([1, 8, 10, 11, 14, 20], F(2, 11)),
             ([1, 4, 9, 11, 15, 18], F(2, 11)), ([2, 3, 5, 12, 17, 18, 19], F(2, 11)), ([2, 3, 5, 12, 16, 18, 20], F(2, 11)),
             ([2, 3, 5, 12, 14, 16, 20], F(4, 11)), ([2, 3, 7, 10, 13, 17, 19], F(2, 11)), ([2, 5, 12, 15, 16, 18], F(1, 11)),
             ([3, 6, 7, 9, 18, 19], F(1, 11)), ([4, 5, 9, 12, 18, 19], F(2, 11)), ([6, 8, 9, 11, 14, 20], F(2, 11)),
             ([6, 8, 11, 14, 16, 20], F(1, 11)), ([4, 6, 8, 9, 11, 19], F(2, 11)), ([4, 6, 8, 9, 11, 14], F(2, 11)),
             ([4, 6, 7, 15, 16, 18], F(1, 11)), ([4, 6, 7, 13, 15, 16], F(2, 11))]
for S, x in COLOURING:
    assert all(b not in adj[a] for a, b in itertools.combinations(S, 2)), S
cover = {v: sum(x for S, x in COLOURING if v in S) for v in V}
total_x = sum(x for S, x in COLOURING)
print(f"fractional colouring: total weight {total_x}, coverage {dict((v, str(cover[v])) for v in V)}")
assert total_x == F(35, 11) and all(cover[v] >= 1 for v in V)
multiset = [S for S, x in COLOURING for _ in range(int(x * 11))]
assert len(multiset) == 35 and all(sum(v in S for S in multiset) >= 11 for v in V)
print("35:11-colouring (35 independent sets, every vertex in at least 11):", multiset)
print("CHECK 4: a fractional colouring of weight 35/11 exists; with CHECK 3 the fractional chromatic number is 35/11")

# ---------- (5) LP solves ----------
def exact_simplex_dual():
    """Maximise sum(y_v) subject to sum(y_v : v in S) <= 1 for every maximal independent set S and y >= 0,
    in exact rational arithmetic (tableau simplex, Bland's rule)."""
    m, k = len(MAXIMAL), n
    T = [[F(1) if (S & bit[V[j]]) else F(0) for j in range(k)] + [F(1) if i == r else F(0) for i in range(m)] + [F(1)]
         for r, S in enumerate(MAXIMAL)]
    z = [F(-1)] * k + [F(0)] * m + [F(0)]
    basis = [k + r for r in range(m)]
    while True:
        enter = next((j for j in range(k + m) if z[j] < 0), None)
        if enter is None: break
        rows = [(T[r][-1] / T[r][enter], r) for r in range(m) if T[r][enter] > 0]
        ratio = min(t for t, _ in rows); leave = min(basis[r] for t, r in rows if t == ratio)
        r0 = basis.index(leave); piv = T[r0][enter]
        T[r0] = [t / piv for t in T[r0]]
        for r in range(m):
            if r != r0 and T[r][enter] != 0:
                f = T[r][enter]; T[r] = [a - f * b for a, b in zip(T[r], T[r0])]
        f = z[enter]; z = [a - f * b for a, b in zip(z, T[r0])]
        basis[r0] = enter
    y = {V[j]: F(0) for j in range(k)}
    for r, bj in enumerate(basis):
        if bj < k: y[V[bj]] = T[r][-1]
    return z[-1], y
val, y = exact_simplex_dual()
print("exact rational simplex (standard library): fractional clique number =", val, "; an optimal weighting:", {v: str(y[v]) for v in V if y[v]})
assert val == F(35, 11) and all(weight(m) <= 1 for m in IND) and sum(y.values()) == F(35, 11)
try:
    import numpy as np
    from scipy.optimize import linprog
    A = np.array([[1.0 if (S & bit[v]) else 0.0 for S in MAXIMAL] for v in V])
    res = linprog(np.ones(len(MAXIMAL)), A_ub=-A, b_ub=-np.ones(n), bounds=(0, None), method="highs")
    print(f"scipy HiGHS (primal LP over the {len(MAXIMAL)} maximal independent sets): minimum weight = {res.fun:.10f} (35/11 = {35/11:.10f})")
    assert abs(res.fun - 35 / 11) < 1e-9
except ImportError:
    print("scipy not installed, numerical LP skipped")
print("CHECK 5: two independent LP solutions give 35/11")

# ---------- (6) wrong routes ----------
try:
    import numpy as np
    allS = np.arange(1, 1 << n, dtype=np.int64)
    def popcount(a):
        a = a - ((a >> 1) & 0x5555555555555555)
        a = (a & 0x3333333333333333) + ((a >> 2) & 0x3333333333333333)
        a = (a + (a >> 4)) & 0x0f0f0f0f0f0f0f0f
        return (a * 0x0101010101010101 >> 56) & 0xff
    best_alpha = np.zeros(len(allS), dtype=np.int64)
    for mk in MAXIMAL: best_alpha = np.maximum(best_alpha, popcount(allS & mk))
    sizes = popcount(allS); ratios = sizes / best_alpha; i = int(np.argmax(ratios))
    hall = F(int(sizes[i]), int(best_alpha[i]))
    print(f"best induced-subgraph ratio |S|/alpha(G[S]) over all 2^20 - 1 subsets (numpy): {hall}, attained for instance by S = {members(int(allS[i]))}")
except ImportError:
    best = F(0); bestS = None
    for r in list(range(17, 21)) + list(range(1, 7)):
        for S in itertools.combinations(V, r):
            Smask = sum(bit[v] for v in S); aS = max(bin(m & Smask).count("1") for m in MAXIMAL)
            if F(r, aS) > best: best, bestS = F(r, aS), S
    hall = best
    print(f"best induced-subgraph ratio over all subsets of size 17 to 20 and 1 to 6 (no numpy): {hall}, for instance S = {bestS}")
assert hall == F(19, 6)
for v in V:
    a_minus = max(bin(m & ~bit[v]).count("1") for m in MAXIMAL)
    if a_minus == 6: print(f"   deleting vertex {v} leaves a 19-vertex subgraph with independence number 6: bound 19/6")

def kfold(k, d):
    """Is there a k:d-colouring (each vertex a d-subset of k colours, adjacent vertices disjoint)?  Colour sets are
    bitmasks; vertex 1 gets colours {0, ..., d-1} and new colours are introduced in index order (symmetry breaking)."""
    subsets = [sum(1 << c for c in S) for S in itertools.combinations(range(k), d)]
    order = [1]; seen = {1}; frontier = [1]
    while frontier:
        nxt = []
        for u in frontier:
            for v in sorted(adj[u], key=lambda x: -len(adj[x] & seen)):
                if v not in seen: seen.add(v); order.append(v); nxt.append(v)
        frontier = nxt
    assign = {1: subsets[0]}
    def rec(i, used):
        if i == len(order): return True
        v = order[i]; forbidden = 0
        for u in adj[v]:
            if u in assign: forbidden |= assign[u]
        maxc = used.bit_length()
        for S in subsets:
            if S & forbidden: continue
            new = S & ~used
            if new and new != (((1 << bin(new).count("1")) - 1) << maxc): continue
            assign[v] = S
            if rec(i + 1, used | S): return True
            del assign[v]
        return False
    found = rec(1, subsets[0])
    return found, ({v: sorted(c for c in range(k) if assign[v] >> c & 1) for v in V} if found else None)
results = {}
for k, d in ((3, 1), (4, 1), (6, 2), (7, 2)):
    found, col = kfold(k, d); results[(k, d)] = found
    print(f"{k}:{d}-colouring exists: {found}" + (f"; one such colouring (vertex: colour set): {col}" if found else ""))
assert not results[(3, 1)] and results[(4, 1)] and not results[(6, 2)] and results[(7, 2)]
print("chromatic number 4 (again, by the 1-fold search); 2-fold chromatic number 7, so the best 2-fold colouring has weight 7/2")
print("ALL CHECKS PASSED. Fractional chromatic number 35/11; n/alpha = 20/7, omega = 3, best induced-subgraph ratio 19/6, chi = 4.")
