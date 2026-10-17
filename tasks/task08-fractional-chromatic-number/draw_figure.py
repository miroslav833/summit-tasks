"""Draws the figure for task08 (test-matrix version 3): the six factors of the fatigue programme with their three levels,
and the ten level combinations that are not available.  Produces image.png (300 dpi) and image.pdf.
Run: python3 draw_figure.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FACTORS = [("Powder", ["TiH$_2$-derived", "HDH", "gas-atomised"]),
           ("Specimen geometry", ["round bar", "flat", "notched"]),
           ("Space-holder content", ["0 vol%", "15 vol%", "30 vol%"]),
           ("Oxygen content", ["0.15 wt%", "0.30 wt%", "0.45 wt%"]),
           ("Load ratio $R$", ["$-1$", "0.1", "0.5"]),
           ("Environment", ["laboratory air", "Ringer's solution", "Ringer's, H-charged"])]
# forbidden pairs as (factor index, level index) couples: A0B0, A0C0, A0D2, A0F1, A1B2, B1E0, C0D0, C1E2, D1F0, D2F1
FORBIDDEN = [((0, 0), (1, 0)), ((0, 0), (2, 0)), ((0, 0), (3, 2)), ((0, 0), (5, 1)), ((0, 1), (1, 2)), ((1, 1), (4, 0)), ((2, 0), (3, 0)), ((2, 1), (4, 2)), ((3, 1), (5, 0)), ((3, 2), (5, 1))]

def draw(out="image"):
    fig, ax = plt.subplots(figsize=(10.0, 8.6)); ax.axis("off")
    ax.text(0.0, 0.985, "Factors and levels of the fatigue test programme (MIM Ti-6Al-7Nb)", fontsize=12.5, fontweight="bold", va="top")
    cells = [[name] + lv for name, lv in FACTORS]
    t1 = ax.table(cellText=cells, colLabels=["Factor", "Level 1", "Level 2", "Level 3"], loc="upper left", bbox=[0.0, 0.60, 1.0, 0.35], cellLoc="center")
    t1.auto_set_font_size(False); t1.set_fontsize(11.5)
    for (r, c), cell in t1.get_celld().items():
        cell.set_edgecolor("black"); cell.set_linewidth(0.8)
        if r == 0: cell.set_text_props(fontweight="bold"); cell.set_facecolor("0.9")
        if c == 0 and r > 0: cell.set_text_props(ha="left"); cell.get_text().set_x(0.03)
    ax.text(0.0, 0.54, "Level combinations that are not available", fontsize=12.5, fontweight="bold", va="top")
    rows = []
    for (fi, li), (fj, lj) in FORBIDDEN:
        rows.append([f"{FACTORS[fi][0]} = {FACTORS[fi][1][li]}", f"{FACTORS[fj][0]} = {FACTORS[fj][1][lj]}"])
    t2 = ax.table(cellText=rows, colLabels=["Level of one factor", "Level of another factor"], loc="upper left", bbox=[0.0, 0.0, 1.0, 0.50], cellLoc="left", colWidths=[0.5, 0.5])
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
