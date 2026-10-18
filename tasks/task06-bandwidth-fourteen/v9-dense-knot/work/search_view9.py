import numpy as np, sys, json, knotlib as K
from scipy.interpolate import CubicSpline
from render_dense import rot
CA = np.load("calpha.npy"); n = len(CA); seed = int(sys.argv[1]); ntr = int(sys.argv[2])
rng = np.random.default_rng(seed); rows = []
t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(CA, axis=0), axis=1))]; cs = CubicSpline(t, CA - CA.mean(0))
u = np.linspace(0, t[-1], 1400); F0 = cs(u); res_of = np.interp(u, t, np.arange(n))     # residue index per sample
for trial in range(ntr):
    v = rng.uniform(-np.pi, np.pi, 3); R = rot(*v)
    F = F0 @ R.T; clos = np.linspace(F[-1], F[0], 25, endpoint=False)[1:]; closed = np.vstack([F, clos])
    D = K.diagram(closed); nf = len(F)
    onc = sum(1 for c in D["crossings"] if c["pi"] >= nf - 1 or c["pj"] >= nf - 1)
    if onc: continue
    # crossings between different parts of the chain (more than 6 residues apart)
    far = [c for c in D["crossings"] if abs(res_of[min(int(c["pi"]), nf - 1)] - res_of[min(int(c["pj"]), nf - 1)]) > 6]
    mindz_far = min((c["dz"] for c in far), default=99); minang_far = min((c["angle"] for c in far), default=90)
    span = np.ptp(F[:, :2], axis=0); aspect = span.min() / span.max()
    rows.append(dict(view=[float(a) for a in v], n=D["n"], far=len(far), mindz_far=round(float(mindz_far), 2), minang_far=round(float(minang_far), 1), aspect=round(float(aspect), 2)))
rows.sort(key=lambda r: -(min(r["mindz_far"], 6) * min(r["minang_far"], 30) * min(r["aspect"], 0.8)))
for r in rows[:8]: print(r)
json.dump(rows[:30], open(f"views9_{seed}.json", "w"))
