"""Ideal three-helix bundle, 36 C-alpha atoms: helices 1-11 (up), 15-25 (down), 28-36 (up); loops 12-14, 26-27."""
import numpy as np, bp, pickle, sys
from scipy.interpolate import CubicSpline
n = 36
HEL = [(1, 11, +1), (15, 25, -1), (28, 36, +1)]
E1 = [(1,6),(3,8),(6,11),(8,13),(10,15),(13,18),(15,20),(17,22),(20,25),(22,27),(24,29),(27,32),(29,34),(31,36)]
E = [(u - 1, w - 1) for u, w in E1]
def build(seed):
    rng = np.random.default_rng(seed)
    R, rise, dth = 2.3, 1.5, np.radians(99.5)
    side = 10.0 + rng.normal(0, 0.4)
    centers = [np.array([0.0, 0.0]), np.array([side, 0.0]), np.array([side / 2, side * np.sqrt(3) / 2])]
    X = np.full((n, 3), np.nan)
    for (a, b, s), c in zip(HEL, centers):
        th0 = rng.uniform(0, 2 * np.pi); z0 = rng.uniform(-1.5, 1.5) + (0 if s > 0 else rise * (b - a))
        # small random tilt of the axis
        tilt = rng.normal(0, 0.06, 2)
        for i in range(a, b + 1):
            k = i - a; th = th0 + s * dth * k; z = z0 + s * rise * k
            p = np.array([c[0] + R * np.cos(th), c[1] + R * np.sin(th), z])
            p[:2] += tilt * z
            X[i - 1] = p
    # loops: cubic spline through the helix ends with an outward control point, resampled at ~3.8 A
    for (a1, b1, _), (a2, b2, _) in zip(HEL[:-1], HEL[1:]):
        p0, p1 = X[b1 - 1], X[a2 - 1]; m = (p0 + p1) / 2; out = m - np.array([*np.mean(centers, 0), m[2]])
        out[2] = 0; out = out / np.linalg.norm(out) * (4.0 + rng.uniform(0, 1.5))
        ctrl = np.array([X[b1 - 2], p0, m + out + np.array([0, 0, rng.uniform(-2, 2)]), p1, X[a2]])
        t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ctrl, axis=0), axis=1))]
        cs = CubicSpline(t, ctrl); u = np.linspace(t[1], t[3], 400); pts = cs(u)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
        k = a2 - b1 - 1                                  # residues to place
        for j in range(1, k + 1): X[b1 - 1 + j] = cs(np.interp(s[-1] * j / (k + 1), s, u))
    return X
rows = []
for seed in range(400):
    X = build(seed); D = np.linalg.norm(X[:, None] - X[None], axis=2)
    bonds = [D[i, i + 1] for i in range(n - 1)]
    mind = min(D[i, j] for i in range(n) for j in range(i + 2, n))
    if mind < 3.9 or max(bonds) > 4.6 or min(bonds) < 3.0: continue
    cnt = bp.count_solutions(X, E)
    pr = [D[u, w] for u, w in E]
    rows.append((abs(max(bonds) - 3.8) + abs(min(bonds) - 3.8), seed, cnt, round(mind, 2), round(min(bonds), 2), round(max(bonds), 2), round(max(pr), 1)))
rows.sort(); print(len(rows), "ok"); [print(r) for r in rows[:6]]
seed = rows[0][1]; X = build(seed)
pickle.dump(dict(seed=seed, X=X, E=E, E1=E1, S=bp.symmetry_vertices(n, E), HEL=HEL), open("bundle.pkl", "wb")); print("saved seed", seed)
