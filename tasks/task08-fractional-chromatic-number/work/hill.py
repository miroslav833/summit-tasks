import pickle, random, sys
import numpy as np, networkx as nx
from layout import G, crossings, min_vertex_edge, min_vertex_dist, normalise
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
best = pickle.load(open("layouts.pkl", "rb"))
def score(pos):
    c = crossings(pos); ve = min_vertex_edge(pos); vv = min_vertex_dist(pos)
    return (c, -min(ve, 0.11), -min(vv, 0.24))
results = []
for c0, _, _, seed, kind, pos0 in best[:3]:
    pos = {v: np.array(p) for v, p in pos0.items()}; sc = score(pos)
    for it in range(6000):
        v = random.choice(list(G.nodes()))
        old = pos[v].copy()
        pos[v] = old + np.random.normal(0, 0.06 if it < 3000 else 0.025, 2)
        pos[v] = np.clip(pos[v], 0, 1)
        new = score(pos)
        if new <= sc: sc = new
        else: pos[v] = old
    pos = normalise(pos); sc = score(pos)
    print(f"start {kind} {seed}: crossings {sc[0]}, min vertex-edge {-sc[1]:.3f}, min vertex-vertex {-sc[2]:.3f}", flush=True)
    results.append((sc, seed, kind, pos)); pickle.dump(results, open(f"hill_{sys.argv[1] if len(sys.argv) > 1 else 0}.pkl", "wb"))
results.sort(key=lambda t: t[0])
pickle.dump(results, open(f"hill_{sys.argv[1] if len(sys.argv) > 1 else 0}.pkl", "wb"))
