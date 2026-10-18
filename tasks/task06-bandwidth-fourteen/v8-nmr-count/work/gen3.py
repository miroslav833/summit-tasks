import numpy as np, bp, pickle, sys
n = 36
HEL = [(1, 11), (15, 25), (28, 36)]
E1 = [(1,6),(3,8),(6,11),(8,13),(10,15),(13,18),(15,20),(17,22),(20,25),(22,27),(24,29),(27,32),(29,34),(31,36)]
E = [(u - 1, w - 1) for u, w in E1]
S = bp.symmetry_vertices(n, E)
print("S =", S, "count", 2 ** len(S), "naive", 2 ** (n - 3 - len(E)))
def in_helix(i):  # 1-based residue
    return any(a <= i <= b for a, b in HEL)
def trace(seed):
    rng = np.random.default_rng(seed)
    ang = np.zeros(n); tor = np.zeros(n)
    for i in range(n):
        r = i + 1
        if in_helix(r) and in_helix(r + 1) and in_helix(r - 1):
            ang[i] = np.radians(91 + rng.normal(0, 2)); tor[i] = np.radians(50 + rng.normal(0, 4))
        else:
            ang[i] = np.radians(rng.uniform(95, 135)); tor[i] = np.radians(rng.uniform(-180, 180))
    X = [np.array([0.0, 0, 0]), np.array([3.8, 0, 0])]
    X.append(X[1] + 3.8 * np.array([-np.cos(ang[1]), np.sin(ang[1]), 0]))
    for i in range(3, n):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = c - b; bc /= np.linalg.norm(bc); nrm = np.cross(b - a, bc); nrm /= np.linalg.norm(nrm); m = np.cross(nrm, bc)
        th, ph = ang[i - 1], tor[i - 1]
        d = np.array([-3.8 * np.cos(th), 3.8 * np.sin(th) * np.cos(ph), 3.8 * np.sin(th) * np.sin(ph)])
        X.append(c + d[0] * bc + d[1] * m + d[2] * nrm)
    return np.array(X)
def axis(X, a, b):
    P = X[a - 1:b]; c = P.mean(0); u, s, vt = np.linalg.svd(P - c); d = vt[0]
    if d @ (P[-1] - P[0]) < 0: d = -d
    return c, d
rows = []
for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 3000):
    X = trace(seed); D = np.linalg.norm(X[:, None] - X[None], axis=2)
    mind = min(D[i, j] for i in range(n) for j in range(i + 2, n))
    if mind < 4.0: continue
    cs = [axis(X, a, b) for a, b in HEL]
    dists = [np.linalg.norm(cs[i][0] - cs[j][0]) for i in range(3) for j in range(i + 1, 3)]
    cosv = [cs[i][1] @ cs[j][1] for i in range(3) for j in range(i + 1, 3)]
    if max(dists) > 13 or min(dists) < 7.5: continue
    if not (cosv[0] < -0.7 and cosv[2] < -0.7): continue      # helix 1 anti 2, 2 anti 3
    rg = np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean())
    rows.append((rg, seed, round(mind, 2), [round(d, 1) for d in dists], [round(c, 2) for c in cosv]))
rows.sort()
print(len(rows), "candidates")
for r in rows[:8]: print(r)
seed = rows[0][1]; X = trace(seed)
cnt = bp.count_solutions(X, E); print("BP count for seed", seed, "=", cnt)
pickle.dump(dict(seed=seed, X=X, E=E, E1=E1, S=S, HEL=HEL), open("instance36.pkl", "wb")); print("saved")
