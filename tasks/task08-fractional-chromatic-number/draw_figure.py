"""Draws the figure for the covering-array task: a chart of the (column, symbol) cells with the forbidden pairs marked.
Produces image.png (300 dpi) and image.pdf.  Run: python3 draw_figure.py"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

K = 5; S = 3
FORBIDDEN = [((0, 0), (4, 1)), ((0, 1), (1, 0)), ((0, 1), (2, 2)), ((0, 2), (1, 1)), ((1, 1), (2, 1)), ((1, 1), (3, 1)), ((3, 0), (4, 0))]

def draw(out="image"):
    n = K * S
    fig, ax = plt.subplots(figsize=(8.0, 8.0))
    idx = lambda c, s: c * S + s
    for i in range(n):
        for j in range(n):
            ci, cj = i // S, j // S
            if ci == cj:
                ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor="0.82", edgecolor="0.6", lw=0.5))
            else:
                ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor="white", edgecolor="0.6", lw=0.5))
    for (ci, si), (cj, sj) in FORBIDDEN:
        for (a, b) in ((idx(ci, si), idx(cj, sj)), (idx(cj, sj), idx(ci, si))):
            ax.add_patch(Rectangle((b, n - 1 - a), 1, 1, facecolor="black", edgecolor="0.6", lw=0.5))
            ax.text(b + 0.5, n - 1 - a + 0.5, "F", color="white", ha="center", va="center", fontsize=11, fontweight="bold")
    for c in range(K + 1):
        ax.plot([c * S, c * S], [0, n], color="black", lw=1.6); ax.plot([0, n], [c * S, c * S], color="black", lw=1.6)
    labels = [f"$x_{c + 1} = {s}$" for c in range(K) for s in range(S)]
    for i, lab in enumerate(labels):
        ax.text(-0.3, n - 1 - i + 0.5, lab, ha="right", va="center", fontsize=10)
        ax.text(i + 0.5, n + 0.3, lab, ha="center", va="bottom", fontsize=10, rotation=90)
    ax.set_xlim(-3.2, n + 0.2); ax.set_ylim(-0.2, n + 3.2); ax.set_aspect("equal"); ax.axis("off")
    ax.text(n / 2, -0.9, "F: forbidden pair of symbols (no row may contain both).  Grey: same column.", ha="center", va="top", fontsize=10.5)
    fig.tight_layout(pad=0.3)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    draw()
