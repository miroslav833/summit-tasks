"""Relax the coarse knotted curve: shorten it while keeping non-adjacent parts at least R apart
(a crude rope tightening). Starts from the planar closed braid for 5_2. Checks the knot type after."""
import numpy as np, knotlib as K, sys
WORD = [1, 1, 1, 2, -1, 2]
R = 1.0; NPT = 360
C = K.smooth(K.build_braid_curve(WORD, 3, h=0.5), NPT)
def resample(P, n):
    return K.smooth(P, n)
def step(P, ks=0.25, kr=0.6):
    n = len(P)
    lap = np.roll(P, 1, axis=0) + np.roll(P, -1, axis=0) - 2 * P
    F = ks * lap
    d = P[:, None] - P[None]; dist = np.linalg.norm(d, axis=2) + 1e-9
    idx = np.abs(np.subtract.outer(np.arange(n), np.arange(n))); idx = np.minimum(idx, n - idx)
    mask = (idx > 6) & (dist < R)
    push = (R - dist) / dist * mask
    F += kr * (d * push[..., None]).sum(1)
    return P + 0.08 * F
rng = np.random.default_rng(0)
C += rng.normal(0, 0.01, C.shape)
for it in range(1, 6001):
    C = step(C)
    if it % 100 == 0: C = resample(C, NPT)
    if it % 1000 == 0:
        n = len(C); d = np.linalg.norm(C[:, None] - C[None], axis=2)
        idx = np.abs(np.subtract.outer(np.arange(n), np.arange(n))); idx = np.minimum(idx, n - idx)
        reach = d[idx > 6].min(); L = np.linalg.norm(np.diff(np.vstack([C, C[:1]]), axis=0), axis=1).sum()
        print(f"iter {it}: length {L:.2f} reach {reach:.3f} ratio {L / reach:.1f}")
D = K.diagram(C); J = K.jones(D["pd"], D["writhe"]) if D["n"] <= 16 else None
known = {-6: -1, -5: 1, -4: -1, -3: 2, -2: -1, -1: 1}
print("after tightening: crossings in z-projection", D["n"], "still 5_2:", J == known or J == {-k: v for k, v in known.items()})
np.save("coarse.npy", C)
