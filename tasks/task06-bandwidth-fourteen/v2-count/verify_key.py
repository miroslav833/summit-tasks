"""Verification of the answer key: the graph in the figure has bandwidth 5 and exactly 6 numberings of
width 5 (3 up to reversal).

Self-contained: python3 only.  Run: python3 verify_key.py
  (1) bandwidth 5: no numbering of width 4 (backtracking with pruning); density certificate: the induced
      subgraph on {1,3,4,7,8,10,11,12,13,14} has ten vertices and diameter 2, so width >= ceil(9/2) = 5;
  (2) all numberings of width 5 by backtracking with pruning: six, listed; a numbering and its reverse
      are counted separately; three up to reversal;
  (3) independent count by a dynamic programme over (set of placed vertices, last five placed);
  (4) the search tree at the top levels, printed with the reason each dead branch dies, so that the
      enumeration can be followed by hand; structural facts shared by all six numberings;
  (5) the trivial bounds and the breadth-first (Cuthill-McKee) numberings from every start vertex.
"""
import itertools, collections, math
from functools import lru_cache
EDGES = [(1, 2), (1, 4), (1, 6), (1, 8), (1, 11), (1, 14), (2, 8), (3, 7), (3, 8), (3, 10), (3, 12), (3, 13),
         (4, 10), (4, 11), (4, 13), (4, 14), (5, 9), (5, 12), (6, 7), (6, 9), (6, 10), (6, 11), (7, 8), (7, 11),
         (9, 13), (9, 14), (11, 13), (11, 14), (12, 14)]
V = list(range(1, 15)); n = 14; adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
assert len(EDGES) == 29 and len(set(frozenset(e) for e in EDGES)) == 29
print("vertices:", n, "edges:", len(EDGES), "degrees:", {v: len(adj[v]) for v in V})
def width(order):
    p = {v: i for i, v in enumerate(order)}; return max(abs(p[u] - p[v]) for u, v in EDGES)

def all_numberings(b, log=None, maxdepth=0):
    """every numbering of width at most b. A vertex goes to the next free position only if all its placed
    neighbours are within b positions, and every placed vertex must still have room within b positions
    for all its unplaced neighbours."""
    sols = []; pos = {}
    def rec(i, path):
        if i == n: sols.append([v for v, _ in sorted(pos.items(), key=lambda kv: kv[1])]); return
        for v in V:
            if v in pos: continue
            bad = [u for u in adj[v] if u in pos and i - pos[u] > b]
            if bad:
                if log is not None and i < maxdepth: log.append(f"{path + [v]}: edge {v}-{bad[0]} would stretch {i - pos[bad[0]]} > {b}")
                continue
            pos[v] = i; reason = None
            for u in list(pos):
                far = [w for w in adj[u] if w not in pos]
                if far and (pos[u] + b) - i < len(far): reason = f"vertex {u} at position {pos[u]+1} still needs {len(far)} neighbours but only {(pos[u] + b) - i} positions remain within reach"; break
            if reason is None: rec(i + 1, path + [v])
            elif log is not None and i < maxdepth: log.append(f"{path + [v]}: {reason}")
            del pos[v]
    rec(0, [])
    return sols

# ---------- (1) bandwidth 5 ----------
print("numberings of width 4:", len(all_numberings(4)))
S = [1, 3, 4, 7, 8, 10, 11, 12, 13, 14]
def dist_in(S):
    D = {}
    for s in S:
        d = {s: 0}; q = collections.deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y in S and y not in d: d[y] = d[x] + 1; q.append(y)
        D[s] = d
    return D
D = dist_in(S); assert all(len(D[s]) == len(S) for s in S)
diam = max(D[s][t] for s in S for t in S)
print(f"certificate subgraph on {S}: {len(S)} vertices, diameter {diam} -> bandwidth >= ceil(9/2) = 5")
assert diam == 2
for s in S:
    for t in S:
        if s < t and t not in adj[s]: print(f"   {s},{t}: common neighbour in S: {sorted(adj[s] & adj[t] & set(S))}")
def diameter_all():
    best = 0
    for s in V:
        d = {s: 0}; q = collections.deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in d: d[y] = d[x] + 1; q.append(y)
        best = max(best, max(d.values()))
    return best
print("diameter of G:", diameter_all(), "-> diameter bound ceil(13/4) =", math.ceil(13 / diameter_all()),
      "; degree bound ceil(6/2) = 3")
print("CHECK 1: bandwidth = 5")

# ---------- (2) all numberings of width 5 ----------
log = []
sols = all_numberings(5, log, maxdepth=2)
print("numberings of width 5:", len(sols))
for s in sols: print("   ", s, " width", width(s), " reverse present:", s[::-1] in sols)
assert len(sols) == 6 and all(width(s) == 5 for s in sols) and all(s[::-1] in sols for s in sols)
classes = sorted(set(tuple(min(s, s[::-1])) for s in sols))
print("up to reversal:", len(classes))
for c in classes:
    tight = sorted((u, v) for u, v in EDGES if abs(c.index(u) - c.index(v)) == 5)
    print("   ", list(c), " edges stretched by exactly 5:", tight)

# ---------- (3) independent count ----------
@lru_cache(maxsize=None)
def count(placed, last, b=5):
    """number of ways to finish a numbering of width at most b: 'last' holds the last b placed vertices;
    a new vertex may only have placed neighbours among them, and the vertex leaving the window must
    have no unplaced neighbour left."""
    if len(placed) == n: return 1
    tot = 0
    for v in V:
        if v in placed: continue
        if any(u not in last for u in adj[v] if u in placed): continue
        if len(last) == b and any(w not in placed and w != v for w in adj[last[0]]): continue
        tot += count(placed | frozenset([v]), (last + (v,))[-b:])
    return tot
c5 = count(frozenset(), tuple()); print("dynamic programme, numberings of width at most 5:", c5); assert c5 == 6
c6 = count.__wrapped__ if False else None
@lru_cache(maxsize=None)
def count6(placed, last):
    if len(placed) == n: return 1
    tot = 0
    for v in V:
        if v in placed: continue
        if any(u not in last for u in adj[v] if u in placed): continue
        if len(last) == 6 and any(w not in placed and w != v for w in adj[last[0]]): continue
        tot += count6(placed | frozenset([v]), (last + (v,))[-6:])
    return tot
print("for comparison, numberings of width at most 6:", count6(frozenset(), tuple()))
print("CHECK 2-3: exactly six numberings of width 5 by two independent methods")

# ---------- (4) structure and search tree ----------
print("structural facts in all six: ends are 2 and 5:", all({s[0], s[-1]} == {2, 5} for s in sols),
      "; 8 next to 2:", all(abs(s.index(8) - s.index(2)) == 1 for s in sols),
      "; 9 next to 5:", all(abs(s.index(9) - s.index(5)) == 1 for s in sols),
      "; 12 next to 9:", all(abs(s.index(12) - s.index(9)) == 1 for s in sols),
      "; from the end at 2: 1 in position 4 or 5:", all(sorted(s, key=lambda v: 0)[0] is not None and (s.index(1) + 1 in (4, 5) if s[0] == 2 else 14 - s.index(1) in (4, 5)) for s in sols),
      "; 3 in position 7 and 6 in position 8:", all((s[6], s[7]) == (3, 6) if s[0] == 2 else (s[7], s[6]) == (3, 6) for s in sols))
def ball(v, r):
    d = {v: 0}; q = collections.deque([v])
    while q:
        x = q.popleft()
        if d[x] == r: continue
        for y in adj[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return set(d)
print("end-vertex test: a vertex at position 1 of a numbering of width 5 has its whole distance-2 ball in positions 1 to 11;")
print("   sizes of the distance-2 balls:", {v: len(ball(v, 2)) for v in V}, "-> only 2 and 5 fit (ball at most 11)")
assert [v for v in V if len(ball(v, 2)) <= 11] == [2, 5]
# 1 cannot be in position 2 next to 2: its five other neighbours fill positions 3 to 7, and their further neighbours must be within 12
close = {2, 1} | adj[1] | set().union(*(adj[u] for u in adj[1] - {2}))
print("   with 2 at position 1 and 1 at position 2, the vertices forced into positions 1 to 12 are", sorted(close), "->", len(close), "vertices, more than 12, so 8 is in position 2")
assert len(close) > 12
print("   position 13 (with 5 in position 14): the vertex there has its distance-2 ball, and 5, inside positions 3 to 14 (twelve positions);")
for x in V:
    if x in (2, 5): continue
    forced = ball(x, 2) | {5} | ({6} if x == 12 else set())
    print(f"      {x}: forced vertices {len(forced)}" + (" (6 joins because it is adjacent to 9, which is within five positions of 5)" if x == 12 else "") + (" -> possible" if len(forced) <= 12 else " -> impossible"))
assert [x for x in V if x not in (2, 5) and len(ball(x, 2) | {5} | ({6} if x == 12 else set())) <= 12] == [9]
print("search tree, first two positions (dead branches with reasons; live branches continue):")
live = sorted(set(tuple(s[:2]) for s in sols))
dead_first = collections.Counter(eval(e.split(":")[0])[0] for e in log if len(eval(e.split(":")[0])) == 1)
print("   first vertex alone:", "dead:", sorted(dead_first), "live:", sorted(set(s[0] for s in sols)))
for entry in log:
    if len(eval(entry.split(":")[0])) >= 2: print("   dead:", entry)
print("   live pairs of first two vertices:", live)
print("   numberings per first vertex:", dict(collections.Counter(s[0] for s in sols)))

# ---------- (5) heuristics ----------
def cuthill_mckee(start, reverse=False):
    order = [start]; seen = {start}; q = collections.deque([start])
    while q:
        v = q.popleft()
        for u in sorted(adj[v], key=lambda u: len(adj[u])):
            if u not in seen: seen.add(u); order.append(u); q.append(u)
    return order[::-1] if reverse else order
ws = sorted(set(width(cuthill_mckee(s, r)) for s in V for r in (False, True)))
print("breadth-first (Cuthill-McKee and reverse) numberings from every start vertex have widths:", ws)
print("ALL CHECKS PASSED. Bandwidth 5, exactly 6 optimal numberings (3 up to reversal).")
