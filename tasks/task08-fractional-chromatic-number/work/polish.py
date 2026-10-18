import pickle, random, sys, math
import numpy as np, networkx as nx
from layout import G, crossings, min_vertex_edge, min_vertex_dist, normalise
random.seed(int(sys.argv[1])); np.random.seed(int(sys.argv[1]))
res = pickle.load(open("hill2_7.pkl", "rb")) + pickle.load(open("hill2_8.pkl", "rb"))
res = [r for r in res if r[0][1] < -0.09 and r[0][2] < -0.19]
def min_angle(pos):
    m = math.pi
    for v in G.nodes():
        angs = sorted(math.atan2(pos[u][1] - pos[v][1], pos[u][0] - pos[v][0]) for u in G[v])
        for i in range(len(angs)):
            dgap = (angs[(i + 1) % len(angs)] - angs[i]) % (2 * math.pi)
            m = min(m, dgap)
    return m
def score(pos):
    c = crossings(pos); ve = min_vertex_edge(pos); vv = min_vertex_dist(pos); ang = min_angle(pos)
    return (c, -min(ve, 0.11), -min(ang, math.radians(28)), -min(vv, 0.22))
out = []
for sc0, seed, kind, pos0 in res:
    pos = {v: np.array(p) for v, p in pos0.items()}; sc = score(pos)
    for it in range(6000):
        v = random.choice(list(G.nodes())); old = pos[v].copy()
        pos[v] = np.clip(old + np.random.normal(0, 0.05 if it < 3000 else 0.02, 2), 0, 1)
        new = score(pos)
        if new <= sc: sc = new
        else: pos[v] = old
    pos = normalise(pos); sc = score(pos)
    print(f"{kind} {seed}: crossings {sc[0]}, ve {-sc[1]:.3f}, min angle {math.degrees(-sc[2]):.1f} deg, vv {-sc[3]:.3f}", flush=True)
    out.append((sc, seed, kind, pos)); pickle.dump(sorted(out, key=lambda t: t[0]), open(f"polish_{sys.argv[1]}.pkl", "wb"))
