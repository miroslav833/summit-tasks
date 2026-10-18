import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fractions import Fraction as F
P = {1: {2: F(1, 2), 5: F(1, 2)}, 4: {5: F(1, 3), 8: F(2, 3)}, 7: {2: F(3, 4), 8: F(1, 4)},
     2: {3: F(2, 3), 6: F(1, 3)}, 5: {6: F(1, 2), 9: F(1, 2)}, 8: {3: F(1, 4), 9: F(3, 4)},
     3: {4: F(1, 3), 7: F(2, 3)}, 6: {1: F(1, 2), 7: F(1, 2)}, 9: {1: F(2, 3), 4: F(1, 3)}}
fig, ax = plt.subplots(figsize=(6.6, 6.0)); ax.axis("off")
cells = [[(f"{P[i][j].numerator}/{P[i][j].denominator}" if j in P[i] else "0") for j in range(1, 10)] for i in range(1, 10)]
t = ax.table(cellText=cells, rowLabels=[str(i) for i in range(1, 10)], colLabels=[str(j) for j in range(1, 10)], loc="center", cellLoc="center")
t.auto_set_font_size(False); t.set_fontsize(12); t.scale(1.0, 1.9)
for (r, c), cell in t.get_celld().items():
    cell.set_linewidth(0.6)
    if r == 0 or c == -1: cell.set_text_props(weight="bold"); cell.set_facecolor("0.92")
ax.text(0.5, 0.97, "row $i$, column $j$:  $P(X_{n+1} = j \\mid X_n = i)$", transform=ax.transAxes, ha="center", fontsize=12)
fig.tight_layout(); fig.savefig("image.png", dpi=300, facecolor="white"); print("ok")
