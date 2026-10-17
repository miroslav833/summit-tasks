"""Figure: offspring probabilities p_k = P(X = k), k = 0..9, of a negative binomial law (shape r, mean m) on a
logarithmic vertical axis with gridlines at 1, 2 and 5 times every power of ten (decades labelled). The law is fixed
by the two points that lie exactly on gridlines, p_0 = 0.5 and p_7 = 0.02; every other point is between gridlines."""
import math, sys, pathlib, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullFormatter
sys.path.insert(0, str(pathlib.Path(__file__).parent / "work"))
from search_pmf import pmf, fit
def params():
    (m, r), = [s for s in fit(0, 0.5, 7, 0.02) if 2 < s[0] < 3]; return m, r
if __name__ == "__main__":
    m, r = params(); p = pmf(m, r)[:10]
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    ax.set_yscale("log"); ax.set_ylim(0.01, 1); ax.set_xlim(-0.6, 9.6)
    major = [0.01, 0.1, 1]; minor = [c * 10.0 ** e for e in (-2, -1) for c in (2, 5)]
    ax.yaxis.set_major_locator(FixedLocator(major)); ax.yaxis.set_minor_locator(FixedLocator(minor))
    ax.yaxis.set_minor_formatter(NullFormatter()); ax.set_yticklabels(["0.01", "0.1", "1"])
    ax.set_xticks(range(10))
    ax.grid(True, which="major", axis="y", color="0.45", lw=0.8); ax.grid(True, which="minor", axis="y", color="0.65", lw=0.6)
    ax.vlines(range(10), 0.01, p, color="0.3", lw=1.0, zorder=2)
    ax.plot(range(10), p, "o", color="black", ms=6, zorder=3)
    ax.set_xlabel("$k$", fontsize=13); ax.set_ylabel("$P(X = k)$", fontsize=13)
    fig.tight_layout(); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
    print(f"m = {m:.10f}, r = {r:.10f}"); print("p:", [f"{v:.5g}" for v in p])
