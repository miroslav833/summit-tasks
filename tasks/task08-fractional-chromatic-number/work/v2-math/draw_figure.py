"""Draws the figure for task08 (revision): a planar 4-regular graph on 20 vertices, straight-line planar drawing with
vertex labels 1 to 20.  Coordinates come from a Tutte (barycentric) embedding with a pentagonal outer face, followed
by a planarity-preserving hill-climb on the distance of every vertex from every non-incident edge and on the angular
resolution at the vertices.  Produces image.png (300 dpi) and
image.pdf.  Run: python3 draw_figure.py"""
import math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EDGES = [(1, 2), (1, 3), (1, 5), (1, 6), (2, 4), (2, 6), (2, 9), (3, 4), (3, 11), (3, 15), (4, 17), (4, 20), (5, 6),
         (5, 7), (5, 8), (6, 10), (7, 8), (7, 11), (7, 12), (8, 12), (8, 18), (9, 10), (9, 16), (9, 17), (10, 16),
         (10, 18), (11, 12), (11, 13), (12, 13), (13, 14), (13, 18), (14, 15), (14, 18), (14, 19), (15, 19), (15, 20),
         (16, 17), (16, 19), (17, 20), (19, 20)]
POS = {1: (0.818, 0.505), 2: (0.612, 0.423), 3: (0.984, 0.356), 4: (0.749, 0.334), 5: (0.702, 0.652), 6: (0.533, 0.556), 7: (0.672, 0.826), 8: (0.516, 0.741), 9: (0.406, 0.422), 10: (0.299, 0.539), 11: (0.698, 1.0), 12: (0.365, 0.842), 13: (0.056, 0.999), 14: (0.0, 0.191), 15: (0.452, 0.0), 16: (0.239, 0.355), 17: (0.5, 0.301), 18: (0.286, 0.702), 19: (0.336, 0.237), 20: (0.517, 0.15)}

def seg_cross(p1, p2, p3, p4):
    def o(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    return (o(p1, p2, p3)*o(p1, p2, p4) < 0) and (o(p3, p4, p1)*o(p3, p4, p2) < 0)
def check():
    cr = sum(seg_cross(POS[a], POS[b], POS[u], POS[v]) for i, (a, b) in enumerate(EDGES) for (u, v) in EDGES[i+1:] if len({a, b, u, v}) == 4)
    def dist(p, a, b):
        dx, dy = b[0]-a[0], b[1]-a[1]; t = max(0, min(1, ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / (dx*dx + dy*dy)))
        return math.hypot(p[0] - a[0] - t*dx, p[1] - a[1] - t*dy)
    ve = min(dist(POS[w], POS[a], POS[b]) for (a, b) in EDGES for w in POS if w not in (a, b))
    deg = {v: sum(v in e for e in EDGES) for v in POS}
    print(f"crossings {cr}, smallest vertex to non-incident edge distance {ve:.3f}, degrees {sorted(set(deg.values()))}")
    assert len(EDGES) == 40 and set(deg.values()) == {4} and cr == 0

def draw(out="image"):
    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    for u, v in EDGES:
        ax.plot([POS[u][0], POS[v][0]], [POS[u][1], POS[v][1]], color="black", lw=1.5, zorder=1, solid_capstyle="round")
    for v, (x, y) in POS.items():
        ax.scatter([x], [y], s=430, facecolor="white", edgecolor="black", linewidth=1.6, zorder=3)
        ax.text(x, y, str(v), ha="center", va="center", fontsize=11, zorder=4)
    ax.set_aspect("equal"); ax.axis("off")
    xs = [p[0] for p in POS.values()]; ys = [p[1] for p in POS.values()]
    ax.set_xlim(min(xs) - 0.08, max(xs) + 0.08); ax.set_ylim(min(ys) - 0.08, max(ys) + 0.08)
    fig.tight_layout(pad=0.2)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    check(); draw()
