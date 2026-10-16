"""Kitagawa diagram for task09 v3: fatigue limit against sqrt(area) of surface drilled holes, log-log, from the model in verify_key.py."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter
HV = 320; DK = 150.0 * 0.65 * math.sqrt(math.pi * 640e-6)
def sw(s): return min(1.43 * (HV + 120) / s ** (1 / 6), DK / (0.65 * math.sqrt(math.pi * s * 1e-6)))
pts = [20, 40, 80, 160, 320, 640, 1280, 2560]
fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.set_xscale("log"); ax.set_yscale("log")
xt = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]; yt = [50, 75, 100, 150, 200, 300, 400, 500]
ax.xaxis.set_major_locator(FixedLocator(xt)); ax.xaxis.set_major_formatter(FixedFormatter([str(v) for v in xt]))
ax.yaxis.set_major_locator(FixedLocator(yt)); ax.yaxis.set_major_formatter(FixedFormatter([str(v) for v in yt]))
ax.xaxis.set_minor_locator(FixedLocator([v * m for v in (10, 100, 1000) for m in range(1, 10)] + [5000]))
ax.yaxis.set_minor_locator(FixedLocator(list(range(50, 100, 10)) + list(range(100, 500, 50)) + [500]))
ax.xaxis.set_minor_formatter(NullFormatter()); ax.yaxis.set_minor_formatter(NullFormatter())
ax.grid(True, which="major", color="0.55", lw=0.8); ax.grid(True, which="minor", color="0.85", lw=0.5)
ax.plot([s for s in pts], [sw(s) for s in pts], "o", color="black", ms=6, label="Ti-6Al-7Nb (MIM), 0.20 wt% O, 320 HV, surface drilled holes, $R=-1$, $10^7$ cycles")
ax.set_xlim(10, 5000); ax.set_ylim(50, 500)
ax.set_xlabel(r"$\sqrt{\mathrm{area}}$ of the defect ($\mu$m)"); ax.set_ylabel("fatigue limit, stress amplitude (MPa)")
ax.legend(loc="upper right", fontsize=8.5, frameon=True)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written; points:", [(s, round(sw(s), 1)) for s in pts])
