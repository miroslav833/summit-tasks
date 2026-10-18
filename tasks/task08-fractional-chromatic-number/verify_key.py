# Number of Hamiltonian cycles of the drawn graph (28 vertices, 42 edges, all of degree 3).
# Run: python3 verify_key.py (standard library only)
import itertools
from collections import Counter

EDGES = "AG AJ AS BK BS BV CH CL CY DI DN DW EL EP EZ FS FX FZ GT Gb HJ Ha IM Ib JV KQ KU LR MO MX NT NV OQ OZ PU PX QY RT Ra Ub WY Wa".split()
V = sorted({v for e in EDGES for v in e}, key=lambda v: (v.islower(), v))
ADJ = {v: sorted({e[1] if e[0] == v else e[0] for e in EDGES if v in e}, key=lambda v: (v.islower(), v)) for v in V}
EDGESET = {frozenset(e) for e in EDGES}

print("1. The graph")
print(f"   vertices {len(V)}, edges {len(EDGES)}, degrees {sorted(Counter(len(ADJ[v]) for v in V).items())}")
for v in V: print(f"   {v}: {' '.join(ADJ[v])}")
# girth by breadth-first search from every vertex
def girth():
    best = 99
    for s in V:
        dist, par, q = {s: 0}, {s: None}, [s]
        for x in q:
            for y in ADJ[x]:
                if y not in dist: dist[y] = dist[x] + 1; par[y] = x; q.append(y)
                elif par[x] != y: best = min(best, dist[x] + dist[y] + 1)
    return best
print(f"   girth {girth()} (no triangles and no 4-cycles)")

print("2. Route 1: depth-first search for Hamiltonian cycles through A")
cycles = set()
def dfs(path, seen):
    v = path[-1]
    if len(path) == len(V):
        if "A" in ADJ[v]: cycles.add(frozenset(frozenset(p) for p in zip(path, path[1:] + ["A"])))
        return
    for w in ADJ[v]:
        if w not in seen:
            seen.add(w); path.append(w); dfs(path, seen); path.pop(); seen.remove(w)
dfs(["A"], {"A"})
print(f"   distinct Hamiltonian cycles (as edge sets): {len(cycles)}")

print("3. Route 2: complements of perfect matchings")
# In a cubic graph a Hamiltonian cycle uses two of the three edges at every vertex, so the unused edges form a
# perfect matching; conversely a perfect matching whose complement is connected leaves a Hamiltonian cycle.
def connected(edges):
    adj = {v: [] for v in V}
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    seen, q = {V[0]}, [V[0]]
    for x in q:
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return len(seen) == len(V)
matchings = good = 0
def rec(M, covered):
    global matchings, good
    free = [v for v in V if v not in covered]
    if not free:
        matchings += 1
        rest = [tuple(e) for e in EDGESET if e not in M]
        if connected(rest): good += 1
        return
    v = free[0]
    for w in ADJ[v]:
        if w not in covered:
            M.add(frozenset((v, w))); rec(M, covered | {v, w}); M.remove(frozenset((v, w)))
rec(set(), frozenset())
print(f"   perfect matchings {matchings}, of which {good} leave a single 28-cycle")
assert good == len(cycles) == 52

print("4. Case split used in the written solution")
def has(c, a, b): return frozenset((a, b)) in c
for x in ADJ["D"]:
    part = [c for c in cycles if not has(c, "D", x)]
    other = [w for w in ADJ["D"] if w != x]
    # second level: which edge is left out at the first neighbour of D that the cycle uses
    y = other[0]; sub = Counter(next(w for w in ADJ[y] if not has(c, y, w)) for c in part)
    detail = ", ".join(f"{y}{w} left out: {sub[w]}" for w in ADJ[y] if w != "D")
    print(f"   D{x} left out: {len(part)}   ({detail})")

print("5. Parity check: every edge lies on an even number of Hamiltonian cycles (Smith's theorem for cubic graphs)")
through = {e: sum(1 for c in cycles if frozenset(e) in c) for e in EDGES}
print("   " + " ".join(f"{e}:{n}" for e, n in through.items()))
assert all(n % 2 == 0 for n in through.values()) and sum(through.values()) == 28 * 52
print(f"   all even; sum over edges = {sum(through.values())} = 28 x 52")

print("6. The 52 cycles, each written from A")
def walk(c):
    adj = {v: [] for v in V}
    for e in c:
        a, b = tuple(e); adj[a].append(b); adj[b].append(a)
    path = ["A", min(adj["A"])]
    while len(path) < len(V): path.append(next(w for w in adj[path[-1]] if w != path[-2]))
    return "".join(path)
for i, s in enumerate(sorted(walk(c) for c in cycles), 1): print(f"   {i:2d}. {s}")

print("7. Wrong answers: 104 counts each cycle once per direction; 26 halves twice; 48, 50, 51 lose cycles in the case split")
print("ALL CHECKS PASSED: the graph has 52 Hamiltonian cycles")
