from fractions import Fraction as F
import random, itertools
import sympy as sp
# Candidate 1: exact by sympy first-step, and Monte Carlo
AH, AT, BH, BT = sp.symbols("AH AT BH BT")
s = sp.solve([sp.Eq(AH, sp.Rational(3,4) + sp.Rational(1,4)*BT), sp.Eq(BH, sp.Rational(1,4) + sp.Rational(3,4)*AT),
              sp.Eq(AT, sp.Rational(3,4)*BH), sp.Eq(BT, sp.Rational(1,4)*AH)], [AH, AT, BH, BT])
c1 = sp.Rational(3,4)*s[BH] + sp.Rational(1,4)*s[BT]; print("candidate 1 exact:", c1)
rnd = random.Random(1); win = 0; N = 400000
for _ in range(N):
    st, prev = 0, None
    while True:
        h = rnd.random() < (0.75 if st == 0 else 0.25); sym = "H" if h else "T"
        if prev == sym: win += (sym == "H"); break
        prev, st = sym, 1 - st
print("candidate 1 Monte Carlo:", win / N, "vs", float(c1))
# Candidate 2: full linear system, independently written
V = ["L", "W", "s", "a", "b", "c", "d", "e"]
E = {("L","a"):2, ("L","s"):1, ("L","b"):1, ("a","c"):1, ("a","d"):1, ("s","c"):1, ("s","e"):1, ("b","d"):1, ("b","e"):1, ("c","W"):1, ("d","W"):1, ("e","W"):1}
import networkx as nx
G = nx.Graph(); [G.add_edge(u, v, w=w) for (u, v), w in E.items()]
print("candidate 2 graph is the cube:", nx.is_isomorphic(G, nx.hypercube_graph(3)))
h = {v: sp.Symbol("h_" + v) for v in V}
eqs = [sp.Eq(h["L"], 0), sp.Eq(h["W"], 1)]
for v in V:
    if v in ("L", "W"): continue
    tot = sum(G[v][u]["w"] for u in G[v]); eqs.append(sp.Eq(h[v], sum(G[v][u]["w"] * h[u] for u in G[v]) / tot))
sol = sp.solve(eqs, list(h.values())); print("candidate 2 exact:", {v: sol[h[v]] for v in V})
print("distance L-W:", nx.shortest_path_length(G, "L", "W"))
