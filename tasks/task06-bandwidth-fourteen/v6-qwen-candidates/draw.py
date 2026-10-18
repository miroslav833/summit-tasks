import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
# candidate 1: two-state generator
fig, ax = plt.subplots(figsize=(6.4, 3.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
for x, name, ph, pt in ((2.5, "A", "3/4", "1/4"), (7.5, "B", "1/4", "3/4")):
    ax.add_patch(FancyBboxPatch((x - 1.1, 1.3), 2.2, 2.4, boxstyle="round,pad=0.05", fc="white", ec="black", lw=1.5))
    ax.text(x, 3.15, name, ha="center", va="center", fontsize=15, weight="bold")
    ax.text(x, 2.4, f"H: {ph}", ha="center", va="center", fontsize=12); ax.text(x, 1.8, f"T: {pt}", ha="center", va="center", fontsize=12)
ax.add_patch(FancyArrowPatch((3.7, 3.1), (6.3, 3.1), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=16, lw=1.3))
ax.add_patch(FancyArrowPatch((6.3, 1.9), (3.7, 1.9), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=16, lw=1.3))
ax.text(5, 4.0, "switch after each emission", ha="center", fontsize=10); ax.text(5, 1.0, "switch after each emission", ha="center", fontsize=10)
ax.add_patch(FancyArrowPatch((0.2, 2.5), (1.35, 2.5), arrowstyle="-|>", mutation_scale=14, lw=1.2, ls="--"))
ax.text(0.2, 2.85, "start", fontsize=10)
fig.tight_layout(); fig.savefig("cand1.png", dpi=300, facecolor="white"); plt.close(fig)
# candidate 2: cube drawing, L and W opposite, thick edge L-a with label 2
P = {"L": (0, 0), "a": (2.4, 0), "s": (0, 2.4), "b": (1.0, 0.9), "c": (2.4, 2.4), "d": (3.4, 0.9), "e": (1.0, 3.3), "W": (3.4, 3.3)}
E = [("L","a",2), ("L","s",1), ("L","b",1), ("a","c",1), ("a","d",1), ("s","c",1), ("s","e",1), ("b","d",1), ("b","e",1), ("c","W",1), ("d","W",1), ("e","W",1)]
fig, ax = plt.subplots(figsize=(5.6, 5.4))
for u, v, w in E:
    (x1, y1), (x2, y2) = P[u], P[v]
    ax.plot([x1, x2], [y1, y2], color="black", lw=4.5 if w == 2 else 1.4, zorder=1)
    if w == 2: ax.text((x1 + x2) / 2, (y1 + y2) / 2 - 0.22, "2", ha="center", fontsize=12)
for v, (x, y) in P.items():
    ax.scatter([x], [y], s=650, fc="white", ec="black", lw=1.6, zorder=3)
    if v == "s": ax.scatter([x], [y], s=1000, fc="none", ec="black", lw=1.2, zorder=2)
    ax.text(x, y, v, ha="center", va="center", fontsize=13, zorder=4)
ax.text(1.7, -0.75, "thin edges: conductance 1    thick edge: conductance 2    start at s", ha="center", fontsize=9.5)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6, 4.0); ax.set_ylim(-1.0, 3.9)
fig.tight_layout(); fig.savefig("cand2.png", dpi=300, facecolor="white"); plt.close(fig)
print("drawn")
