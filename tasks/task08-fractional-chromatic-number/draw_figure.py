"""Draws the figure for task08 (engineering): long-crack fatigue crack growth data of a MIM Ti-6Al-7Nb alloy at
R = 0.1 and R = 0.7 on log-log axes, generated from the stated model, with the dashed Paris fits.  Produces image.png
(300 dpi) and image.pdf.  Run: python3 draw_figure.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter

C = 1.0e-12; M = 3; DK_TH_EFF = 2.5; KOP_RATIO = 0.55
U01 = (1 - KOP_RATIO) / (1 - 0.1)                       # dK_eff / dK at R = 0.1  (= 7/9)
DK_EFF_POINTS = [2.6, 2.75, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0, 50.0, 70.0, 100.0]

def intrinsic(dk_eff):
    return C * dk_eff ** M * (1 - (DK_TH_EFF / dk_eff) ** 4)
def data():
    """(dK, da/dN) for the two series; R = 0.7 is closure-free, R = 0.1 is shifted by 1/U in dK."""
    r07 = [(d, intrinsic(d)) for d in DK_EFF_POINTS]
    r01 = [(d / U01, intrinsic(d)) for d in DK_EFF_POINTS]
    return r01, r07

def draw(out="image"):
    r01, r07 = data()
    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    xs = [2.0, 300.0]
    ax.plot(xs, [C * x ** M for x in xs], "k--", lw=1.0, label="Paris fit", zorder=2)
    ax.plot(xs, [C * (U01 * x) ** M for x in xs], "k--", lw=1.0, zorder=2)
    ax.plot([d for d, _ in r01], [r for _, r in r01], "o", mfc="white", mec="black", ms=6.5, mew=1.2, label="$R = 0.1$", zorder=3)
    ax.plot([d for d, _ in r07], [r for _, r in r07], "s", mfc="black", mec="black", ms=5.5, label="$R = 0.7$", zorder=3)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(2, 300); ax.set_ylim(1e-12, 1e-5)
    ax.set_xlabel(r"$\Delta K$  (MPa$\sqrt{\mathrm{m}}$)", fontsize=12)
    ax.set_ylabel(r"$da/dN$  (m/cycle)", fontsize=12)
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=range(2, 10), numticks=20))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
    ax.xaxis.set_minor_formatter(FuncFormatter(lambda v, p: f"{v:g}" if v in (2, 3, 5, 20, 30, 50, 200) else ""))
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=range(2, 10), numticks=20))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="major", color="0.55", lw=0.8)
    ax.grid(True, which="minor", color="0.85", lw=0.5)
    ax.tick_params(axis="both", which="both", labelsize=10)
    ax.legend(loc="upper left", fontsize=11, frameon=True)
    ax.text(0.98, 0.03, "MIM Ti-6Al-7Nb, long cracks, lab air", transform=ax.transAxes, ha="right", va="bottom", fontsize=10)
    fig.tight_layout(pad=0.4)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    r01, r07 = data()
    print("R = 0.7 points (dK, da/dN):", [(round(d, 3), f"{r:.3e}") for d, r in r07])
    print("R = 0.1 points (dK, da/dN):", [(round(d, 3), f"{r:.3e}") for d, r in r01])
    draw()
