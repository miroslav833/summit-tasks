"""Candidate A: 9-state chain with period 3 hidden by the layout. Classes C0 = {1,4,7}, C1 = {2,5,8}, C2 = {3,6,9},
transitions only C_k -> C_{k+1}. Positions are shuffled so no three-column structure shows."""
import random, itertools, math
from fractions import Fraction as F
import numpy as np, networkx as nx, sympy as sp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
cls = {1: 0, 4: 0, 7: 0, 2: 1, 5: 1, 8: 1, 3: 2, 6: 2, 9: 2}
# hand-chosen transition matrix with small-denominator fractions, each row to two states of the next class
P = {1: {2: F(1, 2), 5: F(1, 2)}, 4: {5: F(1, 3), 8: F(2, 3)}, 7: {2: F(3, 4), 8: F(1, 4)},
     2: {3: F(2, 3), 6: F(1, 3)}, 5: {6: F(1, 2), 9: F(1, 2)}, 8: {3: F(1, 4), 9: F(3, 4)},
     3: {4: F(1, 3), 7: F(2, 3)}, 6: {1: F(1, 2), 7: F(1, 2)}, 9: {1: F(2, 3), 4: F(1, 3)}}
for i, row in P.items(): assert sum(row.values()) == 1 and all(cls[j] == (cls[i] + 1) % 3 for j in row)
M = sp.zeros(9, 9)
for i, row in P.items():
    for j, p in row.items(): M[i - 1, j - 1] = sp.Rational(p.numerator, p.denominator)
pi = sp.Matrix(sp.symbols("p1:10"))
sol = sp.solve(list(pi.T * M - pi.T) + [sum(pi) - 1], list(pi))
piv = [sol[sp.Symbol(f"p{k}")] for k in range(1, 10)]
print("stationary:", piv)
# exact limit of P^(6n) from 1 to 4, by high matrix power in rationals
Mn = M ** 3
L = (Mn ** 200)[0, 3]
print("P^(600)[1,4] =", float(L), " 3*pi_4 =", float(3 * piv[3]), " pi_4 =", float(piv[3]))
G = nx.DiGraph([(i, j) for i, r in P.items() for j in r])
print("period:", math.gcd(*[len(c) for c in nx.simple_cycles(G)]), "strongly connected:", nx.is_strongly_connected(G))
pickle_pos = None
# layout: search positions minimising crossings, avoiding a visible 3-layer structure
rnd = random.Random(4)
def crossings(pos):
    E = list(G.edges()); c = 0
    def o(a, b, cc): return (b[0]-a[0])*(cc[1]-a[1]) - (b[1]-a[1])*(cc[0]-a[0])
    for (a, b), (u, v) in itertools.combinations(E, 2):
        if len({a, b, u, v}) < 4: continue
        p1, p2, p3, p4 = pos[a], pos[b], pos[u], pos[v]
        if o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0: c += 1
    return c
best = None
slots = [(math.cos(2 * math.pi * k / 9), math.sin(2 * math.pi * k / 9)) for k in range(9)]
for perm in itertools.permutations(range(1, 10)):
    if rnd.random() > 0.02: continue
    pos = {v: slots[k] for k, v in enumerate(perm)}
    # reject layouts where each class sits on every third slot (that would show the period)
    if all(cls[perm[k]] == (cls[perm[0]] + k) % 3 for k in range(9)): continue
    c = crossings(pos)
    if best is None or c < best[0]: best = (c, pos)
print("crossings:", best[0])
pos = best[1]
fig, ax = plt.subplots(figsize=(6.4, 6.4))
for i, row in P.items():
    for j, p in row.items():
        a, b = np.array(pos[i]), np.array(pos[j])
        rad = 0.12
        arr = FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", mutation_scale=15, lw=1.2, shrinkA=17, shrinkB=17, color="black")
        ax.add_patch(arr)
        mid = (a + b) / 2; d = b - a; nrm = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        lp = mid + nrm * (0.06 + rad * np.linalg.norm(d) / 2)
        ax.text(*lp, f"{p.numerator}/{p.denominator}", fontsize=9, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.4))
for v, (x, y) in pos.items():
    ax.scatter([x], [y], s=620, fc="white", ec="black", lw=1.5, zorder=3); ax.text(x, y, str(v), ha="center", va="center", fontsize=12, zorder=4)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
fig.tight_layout(); fig.savefig("image.png", dpi=300, facecolor="white")
