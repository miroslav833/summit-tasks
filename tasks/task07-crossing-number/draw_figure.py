"""Figure for the crossing-number task: the graph drawn with its vertices on a circle (a circular
layout gives nothing away about the optimal drawing).  Writes image.png (300 dpi) and image.pdf."""
import math, sys, ast, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
TASK = HERE.parent if HERE.name == "work" else HERE


def draw(edges, order=None, outstem="image"):
    verts = sorted({v for e in edges for v in e})
    if order is None:
        order = verts
    n = len(order)
    R = 1.0
    pos = {}
    for i, v in enumerate(order):
        ang = math.pi / 2 - 2 * math.pi * i / n   # vertex 1 at the top, then clockwise
        pos[v] = (R * math.cos(ang), R * math.sin(ang))
    fig, ax = plt.subplots(figsize=(5.2, 5.2), dpi=300)
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        ax.plot([x1, x2], [y1, y2], color="0.25", lw=1.1, zorder=1, solid_capstyle="round")
    for v in verts:
        x, y = pos[v]
        ax.add_patch(plt.Circle((x, y), 0.085, facecolor="white", edgecolor="black", lw=1.2, zorder=3))
        ax.text(x, y, str(v), ha="center", va="center", fontsize=10.5, zorder=4)
    ax.set_xlim(-1.18, 1.18); ax.set_ylim(-1.18, 1.18)
    ax.set_aspect("equal"); ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(TASK / f"{outstem}.png", dpi=300, facecolor="white")
    fig.savefig(TASK / f"{outstem}.pdf", facecolor="white")
    plt.close(fig)
    return pos


if __name__ == "__main__":
    edges = ast.literal_eval(open(HERE / "chosen_edges.txt").read()) if len(sys.argv) < 2 else ast.literal_eval(sys.argv[1])
    draw(edges)
    print("drawn", len(edges), "edges")
