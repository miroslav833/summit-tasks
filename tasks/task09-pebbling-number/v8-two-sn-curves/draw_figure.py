"""S-N figure for task09 v8: two Basquin fits (R = -1 and R = 0.1) on semi-log axes with 1-2-5 cycle gridlines and 10 MPa stress gridlines; each fit passes through two exact gridline crossings; knees at 1e7."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, MultipleLocator
NE = 1e7
def fit(n1, s1, n2, s2):
    k = math.log(n2 / n1) / math.log(s1 / s2); return k, s1 * n1 ** (1 / k)
K1, A1 = fit(5e4, 310, 2e6, 230); K2, A2 = fit(2e5, 240, 5e6, 190)
se1, se2 = A1 * NE ** (-1 / K1), A2 * NE ** (-1 / K2)
fig, ax = plt.subplots(figsize=(7.4, 5.2))
ax.set_xscale("log"); ax.set_xlim(1e4, 1e8); ax.set_ylim(100, 400)
XL = sorted(v * m for v in (1e4, 1e5, 1e6, 1e7) for m in (1, 2, 5)) + [1e8]
def lab(v):
    e = int(math.floor(math.log10(v))); m = v / 10 ** e
    return (r"$10^{%d}$" % e) if abs(m - 1) < 1e-9 else (r"$%d \times 10^{%d}$" % (round(m), e))
ax.xaxis.set_major_locator(FixedLocator(XL)); ax.xaxis.set_major_formatter(FixedFormatter([lab(v) for v in XL])); ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_locator(MultipleLocator(50)); ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.grid(True, which="major", axis="x", color="0.5", lw=0.8); ax.grid(True, which="major", axis="y", color="0.5", lw=0.8); ax.grid(True, which="minor", axis="y", color="0.8", lw=0.5)
xs = [1e4 * 10 ** (i / 300) for i in range(0, 901)]
ax.plot(xs, [A1 * x ** (-1 / K1) for x in xs], "-", color="black", lw=1.3, label="fit, $R=-1$, knee at $10^7$"); ax.plot([NE, 1e8], [se1, se1], "-", color="black", lw=1.3)
ax.plot(xs, [A2 * x ** (-1 / K2) for x in xs], "--", color="black", lw=1.3, label="fit, $R=0.1$, knee at $10^7$"); ax.plot([NE, 1e8], [se2, se2], "--", color="black", lw=1.3)
p1 = [1.4e4, 3e4, 7e4, 1.5e5, 3.5e5, 7e5, 1.4e6, 3.5e6, 7e6]; p2 = [1.4e4, 3.5e4, 8e4, 1.5e5, 3.5e5, 8e5, 1.5e6, 3.5e6, 7e6]
ax.plot(p1, [A1 * p ** (-1 / K1) for p in p1], "o", color="black", ms=5.5, label="failures, $R=-1$")
ax.plot(p2, [A2 * p ** (-1 / K2) for p in p2], "s", color="black", mfc="white", ms=5.5, label="failures, $R=0.1$")
ax.plot([2e7, 5e7], [se1, se1], ">", color="black", ms=7, mfc="white"); ax.plot([2e7, 5e7], [se2, se2], ">", color="black", ms=7, mfc="white", label="run-outs")
ax.set_xlabel("cycles to failure $N$"); ax.set_ylabel("stress amplitude (MPa)"); ax.tick_params(axis="x", labelsize=8.5)
ax.legend(loc="upper right", fontsize=8.5, frameon=True)
fig.tight_layout(pad=0.4); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
print("figure written; K1", round(K1, 4), "A1", round(A1, 2), "se1", round(se1, 2), "K2", round(K2, 4), "A2", round(A2, 2), "se2", round(se2, 2))
