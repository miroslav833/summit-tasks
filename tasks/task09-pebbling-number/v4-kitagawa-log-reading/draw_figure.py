"""Kitagawa diagram for task09 v4: standard logarithmic axes (decade labels, unlabelled minor gridlines at 2..9), points off the gridlines."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter
HV = 320; DK = 200.0 * 0.50 * math.sqrt(math.pi * 600e-6)
def sw(s): return min(1.43 * (HV + 120) / s ** (1 / 6), DK / (0.65 * math.sqrt(math.pi * s * 1e-6)))
pts = [25, 50, 90, 170, 480, 650, 850, 1100]
fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.set_xscale("log"); ax.set_yscale("log")
ax.xaxis.set_major_locator(LogLocator(base=10, numticks=6)); ax.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
ax.xaxis.set_minor_locator(LogLocator(base=10, subs=range(2, 10), numticks=12)); ax.yaxis.set_minor_locator(LogLocator(base=10, subs=range(2, 10), numticks=12))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}")); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax.xaxis.set_minor_formatter(NullFormatter()); ax.yaxis.set_minor_formatter(NullFormatter())
ax.grid(True, which="major", color="0.5", lw=0.9); ax.grid(True, which="minor", color="0.85", lw=0.5)
ax.plot(pts, [sw(s) for s in pts], "o", color="black", ms=6, label="Ti-6Al-7Nb (MIM), 0.20 wt% O, 320 HV, surface drilled holes, $R=-1$, $10^7$ cycles")
ax.set_xlim(10, 10000); ax.set_ylim(50, 1000)
ax.set_xlabel(r"$\sqrt{\mathrm{area}}$ of the defect ($\mu$m)"); ax.set_ylabel("fatigue limit, stress amplitude (MPa)")
ax.legend(loc="upper right", fontsize=8.5, frameon=True)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written; points:", [(s, round(sw(s), 1)) for s in pts])
