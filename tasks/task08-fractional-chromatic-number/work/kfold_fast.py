import itertools, time, sys
EDGES = [(1, 5), (1, 8), (1, 9), (1, 10), (2, 3), (2, 7), (2, 9), (2, 10), (3, 5), (3, 6), (3, 12), (4, 6), (4, 9), (4, 11), (4, 12), (5, 7), (5, 12), (6, 7), (6, 8), (7, 11), (8, 10), (8, 11), (9, 10), (11, 12)]
V = list(range(1, 13)); adj = {v: set() for v in V}
for u, v in EDGES: adj[u].add(v); adj[v].add(u)
def kfold(k, d):
    """k:d-colouring search with bitmask colour sets.  Symmetry breaking: vertex 1 gets colours {0..d-1}; the
    colours are otherwise interchangeable, so a vertex may use a new colour c only if every colour below c has
    already appeared (canonical first-use order)."""
    subsets = [sum(1 << c for c in S) for S in itertools.combinations(range(k), d)]
    order = [1]; seen = {1}; frontier = [1]
    while frontier:
        nxt = []
        for u in frontier:
            for v in sorted(adj[u], key=lambda x: -len(adj[x] & seen)):
                if v not in seen: seen.add(v); order.append(v); nxt.append(v)
        frontier = nxt
    assign = {}
    def rec(i, used):
        if i == len(order): return True
        v = order[i]
        forbidden = 0
        for u in adj[v]:
            if u in assign: forbidden |= assign[u]
        maxc = used.bit_length()           # colours 0..maxc-1 have been used so far (canonical by induction)
        for S in subsets:
            if S & forbidden: continue
            new = S & ~used
            if new and new != (((1 << bin(new).count("1")) - 1) << maxc): continue   # new colours must be the next indices
            assign[v] = S
            if rec(i + 1, used | S): return True
            del assign[v]
        return False
    assign[1] = subsets[0]
    return rec(1, subsets[0])
for k, d in ((6, 2), (7, 2), (9, 3), (10, 3), (12, 4), (13, 4)):
    t = time.time(); r = kfold(k, d); print(f"{k}:{d} -> {r}  ({time.time()-t:.1f}s)", flush=True)
