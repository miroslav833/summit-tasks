"""Z-buffered sphere-swept tube rendering of the knotted backbone.
usage: render2.py seed wob ax ay az out.png [--labels]"""
import numpy as np, sys, json, knotlib as K, torus_curve as T
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
word = [1,1,1,-2,-1,-1,-1,-2]
seed, wob = int(sys.argv[1]), float(sys.argv[2]); ang = [float(a) for a in sys.argv[3:6]]; out = sys.argv[6]
labels = "--labels" in sys.argv
NPT = 1800
import os, torus2
CURVE = os.environ.get('CURVE', 'torus')
sm = torus2.curve(word, seed, amp=wob, n=NPT) if CURVE == 'torus2' else T.torus_closure(word, wobble=wob, seed=seed, n=NPT)
Q = sm @ K.rotmat(*ang).T
D = K.diagram(Q)
cen = Q[:, :2].mean(0); r2 = np.linalg.norm(Q[:, :2] - cen, axis=1)
cross_par = sorted([c["pi"] for c in D["crossings"]] + [c["pj"] for c in D["crossings"]])
def clear(i, m=45): return all(min(abs(p - i), NPT - abs(p - i)) > m for p in cross_par)
i0 = next(i for i in np.argsort(-r2) if clear(i))
GAP = 10
start = (i0 + GAP // 2) % NPT
idx = [(start + k) % NPT for k in range(NPT - GAP)]
P = Q[idx]                                   # open chain, N = P[0], C = P[-1]
# ---- raster
Wpx, Hpx = 2400, 2000; margin = 0.10
xy = P[:, :2]; lo = xy.min(0); hi = xy.max(0); span = (hi - lo)
scale = min((Wpx * (1 - 2 * margin)) / span[0], (Hpx * (1 - 2 * margin)) / span[1])
off = np.array([Wpx, Hpx]) / 2 - scale * (lo + hi) / 2
pix = xy * scale + off; pix[:, 1] = Hpx - pix[:, 1]
depth = P[:, 2] * scale
# resample to ~1 px spacing
seg = np.linalg.norm(np.diff(pix, axis=0), axis=1); s = np.r_[0, np.cumsum(seg)]
u = np.arange(0, s[-1], 1.0)
cx = np.interp(u, s, pix[:, 0]); cy = np.interp(u, s, pix[:, 1]); cz = np.interp(u, s, depth); ci = u / s[-1]
R, GAPPX = 24.0, 11.0
zbuf = np.full((Hpx, Wpx), -np.inf); kbuf = np.full((Hpx, Wpx), -1, int); nbuf = np.zeros((Hpx, Wpx, 3))
rr = int(np.ceil(R)) + 1
for k in range(len(u)):
    x0, y0 = int(round(cx[k])), int(round(cy[k]))
    xs = np.arange(max(0, x0 - rr), min(Wpx, x0 + rr + 1)); ys = np.arange(max(0, y0 - rr), min(Hpx, y0 + rr + 1))
    X, Y = np.meshgrid(xs, ys); dx = X - cx[k]; dy = Y - cy[k]; d2 = dx * dx + dy * dy
    inside = d2 <= R * R
    h = np.sqrt(np.clip(R * R - d2, 0, None))
    zs = cz[k] + h
    win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    upd = inside & (zs > win)
    win[upd] = zs[upd]
    kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = k
    nb = nbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    nb[upd] = np.stack([dx / R, -dy / R, h / R], -1)[upd]
# gap pass: pixels in the ring r<d<=r+gap of a sample whose tube lies in front of the surface there
gapmask = np.zeros((Hpx, Wpx), bool); rg = int(np.ceil(R + GAPPX)) + 1
for k in range(len(u)):
    x0, y0 = int(round(cx[k])), int(round(cy[k]))
    xs = np.arange(max(0, x0 - rg), min(Wpx, x0 + rg + 1)); ys = np.arange(max(0, y0 - rg), min(Hpx, y0 + rg + 1))
    X, Y = np.meshgrid(xs, ys); d2 = (X - cx[k]) ** 2 + (Y - cy[k]) ** 2
    ring = (d2 > R * R) & (d2 <= (R + GAPPX) ** 2)
    win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    kw = kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    behind = (win < cz[k] - 0.5 * R) & (kw >= 0) & (np.abs(kw - k) > 6 * R)   # a different part of the chain, clearly behind
    gapmask[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1] |= ring & behind
# shading
img = np.ones((Hpx, Wpx, 3))
hit = kbuf >= 0
cmap = plt.get_cmap("turbo")
base = cmap(0.04 + 0.92 * ci[kbuf.clip(0)])[..., :3]
light = np.array([-0.45, 0.55, 0.70]); light /= np.linalg.norm(light)
ndotl = np.clip((nbuf * light).sum(-1), 0, 1)
view = np.array([0, 0, 1.0]); half = light + view; half /= np.linalg.norm(half)
spec = np.clip((nbuf * half).sum(-1), 0, 1) ** 40
col = base * (0.35 + 0.65 * ndotl)[..., None] + 0.35 * spec[..., None]
# depth cue: farther parts slightly darker
zn = (zbuf - np.nanmin(zbuf[hit])) / (np.nanmax(zbuf[hit]) - np.nanmin(zbuf[hit]) + 1e-9)
col = col * (0.80 + 0.20 * zn)[..., None]
img[hit] = np.clip(col[hit], 0, 1)
img[gapmask & ~hit] = 1.0
img[gapmask & hit] = 1.0   # ring cuts the farther tube
# re-draw the nearer tube over its own gap ring: the ring belonged to sample k; pixels of other samples in front must stay.
# (ring pixels where the surface is NOT behind the ring's sphere were excluded, so nothing in front was erased.)
# thin dark outline around the tube silhouette
from scipy import ndimage
sil = hit & ~gapmask
edge = sil & ~ndimage.binary_erosion(sil, iterations=2)
img[edge] = img[edge] * 0.45
fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax_ = fig.add_axes([0, 0, 1, 1]); ax_.set_axis_off()
ax_.imshow(img, interpolation="bilinear"); ax_.set_xlim(0, Wpx); ax_.set_ylim(Hpx, 0)
Npx, Cpx = pix[0], pix[-1]
ax_.plot([Npx[0], Cpx[0]], [Npx[1], Cpx[1]], color="0.4", lw=2.0, ls=(0, (4, 3)), zorder=0.5)
cpix = cen * scale + off; cpix[1] = Hpx - cpix[1]
for p, q, lab in ((pix[0], pix[14], "N"), (pix[-1], pix[-15], "C")):
    back = q - p; back /= np.linalg.norm(back)            # into the chain, away from the gap
    v = p - cpix; v /= np.linalg.norm(v)                  # away from the centre of the figure
    perp = v - back * (v @ back); perp /= np.linalg.norm(perp) + 1e-9
    ax_.text(p[0] + 70 * back[0] + 62 * perp[0], p[1] + 70 * back[1] + 62 * perp[1], lab, fontsize=24, ha="center", va="center", fontweight="bold")
if labels:
    for c in D["crossings"]:
        q = c["pt"] * scale + off
        ax_.text(q[0], Hpx - q[1] - 40, str(c["id"] + 1), fontsize=15, color="red", ha="center")
fig.savefig(out, facecolor="white")
signs = [c["sign"] for c in D["crossings"]]
rec = dict(curve=CURVE, seed=seed, wob=wob, ang=ang, npt=NPT, cut=int(i0), gap=GAP, n=D["n"], writhe=D["writhe"], pd=D["pd"], signs=signs,
           crossings=[dict(id=c["id"], px=float(c["pt"][0] * scale + off[0]), py=float(Hpx - (c["pt"][1] * scale + off[1])), sign=c["sign"], over_first=bool(c["over_i"]), pi=float(c["pi"]), pj=float(c["pj"])) for c in D["crossings"]],
           mindist=float(D["mindist"] * scale), minangle=float(D["minangle"]), mindz=float(D["mindz"] * scale), R=R, gappx=GAPPX)
json.dump(rec, open(out.replace(".png", ".json"), "w"), indent=1)
print("n", D["n"], "writhe", D["writhe"], "mindist px", round(rec["mindist"]), "minangle", round(rec["minangle"], 1), "mindz px", round(rec["mindz"]))
