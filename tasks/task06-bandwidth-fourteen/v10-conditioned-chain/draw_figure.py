import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fractions import Fraction as F
P = {1: {5: F(1, 6), 3: F(5, 6)}, 2: {5: F(1, 5), 1: F(1, 2), 3: F(3, 10)}, 3: {4: F(2, 3), 5: F(1, 3)},
     4: {6: F(1, 4), 2: F(3, 4)}, 5: {5: F(1)}, 6: {6: F(1)}}
fig, ax = plt.subplots(figsize=(5.6, 4.4)); ax.axis("off")
def fmt(p): return "1" if p == 1 else f"{p.numerator}/{p.denominator}"
cells = [[(fmt(P[i][j]) if j in P[i] else "0") for j in range(1, 7)] for i in range(1, 7)]
t = ax.table(cellText=cells, rowLabels=[str(i) for i in range(1, 7)], colLabels=[str(j) for j in range(1, 7)], loc="center", cellLoc="center")
t.auto_set_font_size(False); t.set_fontsize(13); t.scale(1.0, 2.0)
for (r, c), cell in t.get_celld().items():
    cell.set_linewidth(0.6)
    if r == 0 or c == -1: cell.set_text_props(weight="bold"); cell.set_facecolor("0.92")
ax.text(0.5, 0.98, "row $i$, column $j$:  $P(X_{n+1} = j \\mid X_n = i)$", transform=ax.transAxes, ha="center", fontsize=12)
fig.tight_layout(); fig.savefig("image.png", dpi=300, facecolor="white"); print("ok")
