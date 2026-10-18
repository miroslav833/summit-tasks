"""Cartoon-style rendering: smooth tube through the C-alpha trace, spheres with residue numbers,
dashed restraint lines. usage: draw2.py bundle.pkl out.png [ax ay az] [--nolabels]"""
import numpy as np, sys, pickle
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.interpolate import CubicSpline
from draw import rot, line_clearance

def render(X, E1, out, view, Wpx=2400, Hpx=2000, Rb=24.0, Rt=13.0, labels=True):
    n = len(X); P = X - X.mean(0); Q = P @ rot(*view).T
    cam = 110.0
    def project(V):
        pe = cam / (cam - V[:, 2]); xy = V[:, :2] * pe[:, None]; return xy, pe
    xyA, peA = project(Q)
    span = np.ptp(xyA, axis=0); scale = min(Wpx * 0.76 / span[0], Hpx * 0.76 / span[1])
    off = np.array([Wpx, Hpx]) / 2 - scale * (xyA.max(0) + xyA.min(0)) / 2
    def topix(xy): p = xy * scale + off; p[:, 1] = Hpx - p[:, 1]; return p
    pix = topix(xyA); depth = Q[:, 2] * scale
    # smooth tube through the atoms
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; cs = CubicSpline(t, Q)
    u = np.linspace(0, t[-1], 3000); T = cs(u); xyT, peT = project(T); pixT = topix(xyT); depT = T[:, 2] * scale
    zbuf = np.full((Hpx, Wpx), -np.inf); col = np.ones((Hpx, Wpx, 3)); nrm = np.zeros((Hpx, Wpx, 3))
    def stamp(c, z, R, rgb):
        x0, y0 = int(round(c[0])), int(round(c[1])); r = int(np.ceil(R)) + 1
        xs = np.arange(max(0, x0 - r), min(Wpx, x0 + r + 1)); ys = np.arange(max(0, y0 - r), min(Hpx, y0 + r + 1))
        if len(xs) == 0 or len(ys) == 0: return
        Xg, Yg = np.meshgrid(xs, ys); dx = Xg - c[0]; dy = Yg - c[1]; d2 = dx * dx + dy * dy
        h = np.sqrt(np.clip(R * R - d2, 0, None)); zs = z + h; inside = d2 <= R * R
        win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; upd = inside & (zs > win); win[upd] = zs[upd]
        col[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = rgb
        nrm[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = np.stack([dx / R, -dy / R, h / R], -1)[upd]
    cmap = plt.get_cmap("turbo")
    for k in range(len(u)):
        stamp(pixT[k], depT[k], Rt * peT[k], np.array(cmap(0.05 + 0.9 * u[k] / t[-1])[:3]))
    for k in range(n): stamp(pix[k], depth[k], Rb * peA[k], np.array([0.88, 0.88, 0.88]))
    hit = zbuf > -np.inf
    light = np.array([-0.4, 0.5, 0.75]); light /= np.linalg.norm(light); ndl = np.clip((nrm * light).sum(-1), 0, 1)
    half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half); spec = np.clip((nrm * half).sum(-1), 0, 1) ** 50
    img = np.ones((Hpx, Wpx, 3)); shade = col * (0.40 + 0.60 * ndl)[..., None] + 0.35 * spec[..., None]
    zn = (zbuf - zbuf[hit].min()) / (zbuf[hit].max() - zbuf[hit].min() + 1e-9); shade = shade * (0.78 + 0.22 * zn)[..., None]
    img[hit] = np.clip(shade[hit], 0, 1)
    edge = hit & ~ndimage.binary_erosion(hit, iterations=2); img[edge] *= 0.5
    dz = np.abs(np.diff(zbuf, axis=0, prepend=zbuf[:1])); dz2 = np.abs(np.diff(zbuf, axis=1, prepend=zbuf[:, :1]))
    jump = hit & ((dz > 18) | (dz2 > 18)) & np.isfinite(dz) & np.isfinite(dz2); img[jump] *= 0.55
    fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(img, interpolation="bilinear"); ax.set_xlim(0, Wpx); ax.set_ylim(Hpx, 0)
    for li, (a, b) in enumerate(E1):
        p, q = pix[a - 1], pix[b - 1]
        ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=2.4, ls=(0, (5, 4)), zorder=3)
        frac = {(24, 29): 0.42, (29, 34): 0.72, (10, 15): 0.30, (13, 18): 0.62}.get((a, b), (0.30, 0.45, 0.60, 0.75)[li % 4])
        m = p + frac * (q - p)
        ax.text(m[0], m[1], f"{a}-{b}", fontsize=10, ha="center", va="center", color="black", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="black", lw=0.6, alpha=0.95))
    if labels:
        for k in range(n):
            ax.text(pix[k][0], pix[k][1], str(k + 1), fontsize=11.5 * peA[k], ha="center", va="center", color="black", fontweight="bold", zorder=4)
    for k, lab in ((0, "N"), (n - 1, "C")):
        v = pix[k] - pix[1 if k == 0 else n - 2]; v /= np.linalg.norm(v)
        ax.text(pix[k][0] + 2.8 * Rb * v[0], pix[k][1] + 2.8 * Rb * v[1], lab, fontsize=22, ha="center", va="center", fontweight="bold")
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return pix

if __name__ == "__main__":
    inst = pickle.load(open(sys.argv[1], "rb")); X = inst["X"]; E1 = inst["E1"]
    args = [a for a in sys.argv[3:] if not a.startswith("--")]
    if len(args) >= 3: view = tuple(float(v) for v in args[:3])
    else:
        rng = np.random.default_rng(1); best = None
        for _ in range(4000):
            v = tuple(rng.uniform(-np.pi, np.pi, 3)); c = line_clearance(X, E1, v)
            # also prefer views where atom centres are well separated in projection
            Q = (X - X.mean(0)) @ rot(*v).T; xy = Q[:, :2]
            dmin = min(np.linalg.norm(xy[i] - xy[j]) for i in range(len(X)) for j in range(i + 1, len(X)))
            score = 2.0 * min(c, 1.5) + min(dmin, 1.6)
            if best is None or score > best[0]: best = (score, v, c, dmin)
        view = best[1]; print("view", [round(a, 3) for a in view], "line clearance", round(best[2], 2), "atom sep", round(best[3], 2))
    render(X, E1, sys.argv[2], view, labels="--nolabels" not in sys.argv); print("written", sys.argv[2])
