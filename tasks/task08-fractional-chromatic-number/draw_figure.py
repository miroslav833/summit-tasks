# The drawn graph: 28 vertices, 42 edges, every vertex of degree 3. Positions are fixed so the figure is reproducible.
# Run: python3 draw_figure.py (needs matplotlib)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EDGES = "AG AJ AS BK BS BV CH CL CY DI DN DW EL EP EZ FS FX FZ GT Gb HJ Ha IM Ib JV KQ KU LR MO MX NT NV OQ OZ PU PX QY RT Ra Ub WY Wa".split()
POS = {"A": (0.202, -0.1031),
       "B": (-0.0271, -0.1881),
       "C": (0.8587, 0.0705),
       "D": (-0.2273, 0.7744),
       "E": (0.1167, -0.6798),
       "F": (-0.4735, -0.8997),
       "G": (-0.1002, 0.3004),
       "H": (1.0, 0.3544),
       "I": (-0.7073, 0.4023),
       "J": (0.5595, 0.0971),
       "K": (-0.3794, -0.151),
       "L": (0.6206, -0.241),
       "M": (-0.8686, -0.181),
       "N": (0.0584, 0.6707),
       "O": (-0.4371, -0.4075),
       "P": (-0.463, -0.6618),
       "Q": (-0.1182, -0.0303),
       "R": (0.7087, 0.3376),
       "S": (-0.0836, -0.5399),
       "T": (0.2729, 0.558),
       "U": (-0.6326, -0.1874),
       "V": (0.1838, 0.28),
       "W": (0.3551, 0.7811),
       "X": (-0.8189, -0.6782),
       "Y": (0.4046, 0.2936),
       "Z": (-0.2394, -0.8568),
       "a": (0.8227, 0.6848),
       "b": (-0.5866, 0.1987)}

fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
for e in EDGES:
    (x1, y1), (x2, y2) = POS[e[0]], POS[e[1]]
    ax.plot([x1, x2], [y1, y2], color="0.2", lw=1.3, zorder=1)
for v, (x, y) in POS.items():
    ax.scatter([x], [y], s=380, facecolor="white", edgecolor="0.1", linewidths=1.2, zorder=2)
    ax.text(x, y, v, ha="center", va="center", fontsize=10, zorder=3)
ax.set_aspect("equal"); ax.set_axis_off(); fig.tight_layout()
fig.savefig("image.png"); fig.savefig("image.pdf")
print("figure saved:", len(POS), "vertices,", len(EDGES), "edges")
