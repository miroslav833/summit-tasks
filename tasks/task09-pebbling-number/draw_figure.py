import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, sys
sys.path.insert(0, "..")
EDGES = [(1,2),(1,3),(1,6),(2,3),(2,8),(3,5),(4,6),(4,7),(5,7),(6,7),(6,9),(7,8),(8,10),(9,10)]
POS = {1: (0.0, 2.0), 2: (3.0, 2.0), 3: (1.5, 1.55), 4: (0.55, 0.85), 5: (1.5, 0.95),
       6: (-0.5, 0.25), 7: (1.5, 0.3), 8: (3.5, 0.25), 9: (0.6, -0.6), 10: (2.4, -0.6)}
out = sys.argv[1] if len(sys.argv) > 1 else "image.png"
fig, ax = plt.subplots(figsize=(6.4, 5.2))
for u, v in EDGES:
    ax.plot([POS[u][0], POS[v][0]], [POS[u][1], POS[v][1]], color="black", lw=1.4, zorder=1)
for v, (x, y) in POS.items():
    if v == 3:
        ax.scatter([x], [y], s=900, facecolor="white", edgecolor="black", linewidth=1.5, zorder=2)
    ax.scatter([x], [y], s=460, facecolor="white", edgecolor="black", linewidth=1.5, zorder=3)
    ax.text(x, y, str(v), ha="center", va="center", fontsize=11, zorder=4)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.85, 3.85); ax.set_ylim(-0.95, 2.35)
fig.tight_layout(pad=0.3); fig.savefig(out, dpi=300, facecolor="white"); fig.savefig(out.replace(".png", ".pdf"), facecolor="white")
