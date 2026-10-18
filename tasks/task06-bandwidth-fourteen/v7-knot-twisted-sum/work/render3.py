"""Warp the planar twisted-sum diagram smoothly (keeps the diagram combinatorics), add a small depth
wobble, render as a shaded tube. usage: render3.py seed amp out.png [--labels]"""
import numpy as np, sys, json, knotlib as K, altcheck as A, twisted_sum as T
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
seed, amp, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]; labels = "--labels" in sys.argv
rng = np.random.default_rng(seed)
C = K.smooth(T.build(1, True, True), 3000)
# planar warp: x' = x + sum a cos(k.x + phi) in both coordinates, low frequency, small amplitude
X = C[:, :2].copy(); L = np.ptp(X, axis=0).max()
W = np.zeros_like(X)
for _ in range(5):
    kx, ky = rng.uniform(-1.2, 1.2, 2) * 2 * np.pi / L; ph = rng.uniform(0, 2 * np.pi, 2); a = rng.normal(0, amp * L, 2)
    W[:, 0] += a[0] * np.cos(kx * X[:, 0] + ky * X[:, 1] + ph[0]); W[:, 1] += a[1] * np.cos(kx * X[:, 0] + ky * X[:, 1] + ph[1])
# rotate the whole picture a bit and shear slightly
th = rng.uniform(-0.5, 0.5); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
X = (X + W) @ R.T
Z = C[:, 2].copy()
u = np.linspace(0, 2 * np.pi, len(C), endpoint=False)
for m in range(1, 5): Z += 0.10 * rng.normal() * np.cos(m * u + rng.uniform(0, 2 * np.pi))
Q = np.c_[X, Z]
D = K.diagram(Q)
# the open chain: cut on the outer closure arc of 5_1 (farthest from centre, away from crossings)
N = len(Q); cen = Q[:, :2].mean(0); r = np.linalg.norm(Q[:, :2] - cen, axis=1)
cp = sorted([c["pi"] for c in D["crossings"]] + [c["pj"] for c in D["crossings"]])
def clear(i, m=60): return all(min(abs(p - i), N - abs(p - i)) > m for p in cp)
i0 = next(i for i in np.argsort(-r) if clear(i)); GAP = 14
start = (i0 + GAP // 2) % N; idx = [(start + k) % N for k in range(N - GAP)]; P = Q[idx]
# ---- raster (same method as v5)
Wpx, Hpx = 2400, 2000; margin = 0.09
xy = P[:, :2]; lo = xy.min(0); hi = xy.max(0); span = hi - lo
scale = min(Wpx * (1 - 2 * margin) / span[0], Hpx * (1 - 2 * margin) / span[1])
off = np.array([Wpx, Hpx]) / 2 - scale * (lo + hi) / 2
pix = xy * scale + off; pix[:, 1] = Hpx - pix[:, 1]; depth = P[:, 2] * scale
seg = np.linalg.norm(np.diff(pix, axis=0), axis=1); s = np.r_[0, np.cumsum(seg)]; uu = np.arange(0, s[-1], 1.0)
cx = np.interp(uu, s, pix[:, 0]); cy = np.interp(uu, s, pix[:, 1]); cz = np.interp(uu, s, depth); ci = uu / s[-1]
Rr, GAPPX = 16.0, 8.0
zbuf = np.full((Hpx, Wpx), -np.inf); kbuf = np.full((Hpx, Wpx), -1, int); nbuf = np.zeros((Hpx, Wpx, 3)); rr = int(np.ceil(Rr)) + 1
for k in range(len(uu)):
    x0, y0 = int(round(cx[k])), int(round(cy[k]))
    xs = np.arange(max(0, x0 - rr), min(Wpx, x0 + rr + 1)); ys = np.arange(max(0, y0 - rr), min(Hpx, y0 + rr + 1))
    Xg, Yg = np.meshgrid(xs, ys); dx = Xg - cx[k]; dy = Yg - cy[k]; d2 = dx * dx + dy * dy; inside = d2 <= Rr * Rr
    h = np.sqrt(np.clip(Rr * Rr - d2, 0, None)); zs = cz[k] + h
    win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; upd = inside & (zs > win); win[upd] = zs[upd]
    kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = k
    nbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = np.stack([dx / Rr, -dy / Rr, h / Rr], -1)[upd]
gapmask = np.zeros((Hpx, Wpx), bool); rg = int(np.ceil(Rr + GAPPX)) + 1
for k in range(len(uu)):
    x0, y0 = int(round(cx[k])), int(round(cy[k]))
    xs = np.arange(max(0, x0 - rg), min(Wpx, x0 + rg + 1)); ys = np.arange(max(0, y0 - rg), min(Hpx, y0 + rg + 1))
    Xg, Yg = np.meshgrid(xs, ys); d2 = (Xg - cx[k]) ** 2 + (Yg - cy[k]) ** 2; ring = (d2 > Rr * Rr) & (d2 <= (Rr + GAPPX) ** 2)
    win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; kw = kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    behind = (win < cz[k] - 0.5 * Rr) & (kw >= 0) & (np.abs(kw - k) > 6 * Rr)
    gapmask[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1] |= ring & behind
img = np.ones((Hpx, Wpx, 3)); hit = kbuf >= 0; cmap = plt.get_cmap("turbo")
base = cmap(0.04 + 0.92 * ci[kbuf.clip(0)])[..., :3]
light = np.array([-0.45, 0.55, 0.70]); light /= np.linalg.norm(light); ndotl = np.clip((nbuf * light).sum(-1), 0, 1)
half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half); spec = np.clip((nbuf * half).sum(-1), 0, 1) ** 40
col = base * (0.35 + 0.65 * ndotl)[..., None] + 0.35 * spec[..., None]
zn = (zbuf - zbuf[hit].min()) / (zbuf[hit].max() - zbuf[hit].min() + 1e-9); col = col * (0.80 + 0.20 * zn)[..., None]
img[hit] = np.clip(col[hit], 0, 1); img[gapmask] = 1.0
sil = hit & ~gapmask; edge = sil & ~ndimage.binary_erosion(sil, iterations=2); img[edge] *= 0.45
fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax_ = fig.add_axes([0, 0, 1, 1]); ax_.set_axis_off()
ax_.imshow(img, interpolation="bilinear"); ax_.set_xlim(0, Wpx); ax_.set_ylim(Hpx, 0)
Npx, Cpx = pix[0], pix[-1]
ax_.plot([Npx[0], Cpx[0]], [Npx[1], Cpx[1]], color="0.4", lw=2.0, ls=(0, (4, 3)), zorder=0.5)
cpix = cen * scale + off; cpix[1] = Hpx - cpix[1]
for p, q, lab in ((pix[0], pix[14], "N"), (pix[-1], pix[-15], "C")):
    back = q - p; back /= np.linalg.norm(back); v = p - cpix; v /= np.linalg.norm(v)
    perp = v - back * (v @ back); perp /= np.linalg.norm(perp) + 1e-9
    ax_.text(p[0] + 70 * back[0] + 60 * perp[0], p[1] + 70 * back[1] + 60 * perp[1], lab, fontsize=24, ha="center", va="center", fontweight="bold")
if labels:
    for c in D["crossings"]:
        q = c["pt"] * scale + off; ax_.text(q[0], Hpx - q[1] - 40, str(c["id"] + 1), fontsize=15, color="red", ha="center")
fig.savefig(out, facecolor="white")
rec = dict(seed=seed, amp=amp, n=D["n"], writhe=D["writhe"], alternating=A.alternating(D), nugatory=[i + 1 for i in A.nugatory(D)],
           det=K.determinant(D["pd"]), signs=[c["sign"] for c in D["crossings"]],
           crossings=[dict(id=c["id"] + 1, px=float(c["pt"][0] * scale + off[0]), py=float(Hpx - (c["pt"][1] * scale + off[1])), sign=c["sign"]) for c in D["crossings"]],
           mindist_px=float(D["mindist"] * scale), minangle=float(D["minangle"]), mindz_px=float(D["mindz"] * scale))
json.dump(rec, open(out.replace(".png", ".json"), "w"), indent=1)
print({k: rec[k] for k in ("n", "alternating", "nugatory", "det", "mindist_px", "minangle", "mindz_px")})
