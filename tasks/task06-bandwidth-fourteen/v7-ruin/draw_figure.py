"""Claim-size survival function S(t) = (1 + t/sigma)^(-alpha) (Lomax) on log-log axes, 1-2-5 gridlines on the vertical
axis, labelled abscissae with vertical gridlines; drawn exactly through the crossings (5, 0.02) and (20, 0.0005)."""
import math, sys, pathlib, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).parent / "work"))
from search import fit
(s, a), = fit(5, 0.02, 20, 0.0005)
t = np.logspace(0, 2, 1200); S = (1 + t / s) ** (-a)
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=300)
ax.loglog(t, S, "-", color="0.15", lw=1.4)
ax.set_xlim(1, 100); ax.set_ylim(1e-5, 1)
ticks = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100]
ax.set_xticks(ticks); ax.set_xticklabels([str(x) for x in ticks])
ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10, subs=(2.0, 5.0), numticks=12))
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.grid(True, which="major", color="0.6", lw=0.7); ax.grid(True, which="minor", color="0.78", lw=0.5)
ax.set_xlabel("$t$"); ax.set_ylabel("$S(t) = P(X > t)$")
fig.tight_layout(); fig.savefig("image.png"); fig.savefig("image.pdf"); print(f"sigma={s:.6f} alpha={a:.6f}")
