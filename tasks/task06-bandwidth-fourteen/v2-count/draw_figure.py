"""Figure for task06 v2: the 14-vertex graph of task06 with two more edges (6-7 and 6-10), 29 edges.
Positions start from the task06 layout (work/chosen.pkl of the parent task) and are relaxed with the
parent's spring step; the drawing is then checked for crossings and for label spacing."""
import pickle, sys, pathlib, itertools
import numpy as np, networkx as nx
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "work"))
from draw_graph import draw, crossings, relax
EDGES = [(1, 2), (1, 4), (1, 6), (1, 8), (1, 11), (1, 14), (2, 8), (3, 7), (3, 8), (3, 10), (3, 12), (3, 13),
         (4, 10), (4, 11), (4, 13), (4, 14), (5, 9), (5, 12), (6, 7), (6, 9), (6, 10), (6, 11), (7, 8), (7, 11),
         (9, 13), (9, 14), (11, 13), (11, 14), (12, 14)]
assert len(EDGES) == 29
G = nx.Graph(EDGES)
d = pickle.load(open(HERE.parent / "work" / "chosen.pkl", "rb"))
pos = {v: np.array(p, dtype=float) for v, p in d["pos"].items()}
print("crossings with the parent positions:", crossings(G, pos))
# move vertex 6 to a spot where its five edges cross little; try a grid of candidate positions
best = None
for x in np.linspace(-1.0, 1.0, 41):
    for y in np.linspace(-1.1, 0.9, 41):
        p = dict(pos); p[6] = np.array([x, y])
        dmin = min(np.linalg.norm(p[6] - p[v]) for v in G.nodes() if v != 6)
        if dmin < 0.28: continue
        c = crossings(G, p)
        if best is None or c < best[0]: best = (c, x, y)
print("best position for 6:", best)
pos[6] = np.array(best[1:])
print("crossings after moving 6:", crossings(G, pos))
dmin = min(np.linalg.norm(pos[u] - pos[v]) for u, v in itertools.combinations(G.nodes(), 2))
print("smallest vertex distance:", round(dmin, 3))
pickle.dump({"G": G, "pos": pos}, open(HERE / "work" / "figure_pos.pkl", "wb"))
if __name__ == "__main__": draw(G, pos, str(HERE / "image.png"))
if __name__ == "__main__": print("written image.png / image.pdf")
