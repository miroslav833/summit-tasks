"""Branch and prune for a discretizable distance geometry instance.
Atoms 1..n (0-based 0..n-1); distances known for |i-j|<=3 and for the pruning pairs E.
count_solutions(X, E) rebuilds all conformations with atoms 0,1,2 fixed to those of X."""
import numpy as np, itertools
def trilaterate(p1, p2, p3, d1, d2, d3):
    """the two points at distances d1,d2,d3 from p1,p2,p3 (generic case)"""
    ex = p2 - p1; dd = np.linalg.norm(ex); ex /= dd
    i = ex @ (p3 - p1); ey = p3 - p1 - i * ex; j = np.linalg.norm(ey); ey /= j
    ez = np.cross(ex, ey)
    x = (d1 * d1 - d2 * d2 + dd * dd) / (2 * dd)
    y = (d1 * d1 - d3 * d3 + i * i + j * j) / (2 * j) - i * x / j
    z2 = d1 * d1 - x * x - y * y
    if z2 < -1e-9: return []
    z = np.sqrt(max(z2, 0.0))
    return [p1 + x * ex + y * ey + z * ez, p1 + x * ex + y * ey - z * ez]
def count_solutions(X, E, tol=1e-6, keep=False):
    n = len(X); D = np.linalg.norm(X[:, None] - X[None], axis=2)
    prune = {}
    for u, w in E: prune.setdefault(max(u, w), []).append(min(u, w))
    sols = []; stack = [[X[0], X[1], X[2]]]
    leaves = 0
    while stack:
        P = stack.pop(); v = len(P)
        if v == n: sols.append(np.array(P)); continue
        for cand in trilaterate(P[v - 3], P[v - 2], P[v - 1], D[v, v - 3], D[v, v - 2], D[v, v - 1]):
            if all(abs(np.linalg.norm(cand - P[u]) - D[v, u]) < tol for u in prune.get(v, [])):
                stack.append(P + [cand])
    return (len(sols), sols) if keep else len(sols)
def symmetry_vertices(n, E):
    """Liberti et al.: v>=4 (1-based) is a symmetry vertex iff no pruning edge {u,w} has u+3 < v <= w."""
    S = []
    for v in range(4, n + 1):
        if not any(u + 3 < v <= w for u, w in ((min(e) + 1, max(e) + 1) for e in E)): S.append(v)
    return S
