"""S-N figure for task09 v6: semi-log (linear stress amplitude, log cycles with 1-2-5 gridlines), Basquin fit through two exact gridline crossings, knee at 1e7."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, MultipleLocator
N1, S1, N2, S2 = 5e4, 310.0, 2e6, 230.0; NE = 1e7
k = math.log(N2 / N1) / math.log(S1 / S2); A = S1 * N1 ** (1 / k); se = A * NE ** (-1 / k)
def sn(n): return A * n ** (-1 / k)
fig, ax = plt.subplots(figsize=(7.4, 5.2))
ax.set_xscale("log"); ax.set_xlim(1e4, 1e8); ax.set_ylim(150, 400)
XL = sorted(v * m for v in (1e4, 1e5, 1e6, 1e7) for m in (1, 2, 5)) + [1e8]
def lab(v):
    e = int(math.floor(math.log10(v))); m = v / 10 ** e
    return (r"$10^{%d}$" % e) if abs(m - 1) < 1e-9 else (r"$%d \times 10^{%d}$" % (round(m), e))
ax.xaxis.set_major_locator(FixedLocator(XL)); ax.xaxis.set_major_formatter(FixedFormatter([lab(v) for v in XL])); ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_locator(MultipleLocator(50)); ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.grid(True, which="major", axis="x", color="0.5", lw=0.8); ax.grid(True, which="major", axis="y", color="0.5", lw=0.8); ax.grid(True, which="minor", axis="y", color="0.8", lw=0.5)
xs = [1e4 * 10 ** (i / 300) for i in range(0, 901)]
ax.plot(xs, [sn(x) for x in xs], "-", color="black", lw=1.3, label="Basquin fit, knee at $10^7$ cycles")
ax.plot([NE, 1e8], [se, se], "-", color="black", lw=1.3)
pts = [1.4e4, 3e4, 7e4, 1.5e5, 3.5e5, 7e5, 1.4e6, 3.5e6, 7e6]
ax.plot(pts, [sn(p) for p in pts], "o", color="black", ms=6, label="failures, MIM Ti-6Al-7Nb, $R=-1$")
ax.plot([2e7, 5e7], [se, se], ">", color="black", ms=7, mfc="white", label="run-outs")
ax.set_xlabel("cycles to failure $N$"); ax.set_ylabel("stress amplitude (MPa)")
ax.tick_params(axis="x", labelsize=8.5)
ax.legend(loc="upper right", fontsize=8.5, frameon=True)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written; k", round(k, 4), "A", round(A, 2), "sigma_e", round(se, 2), "points", [(p, round(sn(p), 1)) for p in pts])
