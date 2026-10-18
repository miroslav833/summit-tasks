"""Draws the figure for task08 (test-matrix version): the five factors of the fatigue programme with their three levels,
and the five level combinations that are not available.  Produces image.png (300 dpi) and image.pdf.
Run: python3 draw_figure.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FACTORS = [("Powder", ["TiH$_2$-derived", "HDH", "gas-atomised"]),
           ("Specimen geometry", ["round bar", "flat", "notched"]),
           ("Space-holder content", ["0 vol%", "15 vol%", "30 vol%"]),
           ("Oxygen content", ["0.15 wt%", "0.30 wt%", "0.45 wt%"]),
           ("Load ratio $R$", ["$-1$", "0.1", "0.5"])]
# forbidden pairs as (factor index, level index) couples: A0C1, A0C2, A1D0, A2B1, B0D1
FORBIDDEN = [((0, 0), (2, 1)), ((0, 0), (2, 2)), ((0, 1), (3, 0)), ((0, 2), (1, 1)), ((1, 0), (3, 1))]
REASON = ["foam collapses on dehydrogenation", "foam collapses on dehydrogenation", "HDH powder too high in oxygen",
          "feedstock does not fill the mould", "no stock"]

def draw(out="image"):
    fig, ax = plt.subplots(figsize=(11.0, 6.2)); ax.axis("off")
    ax.text(0.0, 0.97, "Factors and levels of the fatigue test programme (MIM Ti-6Al-7Nb)", fontsize=12.5, fontweight="bold", va="top")
    cells = [[name] + lv for name, lv in FACTORS]
    t1 = ax.table(cellText=cells, colLabels=["Factor", "Level 1", "Level 2", "Level 3"], loc="upper left", bbox=[0.0, 0.52, 1.0, 0.40], cellLoc="center")
    t1.auto_set_font_size(False); t1.set_fontsize(11.5)
    for (r, c), cell in t1.get_celld().items():
        cell.set_edgecolor("black"); cell.set_linewidth(0.8)
        if r == 0: cell.set_text_props(fontweight="bold"); cell.set_facecolor("0.9")
        if c == 0 and r > 0: cell.set_text_props(ha="left"); cell.get_text().set_x(0.03)
    ax.text(0.0, 0.46, "Level combinations that cannot be produced or tested", fontsize=12.5, fontweight="bold", va="top")
    rows = []
    for (fi, li), (fj, lj) in FORBIDDEN:
        rows.append([f"{FACTORS[fi][0]} = {FACTORS[fi][1][li]}", f"{FACTORS[fj][0]} = {FACTORS[fj][1][lj]}"])
    for row, reason in zip(rows, REASON): row.append(reason)
    t2 = ax.table(cellText=rows, colLabels=["Level of one factor", "Level of another factor", "Reason"], loc="upper left", bbox=[0.0, 0.04, 1.0, 0.38], cellLoc="left", colWidths=[0.34, 0.36, 0.30])
    t2.auto_set_font_size(False); t2.set_fontsize(11.5)
    for (r, c), cell in t2.get_celld().items():
        cell.set_edgecolor("black"); cell.set_linewidth(0.8); cell.get_text().set_x(0.03)
        if r == 0: cell.set_text_props(fontweight="bold"); cell.set_facecolor("0.9")
    fig.tight_layout(pad=0.3)
    here = pathlib.Path(__file__).parent
    fig.savefig(here / f"{out}.png", dpi=300, facecolor="white"); fig.savefig(here / f"{out}.pdf", facecolor="white"); plt.close(fig)
    print("wrote", out + ".png", out + ".pdf")

if __name__ == "__main__":
    draw()
