"""Kitagawa diagram for task09 v5: El Haddad fit through surface drilled-hole data, 1-2-5 logarithmic grid."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
a0 = 200.0 / 3.0; sw0 = 200.0
def curve(s): return sw0 * math.sqrt(a0 / (s + a0))
xs = [15 * 10 ** (i / 200) for i in range(0, 200 * 3)]; xs = [x for x in xs if x <= 8000]
data = [30, 75, 140, 330, 700, 1500, 3500]          # drilled-hole sizes of the specimens, none at a crossing
fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.set_xscale("log"); ax.set_yscale("log")
XL = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]; YL = [20, 50, 100, 200, 500, 1000]
ax.xaxis.set_major_locator(FixedLocator(XL)); ax.xaxis.set_major_formatter(FixedFormatter([str(v) for v in XL])); ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_locator(FixedLocator(YL)); ax.yaxis.set_major_formatter(FixedFormatter([str(v) for v in YL])); ax.yaxis.set_minor_locator(NullLocator())
ax.grid(True, which="major", color="0.55", lw=0.8)
ax.plot(xs, [curve(x) for x in xs], "-", color="black", lw=1.3, label="El Haddad fit")
ax.plot(data, [curve(s) for s in data], "o", color="black", ms=6, label="CP titanium (MIM), surface drilled holes, $R=-1$, $10^7$ cycles")
ax.set_xlim(10, 10000); ax.set_ylim(20, 1000)
ax.set_xlabel(r"$\sqrt{\mathrm{area}}$ of the defect ($\mu$m)"); ax.set_ylabel("fatigue limit, stress amplitude (MPa)")
ax.legend(loc="upper right", fontsize=8.5, frameon=True)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written; data points:", [(s, round(curve(s), 1)) for s in data])
