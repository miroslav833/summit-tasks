import json, collections, sys, time
sys.path.insert(0, "../work/rev")
from pebble2 import pi_rooted, decode
g = json.load(open("graph.json")); E = [tuple(e) for e in g["edges"]]; n = 14; T = g["target"] - 1
adj = [[] for _ in range(n)]
for u, v in E: adj[u-1].append(v-1); adj[v-1].append(u-1)
t=time.time(); p, sizes, last = pi_rooted(adj, n, T, cap=3_000_000)
print("pi =", p, "sizes", sizes, f"{time.time()-t:.0f}s")
B = [1 << (5*v) for v in range(n)]
def cnt(c,v): return (c>>(5*v))&31
def reach_set(c0):
    seen = {c0}; q = collections.deque([c0])
    while q:
        c = q.popleft()
        for u in range(n):
            if cnt(c,u) >= 2:
                for w in adj[u]:
                    t = c - 2*B[u] + B[w]
                    if t not in seen: seen.add(t); q.append(t)
    return seen
res = []
for c in last:
    S = reach_set(c); mx = {v+1: max(cnt(s,v) for s in S) for v in range(n)}
    assert mx[T+1] == 0
    cfg = {v+1: x for v, x in decode(c, n).items()}
    res.append((len(S), cfg, mx))
for sz, cfg, mx in sorted(res): print(sz, cfg, "max on 2,3:", mx[2], mx[3], "max on 4,5,6,8,10:", mx[4], mx[5], mx[6], mx[8], mx[10])
# template configs: regrow layers to find T1/T2 examples
from layers import layers_all, npiles
L = layers_all(adj, n, T)
for k in range(len(L)-1, 0, -1):
    one = [decode(c,n) for c in L[k] if npiles(c,n) <= 1]
    if one: print("T1: largest one-pile failing has", k, "pebbles, e.g.", [{v+1:x for v,x in d.items()} for d in one[:3]], "count", len(one)); break
for k in range(len(L)-1, 0, -1):
    two = [decode(c,n) for c in L[k] if npiles(c,n) <= 2]
    if two: print("T2: largest two-pile failing has", k, "pebbles, e.g.", [{v+1:x for v,x in d.items()} for d in two[:6]], "count", len(two)); break
for k in range(len(L)-1, 0, -1):
    three = [decode(c,n) for c in L[k] if npiles(c,n) <= 3]
    if three: print("T3: largest three-pile failing has", k, "pebbles, count", len(three)); break
