"""Draws the figure for task08: chart of the forbidden symbol pairs of a six-column array (x1..x5 over {0,1,2}, x6 over
{0,1}).  Produces image.png (300 dpi) and image.pdf.  Run: python3 draw_figure.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

LEVELS = [3, 3, 3, 3, 3, 2]
FORBIDDEN = [((0, 1), (1, 1)), ((0, 1), (2, 2)), ((0, 1), (4, 1)), ((0, 2), (2, 0)), ((0, 2), (3, 0)),
             ((2, 0), (4, 0)), ((2, 1), (5, 0)), ((2, 2), (4, 1)), ((3, 0), (4, 1)), ((3, 2), (5, 0))]

def draw(out="image"):
    cells = [(c, s) for c, l in enumerate(LEVELS) for s in range(l)]; n = len(cells); idx = {cs: i for i, cs in enumerate(cells)}
    starts = [0]
    for l in LEVELS: starts.append(starts[-1] + l)
    fig, ax = plt.subplots(figsize=(8.4, 8.4))
    for i, (ci, _) in enumerate(cells):
        for j, (cj, _) in enumerate(cells):
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor="0.82" if ci == cj else "white", edgecolor="0.6", lw=0.5))
    for a, b in FORBIDDEN:
        for (p, q) in ((idx[a], idx[b]), (idx[b], idx[a])):
            ax.add_patch(Rectangle((q, n - 1 - p), 1, 1, facecolor="black", edgecolor="0.6", lw=0.5))
            ax.text(q + 0.5, n - 1 - p + 0.5, "F", color="white", ha="center", va="center", fontsize=11, fontweight="bold")
    for s in starts:
        ax.plot([s, s], [0, n], color="black", lw=1.6); ax.plot([0, n], [n - s, n - s], color="black", lw=1.6)
    for i, (c, s) in enumerate(cells):
        lab = f"$x_{c + 1} = {s}$"
        ax.text(-0.3, n - 1 - i + 0.5, lab, ha="right", va="center", fontsize=10)
        ax.text(i + 0.5, n + 0.3, lab, ha="center", va="bottom", fontsize=10, rotation=90)
    ax.set_xlim(-3.2, n + 0.2); ax.set_ylim(-1.6, n + 3.2); ax.set_aspect("equal"); ax.axis("off")
    ax.text(n / 2, -0.5, "F: forbidden pair of symbols (no row may contain both).  Grey: same column.", ha="center", va="top", fontsize=10.5)
    fig.tight_layout(pad=0.3)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    draw()
