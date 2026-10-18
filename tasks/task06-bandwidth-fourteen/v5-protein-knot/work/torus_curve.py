import numpy as np, knotlib as K
def braid_strand_paths(word, nstr=3, h=0.45, step=1.0):
    pos = list(range(nstr)); paths = {s: [np.array([float(s), 0.0, 0.0])] for s in range(nstr)}; y = 0.0
    for g in word:
        i = abs(g) - 1
        a = [s for s in range(nstr) if pos[s] == i][0]; b = [s for s in range(nstr) if pos[s] == i + 1][0]
        for t in np.linspace(0, 1, 13)[1:]:
            s_ = 0.5 - 0.5 * np.cos(np.pi * t); bump = np.sin(np.pi * t)
            za = h * bump * (1 if g > 0 else -1)
            paths[a].append(np.array([i + s_, y + t * step, za])); paths[b].append(np.array([i + 1 - s_, y + t * step, -za]))
        for s in range(nstr):
            if s not in (a, b): paths[s].append(np.array([float(pos[s]), y + step, 0.0]))
        pos[a], pos[b] = i + 1, i; y += step
    return paths, pos, y

def torus_closure(word, nstr=3, R0=2.2, dr=0.8, h=0.45, pad=1.0, wobble=0.0, seed=0, n=1400):
    """closed 3-braid wrapped around the z axis: x -> radius R0 + dr*x, y -> angle, z -> axial."""
    paths, pos, Y = braid_strand_paths(word, nstr, h)
    # concatenate strands following the permutation; add a straight pad after each strand so the
    # wrap closes smoothly (pad in y continues the angle)
    curve = []; s = 0; yoff = 0.0
    for _ in range(nstr):
        P = np.array(paths[s]); P = P + np.array([0, yoff, 0])
        curve.append(P)
        yoff += Y + pad
        curve.append(np.array([[pos[s], yoff - pad + pad * 0.5, 0.0]]))   # mid pad point at the new position
        s = pos[s]
    assert s == 0
    C = np.vstack(curve)
    total = nstr * (Y + pad)
    # positions along pad: the strand ended at pos and the next strand starts at the same x, fine.
    theta = 2 * np.pi * C[:, 1] / (Y + pad)
    rho = R0 + dr * C[:, 0]
    pts = np.c_[rho * np.cos(theta), rho * np.sin(theta), C[:, 2]]
    sm = K.smooth(pts, n)
    if wobble > 0:
        rng = np.random.default_rng(seed)
        u = np.linspace(0, 2 * np.pi, n, endpoint=False)
        for k in range(3):
            for m in range(2, 6):
                sm[:, k] += wobble * rng.normal() / m * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    return sm
if __name__ == "__main__":
    word = [1,1,1,-2,-1,-1,-1,-2]
    sm = torus_closure(word)
    D = K.diagram(sm)
    print("top view n", D["n"], "writhe", D["writhe"], K.jones_str(K.jones(D["pd"], D["writhe"])), "3col", K.colorings(D["pd"], 3))
    sm = torus_closure(word, wobble=0.25, seed=3)
    D = K.diagram(sm)
    print("wobble top view n", D["n"], K.jones_str(K.jones(D["pd"], D["writhe"])) if D["n"] < 16 else "")
