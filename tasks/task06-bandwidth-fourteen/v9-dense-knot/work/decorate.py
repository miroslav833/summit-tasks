"""Turn the coarse closed curve into a C-alpha chain: helices (axis along the curve, radius 2.3 A,
rise 1.5 A, 100 deg per residue) and loops (3.3 A per residue along the curve with a small zigzag).
The closed curve is cut at a point on the outside; the chain runs from one side of the cut round to
the other. usage: decorate.py seed scale_A_per_unit  -> calpha.npy, segments.json"""
import numpy as np, json, sys, knotlib as K
from scipy.interpolate import CubicSpline
seed, SCALE = int(sys.argv[1]), float(sys.argv[2])
rng = np.random.default_rng(seed)
C = np.load("coarse.npy") * SCALE                      # closed, N points
N = len(C)
# reach of the coarse curve: smallest distance between points at least 40 samples apart along the curve
d = np.linalg.norm(C[:, None] - C[None], axis=2)
idx = np.abs(np.subtract.outer(np.arange(N), np.arange(N))); idx = np.minimum(idx, N - idx)
reach = d[idx >= 40].min()
# cut point: farthest from centre
cen = C.mean(0); i0 = int(np.argmax(np.linalg.norm(C - cen, axis=1)))
order = [(i0 + k) % N for k in range(N)]
P = C[order]                                          # open polyline starting just after the cut
s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
L = s[-1]
cs = CubicSpline(s, P)
# segment plan along arclength: alternate loop / helix / loop / strand ...
plan = []; pos = 0.0; kind = "loop"
while True:
    if kind == "loop":
        nres = int(rng.integers(3, 7)); length = nres * 3.25
    elif kind == "helix":
        nres = int(rng.integers(10, 19)); length = nres * 1.5
    else:  # strand (extended)
        nres = int(rng.integers(5, 9)); length = nres * 3.3
    if pos + length > L - 8: 
        nres = max(2, int((L - 8 - pos) / 3.25)); plan.append(("loop", nres, pos, pos + nres * 3.25)); break
    plan.append((kind, nres, pos, pos + length)); pos += length
    kind = {"loop": rng.choice(["helix", "helix", "strand"]), "helix": "loop", "strand": "loop"}[kind]
# parallel-transport frame along the curve
def frame(sv):
    T = cs(sv, 1); T /= np.linalg.norm(T, axis=1)[:, None]
    n1 = np.zeros_like(T); n2 = np.zeros_like(T)
    v = np.cross(T[0], [0, 0, 1.0]);
    if np.linalg.norm(v) < 1e-3: v = np.cross(T[0], [0, 1.0, 0])
    n1[0] = v / np.linalg.norm(v)
    for k in range(1, len(sv)):
        v = n1[k - 1] - T[k] * (T[k] @ n1[k - 1]); n1[k] = v / np.linalg.norm(v)
    n2 = np.cross(T, n1)
    return T, n1, n2
CA = []; segs = []
theta = rng.uniform(0, 2 * np.pi)
for kind, nres, a, b in plan:
    sv = np.linspace(a, b, nres, endpoint=False) + (b - a) / nres / 2
    T, n1, n2 = frame(sv); axis = cs(sv)
    start = len(CA)
    for k in range(nres):
        if kind == "helix":
            theta += np.radians(100.0)
            CA.append(axis[k] + 2.3 * (np.cos(theta) * n1[k] + np.sin(theta) * n2[k]))
        elif kind == "strand":
            CA.append(axis[k] + 0.95 * (1 if k % 2 == 0 else -1) * n1[k])
        else:
            theta += np.radians(rng.uniform(60, 140))
            CA.append(axis[k] + 0.9 * (np.cos(theta) * n1[k] + np.sin(theta) * n2[k]))
    segs.append(dict(kind=kind, first=start + 1, last=len(CA)))
CA = np.array(CA); n = len(CA)
D = np.linalg.norm(CA[:, None] - CA[None], axis=2)
bonds = np.array([D[i, i + 1] for i in range(n - 1)])
nb = min(D[i, j] for i in range(n) for j in range(i + 3, n))
print(f"scale {SCALE} A/unit: coarse length {L:.0f} A, reach {reach:.1f} A, residues {n}, bonds {bonds.min():.2f}-{bonds.max():.2f}, min nonbonded {nb:.2f}")
print("segments:", [(k, f, l) for k, f, l in ((g['kind'], g['first'], g['last']) for g in segs)])
np.save("calpha.npy", CA); np.save("coarse_open.npy", P)
json.dump(dict(seed=seed, scale=SCALE, n=n, segments=segs, reach=float(reach), cut_index=i0), open("segments.json", "w"), indent=1)
