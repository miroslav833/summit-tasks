"""Figure for task09 v2: 13-vertex, 19-edge planar graph, target vertex 9 drawn with a double circle."""
import json, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
g = json.load(open("graph.json")); EDGES = [tuple(e) for e in g["edges"]]; POS = {int(k): v for k, v in g["pos"].items()}; T = g["target"]
def crossings():
    def o(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    def cross(p1, p2, p3, p4): return (o(p1,p2,p3)*o(p1,p2,p4) < 0) and (o(p3,p4,p1)*o(p3,p4,p2) < 0)
    return sum(1 for i in range(len(EDGES)) for j in range(i+1, len(EDGES)) if len(set(EDGES[i]+EDGES[j])) == 4 and cross(POS[EDGES[i][0]], POS[EDGES[i][1]], POS[EDGES[j][0]], POS[EDGES[j][1]]))
assert crossings() == 0
out = sys.argv[1] if len(sys.argv) > 1 else "image.png"
fig, ax = plt.subplots(figsize=(7.0, 6.5))
for u, v in EDGES: ax.plot([POS[u][0], POS[v][0]], [POS[u][1], POS[v][1]], color="black", lw=1.4, zorder=1)
for v, (x, y) in POS.items():
    if v == T: ax.scatter([x], [y], s=820, facecolor="white", edgecolor="black", linewidth=1.5, zorder=2)
    ax.scatter([x], [y], s=420, facecolor="white", edgecolor="black", linewidth=1.5, zorder=3)
    ax.text(x, y, str(v), ha="center", va="center", fontsize=11, zorder=4)
ax.set_aspect("equal"); ax.axis("off")
xs = [p[0] for p in POS.values()]; ys = [p[1] for p in POS.values()]
ax.set_xlim(min(xs) - 0.12, max(xs) + 0.12); ax.set_ylim(min(ys) - 0.12, max(ys) + 0.12)
fig.tight_layout(pad=0.3); fig.savefig(out, dpi=300, facecolor="white"); fig.savefig(out.replace(".png", ".pdf"), facecolor="white")
print("figure written, crossings", crossings())
