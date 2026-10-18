import pickle, glob, pathlib, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
M = pickle.load(open(sorted(glob.glob(str(pathlib.Path(__file__).parent / "work" / sys.argv[1])))[0], "rb"))
n, m = len(M), len(M[0])
fig, ax = plt.subplots(figsize=(0.62 * m + 1.6, 0.55 * n + 1.2))
for i, r in enumerate(M):
    for j, x in enumerate(r):
        ax.scatter([j], [-i], s=230, fc="black" if x else "white", ec="black", lw=1.4, zorder=3)
    ax.text(-0.9, -i, f"$s_{{{i+1}}}$", ha="right", va="center", fontsize=12)
for j in range(m): ax.text(j, 0.85, str(j + 1), ha="center", va="center", fontsize=11)
ax.text((m - 1) / 2, 1.55, "position", ha="center", fontsize=11)
ax.set_xlim(-2.0, m - 0.4); ax.set_ylim(-n + 0.4, 2.0); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=300, facecolor="white"); print("ok")
