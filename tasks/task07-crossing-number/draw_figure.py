"""Figure for the crack-growth task: log-log da/dN against delta K for two load ratios, generated from
the model in work/model.py.  The straight lines are the Paris fits; each passes exactly through the
two anchor points marked with crosses on gridline intersections.  Writes image.png (300 dpi) and
image.pdf next to this script."""
import pathlib, math, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "work"))
import model as M

rng = np.random.default_rng(7)


def points(U, dK_values):
    """Model rates with a near-threshold knee and small scatter, for the plotted data symbols."""
    out = []
    for k in dK_values:
        ke = U * k
        if ke <= M.dKth_eff:
            continue
        rate = M.C * ke ** M.n * (1 - (M.dKth_eff / ke) ** 2) ** 1.5
        rate *= math.exp(rng.normal(0, 0.06))
        out.append((k, rate))
    return out


def draw(outstem="image"):
    fig, ax = plt.subplots(figsize=(6.4, 5.6), dpi=300)
    k05 = [2.8, 3.0, 3.3, 3.6, 4.0, 4.5, 5, 6, 7, 8, 10, 12, 15, 18, 22, 27, 33, 40]
    k01 = [5.5, 6.0, 6.5, 7.2, 8, 9, 10, 12, 14, 17, 20, 24, 29, 35]
    p05 = points(M.U05, k05); p01 = points(M.U01, k01)
    ax.loglog([p[0] for p in p01], [p[1] for p in p01], "o", ms=5.5, mfc="black", mec="black", label="$R = 0.1$", zorder=4)
    ax.loglog([p[0] for p in p05], [p[1] for p in p05], "s", ms=5.5, mfc="white", mec="black", mew=1.1, label="$R = 0.5$", zorder=4)
    # Paris fit lines over the Paris regime, through the anchors
    kk = np.array([3.6, 60.0])
    ax.loglog(kk, M.C * (M.U05 * kk) ** M.n, "-", color="0.2", lw=1.1, zorder=3, label="Paris fit, $R = 0.5$")
    kk1 = np.array([7.0, 100.0])
    ax.loglog(kk1, M.C * (M.U01 * kk1) ** M.n, "--", color="0.2", lw=1.1, zorder=3, label="Paris fit, $R = 0.1$")
    anchors = [(5, 1e-9), (50, 1e-6), (10, 1e-9), (100, 1e-6)]
    ax.loglog([a[0] for a in anchors], [a[1] for a in anchors], "+", color="black", ms=11, mew=1.6, zorder=5, label="fit anchors (on gridlines)")
    ax.set_xlim(2, 120); ax.set_ylim(1e-11, 1e-5)
    ax.set_xlabel(r"$\Delta K$  (MPa$\sqrt{\mathrm{m}}$)")
    ax.set_ylabel(r"$\mathrm{d}a/\mathrm{d}N$  (m/cycle)")
    ax.set_xticks([2, 3, 5, 10, 20, 30, 50, 100]); ax.set_xticklabels(["2", "3", "5", "10", "20", "30", "50", "100"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.grid(True, which="major", color="0.75", lw=0.6)
    ax.grid(True, which="minor", color="0.9", lw=0.4)
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / f"{outstem}.png", dpi=300, facecolor="white")
    fig.savefig(HERE / f"{outstem}.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw()
    print("figure written")
