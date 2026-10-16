"""Figure for the crossing-number task: a straight-line drawing of the graph with exactly four
crossings (coordinates chosen by a layout search for clarity).  Writes image.png (300 dpi) and
image.pdf next to this script."""
import pathlib, itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
EDGES = [(1, 2), (1, 5), (1, 9), (1, 10), (2, 3), (2, 4), (2, 6), (3, 5), (3, 6), (3, 8), (3, 9), (4, 5), (4, 6), (4, 8), (4, 10), (5, 6), (6, 7), (7, 8), (7, 9), (7, 10), (8, 10)]
COORDS = {1: (0, 1), 2: (0, 20), 3: (17, 17), 4: (6, 7), 5: (6, 13), 6: (12, 12), 7: (10, 7), 8: (12, 3), 9: (19, 0), 10: (4, 3)}


def draw(pos=COORDS, edges=EDGES, outstem="image"):
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    fig, ax = plt.subplots(figsize=(6.0, 6.0 * (h + 2.4) / (w + 2.4)), dpi=300)
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        ax.plot([x1, x2], [y1, y2], color="0.25", lw=1.2, zorder=1, solid_capstyle="round")
    r = 0.55
    for v, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), r, facecolor="white", edgecolor="black", lw=1.2, zorder=3))
        ax.text(x, y, str(v), ha="center", va="center", fontsize=10.5, zorder=4)
    ax.set_xlim(min(xs) - 1.2, max(xs) + 1.2); ax.set_ylim(min(ys) - 1.2, max(ys) + 1.2)
    ax.set_aspect("equal"); ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(HERE / f"{outstem}.png", dpi=300, facecolor="white")
    fig.savefig(HERE / f"{outstem}.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw()
    print("drawn", len(EDGES), "edges")
