import numpy as np, bp, pickle, sys
n = 20
E1 = [(1, 6), (3, 7), (5, 10), (7, 12), (10, 15), (12, 16), (14, 19), (16, 20)]
E = [(u - 1, w - 1) for u, w in E1]
S = bp.symmetry_vertices(n, E)
print("symmetry vertices:", S, "-> expected count", 2 ** len(S), "; naive 2^(n-3-m) =", 2 ** (n - 3 - len(E)))
def trace(seed):
    rng = np.random.default_rng(seed)
    ang = []; tor = []
    for i in range(n):
        if i < 9 or i >= 12: ang.append(np.radians(91 + rng.normal(0, 2.5))); tor.append(np.radians(50 + rng.normal(0, 5)))
        else: ang.append(np.radians(rng.uniform(95, 130))); tor.append(np.radians(rng.uniform(-180, 180)))
    X = [np.array([0.0, 0, 0]), np.array([3.8, 0, 0])]
    X.append(X[1] + 3.8 * np.array([-np.cos(ang[1]), np.sin(ang[1]), 0]))
    for i in range(3, n):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = c - b; bc /= np.linalg.norm(bc); nrm = np.cross(b - a, bc); nrm /= np.linalg.norm(nrm); m = np.cross(nrm, bc)
        th, ph = ang[i - 1], tor[i - 1]
        d = np.array([-3.8 * np.cos(th), 3.8 * np.sin(th) * np.cos(ph), 3.8 * np.sin(th) * np.sin(ph)])
        X.append(c + d[0] * bc + d[1] * m + d[2] * nrm)
    return np.array(X)
rows = []
for seed in range(400):
    X = trace(seed); D = np.linalg.norm(X[:, None] - X[None], axis=2)
    mind = min(D[i, j] for i in range(n) for j in range(i + 2, n))
    if mind < 4.0: continue
    # compactness: the two helix axes antiparallel and close: distance between centroids of 1-9 and 13-20
    c1 = X[:9].mean(0); c2 = X[12:].mean(0); dc = np.linalg.norm(c1 - c2)
    a1 = X[8] - X[0]; a2 = X[19] - X[12]; cosang = a1 @ a2 / np.linalg.norm(a1) / np.linalg.norm(a2)
    if dc > 11 or cosang > -0.6: continue
    pr = [D[u, w] for u, w in E]
    cnt = bp.count_solutions(X, E)
    rows.append((dc, seed, cnt, round(mind, 2), round(max(pr), 1), round(cosang, 2)))
rows.sort()
for r in rows[:10]: print(r)
seed = rows[0][1]; X = trace(seed)
pickle.dump(dict(seed=seed, X=X, E=E, E1=E1, S=S), open("instance.pkl", "wb")); print("saved seed", seed)
