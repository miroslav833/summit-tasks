"""Verification of the answer key: the bandwidth of the 14-vertex graph in the figure is 5.

Self-contained: python3 only.  Run: python3 verify_key.py
  (1) exact bandwidth by backtracking over numberings with pruning: no numbering of width 4, one of
      width 5 is printed with every edge stretch;
  (2) independent exact check by a dynamic programme over (set of placed vertices, last b placed);
  (3) every cheap lower bound stops at 4: degree bound 2, diameter bound 4, and the density bound
      ceil((|S|-1)/diam(S)) is at most 4 over ALL connected induced subgraphs S (all 2^14 subsets);
  (4) the width-4 search tree, printed to depth 3 with the reason each branch dies and the number of
      nodes visited, so that the exhaustive argument can be followed by hand;
  (5) the number of optimal numberings and the Cuthill-McKee widths; the 2-ball end test (|B(v,2)| <= 9 holds for six vertices, so the ends of a width-4 numbering are not forced) and the prefix-boundary admissible pairs (18).
"""
import itertools, math, collections
from functools import lru_cache
EDGES = [(1, 7), (1, 14), (2, 7), (2, 10), (2, 14), (3, 6), (3, 11), (3, 13), (4, 5), (4, 6), (4, 8), (4, 9), (5, 8), (6, 11), (6, 12), (6, 13), (7, 11), (7, 12), (7, 13), (8, 10), (9, 10), (10, 12), (10, 14), (12, 14), (13, 14)]
V = list(range(1, 15)); n = 14; adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
assert len(EDGES) == 25 and len(V) == 14
print("edges:", sorted(map(sorted, EDGES))); print("degrees:", {v: len(adj[v]) for v in V})
def width(order):
    p = {v: i for i, v in enumerate(order)}; return max(abs(p[u] - p[v]) for u, v in EDGES)

# ---------- (1) backtracking ----------
def search(b, log=None, maxdepth=0):
    sols = []; pos = {}; nodes = [0]
    def rec(i, path):
        nodes[0] += 1
        if i == n: sols.append([v for v, _ in sorted(pos.items(), key=lambda kv: kv[1])]); return
        for v in V:
            if v in pos: continue
            bad = [u for u in adj[v] if u in pos and i - pos[u] > b]
            if bad:
                if log is not None and i < maxdepth: log.append(f"{path + [v]}: edge {v}-{bad[0]} would stretch {i - pos[bad[0]]}")
                continue
            pos[v] = i; reason = None
            for u in list(pos):
                far = [w for w in adj[u] if w not in pos]
                if far and (pos[u] + b) - i < len(far): reason = f"vertex {u} (position {pos[u]+1}) still needs {len(far)} neighbours {sorted(far)} but only {(pos[u] + b) - i} positions within reach remain"; break
            if reason is None: rec(i + 1, path + [v])
            elif log is not None and i < maxdepth: log.append(f"{path + [v]}: {reason}")
            del pos[v]
    rec(0, [])
    return sols, nodes[0]
log4 = []
s4, nodes4 = search(4, log4, maxdepth=3)
s5, nodes5 = search(5)
print(f"backtracking: numberings of width 4: {len(s4)} ({nodes4} nodes visited); numberings of width 5: {len(s5)}")
assert len(s4) == 0 and len(s5) > 0
order = s5[0]; pos = {v: i + 1 for i, v in enumerate(order)}
print("a numbering of width 5 (position 1 to 14):", order)
for u, v in sorted(map(sorted, EDGES)): print(f"   edge {u}-{v}: stretch {abs(pos[u]-pos[v])}")
assert width(order) == 5

# ---------- (2) dynamic programme ----------
def bandwidth_le(b):
    @lru_cache(maxsize=None)
    def ok(placed, last):
        if len(placed) == n: return True
        for v in V:
            if v in placed: continue
            if any(u not in last for u in adj[v] if u in placed): continue
            if len(last) == b and any(w not in placed and w != v for w in adj[last[0]]): continue
            if ok(placed | frozenset([v]), (last + (v,))[-b:]): return True
        return False
    return ok(frozenset(), tuple())
print("dynamic programme: width 4 possible:", bandwidth_le(4), "; width 5 possible:", bandwidth_le(5))
assert not bandwidth_le(4) and bandwidth_le(5)
print("CHECK 1-2: bandwidth = 5 by two independent exact methods")

# ---------- (3) cheap bounds ----------
def bfs(src, allowed):
    d = {src: 0}; q = collections.deque([src])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in allowed and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
diamG = max(max(bfs(s, set(V)).values()) for s in V); Delta = max(len(adj[v]) for v in V)
print(f"degree bound ceil(Delta/2) = {math.ceil(Delta/2)}; diameter bound ceil((n-1)/diam) = {math.ceil((n-1)/diamG)} (diam = {diamG})")
best = 0; bestS = None
for mask in range(1, 1 << n):
    S = {V[i] for i in range(n) if mask >> i & 1}
    if len(S) < 2: continue
    s0 = next(iter(S)); d = bfs(s0, S)
    if len(d) != len(S): continue
    diam = max(max(bfs(s, S).values()) for s in S)
    val = math.ceil((len(S) - 1) / diam)
    if val > best: best, bestS = val, sorted(S)
print(f"density bound over all {2**n - 1} subsets (connected induced subgraphs only): max = {best}, attained e.g. by {bestS}")
assert best == 4
print("CHECK 3: every cheap lower bound gives at most 4")

# ---------- (4) the width-4 search tree ----------
print(f"width-4 search tree: {nodes4} nodes visited; branches at depth <= 3 and why they die:")
for e in log4: print("   ", e)
# ---------- (5) ----------
print("number of numberings of width 5:", len(s5))
def cuthill_mckee(start, reverse=False):
    order = [start]; seen = {start}; q = collections.deque([start])
    while q:
        v = q.popleft()
        for u in sorted(adj[v], key=lambda u: len(adj[u])):
            if u not in seen: seen.add(u); order.append(u); q.append(u)
    return order[::-1] if reverse else order
cm = sorted(set(width(cuthill_mckee(s, r)) for s in V for r in (False, True))); print("Cuthill-McKee widths from every start (and reversed):", cm)
ball2 = {v: len({v} | adj[v] | set().union(*[adj[u] for u in adj[v]])) for v in V}
print("|B(v,2)| per vertex:", ball2, "; eligible ends of a width-4 numbering (|B| <= 9):", [v for v in V if ball2[v] <= 9])
adm = [(u, w) for u, w in itertools.combinations(V, 2) if len((adj[u] | adj[w]) - {u, w}) <= 4]
print("pairs with at most 4 outside neighbours (prefix-boundary admissible):", len(adm), adm)
print("ALL CHECKS PASSED. Bandwidth 5.")
