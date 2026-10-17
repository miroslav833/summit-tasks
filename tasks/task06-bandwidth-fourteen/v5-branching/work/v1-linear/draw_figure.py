"""Figure: offspring generating function f(s) = (1 + (m/r)(1-s))^(-r) of a Galton-Watson process on [0, 1], with the
diagonal y = s. Gridlines every 0.1 on both axes, every gridline labelled. The parameters are fixed by the two exact
crossings (0, 0.4) and (0.4, 0.5); nothing else is marked."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
def f(s, m, r): return (1 + (m / r) * (1 - s)) ** (-r)
def params():
    def eqs(x):
        m, lr = x; r = math.exp(lr); return [f(0.0, m, r) - 0.4, f(0.4, m, r) - 0.5]
    m, lr = fsolve(eqs, [2.2, math.log(0.6)], xtol=1e-14); return m, math.exp(lr)
if __name__ == "__main__":
    m, r = params()
    s = np.linspace(0, 1, 2001)
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    ax.plot(s, f(s, m, r), color="black", lw=1.8, zorder=3)
    ax.plot([0, 1], [0, 1], color="black", lw=1.0, ls="--", zorder=2)
    ticks = [round(0.1 * i, 1) for i in range(11)]
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.set_xticklabels([f"{t:g}" for t in ticks]); ax.set_yticklabels([f"{t:g}" for t in ticks])
    ax.grid(True, color="0.55", lw=0.6, zorder=1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("$s$", fontsize=13); ax.set_ylabel("$f(s)$", fontsize=13)
    ax.text(0.25, 0.205, "$y = s$", fontsize=11, rotation=45, ha="center", va="center", backgroundcolor="white")
    fig.tight_layout(); fig.savefig("image.png", dpi=300, facecolor="white"); fig.savefig("image.pdf", facecolor="white")
    print(f"m = {m:.10f}, r = {r:.10f}")
