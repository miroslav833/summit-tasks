import numpy as np, knotlib as K, torus_curve as T
def curve(word, seed, amp=0.6, R0=3.0, dr=0.8, h=0.45, n=1400, harm=(2,3,4,5,6,7)):
    paths, pos, Y = T.braid_strand_paths(word, 3, h)
    curve = []; s = 0; yoff = 0.0; pad = 1.0
    for _ in range(3):
        P = np.array(paths[s]) + np.array([0, yoff, 0]); curve.append(P); yoff += Y + pad
        curve.append(np.array([[pos[s], yoff - pad * 0.5, 0.0]])); s = pos[s]
    C = np.vstack(curve)
    theta = 2 * np.pi * C[:, 1] / (Y + pad); rho = R0 + dr * C[:, 0]
    pts = np.c_[rho * np.cos(theta), rho * np.sin(theta), C[:, 2]]
    sm = K.smooth(pts, n)
    rng = np.random.default_rng(seed)
    u = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # axial wobble (z) with several harmonics, plus a weaker radial one
    for m in harm:
        sm[:, 2] += amp * rng.normal() / np.sqrt(m) * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    rad = np.zeros(n)
    for m in harm:
        rad += 0.35 * amp * rng.normal() / np.sqrt(m) * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    r = np.linalg.norm(sm[:, :2], axis=1); f = (r + rad) / r
    sm[:, 0] *= f; sm[:, 1] *= f
    return sm
