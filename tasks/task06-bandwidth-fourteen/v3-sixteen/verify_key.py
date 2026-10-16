"""Verification of the answer key: the bandwidth of the 16-vertex, 27-edge graph in the figure is 5.

Self-contained: python3 only.  Run: python3 verify_key.py
  (1) no numbering of width 4, by the prefix-boundary chain: in a numbering of width b, the set P of the
      first k vertices has at most b neighbours outside P (each of them must come within b positions of
      its earliest neighbour, so all of them sit in the next b positions). Growing P one vertex at a time
      and keeping only sets with at most 4 outside neighbours, the chain dies at k = 6; every surviving set
      is printed with its outside neighbours, so the proof can be checked by hand (57 sets);
  (2) the same conclusion by backtracking over numberings with pruning, and by a dynamic programme over
      (set of placed vertices, last four placed), two independent exact methods;
  (3) the numbering 1,10,9,15,3,2,8,6,12,14,13,4,5,7,11,16 (positions 1 to 16) has width 5; every edge is
      listed with its stretch; it is the only numbering of width 5 apart from its reverse;
  (4) the easy bounds: degree bound ceil(6/2) = 3, diameter bound ceil(15/4) = 4, and the density bound
      ceil((k-1)/d) over every connected induced subgraph is at most 4 (all 2^16 subsets checked), so no
      bound of that kind reaches 5;
  (5) breadth-first (Cuthill-McKee and reverse) numberings from every start vertex have widths 7 to 10.
"""
import itertools, collections, math
from functools import lru_cache
EDGES = [(1, 3), (1, 10), (2, 3), (2, 9), (2, 12), (2, 13), (3, 10), (3, 12), (3, 14), (3, 15), (4, 8), (4, 16), (5, 6), (5, 7), (6, 9), (6, 14), (6, 15), (7, 12), (7, 16), (8, 9), (8, 10), (8, 13), (9, 15), (11, 13), (11, 14), (12, 15), (13, 16)]
V = list(range(1, 17)); n = 16; adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
assert len(EDGES) == 27 and len(set(frozenset(e) for e in EDGES)) == 27
print("vertices:", n, "edges:", len(EDGES), "degrees:", {v: len(adj[v]) for v in V})
def width(order):
    p = {v: i for i, v in enumerate(order)}; return max(abs(p[u] - p[v]) for u, v in EDGES)
def boundary(P): return set().union(*(adj[v] for v in P)) - set(P) if P else set()

# ---------- (1) prefix-boundary chain for width 4 ----------
print("\n(1) prefix-boundary chain, width 4: sets P of the first k vertices with at most 4 outside neighbours")
b = 4; layers = [frozenset()]; total = 0
for k in range(1, n):
    new = set()
    for P in layers:
        for v in V:
            if v not in P and len(boundary(P | {v})) <= b: new.add(P | {v})
    layers = sorted(new, key=sorted); total += len(layers)
    print(f"   k = {k}: {len(layers)} sets")
    for P in layers: print(f"      {sorted(P)}  outside neighbours {sorted(boundary(P))}")
    if not layers: print(f"   no set of {k} vertices has at most 4 outside neighbours, so no numbering of width 4 exists"); break
assert not layers
print(f"   sets listed in the chain: {total}")
print("CHECK 1: bandwidth >= 5 by the prefix-boundary chain")

# ---------- (2) two exact methods ----------
def all_numberings(b, cap=10):
    sols = []; pos = {}
    def rec(i):
        if len(sols) >= cap: return
        if i == n: sols.append([v for v, _ in sorted(pos.items(), key=lambda kv: kv[1])]); return
        for v in V:
            if v in pos or any(i - pos[u] > b for u in adj[v] if u in pos): continue
            pos[v] = i; ok = True
            for u in list(pos):
                far = [w for w in adj[u] if w not in pos]
                if far and (pos[u] + b) - i < len(far): ok = False; break
            if ok: rec(i + 1)
            del pos[v]
    rec(0); return sols
def count_dp(b):
    @lru_cache(maxsize=None)
    def cnt(placed, last):
        if len(placed) == n: return 1
        tot = 0
        for v in V:
            if v in placed: continue
            if any(u not in last for u in adj[v] if u in placed): continue
            if len(last) == b and any(w not in placed and w != v for w in adj[last[0]]): continue
            tot += cnt(placed | frozenset([v]), (last + (v,))[-b:])
        return tot
    return cnt(frozenset(), tuple())
s4 = all_numberings(4); s5 = all_numberings(5)
print("\n(2) backtracking: numberings of width 4:", len(s4), "; of width 5:", len(s5))
c4 = count_dp(4); c5 = count_dp(5)
print("    dynamic programme: numberings of width at most 4:", c4, "; at most 5:", c5)
assert len(s4) == 0 and c4 == 0 and len(s5) == 2 and c5 == 2
print("CHECK 2: bandwidth = 5 by two independent exact methods; exactly two numberings of width 5 (one up to reversal)")

# ---------- (3) the numbering ----------
order = [1, 10, 9, 15, 3, 2, 8, 6, 12, 14, 13, 4, 5, 7, 11, 16]
assert sorted(order) == V and order in s5 and order[::-1] in s5
p = {v: i + 1 for i, v in enumerate(order)}
print("\n(3) numbering (vertex -> position):", {v: p[v] for v in V})
print("    stretches:", ", ".join(f"{u}-{v}: {abs(p[u]-p[v])}" for u, v in EDGES))
print("    width:", width(order)); assert width(order) == 5
print("CHECK 3: bandwidth <= 5")

# ---------- (4) easy bounds ----------
def dist_from(s, S=None):
    S = set(V) if S is None else S; d = {s: 0}; q = collections.deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in S and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
diam = max(max(dist_from(s).values()) for s in V)
print("\n(4) degree bound ceil(6/2) =", math.ceil(max(len(adj[v]) for v in V) / 2), "; diameter", diam, "-> diameter bound ceil(15/%d) =" % diam, math.ceil(15 / diam))
best = (0, None)
for mask in range(1, 1 << n):
    S = [V[i] for i in range(n) if mask >> i & 1]
    if len(S) < 3: continue
    d0 = dist_from(S[0], set(S))
    if len(d0) < len(S): continue
    dS = max(max(dist_from(s, set(S)).values()) for s in S)
    val = math.ceil((len(S) - 1) / dS)
    if val > best[0] or (val == best[0] and len(S) < len(best[1])): best = (val, S)
print("    density bound over all connected induced subgraphs:", best[0], "attained e.g. by", best[1], "; it never reaches 5")
assert best[0] == 4
print("CHECK 4: no degree, diameter or density bound gives 5")

# ---------- (5) heuristics ----------
def cm(start, reverse=False):
    order = [start]; seen = {start}; q = collections.deque([start])
    while q:
        v = q.popleft()
        for u in sorted(adj[v], key=lambda u: len(adj[u])):
            if u not in seen: seen.add(u); order.append(u); q.append(u)
    return order[::-1] if reverse else order
ws = sorted(set(width(cm(s, r)) for s in V for r in (False, True)))
print("\n(5) Cuthill-McKee and reverse Cuthill-McKee numberings from every start vertex have widths:", ws)
print("\nALL CHECKS PASSED. Bandwidth 5; lower bound by the 57-set prefix chain, upper bound by the unique numbering.")
