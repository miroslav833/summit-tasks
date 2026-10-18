"""Render the knotted backbone as a shaded tube with a protein-style rainbow colouring.
usage: render.py seed wob ax ay az out.png [--labels]"""
import numpy as np, sys, json, knotlib as K, torus_curve as T
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
word = [1,1,1,-2,-1,-1,-1,-2]
seed, wob = int(sys.argv[1]), float(sys.argv[2]); ang = [float(a) for a in sys.argv[3:6]]; out = sys.argv[6]
labels = "--labels" in sys.argv
NPT = 1800
sm = T.torus_closure(word, wobble=wob, seed=seed, n=NPT)
Q = sm @ K.rotmat(*ang).T
D = K.diagram(Q)
# choose the cut (termini): point farthest from centre with no crossing within 40 samples
cen = Q[:, :2].mean(0); r = np.linalg.norm(Q[:, :2] - cen, axis=1)
cross_par = sorted([c["pi"] for c in D["crossings"]] + [c["pj"] for c in D["crossings"]])
def clear(i, m=45):
    return all(min(abs(p - i), NPT - abs(p - i)) > m for p in cross_par)
order = np.argsort(-r)
i0 = next(i for i in order if clear(i))
GAP = 10
start = (i0 + GAP // 2) % NPT                      # chain runs from start (N) all the way round to end (C)
idx = [(start + k) % NPT for k in range(NPT - GAP)]
P = Q[idx]
# verify the closure gap holds no crossing
assert clear(i0, GAP), "crossing inside the terminal gap"
# drawing
W, HALO = 14.0, 7.0
fig = plt.figure(figsize=(12, 10), dpi=200); ax_ = fig.add_axes([0, 0, 1, 1]); ax_.set_axis_off()
xy = P[:, :2]; z = P[:, 2]
span = np.ptp(xy, axis=0).max()
ax_.set_xlim(xy[:, 0].min() - 0.12 * span, xy[:, 0].max() + 0.12 * span)
ax_.set_ylim(xy[:, 1].min() - 0.12 * span, xy[:, 1].max() + 0.12 * span)
ax_.set_aspect("equal")
cmap = plt.get_cmap("turbo")
CH = 6                           # segments per chunk
chunks = []
for a in range(0, len(P) - 1, CH):
    b = min(a + CH, len(P) - 1)
    chunks.append((z[a:b + 1].mean(), a, b))
chunks.sort()
zmin, zmax = z.min(), z.max()
for zm, a, b in chunks:
    pts = xy[a:b + 1]
    col = cmap(0.05 + 0.9 * (a / len(P)))
    shade = 0.55 + 0.45 * (zm - zmin) / (zmax - zmin)      # nearer = brighter
    col2 = tuple(np.clip(np.array(col[:3]) * shade, 0, 1))
    ax_.plot(pts[:, 0], pts[:, 1], color="white", lw=W + HALO, solid_capstyle="butt", solid_joinstyle="round", zorder=1)
    ax_.plot(pts[:, 0], pts[:, 1], color=col2, lw=W, solid_capstyle="round", solid_joinstyle="round", zorder=1)
    ax_.plot(pts[:, 0], pts[:, 1], color=tuple(np.clip(np.array(col2) + 0.25, 0, 1)), lw=W * 0.35, solid_capstyle="round", solid_joinstyle="round", zorder=1)
# termini and closure
N_, C_ = xy[0], xy[-1]
ax_.plot([N_[0], C_[0]], [N_[1], C_[1]], color="0.45", lw=2.2, ls=(0, (4, 3)), zorder=0.5)
for p, lab, dx in ((N_, "N", -1), (C_, "C", 1)):
    v = p - cen; v = v / np.linalg.norm(v)
    ax_.text(p[0] + 0.07 * span * v[0], p[1] + 0.07 * span * v[1], lab, fontsize=26, ha="center", va="center", fontweight="bold")
if labels:
    for c in D["crossings"]:
        ax_.text(c["pt"][0], c["pt"][1] + 0.03 * span, str(c["id"] + 1), fontsize=16, color="red", ha="center")
fig.savefig(out, facecolor="white")
# record the diagram
signs = [c["sign"] for c in D["crossings"]]
rec = dict(seed=seed, wob=wob, ang=ang, npt=NPT, cut=int(i0), gap=GAP, n=D["n"], writhe=D["writhe"], pd=D["pd"],
           signs=signs, crossings=[dict(id=c["id"], x=float(c["pt"][0]), y=float(c["pt"][1]), sign=c["sign"], over_first=bool(c["over_i"]), pi=float(c["pi"]), pj=float(c["pj"])) for c in D["crossings"]],
           mindist=float(D["mindist"] / span), minangle=float(D["minangle"]), mindz=float(D["mindz"]))
json.dump(rec, open(out.replace(".png", ".json"), "w"), indent=1)
print("n", D["n"], "writhe", D["writhe"], "mindist", round(rec["mindist"], 3), "minangle", round(rec["minangle"], 1), "cut at", i0)
