"""Dense protein cartoon: smooth tube through the C-alpha positions, rainbow N to C, z-buffered with
white gaps where the chain passes behind itself, dashed closure between the termini.
usage: render_dense.py calpha.npy out.png ax ay az [--numbers]"""
import numpy as np, sys
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.interpolate import CubicSpline

def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]); return Rz @ Ry @ Rx

def render(CA, out, view, Wpx=2400, Hpx=2000, Rt=11.0, GAPPX=6.0, numbers=False, every=20):
    n = len(CA); Q = (CA - CA.mean(0)) @ rot(*view).T
    xy = Q[:, :2]; span = np.ptp(xy, axis=0); scale = min(Wpx * 0.86 / span[0], Hpx * 0.86 / span[1])
    off = np.array([Wpx, Hpx]) / 2 - scale * (xy.max(0) + xy.min(0)) / 2
    def topix(v): p = v * scale + off; p[:, 1] = Hpx - p[:, 1]; return p
    pix = topix(xy); depth = Q[:, 2] * scale
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; cs = CubicSpline(t, Q)
    u = np.linspace(0, t[-1], int(t[-1] * scale / 0.8)); T = cs(u); pixT = topix(T[:, :2]); depT = T[:, 2] * scale
    zbuf = np.full((Hpx, Wpx), -np.inf); kbuf = np.full((Hpx, Wpx), -1, int); nrm = np.zeros((Hpx, Wpx, 3))
    rr = int(np.ceil(Rt)) + 1
    for k in range(len(u)):
        x0, y0 = int(round(pixT[k][0])), int(round(pixT[k][1]))
        xs = np.arange(max(0, x0 - rr), min(Wpx, x0 + rr + 1)); ys = np.arange(max(0, y0 - rr), min(Hpx, y0 + rr + 1))
        if len(xs) == 0 or len(ys) == 0: continue
        Xg, Yg = np.meshgrid(xs, ys); dx = Xg - pixT[k][0]; dy = Yg - pixT[k][1]; d2 = dx * dx + dy * dy
        h = np.sqrt(np.clip(Rt * Rt - d2, 0, None)); zs = depT[k] + h; inside = d2 <= Rt * Rt
        win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; upd = inside & (zs > win); win[upd] = zs[upd]
        kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = k
        nrm[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = np.stack([dx / Rt, -dy / Rt, h / Rt], -1)[upd]
    # gap ring: pixels within GAPPX outside a sample's tube where the visible surface is a different,
    # farther part of the chain
    gap = np.zeros((Hpx, Wpx), bool); rg = int(np.ceil(Rt + GAPPX)) + 1
    for k in range(0, len(u), 2):
        x0, y0 = int(round(pixT[k][0])), int(round(pixT[k][1]))
        xs = np.arange(max(0, x0 - rg), min(Wpx, x0 + rg + 1)); ys = np.arange(max(0, y0 - rg), min(Hpx, y0 + rg + 1))
        if len(xs) == 0 or len(ys) == 0: continue
        Xg, Yg = np.meshgrid(xs, ys); d2 = (Xg - pixT[k][0]) ** 2 + (Yg - pixT[k][1]) ** 2
        ring = (d2 > Rt * Rt) & (d2 <= (Rt + GAPPX) ** 2)
        win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; kw = kbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
        behind = (win < depT[k] - 0.6 * Rt) & (kw >= 0) & (np.abs(kw - k) > 8 * Rt)
        gap[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1] |= ring & behind
    hit = kbuf >= 0; cmap = plt.get_cmap("turbo")
    base = cmap(0.04 + 0.92 * (u[kbuf.clip(0)] / t[-1]))[..., :3]
    light = np.array([-0.4, 0.5, 0.75]); light /= np.linalg.norm(light); ndl = np.clip((nrm * light).sum(-1), 0, 1)
    half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half); spec = np.clip((nrm * half).sum(-1), 0, 1) ** 40
    img = np.ones((Hpx, Wpx, 3)); shade = base * (0.38 + 0.62 * ndl)[..., None] + 0.33 * spec[..., None]
    zn = (zbuf - zbuf[hit].min()) / (zbuf[hit].max() - zbuf[hit].min() + 1e-9); shade = shade * (0.72 + 0.28 * zn)[..., None]
    img[hit] = np.clip(shade[hit], 0, 1); img[gap] = 1.0
    sil = hit & ~gap; edge = sil & ~ndimage.binary_erosion(sil, iterations=1); img[edge] *= 0.45
    fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(img, interpolation="bilinear"); ax.set_xlim(0, Wpx); ax.set_ylim(Hpx, 0)
    ax.plot([pix[0][0], pix[-1][0]], [pix[0][1], pix[-1][1]], color="0.35", lw=2.0, ls=(0, (4, 3)), zorder=0.5)
    cpix = np.array([Wpx / 2, Hpx / 2])
    for k, lab in ((0, "N"), (n - 1, "C")):
        v = pix[k] - cpix; v /= np.linalg.norm(v)
        ax.text(pix[k][0] + 55 * v[0], pix[k][1] + 55 * v[1], lab, fontsize=24, ha="center", va="center", fontweight="bold")
    if numbers:
        for k in range(every - 1, n, every):
            ax.text(pix[k][0], pix[k][1], str(k + 1), fontsize=9, ha="center", va="center", color="black",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="black", lw=0.5, alpha=0.9), zorder=4)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return pix, depth

if __name__ == "__main__":
    CA = np.load(sys.argv[1]); out = sys.argv[2]; view = tuple(float(v) for v in sys.argv[3:6])
    render(CA, out, view, numbers="--numbers" in sys.argv); print("written", out)
