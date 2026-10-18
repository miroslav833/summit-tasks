"""Choose the view, check the closure segment, verify the fine chain's knot type, render.
usage: finalize.py ax ay az out.png"""
import numpy as np, sys, json, knotlib as K
from scipy.interpolate import CubicSpline
from render_dense import rot, render
CA = np.load("calpha.npy"); n = len(CA)
view = tuple(float(v) for v in sys.argv[1:4]); out = sys.argv[4]
Q = (CA - CA.mean(0)) @ rot(*view).T
# fine closed curve: spline through the C-alphas, plus the straight closure segment
t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; cs = CubicSpline(t, Q)
u = np.linspace(0, t[-1], 2600); F = cs(u)
clos = np.linspace(Q[-1], Q[0], 40, endpoint=False)[1:]
closed = np.vstack([F, clos])
D = K.diagram(closed)
nf = len(F)
on_closure = [c for c in D["crossings"] if c["pi"] >= nf - 1 or c["pj"] >= nf - 1]
print("fine diagram: crossings", D["n"], " crossings on the closure segment:", len(on_closure),
      " min crossing angle %.1f deg" % D["minangle"], " min depth gap %.2f A" % D["mindz"])
# Alexander polynomial of the fine diagram by exact integer evaluation (Bareiss) at several t,
# compared with the coarse curve's polynomial
def arcs_of(pd):
    E = 2 * len(pd); starts = sorted(x[2] for x in pd); arc = {}
    for k, s in enumerate(starts):
        e = s
        while True:
            arc[e] = k; e = (e + 1) % E
            if e in starts: break
    return arc
def alex_eval(pd, signs, tv):
    arc = arcs_of(pd); m = len(pd); M = [[0] * m for _ in range(m)]
    for r, ((a, b, c, d), sg) in enumerate(zip(pd, signs)):
        if sg > 0: M[r][arc[b]] += 1 - tv; M[r][arc[a]] += tv; M[r][arc[c]] += -1
        else: M[r][arc[b]] += 1 - tv; M[r][arc[a]] += -1; M[r][arc[c]] += tv
    A = [row[1:] for row in M[1:]]; N = len(A)      # Bareiss determinant over integers
    sign = 1; prev = 1
    for k in range(N - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, N) if A[i][k] != 0), None)
            if sw is None: return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, N):
            for j in range(k + 1, N):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[N - 1][N - 1]
coarse = np.load("coarse.npy"); Dc = K.diagram(coarse)
Jc = K.jones(Dc["pd"], Dc["writhe"]); known = {-6: -1, -5: 1, -4: -1, -3: 2, -2: -1, -1: 1}
print("coarse curve: crossings", Dc["n"], "det", K.determinant(Dc["pd"]), "Jones is 5_2:", Jc == known or Jc == {-k: v for k, v in known.items()})
ratios = []
for tv in (2, 3, 5, 7):
    af = alex_eval(D["pd"], [c["sign"] for c in D["crossings"]], tv); ac = alex_eval(Dc["pd"], [c["sign"] for c in Dc["crossings"]], tv)
    ratios.append((tv, af, ac))
# Alexander polynomials agree up to +-t^k: the ratio af/ac must be +-tv^k with one k for all tv
ks = []
for tv, af, ac in ratios:
    r = abs(af) / abs(ac) if ac else None; k = round(np.log(r) / np.log(tv)) if r else None
    ks.append((k, abs(af) == abs(ac) * tv ** k if k is not None and k >= 0 else abs(af) * tv ** (-k) == abs(ac)))
print("Alexander(fine)/Alexander(coarse) = +-t^k with k =", [k for k, ok in ks], "exact:", all(ok for _, ok in ks) and len({k for k, _ in ks}) == 1)
print("determinant of the fine diagram:", abs(alex_eval(D["pd"], [c["sign"] for c in D["crossings"]], -1)))
pix, depth = render(CA, out, view)
json.dump(dict(view=view, n=n, fine_crossings=D["n"], closure_crossings=len(on_closure), coarse_crossings=Dc["n"]), open(out.replace(".png", ".json"), "w"))
