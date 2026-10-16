"""Verification of the answer key: the pebbling number of the 13-vertex, 19-edge graph in the figure with
target r = 9 (the double-circled vertex) is 25.

Self-contained, Python standard library only.  Run: python3 verify_key.py   (about 15 minutes)

Definitions.  A configuration c assigns c(v) >= 0 pebbles to each vertex.  A pebbling move removes two
pebbles from a vertex u and adds one pebble to a neighbour of u.  The target r is reachable from c if some
sequence of moves puts a pebble on r.  pi(G, r) is the least k such that every configuration of k pebbles
reaches r.

Route A (layer recursion, integer-encoded configurations).  Let U_k be the set of configurations of k
  pebbles, none on r, from which r is not reachable.  U_0 = {0}.  Adding a pebble never destroys
  reachability, so every member of U_k is a member of U_{k-1} plus one pebble; a candidate c belongs to U_k
  iff no move from c lands on r and every move from c leads into U_{k-1}.  A configuration with two
  pebbles on a neighbour of r reaches r in one move, so candidates with two pebbles on a neighbour of r
  are skipped.  pi(G, r) = 1 + max{k : U_k nonempty}.  Prints |U_k| for every k.
Route B (independent implementation).  The same recursion written separately with tuple-encoded
  configurations and without the neighbour shortcut; the layer sizes must agree exactly.
Certificates.  (i) Direct depth-first search over move sequences: every one of the 28 configurations of 24
  pebbles in U_24 is confirmed unreachable, and every configuration obtained from one of them by adding one
  pebble on a vertex other than r (28 x 12 = 336 configurations of 25 pebbles) is confirmed reachable.
  (ii) Random cross-check: 20,000 random configurations of each size 23, 24, 25 with at most one pebble on
  each neighbour of r are tested by direct search and compared with membership in U_k.
  (iii) The configuration C of the solution (eleven pebbles on 1, eleven on 13, one on 2, one on 10): all
  configurations reachable from C are enumerated by breadth-first search; none has a pebble on 9, and the
  largest number of pebbles ever present on each vertex is printed (never two on 6 or 11).
  (iv) Template bounds: the largest failing configuration with at most one vertex holding two or more
  pebbles (one pile plus single pebbles) and with at most two such vertices.
  (v) The trivial bounds n = 13 and 2^ecc(r) = 16, distances from r, degrees.
"""
import sys, collections, random, time
sys.setrecursionlimit(1000000)
EDGES = [(1,2),(1,3),(2,4),(3,5),(4,5),(4,7),(4,8),(5,6),(5,8),(6,9),(7,8),(7,10),(7,12),(8,11),(8,12),(9,11),(10,12),(10,13),(12,13)]
N = 13; R = 9; V = list(range(1, N + 1))
adj = {v: [] for v in V}
for u, v in EDGES: adj[u].append(v); adj[v].append(u)
for v in V: adj[v].sort()
assert len(EDGES) == 19 and len({tuple(sorted(e)) for e in EDGES}) == 19
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
assert piA == 25
print("  the 28 unreachable configurations of 24 pebbles:")
for c in sorted(LA[24], key=lambda c: tuple(sorted(dec(c).values(), reverse=True))): print("    ", dec(c))

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
print("ROUTE B: identical layer sizes, pi(G, 9) = 25")

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
assert all(not ok(c) for c in LA[24])
ext = {c + B[v] for c in LA[24] for v in OTH}
assert all(ok(c) for c in ext)
print(f"\nCERTIFICATE (i): direct search confirms the 28 configurations of 24 pebbles are unreachable and all {len(ext)} one-pebble extensions reach 9   ({time.time()-t0:.0f} s)")
rng = random.Random(2026); t0 = time.time()
for k in (23, 24, 25):
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
C = enc({1: 11, 13: 11, 2: 1, 10: 1})
assert C in LA[24]
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
print("\nCERTIFICATE (iii): configurations reachable from C = {1: 11, 13: 11, 2: 1, 10: 1}:", len(seen))
print("  largest number of pebbles ever on each vertex:", mx)
assert mx[R] == 0 and mx[6] <= 1 and mx[11] <= 1
print("  no reachable configuration has a pebble on 9, and none has two pebbles on 6 or on 11")
# how many pebbles can ever enter the middle {4,5,7,8} from each branch, over all sequences (DP on the DAG)
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
A_out = (( 2, 4), (3, 5)); B_out = ((10, 7), (12, 7), (12, 8))
print("  maximum number of moves from {1,2,3} into {4,5} over all sequences:", best(C, A_out))
print("  maximum number of moves from {10,12,13} into {7,8} over all sequences:", best(C, B_out))
print("  maximum number of moves 5->6:", best(C, ((5, 6),)), " maximum number of moves 8->11:", best(C, ((8, 11),)))
print("  maximum number of pebbles arriving at 5:", best(C, tuple((u, 5) for u in adj[5])), " at 8:", best(C, tuple((u, 8) for u in adj[8])))

# ------------------------------------------------------------ Certificate (iv): template bounds
def npiles(c): return sum(1 for v in V if cnt(c, v) >= 2)
T1 = max(k for k, U in enumerate(LA) if any(npiles(c) <= 1 for c in U))
T2 = max(k for k, U in enumerate(LA) if any(npiles(c) <= 2 for c in U))
print("\nCERTIFICATE (iv): largest unreachable configuration with one pile plus single pebbles has", T1, "pebbles:", [dec(c) for c in LA[T1] if npiles(c) <= 1][:4])
print("  largest unreachable configuration with at most two piles has", T2, "pebbles")
print("\nALL CHECKS PASSED: pi(G, 9) = 25.")
