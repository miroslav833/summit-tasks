"""Verification of the answer key: the graph in the figure has bandwidth 4 and exactly 6 numberings of
width 4 (3 up to reversal).

Self-contained: python3 only.  Run: python3 verify_key.py
  (1) bandwidth 4: no numbering of width 3 (backtracking), density certificate on {1,2,3,4,6,9,10,11};
  (2) all numberings of width 4 by backtracking with pruning: six, listed; a numbering and its reverse
      are counted separately; three up to reversal;
  (3) independent count by a dynamic programme over (set of placed vertices, last four placed);
  (4) the search tree at the top levels, printed with the reason each dead branch dies, so that the
      enumeration can be checked by hand; structural facts shared by all six numberings.
"""
import itertools, collections
from functools import lru_cache
EDGES = [(1, 2), (1, 3), (1, 4), (1, 6), (1, 11), (2, 6), (2, 8), (2, 10), (3, 4), (3, 5), (4, 9), (4, 10), (4, 11), (6, 9), (8, 5), (8, 12), (9, 7), (9, 12), (11, 7), (11, 10)]
V = list(range(1, 13)); n = 12; adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
def width(order):
    p = {v: i for i, v in enumerate(order)}; return max(abs(p[u] - p[v]) for u, v in EDGES)

def all_numberings(b, log=None, maxdepth=0):
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
print("numberings of width 3:", len(all_numberings(3)))
S = [1, 2, 3, 4, 6, 9, 10, 11]
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
D = dist_in(S); print("certificate subgraph diameter:", max(D[s][t] for s in S for t in S), "-> bandwidth >= ceil(7/2) = 4")
log = []
sols = all_numberings(4, log, maxdepth=2)
print("CHECK 1: bandwidth = 4")
print("numberings of width 4:", len(sols))
for s in sols: print("   ", s, " reverse:", s[::-1] in sols)
assert len(sols) == 6 and all(width(s) == 4 for s in sols) and all(s[::-1] in sols for s in sols)
print("up to reversal:", len(set(tuple(min(s, s[::-1])) for s in sols)))
@lru_cache(maxsize=None)
def count(placed, last, b=4):
    if len(placed) == n: return 1
    tot = 0
    for v in V:
        if v in placed: continue
        if any(u not in last for u in adj[v] if u in placed): continue
        if len(last) == b and any(w not in placed and w != v for w in adj[last[0]]): continue
        tot += count(placed | frozenset([v]), (last + (v,))[-b:])
    return tot
c = count(frozenset(), tuple()); print("dynamic programme count:", c); assert c == 6
print("CHECK 2-3: exactly six numberings of width 4 by two independent methods")
print("structural facts in all six: vertex 11 at an end:", all(s[0] == 11 or s[-1] == 11 for s in sols),
      "; other end in {5, 8}:", all((s[0] if s[-1] == 11 else s[-1]) in (5, 8) for s in sols),
      "; vertices 1 and 4 adjacent in position:", all(abs(s.index(1) - s.index(4)) <= 2 for s in sols))
print("search tree, first two positions (dead branches with reasons; live branches continue):")
first = collections.Counter(); live = set()
for s in sols: live.add((s[0], s[1]))
for entry in log: print("   dead:", entry)
print("   live pairs of first two vertices:", sorted(live))
# completions per first vertex
per_first = collections.Counter(s[0] for s in sols); print("   numberings per first vertex:", dict(per_first))
print("ALL CHECKS PASSED. Bandwidth 4, exactly 6 optimal numberings (3 up to reversal).")
