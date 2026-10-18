import numpy as np, bp, pickle, sys
n = 20
# pruning edges (1-based) chosen so that S = {4, 8, 13, 17}
E1 = [(1, 7), (2, 6), (3, 7), (5, 12), (6, 11), (8, 12), (10, 16), (14, 20)]
E = [(u - 1, w - 1) for u, w in E1]
print("symmetry vertices:", bp.symmetry_vertices(n, E), "-> expected count", 2 ** len(bp.symmetry_vertices(n, E)))
print("naive 2^(n-3-m) =", 2 ** (n - 3 - len(E)), " naive 2^(n-3) =", 2 ** (n - 3))
def trace(seed):
    """protein-like C-alpha trace: virtual bond 3.8, virtual bond angles ~ 91 deg (helix) then ~120 (strand), torsions helix ~50 then extended ~ -170, with noise"""
    rng = np.random.default_rng(seed)
    # segments: residues 1-9 helix, 10-13 turn, 14-20 strand
    ang = []; tor = []
    for i in range(n):
        if i < 9: ang.append(np.radians(91 + rng.normal(0, 3))); tor.append(np.radians(50 + rng.normal(0, 6)))
        elif i < 13: ang.append(np.radians(rng.uniform(95, 125))); tor.append(np.radians(rng.uniform(-150, 150)))
        else: ang.append(np.radians(120 + rng.normal(0, 5))); tor.append(np.radians(-170 + rng.normal(0, 15)))
    X = [np.array([0.0, 0, 0]), np.array([3.8, 0, 0])]
    X.append(X[1] + 3.8 * np.array([-np.cos(ang[1]), np.sin(ang[1]), 0]))
    for i in range(3, n):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = c - b; bc /= np.linalg.norm(bc); nrm = np.cross(b - a, bc); nrm /= np.linalg.norm(nrm); m = np.cross(nrm, bc)
        th, ph = ang[i - 1], tor[i - 1]
        d = np.array([-3.8 * np.cos(th), 3.8 * np.sin(th) * np.cos(ph), 3.8 * np.sin(th) * np.sin(ph)])
        X.append(c + d[0] * bc + d[1] * m + d[2] * nrm)
    return np.array(X)
best = None
for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
    X = trace(seed)
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    mind = min(D[i, j] for i in range(n) for j in range(i + 2, n))
    if mind < 3.6: continue              # no clashes
    cnt = bp.count_solutions(X, E)
    span = np.ptp(X, axis=0)
    # prefer compact but open fragments: pruning pairs not too far
    pr = [D[u, w] for u, w in E]
    print(seed, "count", cnt, "min nonbonded", round(mind, 2), "NOE distances", [round(p, 1) for p in pr], "span", span.round(1))
    if cnt == 2 ** len(bp.symmetry_vertices(n, E)) and max(pr) < 14 and (best is None or max(pr) < best[1]):
        best = (seed, max(pr), X)
print("best seed", best[0], "max NOE", round(best[1], 1))
pickle.dump(dict(seed=best[0], X=best[2], E=E, E1=E1), open("instance.pkl", "wb"))
