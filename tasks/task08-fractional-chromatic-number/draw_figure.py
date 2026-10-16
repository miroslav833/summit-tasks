"""Draws the figure for task08: a 4-regular graph on 12 vertices, straight-line drawing with vertex labels 1 to 12.
Coordinates were found by a spring layout followed by a hill-climb on (number of crossings, distance of every
vertex from every non-incident edge, angular resolution at the vertices).  Produces image.png (300 dpi) and
image.pdf.  Run: python3 draw_figure.py"""
import math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EDGES = [(1, 5), (1, 8), (1, 9), (1, 10), (2, 3), (2, 7), (2, 9), (2, 10), (3, 5), (3, 6), (3, 12), (4, 6),
         (4, 9), (4, 11), (4, 12), (5, 7), (5, 12), (6, 7), (6, 8), (7, 11), (8, 10), (8, 11), (9, 10), (11, 12)]
POS = {1: (0.32, 0.759), 2: (0.009, 0.367), 3: (0.209, 0.0), 4: (0.673, 0.698), 5: (0.481, 0.178), 6: (0.505, 0.551), 7: (0.615, 0.358), 8: (0.532, 1.0), 9: (0.157, 0.602), 10: (0.0, 0.831), 11: (0.994, 0.651), 12: (0.777, 0.041)}

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
    assert len(EDGES) == 24 and set(deg.values()) == {4}

def draw(out="image"):
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    for u, v in EDGES:
        ax.plot([POS[u][0], POS[v][0]], [POS[u][1], POS[v][1]], color="black", lw=1.5, zorder=1, solid_capstyle="round")
    for v, (x, y) in POS.items():
        ax.scatter([x], [y], s=520, facecolor="white", edgecolor="black", linewidth=1.6, zorder=3)
        ax.text(x, y, str(v), ha="center", va="center", fontsize=12, zorder=4)
    ax.set_aspect("equal"); ax.axis("off")
    xs = [p[0] for p in POS.values()]; ys = [p[1] for p in POS.values()]
    ax.set_xlim(min(xs) - 0.08, max(xs) + 0.08); ax.set_ylim(min(ys) - 0.08, max(ys) + 0.08)
    fig.tight_layout(pad=0.2)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    check(); draw()
