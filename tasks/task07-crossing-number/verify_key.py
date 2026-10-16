"""Verification of the answer key: the crossing number of the graph in the figure is 3.

Self-contained, standard library plus networkx (route A only).  Run: python3 verify_key.py

Route A (exhaustive, networkx planarity).  A drawing with k crossings in which adjacent edges do not
  cross and two edges cross at most once is the same thing as a planar embedding of the planarization
  (each crossing replaced by a degree-4 vertex, an edge with several crossings split in the order in
  which they occur along it).  Optimal drawings have both properties, so cr(G) is the least k for
  which some set of k independent edge pairs, with some order of the crossings along each edge, has a
  planar planarization.  The program enumerates k = 1, 2 (no planar planarization) and k = 3 (planar
  planarizations exist and are counted).  It also lists every pair of edges whose removal leaves a
  planar graph (skewness 2) and the value of the greedy "maximum planar subgraph plus shortest-path
  insertion" construction.

Route B (independent, no graph library).  Planarity and embeddings by the Demoucron-Malgrange-
  Pertuiset algorithm written from scratch.  Lower bound: in a drawing with two crossings the two
  crossing pairs are edge-disjoint (a shared edge e would make G - e planar, but no single edge
  removal is planar), so removing one edge from each pair leaves an embedded planar subgraph H with
  m - 2 edges into which each removed edge is inserted with exactly one crossing of an H-edge.  For
  every H = G - {x, y} that is planar, H is 3-connected, so its embedding is unique (Whitney); the
  program prints the faces and shows that x or y has its endpoints on faces at dual distance at
  least 2, so no drawing with two crossings exists.  Upper bound: explicit integer coordinates for
  a straight-line drawing, checked by exact orientation tests, with exactly three crossing pairs.
"""
import itertools, sys
from itertools import permutations, product, combinations
from collections import deque
from fractions import Fraction

EDGES = [(1, 2), (1, 5), (1, 9), (1, 10), (2, 3), (2, 4), (2, 6), (3, 5), (3, 6), (3, 8), (3, 9), (4, 5), (4, 6), (4, 8), (4, 10), (5, 6), (6, 7), (7, 8), (7, 9), (7, 10), (8, 10)]
VERTS = sorted({v for e in EDGES for v in e}); N = len(VERTS); M = len(EDGES)
COORDS = {1: (0, 4), 2: (6, 6), 3: (5, 7), 4: (8, 6), 5: (2, 5), 6: (7, 7), 7: (12, 10), 8: (9, 8), 9: (5, 12), 10: (10, 3)}

print("vertices", N, "edges", M)
print("degrees", {v: sum(v in e for e in EDGES) for v in VERTS})
print("Euler bound m - 3n + 6 =", M - 3 * N + 6)

# ============================ Route A ============================
import networkx as nx


def independent_pairs(edges):
    return [(i, j) for i in range(len(edges)) for j in range(i + 1, len(edges)) if not set(edges[i]) & set(edges[j])]


def planarization(edges, pairs, orders):
    H = nx.Graph(); H.add_nodes_from(v for e in edges for v in e)
    for i, (u, v) in enumerate(edges):
        chain = [u] + [("x", p) for p in orders.get(i, ())] + [v]
        H.add_edges_from(zip(chain, chain[1:]))
    return H


def planar_crossing_sets(edges, k, first_only=False):
    pairs = independent_pairs(edges); found = []
    for chosen in combinations(range(len(pairs)), k):
        per_edge = {}
        for p in chosen:
            for i in pairs[p]:
                per_edge.setdefault(i, []).append(p)
        multi = [i for i, ps in per_edge.items() if len(ps) > 1]
        for perms in product(*[list(permutations(per_edge[i])) for i in multi]):
            orders = {i: tuple(ps) for i, ps in per_edge.items() if len(ps) == 1}
            orders.update(dict(zip(multi, perms)))
            if nx.check_planarity(planarization(edges, [pairs[p] for p in chosen], orders))[0]:
                found.append(([pairs[p] for p in chosen], orders))
                if first_only:
                    return found
                break
    return found


G = nx.Graph(EDGES)
print("\nRoute A")
print("planar:", nx.check_planarity(G)[0], "; vertex connectivity:", nx.node_connectivity(G))
print("independent edge pairs:", len(independent_pairs(EDGES)))
one = [i for i in range(M) if nx.check_planarity(nx.Graph([e for j, e in enumerate(EDGES) if j != i]))[0]]
two = [(i, j) for i, j in combinations(range(M), 2) if nx.check_planarity(nx.Graph([e for k, e in enumerate(EDGES) if k not in (i, j)]))[0]]
print("single edges whose removal gives a planar graph:", [EDGES[i] for i in one])
print("edge pairs whose removal gives a planar graph (skewness 2):", [(EDGES[i], EDGES[j]) for i, j in two])
for k in (1, 2):
    f = planar_crossing_sets(EDGES, k, first_only=True)
    print(f"drawings with {k} crossings:", "exist" if f else "none")
    assert not f
f3 = planar_crossing_sets(EDGES, 3)
print("drawings with 3 crossings: crossing sets with a planar planarization:", len(f3))
assert f3
for pairs, orders in f3[:5]:
    print("   crossing pairs", [(EDGES[i], EDGES[j]) for i, j in pairs])


def faces_of(emb):
    seen = set(); faces = []
    for u, v in emb.edges():
        if (u, v) not in seen:
            faces.append(emb.traverse_face(u, v, mark_half_edges=seen))
    return faces


def dual_path(faces, u, v):
    edge_faces = {}
    for fi, face in enumerate(faces):
        for a, b in zip(face, face[1:] + face[:1]):
            edge_faces.setdefault(frozenset((a, b)), []).append(fi)
    D = nx.Graph(); D.add_nodes_from(range(len(faces)))
    for e, fs in edge_faces.items():
        if len(fs) == 2 and fs[0] != fs[1] and not D.has_edge(*fs):
            D.add_edge(fs[0], fs[1], via=e)
    best = None
    for s in [fi for fi, f in enumerate(faces) if u in f]:
        paths = nx.single_source_shortest_path(D, s)
        for t in [fi for fi, f in enumerate(faces) if v in f]:
            if t in paths and (best is None or len(paths[t]) - 1 < len(best)):
                best = [D.edges[a, b]["via"] for a, b in zip(paths[t], paths[t][1:])]
    return best


def insert(pedges, u, v):
    planar, emb = nx.check_planarity(nx.Graph(pedges)); assert planar
    path = dual_path(faces_of(emb), u, v); new = list(pedges); prev = u
    for idx, e in enumerate(path):
        a, b = tuple(e); x = ("d", u, v, idx)
        new.remove((a, b) if (a, b) in new else (b, a)); new += [(a, x), (x, b), (prev, x)]; prev = x
    new.append((prev, v)); return new, len(path)


print("greedy construction: maximum planar subgraph, then shortest-path insertion of the two missing edges")
best = None
for i, j in two:
    for order in ((i, j), (j, i)):
        cur = [e for k, e in enumerate(EDGES) if k not in (i, j)]; tot = 0
        for k in order:
            cur, c = insert(cur, *EDGES[k]); tot += c
        print(f"   remove {EDGES[i]}, {EDGES[j]}; insert {EDGES[order[0]]} then {EDGES[order[1]]}: {tot} crossings")
        best = tot if best is None else min(best, tot)
print("greedy construction minimum:", best)
print("Route A result: cr(G) = 3")

# ============================ Route B ============================
print("\nRoute B")


def adj_of(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return adj


def connected(adj, removed=()):
    verts = [v for v in adj if v not in removed]
    if not verts:
        return True
    seen = {verts[0]}; q = deque([verts[0]])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in removed and y not in seen:
                seen.add(y); q.append(y)
    return len(seen) == len(verts)


def three_connected(adj):
    return all(connected(adj, (a, b)) for a, b in combinations(adj, 2)) and len(adj) >= 4


def find_cycle(adj):
    start = next(iter(adj)); parent = {start: None}; stack = [start]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in parent:
                parent[w] = v; stack.append(w)
            elif w != parent[v]:
                pv = []; x = v
                while x is not None: pv.append(x); x = parent[x]
                pw = []; x = w
                while x is not None: pw.append(x); x = parent[x]
                c = next(x for x in pv if x in set(pw))
                return pv[:pv.index(c) + 1] + pw[:pw.index(c)][::-1]


def fragments(adj, Hv, He):
    frags = []
    for v in adj:
        if v in Hv:
            for w in adj[v]:
                if w in Hv and v < w and frozenset((v, w)) not in He:
                    frags.append(({frozenset((v, w))}, {v, w}))
    seen = set()
    for v in adj:
        if v in Hv or v in seen:
            continue
        comp = set(); q = deque([v]); seen.add(v)
        while q:
            x = q.popleft(); comp.add(x)
            for y in adj[x]:
                if y not in Hv and y not in seen:
                    seen.add(y); q.append(y)
        es = set(); att = set()
        for x in comp:
            for y in adj[x]:
                es.add(frozenset((x, y)))
                if y in Hv: att.add(y)
        frags.append((es, att))
    return frags


def frag_path(frag, a, b):
    es, att = frag; fadj = {}
    for e in es:
        x, y = tuple(e); fadj.setdefault(x, set()).add(y); fadj.setdefault(y, set()).add(x)
    parent = {a: None}; q = deque([a])
    while q:
        x = q.popleft()
        if x == b: break
        for y in fadj[x]:
            if y not in parent and (y not in att or y == b):
                parent[y] = x; q.append(y)
    p = []; x = b
    while x is not None: p.append(x); x = parent[x]
    return p[::-1]


def dmp_embedding(adj):
    """Faces of a planar embedding of a 2-connected graph (Demoucron-Malgrange-Pertuiset), or None."""
    m = sum(len(s) for s in adj.values()) // 2
    cyc = find_cycle(adj); faces = [list(cyc), list(cyc)[::-1]]
    Hv = set(cyc); He = {frozenset((cyc[i], cyc[(i + 1) % len(cyc)])) for i in range(len(cyc))}
    while len(He) < m:
        choice = None
        for frag in fragments(adj, Hv, He):
            adm = [i for i, f in enumerate(faces) if frag[1] <= set(f)]
            if not adm: return None
            if len(adm) == 1: choice = (frag, adm[0]); break
            if choice is None: choice = (frag, adm[0])
        frag, fi = choice; a, b = sorted(frag[1])[:2]; path = frag_path(frag, a, b)
        face = faces[fi]; n = len(face); ia, ib = face.index(a), face.index(b)
        seg1 = [face[(ia + k) % n] for k in range((ib - ia) % n + 1)]
        seg2 = [face[(ib + k) % n] for k in range((ia - ib) % n + 1)]
        faces[fi] = seg1 + path[1:-1][::-1]; faces.append(seg2 + path[1:-1])
        for x, y in zip(path, path[1:]): He.add(frozenset((x, y))); Hv.add(x); Hv.add(y)
    return faces


def blocks(adj):
    """Biconnected components as sets of edges (depth-first search with low-points)."""
    index = {}; low = {}; stack = []; out = []; counter = [0]
    def dfs(v, parent):
        index[v] = low[v] = counter[0]; counter[0] += 1
        for w in adj[v]:
            if w == parent: continue
            if w not in index:
                stack.append((v, w)); dfs(w, v); low[v] = min(low[v], low[w])
                if low[w] >= index[v]:
                    comp = set()
                    while True:
                        e = stack.pop(); comp.add(frozenset(e))
                        if e == (v, w): break
                    out.append(comp)
            elif index[w] < index[v]:
                stack.append((v, w)); low[v] = min(low[v], index[w])
    for v in adj:
        if v not in index: dfs(v, None)
    return out


def dmp_planar(adj):
    """Planarity of any graph: every block with at least three edges must be planar."""
    for comp in blocks(adj):
        if len(comp) < 3: continue
        sub = {}
        for e in comp:
            x, y = tuple(e); sub.setdefault(x, set()).add(y); sub.setdefault(y, set()).add(x)
        if dmp_embedding(sub) is None: return False
    return True


def check_faces(adj, faces):
    n = len(adj); m = sum(len(s) for s in adj.values()) // 2; seen = {}
    for f in faces:
        for x, y in zip(f, f[1:] + f[:1]):
            assert y in adj[x]; seen[(x, y)] = seen.get((x, y), 0) + 1
    assert all(c == 1 for c in seen.values()) and len(seen) == 2 * m and n - m + len(faces) == 2


def dual_distance(faces, u, v):
    """Smallest number of H-edges a curve from u to v must cross: BFS in the dual from faces at u."""
    edge_faces = {}
    for fi, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]):
            edge_faces.setdefault(frozenset((a, b)), []).append(fi)
    nbr = {fi: set() for fi in range(len(faces))}
    for fs in edge_faces.values():
        if len(fs) == 2: nbr[fs[0]].add(fs[1]); nbr[fs[1]].add(fs[0])
    dist = {fi: 0 for fi, f in enumerate(faces) if u in f}; q = deque(dist)
    while q:
        x = q.popleft()
        for y in nbr[x]:
            if y not in dist: dist[y] = dist[x] + 1; q.append(y)
    return min(dist[fi] for fi, f in enumerate(faces) if v in f)


adj = adj_of(EDGES)
print("G planar by DMP:", dmp_planar(adj))
print("G 3-connected:", three_connected(adj))
removable_single = [e for e in EDGES if dmp_planar(adj_of([f for f in EDGES if f != e]))]
print("single edges whose removal gives a planar graph (DMP):", removable_single)
assert not removable_single
print("Lower bound: every planar G - {x, y}, its unique embedding, and the insertion distance of x and y")
pairs_planar = []
for x, y in combinations(EDGES, 2):
    H = [e for e in EDGES if e not in (x, y)]; hadj = adj_of(H)
    if not dmp_planar(hadj):
        continue
    pairs_planar.append((x, y))
    assert three_connected(hadj), "embedding would not be unique"
    faces = dmp_embedding(hadj); check_faces(hadj, faces)
    dx, dy = dual_distance(faces, *x), dual_distance(faces, *y)
    print(f"   H = G - {{{x}, {y}}}: 3-connected, faces:")
    for f in faces:
        print("      ", "-".join(str(v) for v in f))
    print(f"      insertion distance of {x}: {dx};  of {y}: {dy};  sum {dx + dy}")
    assert max(dx, dy) >= 2
print("   planar pairs found:", len(pairs_planar), "; in every case one missing edge needs at least 2 crossings, so cr(G) >= 3")
print("Shorter argument: a drawing with two crossings {a,b} and {c,d} has four distinct edges (a shared edge e would")
print("   leave G - e planar, and no single deletion is planar), and deleting a,c or a,d or b,c or b,d leaves a planar")
print("   graph, so there would be four distinct planar pairs; only", len(pairs_planar), "exist:", pairs_planar)
assert len(pairs_planar) < 4
# faces of the planar subgraph behind the straight-line drawing: G minus the three crossed edges 1-2, 2-3, 3-8
Hp = [e for e in EDGES if e not in [(1, 2), (2, 3), (3, 8)]]; hp = adj_of(Hp); fp = dmp_embedding(hp); check_faces(hp, fp)
print("Planar subgraph G - {1-2, 2-3, 3-8} (18 edges), faces of an embedding (DMP):")
for f in fp: print("      ", "-".join(str(v) for v in f))
for x in [(1, 2), (2, 3), (3, 8)]:
    print("   insertion distance of", x, "into this embedding:", dual_distance(fp, *x))

print("Upper bound: straight-line drawing with the listed coordinates")


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p):
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


P = COORDS
assert len(set(P.values())) == N
for (u, v) in EDGES:
    for w in VERTS:
        assert w in (u, v) or not on_segment(P[u], P[v], P[w]), "vertex on an edge"
crossing_pairs = []; points = {}
for e, f in combinations(EDGES, 2):
    p1, p2, q1, q2 = P[e[0]], P[e[1]], P[f[0]], P[f[1]]
    if set(e) & set(f):
        s = (set(e) & set(f)).pop(); a = [x for x in e if x != s][0]; b = [x for x in f if x != s][0]
        assert not (orient(P[s], P[a], P[b]) == 0 and (P[a][0] - P[s][0]) * (P[b][0] - P[s][0]) + (P[a][1] - P[s][1]) * (P[b][1] - P[s][1]) > 0), "overlapping adjacent edges"
        continue
    d = [orient(q1, q2, p1), orient(q1, q2, p2), orient(p1, p2, q1), orient(p1, p2, q2)]
    assert 0 not in d or not any(on_segment(q1, q2, p) for p in (p1, p2)) and not any(on_segment(p1, p2, q) for q in (q1, q2)), "touching edges"
    if (d[0] > 0) != (d[1] > 0) and (d[2] > 0) != (d[3] > 0) and 0 not in d:
        den = (p1[0] - p2[0]) * (q1[1] - q2[1]) - (p1[1] - p2[1]) * (q1[0] - q2[0])
        t = Fraction((p1[0] - q1[0]) * (q1[1] - q2[1]) - (p1[1] - q1[1]) * (q1[0] - q2[0]), den)
        pt = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
        points.setdefault(pt, []).append((e, f)); crossing_pairs.append((e, f))
assert all(len(l) == 1 for l in points.values()), "three edges through one point"
print("   coordinates:", P)
print("   crossing pairs:", crossing_pairs)
assert len(crossing_pairs) == 3
print("   exactly 3 crossings, so cr(G) <= 3")
print("Route B result: cr(G) = 3")
print("\nBoth routes agree: the crossing number is 3.")
