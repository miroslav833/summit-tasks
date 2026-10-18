"""Render a compact 27-mer conformation on the 3x3x3 cube as a 3D ball-and-tube picture.
Layers are pulled apart along the vertical axis (exploded view) so that all 27 beads are visible.
usage: draw_cube.py "<path as 27 site indices comma separated>" "<HP sequence>" out.png [--labels]
Sites are indexed x*9 + y*3 + z with x, y, z in 0..2."""
import numpy as np, sys
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

def coords(site):
    return np.array([site // 9, (site // 3) % 3, site % 3], float)

def render(path, seq, out, labels=False, explode=1.9, view=(0.52, -0.33, 0.35), Wpx=2400, Hpx=2000,
           Rb=46.0, Rt=16.0):
    P = np.array([coords(s) for s in path])
    P[:, 2] *= explode                                  # pull the three z layers apart
    P -= P.mean(0)
    # view rotation: rotate about x then y then z (viewer looks down the final z axis)
    def rot(ax, ay, az):
        cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
        Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]); return Rz @ Ry @ Rx
    Q = P @ rot(*view).T
    # mild perspective
    cam = 14.0
    persp = cam / (cam - Q[:, 2])
    xy = Q[:, :2] * persp[:, None]
    span = np.ptp(xy, axis=0); scale = min(Wpx * 0.78 / span[0], Hpx * 0.78 / span[1])
    pix = xy * scale + np.array([Wpx, Hpx]) / 2 - scale * (xy.max(0) + xy.min(0)) / 2
    pix[:, 1] = Hpx - pix[:, 1]
    depth = Q[:, 2] * scale
    zbuf = np.full((Hpx, Wpx), -np.inf); col = np.ones((Hpx, Wpx, 3)); nrm = np.zeros((Hpx, Wpx, 3)); kind = np.zeros((Hpx, Wpx), int)
    def stamp_sphere(c, z, R, rgb, tag):
        x0, y0 = int(round(c[0])), int(round(c[1])); r = int(np.ceil(R)) + 1
        xs = np.arange(max(0, x0 - r), min(Wpx, x0 + r + 1)); ys = np.arange(max(0, y0 - r), min(Hpx, y0 + r + 1))
        X, Y = np.meshgrid(xs, ys); dx = X - c[0]; dy = Y - c[1]; d2 = dx * dx + dy * dy
        h = np.sqrt(np.clip(R * R - d2, 0, None)); zs = z + h; inside = d2 <= R * R
        win = zbuf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]; upd = inside & (zs > win)
        win[upd] = zs[upd]
        col[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = rgb
        nrm[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = np.stack([dx / R, -dy / R, h / R], -1)[upd]
        kind[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1][upd] = tag
    # tubes: sphere sweep between consecutive beads
    grey = np.array([0.72, 0.72, 0.72])
    for k in range(len(P) - 1):
        a, b = pix[k], pix[k + 1]; za, zb = depth[k], depth[k + 1]
        n = int(np.linalg.norm(b - a) / 1.0) + 2
        for t in np.linspace(0, 1, n):
            stamp_sphere(a + t * (b - a), za + t * (zb - za), Rt * (persp[k] + t * (persp[k + 1] - persp[k])), grey, 1)
    hcol = np.array([0.93, 0.45, 0.10]); pcol = np.array([0.33, 0.55, 0.90])
    for k in range(len(P)):
        stamp_sphere(pix[k], depth[k], Rb * persp[k], hcol if seq[k] == "H" else pcol, 2)
    hit = zbuf > -np.inf
    light = np.array([-0.4, 0.5, 0.75]); light /= np.linalg.norm(light)
    ndl = np.clip((nrm * light).sum(-1), 0, 1); half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half)
    spec = np.clip((nrm * half).sum(-1), 0, 1) ** 50
    img = np.ones((Hpx, Wpx, 3))
    shade = col * (0.38 + 0.62 * ndl)[..., None] + 0.4 * spec[..., None]
    img[hit] = np.clip(shade[hit], 0, 1)
    from scipy import ndimage
    edge = hit & ~ndimage.binary_erosion(hit, iterations=2)
    img[edge] *= 0.5
    # outline between a bead and whatever is behind it
    dz = np.abs(np.diff(zbuf, axis=0, prepend=zbuf[:1]))
    dz2 = np.abs(np.diff(zbuf, axis=1, prepend=zbuf[:, :1]))
    jump = hit & ((dz > 25) | (dz2 > 25)) & np.isfinite(dz) & np.isfinite(dz2)
    img[jump] *= 0.55
    fig = plt.figure(figsize=(Wpx / 200, Hpx / 200), dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(img, interpolation="bilinear"); ax.set_xlim(0, Wpx); ax.set_ylim(Hpx, 0)
    if labels:
        for k in range(len(P)):
            ax.text(pix[k][0], pix[k][1], str(k + 1), fontsize=12, ha="center", va="center", color="black" if seq[k] == "P" else "white", fontweight="bold")
    # terminus labels
    for k, lab in ((0, "N"), (len(P) - 1, "C")):
        v = pix[k] - pix[1 if k == 0 else -2]; v /= np.linalg.norm(v)
        ax.text(pix[k][0] + 1.6 * Rb * v[0], pix[k][1] + 1.6 * Rb * v[1], lab, fontsize=22, ha="center", va="center", fontweight="bold")
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return pix, depth

if __name__ == "__main__":
    path = [int(v) for v in sys.argv[1].split(",")]; seq = sys.argv[2]; out = sys.argv[3]
    render(path, seq, out, labels="--labels" in sys.argv)
    print("written", out)
