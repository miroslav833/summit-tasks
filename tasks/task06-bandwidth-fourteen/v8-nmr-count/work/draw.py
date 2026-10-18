"""3D ball-and-tube rendering of the C-alpha fragment with numbered atoms and dashed restraint lines.
usage: draw.py instance.pkl out.png [ax ay az]"""
import numpy as np, sys, pickle
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage

def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]); return Rz @ Ry @ Rx

def render(X, E1, out, view=(0.4, -0.5, 0.2), Wpx=2400, Hpx=2000, Rb=27.0, Rt=10.0, labels=True):
    n = len(X)
    P = X - X.mean(0); Q = P @ rot(*view).T
    cam = 90.0; persp = cam / (cam - Q[:, 2])
    xy = Q[:, :2] * persp[:, None]
    span = np.ptp(xy, axis=0); scale = min(Wpx * 0.74 / span[0], Hpx * 0.74 / span[1])
    pix = xy * scale + np.array([Wpx, Hpx]) / 2 - scale * (xy.max(0) + xy.min(0)) / 2; pix[:, 1] = Hpx - pix[:, 1]
    depth = Q[:, 2] * scale
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
    for k in range(n - 1):
        a, b = pix[k], pix[k + 1]; za, zb = depth[k], depth[k + 1]; m = int(np.linalg.norm(b - a)) + 2
        ca = np.array(cmap(0.05 + 0.9 * k / (n - 1))[:3]); cb = np.array(cmap(0.05 + 0.9 * (k + 1) / (n - 1))[:3])
        for t in np.linspace(0, 1, m): stamp(a + t * (b - a), za + t * (zb - za), Rt * (persp[k] + t * (persp[k + 1] - persp[k])), ca + t * (cb - ca))
    for k in range(n): stamp(pix[k], depth[k], Rb * persp[k], np.array([0.86, 0.86, 0.86]))
    hit = zbuf > -np.inf
    light = np.array([-0.4, 0.5, 0.75]); light /= np.linalg.norm(light); ndl = np.clip((nrm * light).sum(-1), 0, 1)
    half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half); spec = np.clip((nrm * half).sum(-1), 0, 1) ** 50
    img = np.ones((Hpx, Wpx, 3)); shade = col * (0.40 + 0.60 * ndl)[..., None] + 0.35 * spec[..., None]
    img[hit] = np.clip(shade[hit], 0, 1)
    edge = hit & ~ndimage.binary_erosion(hit, iterations=2); img[edge] *= 0.5
    dz = np.abs(np.diff(zbuf, axis=0, prepend=zbuf[:1])); dz2 = np.abs(np.diff(zbuf, axis=1, prepend=zbuf[:, :1]))
    jump = hit & ((dz > 20) | (dz2 > 20)) & np.isfinite(dz) & np.isfinite(dz2); img[jump] *= 0.55
    fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(img, interpolation="bilinear"); ax.set_xlim(0, Wpx); ax.set_ylim(Hpx, 0)
    # restraint lines: dashed, drawn on top, with the pair written at the midpoint
    for (u, w) in E1:
        a, b = pix[u - 1], pix[w - 1]
        ax.plot([a[0], b[0]], [a[1], b[1]], color="black", lw=2.2, ls=(0, (5, 4)), zorder=3)
    if labels:
        for k in range(n):
            ax.text(pix[k][0], pix[k][1], str(k + 1), fontsize=13 * persp[k], ha="center", va="center", color="black", fontweight="bold", zorder=4)
    for k, lab in ((0, "N"), (n - 1, "C")):
        v = pix[k] - pix[1 if k == 0 else n - 2]; v /= np.linalg.norm(v)
        ax.text(pix[k][0] + 2.0 * Rb * v[0], pix[k][1] + 2.0 * Rb * v[1], lab, fontsize=22, ha="center", va="center", fontweight="bold")
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return pix, depth

def line_clearance(X, E1, view):
    """smallest distance in the picture between a dashed line and an atom centre that is not one of its ends,
    and between two dashed lines' midpoints; used to pick a readable view"""
    n = len(X); P = X - X.mean(0); Q = P @ rot(*view).T; xy = Q[:, :2]
    worst = np.inf
    for (u, w) in E1:
        a, b = xy[u - 1], xy[w - 1]; d = b - a; L = np.linalg.norm(d)
        for k in range(n):
            if k in (u - 1, w - 1): continue
            t = np.clip((xy[k] - a) @ d / (L * L), 0, 1); dist = np.linalg.norm(xy[k] - (a + t * d)); worst = min(worst, dist)
    return worst

if __name__ == "__main__":
    inst = pickle.load(open(sys.argv[1], "rb")); X = inst["X"]; E1 = inst["E1"]
    if len(sys.argv) > 3: view = tuple(float(v) for v in sys.argv[3:6])
    else:
        rng = np.random.default_rng(0); best = None
        for _ in range(400):
            v = tuple(rng.uniform(-np.pi, np.pi, 3)); c = line_clearance(X, E1, v)
            if best is None or c > best[0]: best = (c, v)
        view = best[1]; print("view", [round(a, 3) for a in view], "clearance", round(best[0], 2))
    render(X, E1, sys.argv[2], view=view); print("written", sys.argv[2])
