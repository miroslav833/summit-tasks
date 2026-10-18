"""Checks answer key for the graph in the figure: rooted pebbling number of the 14-vertex, 20-edge graph with
target r = 1 (vertex with double circle) is 27.

Only Python standard library is used. Run: python3 verify_key.py (it takes about four minutes).

Definitions. Configuration c puts c(v) >= 0 pebbles on each vertex v. One pebbling move takes two pebbles
off vertex u and puts one pebble on a neighbour of u. Target r is reachable from c when there is a sequence
of moves which puts a pebble on r, and pi(G, r) is the smallest k such that r is reachable from each
configuration of k pebbles.

Route A, layer recursion with configurations stored as integers. U_k is the set of configurations of k
  pebbles with no pebble on r, from which r is not reachable, and U_0 = {0}. Adding a pebble never makes
  r unreachable, so each member of U_k is a member of U_{k-1} with one more pebble, and candidate c is in
  U_k when no move from c lands on r and each move from c goes into U_{k-1}. When a neighbour of r holds
  two pebbles, r is reached in one move, so such candidates are skipped. Then pi(G, r) = 1 + max{k : U_k
  nonempty}, and the program prints |U_k| for each k.
Route B, same recursion written again separately, with configurations stored as tuples and without the
  neighbour shortcut. Layer sizes have to be identical to Route A.
Certificates. (i) Direct depth-first search over move sequences checks that each of the 20 configurations
  of 26 pebbles in U_26 is unreachable, and that each configuration made from one of them by adding one
  pebble on a vertex other than r is reachable.
  (ii) Random check: 20,000 random configurations of each size 25, 26 and 27, with at most one pebble on
  each neighbour of r, are tested by direct search and compared with membership in U_k.
  (iii) Configuration C of the solution (fifteen pebbles on 7, seven on 11, three on 14, one on 13): breadth
  first search lists each configuration reachable from C, and none of them has a pebble on 1. Then a
  dynamic programme over the same configurations gives the largest number of moves along chosen edges over
  all move sequences, for C and also for the pocket {11: 7} alone and the left part {7: 15, 14: 3, 13: 1}
  alone.
  (iv) Pile bounds: largest failing configuration where at most one vertex holds two or more pebbles (one
  pile and single pebbles), at most two such vertices, and at most three.
  (v) Trivial bounds n = 14 and 2^ecc(r) = 16, distances from r, degrees.
  (vi) The two facts stated in the question, for the left side S = {2, 5, 7, 8, 9, 12, 13, 14}: each
  configuration with all pebbles on S and at least 20 pebbles reaches r, and each one with at least 19
  pebbles can gather two pebbles on 8 at the same time using moves which land only on S. Also the fact
  used in the solution for the right side T = {3, 4, 6, 10, 11}: each configuration with all pebbles on T
  and at least 9 pebbles reaches r. Each threshold is computed exactly by the same layer recursion,
  restricted to configurations on S or T.
"""
import sys, collections, random, time
sys.setrecursionlimit(1000000)
EDGES = [(1,2),(1,3),(2,5),(2,8),(3,4),(3,6),(3,10),(4,10),(4,11),(5,8),(5,9),(6,8),(6,10),(7,9),(7,12),(8,13),(9,12),(10,11),(12,14),(13,14)]
N = 14; R = 1; V = list(range(1, N + 1))
adj = {v: [] for v in V}
for u, v in EDGES: adj[u].append(v); adj[v].append(u)
for v in V: adj[v].sort()
assert len(EDGES) == 20 and len({tuple(sorted(e)) for e in EDGES}) == 20
print("vertices:", N, " edges:", len(EDGES), " target r =", R)
print("adjacency:", {v: adj[v] for v in V})
print("degrees:", {v: len(adj[v]) for v in V})
def bfs(s):
    d = {s: 0}; q = collections.deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return d
D = bfs(R); ecc = max(D.values())
print("distances from r:", dict(sorted(D.items(), key=lambda x: (x[1], x[0]))), " eccentricity of r:", ecc)
print("trivial lower bounds: n =", N, " 2^ecc =", 2 ** ecc)

# ------------------------------------------------------------ Route A (integers, 5 bits per vertex)
B = {v: 1 << (5 * (v - 1)) for v in V}
def cnt(c, v): return (c >> (5 * (v - 1))) & 31
def enc(cfg): return sum(x << (5 * (v - 1)) for v, x in cfg.items())
def dec(c): return {v: cnt(c, v) for v in V if cnt(c, v)}
NB = set(adj[R]); OTH = [v for v in V if v != R]
def layers_A():
    U = {0}; L = [U]
    while U:
        prev = U; cand = set()
        for c in prev:
            for v in OTH:
                if v in NB and cnt(c, v) >= 1: continue
                cand.add(c + B[v])
        U = set()
        for c in cand:
            stuck = True
            for u in OTH:
                if cnt(c, u) >= 2:
                    base = c - 2 * B[u]
                    for w in adj[u]:
                        if w == R or (base + B[w]) not in prev: stuck = False; break
                    if not stuck: break
            if stuck: U.add(c)
        L.append(U)
    return L
t0 = time.time(); LA = layers_A(); piA = len(LA) - 1
print("\nROUTE A: layer sizes |U_k| for k = 0, 1, ...:", [len(U) for U in LA])
print(f"ROUTE A: pi(G, {R}) = {piA}   ({time.time()-t0:.0f} s)")
assert piA == 27
print("  the 20 unreachable configurations of 26 pebbles:")
for c in sorted(LA[26], key=lambda c: tuple(sorted(dec(c).values(), reverse=True))): print("    ", dec(c))

# ------------------------------------------------------------ Route B (tuples, no shortcut)
def layers_B():
    U = {tuple([0] * N)}; sizes = [1]
    while U:
        prev = U; cand = set()
        for c in prev:
            for v in OTH:
                l = list(c); l[v - 1] += 1; cand.add(tuple(l))
        U = set()
        for c in cand:
            stuck = True
            for u in OTH:
                if c[u - 1] >= 2:
                    for w in adj[u]:
                        if w == R: stuck = False; break
                        l = list(c); l[u - 1] -= 2; l[w - 1] += 1
                        if tuple(l) not in prev: stuck = False; break
                    if not stuck: break
            if stuck: U.add(c)
        sizes.append(len(U))
    return sizes
t0 = time.time(); sB = layers_B()
print("\nROUTE B: layer sizes:", sB, f"  ({time.time()-t0:.0f} s)")
assert sB == [len(U) for U in LA]
print("ROUTE B: identical layer sizes, pi(G, 1) = 27")

# ------------------------------------------------------------ Certificate (i), (ii): direct search
def reach_checker():
    memo = {}
    def ok(c):
        if cnt(c, R) >= 1: return True
        v = memo.get(c)
        if v is not None: return v
        memo[c] = False; res = False
        for u in OTH:
            if cnt(c, u) >= 2:
                base = c - 2 * B[u]
                for w in adj[u]:
                    if ok(base + B[w]): res = True; break
                if res: break
        memo[c] = res; return res
    return ok
ok = reach_checker(); t0 = time.time()
assert all(not ok(c) for c in LA[26])
ext = {c + B[v] for c in LA[26] for v in OTH}
assert all(ok(c) for c in ext)
print(f"\nCERTIFICATE (i): direct search confirms the 20 configurations of 26 pebbles are unreachable and all {len(ext)} one-pebble extensions reach 1   ({time.time()-t0:.0f} s)")
rng = random.Random(2026); t0 = time.time()
for k in (25, 26, 27):
    agree = 0; tested = 0; bad = 0
    while tested < 20000:
        cfg = [0] * N
        for _ in range(k): cfg[rng.choice(OTH) - 1] += 1
        if any(cfg[v - 1] >= 2 for v in NB): continue
        c = sum(x << (5 * i) for i, x in enumerate(cfg)); tested += 1
        inU = (k < len(LA)) and (c in LA[k]); direct = not ok(c)
        if inU == direct: agree += 1
        else: bad += 1
        if direct: bad_ = None
    print(f"CERTIFICATE (ii): size {k}: {tested} random configurations, layer membership and direct search agree on {agree}, disagree on {bad}")
    assert bad == 0
print(f"   ({time.time()-t0:.0f} s)")

# ------------------------------------------------------------ Certificate (iii): the configuration C
C = enc({7: 15, 11: 7, 14: 3, 13: 1})
assert C in LA[26]
seen = {C}; q = collections.deque([C])
while q:
    c = q.popleft()
    for u in OTH:
        if cnt(c, u) >= 2:
            base = c - 2 * B[u]
            for w in adj[u]:
                t = base + B[w]
                if t not in seen: seen.add(t); q.append(t)
mx = {v: max(cnt(c, v) for c in seen) for v in V}
print("\nCERTIFICATE (iii): configurations reachable from C = {7: 15, 11: 7, 14: 3, 13: 1}:", len(seen))
print("  largest number of pebbles ever on each vertex:", mx)
assert mx[R] == 0 and mx[2] <= 1 and mx[3] <= 1
print("  no reachable configuration has a pebble on 1, and none has two pebbles on 2 or on 3")
# how many pebbles can ever cross the key edges, over all move sequences (DP on the DAG of configurations)
import functools
@functools.lru_cache(maxsize=None)
def best(c, key):
    b = 0
    for u in OTH:
        if cnt(c, u) >= 2:
            base = c - 2 * B[u]
            for w in adj[u]:
                gain = 1 if (u, w) in key else 0
                b = max(b, gain + best(base + B[w], key))
    return b
L_out = ((9, 5), (13, 8)); R_out = ((11, 4), (11, 10))
print("  maximum number of moves from the left part {7,9,12,13,14} into {5,8} over all sequences:", best(C, L_out))
print("  maximum number of moves out of 11 over all sequences:", best(C, R_out))
print("  maximum number of pebbles arriving at 2:", best(C, tuple((u, 2) for u in adj[2] if u != R)), " at 3:", best(C, tuple((u, 3) for u in adj[3] if u != R)))
for nm, part in (("pocket {11: 7} alone", {11: 7}), ("left part {7: 15, 14: 3, 13: 1} alone", {7: 15, 14: 3, 13: 1})):
    P = enc(part)
    print(f"  {nm}: most pebbles arriving at 2:", best(P, tuple((u, 2) for u in adj[2] if u != R)), " at 3:", best(P, tuple((u, 3) for u in adj[3] if u != R)), " moves 8->6:", best(P, ((8, 6),)))
print("  for C: moves 8->6 at most", best(C, ((8, 6),)), " moves 6->3 at most", best(C, ((6, 3),)))
print("  maximum number of pebbles arriving at 5:", best(C, tuple((u, 5) for u in adj[5])), " at 8:", best(C, tuple((u, 8) for u in adj[8])), " at 4:", best(C, tuple((u, 4) for u in adj[4])), " at 6:", best(C, tuple((u, 6) for u in adj[6])), " at 10:", best(C, tuple((u, 10) for u in adj[10])))

# ------------------------------------------------------------ Certificate (iv): template bounds
def npiles(c): return sum(1 for v in V if cnt(c, v) >= 2)
T1 = max(k for k, U in enumerate(LA) if any(npiles(c) <= 1 for c in U))
T2 = max(k for k, U in enumerate(LA) if any(npiles(c) <= 2 for c in U))
T3 = max(k for k, U in enumerate(LA) if any(npiles(c) <= 3 for c in U))
print("\nCERTIFICATE (iv): largest unreachable configuration with one pile plus single pebbles has", T1, "pebbles:", [dec(c) for c in LA[T1] if npiles(c) <= 1][:4])
print("  largest unreachable configuration with at most two piles has", T2, "pebbles:", [dec(c) for c in LA[T2] if npiles(c) <= 2])
print("  largest unreachable configuration with at most three piles has", T3, "pebbles")

# ------------------------------------------------------------ Certificate (vi): facts of the question
def maxfail(target, support, banned=()):
    memo = {}
    def unreach(c):
        if cnt(c, target): return False
        if c in memo: return memo[c]
        memo[c] = True; res = True
        for u in V:
            if cnt(c, u) >= 2:
                for w in adj[u]:
                    if w in banned: continue
                    if not unreach(c - 2 * B[u] + B[w]): res = False; break
                if not res: break
        memo[c] = res; return res
    U = {0}; k = 0; last = U
    while U:
        cand = {c + B[v] for c in U for v in support}
        U = {c for c in cand if unreach(c)}
        if U: last = U; k += 1
    return k, sorted(last)
S_LEFT = [2, 5, 7, 8, 9, 12, 13, 14]; T_RIGHT = [3, 4, 6, 10, 11]
kL, lastL = maxfail(R, S_LEFT)
k8, last8 = maxfail(6, S_LEFT, banned=tuple(v for v in V if v not in S_LEFT and v != 6))
kT, lastT = maxfail(R, T_RIGHT)
print("\nCERTIFICATE (vi): left side S alone, largest configuration from which r is not reachable:", kL, "pebbles,", len(lastL), "such configurations")
print("  left side S alone, largest configuration from which two pebbles can not be gathered on 8 (moves landing only on S):", k8, "pebbles:", [dec(c) for c in last8])
print("  right side T alone, largest configuration from which r is not reachable:", kT, "pebbles:", [dec(c) for c in lastT])
assert kL == 19 and k8 == 18 and kT == 8
print("  so: at least 20 pebbles on S reach r, at least 19 pebbles on S gather two pebbles on 8, at least 9 pebbles on T reach r")
print("\nALL CHECKS PASSED: pi(G, 1) = 27.")
