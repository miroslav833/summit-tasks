"""Find a clean straight-line drawing of the graph: few crossings, no vertex near a non-incident edge."""
import sys, pickle
import numpy as np, networkx as nx
sys.path.insert(0, "..")
import importlib.util
spec = importlib.util.spec_from_file_location("vk", "../verify_key.py")
EDGES = [(1, 5), (1, 8), (1, 9), (1, 10), (2, 3), (2, 7), (2, 9), (2, 10), (3, 5), (3, 6), (3, 12), (4, 6),
         (4, 9), (4, 11), (4, 12), (5, 7), (5, 12), (6, 7), (6, 8), (7, 11), (8, 10), (8, 11), (9, 10), (11, 12)]
G = nx.Graph(EDGES)

def seg_cross(p1, p2, p3, p4):
    def o(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    return (o(p1, p2, p3)*o(p1, p2, p4) < 0) and (o(p3, p4, p1)*o(p3, p4, p2) < 0)
def crossings(pos):
    E = list(G.edges()); c = 0
    for i in range(len(E)):
        for j in range(i+1, len(E)):
            a, b = E[i]; u, v = E[j]
            if len({a, b, u, v}) < 4: continue
            if seg_cross(pos[a], pos[b], pos[u], pos[v]): c += 1
    return c
def pt_seg_dist(p, a, b):
    p, a, b = map(np.asarray, (p, a, b)); d = b - a
    t = np.clip(np.dot(p - a, d) / np.dot(d, d), 0, 1)
    return np.linalg.norm(p - (a + t * d))
def min_vertex_edge(pos):
    m = 1e9
    for v in G.nodes():
        for a, b in G.edges():
            if v in (a, b): continue
            m = min(m, pt_seg_dist(pos[v], pos[a], pos[b]))
    return m
def min_vertex_dist(pos):
    P = np.array([pos[v] for v in G.nodes()])
    D = np.linalg.norm(P[:, None] - P[None], axis=2) + np.eye(len(P)) * 9
    return D.min()
def normalise(pos):
    P = np.array(list(pos.values())); lo, hi = P.min(0), P.max(0); s = (hi - lo).max()
    return {v: (np.array(p) - lo) / s for v, p in pos.items()}
if __name__ == "__main__":
  best = []
  for seed in range(400):
      for kind in ("spring", "kk"):
          pos = nx.spring_layout(G, seed=seed, iterations=200) if kind == "spring" else nx.kamada_kawai_layout(G, pos=nx.random_layout(G, seed=seed))
          pos = normalise(pos)
          c = crossings(pos); ve = min_vertex_edge(pos); vv = min_vertex_dist(pos)
          best.append((c, -min(ve, 0.12), -vv, seed, kind, pos))
  best.sort(key=lambda t: (t[0], t[1], t[2]))
  for c, ve, vv, seed, kind, pos in best[:10]:
      print(f"crossings={c} min vertex-edge={-ve:.3f} min vertex-vertex={-vv:.3f} seed={seed} {kind}")
  pickle.dump(best[:10], open("layouts.pkl", "wb"))
