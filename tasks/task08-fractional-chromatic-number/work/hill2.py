import pickle, random, sys
import numpy as np, networkx as nx
from layout import G, crossings, min_vertex_edge, min_vertex_dist, normalise
random.seed(int(sys.argv[1])); np.random.seed(int(sys.argv[1]))
res = pickle.load(open("hill_1.pkl", "rb"))
def score(pos):
    c = crossings(pos); ve = min_vertex_edge(pos); vv = min_vertex_dist(pos)
    return (c, -min(ve, 0.11), -min(vv, 0.24))
out = []
for sc0, seed, kind, pos0 in res:
    for rep in range(3):
        pos = {v: np.array(p) for v, p in pos0.items()}; sc = score(pos); T = 0.6
        for it in range(8000):
            v = random.choice(list(G.nodes())); old = pos[v].copy()
            pos[v] = np.clip(old + np.random.normal(0, 0.12 if it < 4000 else 0.03, 2), 0, 1)
            new = score(pos)
            # annealing on crossings only, strict on the distance terms
            if new[0] < sc[0] or (new[0] == sc[0] and new[1:] <= sc[1:]) or (new[0] == sc[0] + 1 and new[1:] <= sc[1:] and random.random() < T * (1 - it / 8000)):
                sc = new
            else: pos[v] = old
        pos = normalise(pos); sc = score(pos)
        print(f"{kind} {seed} rep {rep}: crossings {sc[0]}, ve {-sc[1]:.3f}, vv {-sc[2]:.3f}", flush=True)
        out.append((sc, seed, kind, pos)); pickle.dump(sorted(out, key=lambda t: t[0]), open(f"hill2_{sys.argv[1]}.pkl", "wb"))
