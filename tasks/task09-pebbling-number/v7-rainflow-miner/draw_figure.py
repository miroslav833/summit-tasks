"""Stress history figure for task09 v7: one period of 24 reversals, values on the 25 MPa gridlines."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
HIST = [-175, 150, -150, 375, 150, 325, -175, 300, -50, 325, 150, 325, 300, 350, -125, 275, -200, 400, -200, 375, 50, 150, -200, 375]
fig, ax = plt.subplots(figsize=(9.0, 4.8))
idx = list(range(1, 25))
ax.plot(idx, HIST, "-", color="black", lw=1.2, zorder=2); ax.plot(idx, HIST, "o", color="black", ms=4.5, zorder=3)
ax.set_xlim(0.5, 24.5); ax.set_ylim(-250, 450)
ax.xaxis.set_major_locator(MultipleLocator(1)); ax.yaxis.set_major_locator(MultipleLocator(100)); ax.yaxis.set_minor_locator(MultipleLocator(25))
ax.grid(True, which="major", axis="y", color="0.5", lw=0.8); ax.grid(True, which="minor", axis="y", color="0.82", lw=0.5); ax.grid(True, which="major", axis="x", color="0.85", lw=0.5)
ax.axhline(0, color="0.3", lw=1.0)
ax.set_xlabel("reversal number within one period"); ax.set_ylabel("stress (MPa)")
ax.tick_params(axis="x", labelsize=8.5)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written")
