"""Key check for the dense knotted protein (task06 v9).

Construction (work/): coarse.py builds the closure of the 3-braid s1^3 s2 s1^-1 s2, the knot 5_2;
tighten.py relaxes it to a compact curve of clearance 1 unit; decorate.py scales it to 9.2 A per
unit and lays 200 C-alpha atoms along it as helices (radius 2.3 A, rise 1.5 A), strands and loops,
all within 2.3 A of the axis; render_dense.py draws the tube from the view in work/image_view.json.
Every part of the chain stays within 2.3 A of the axis and distinct parts of the axis stay 9.2 A
apart, so the chain is isotopic to the axis and has its knot type. This script also checks the type
directly from the drawn chain:
  1. axis curve: Jones polynomial equals that of 5_2 (unique among knots up to 9 crossings);
  2. full chain plus the straight closure between the termini, projected along the drawing
     direction: Alexander polynomial equals the axis curve's up to a unit (exact integer
     evaluations at t = 2, 3, 5, 7), determinant 7;
  3. the closure segment carries no crossing in the drawing, and every crossing between parts of
     the chain more than six residues apart has a clear depth separation.
Crossing number of 5_2 is 5 (Rolfsen table). Run: python3 verify_key.py (numpy, scipy, sympy).
"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "work"))
import knotlib as K
from scipy.interpolate import CubicSpline
from render_dense import rot

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
    A = [row[1:] for row in M[1:]]; N = len(A); sign = 1; prev = 1
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

CA = np.load(os.path.join(HERE, "work", "calpha.npy")); n = len(CA)
view = json.load(open(os.path.join(HERE, "work", "image_view.json")))["view"]
seg = json.load(open(os.path.join(HERE, "work", "segments.json")))
print("residues:", n, " view:", [round(v, 4) for v in view])
print("secondary structure:", ", ".join(f"{s['kind']} {s['first']}-{s['last']}" for s in seg["segments"]))
D_ca = np.linalg.norm(CA[:, None] - CA[None], axis=2)
print("C-alpha spacing %.2f-%.2f A, smallest non-bonded distance %.2f A" % (min(D_ca[i, i + 1] for i in range(n - 1)), max(D_ca[i, i + 1] for i in range(n - 1)), min(D_ca[i, j] for i in range(n) for j in range(i + 3, n))))

print("\n== 1. axis curve")
coarse = np.load(os.path.join(HERE, "work", "coarse.npy"))
Dc = K.diagram(coarse); Jc = K.jones(Dc["pd"], Dc["writhe"]); known = {-6: -1, -5: 1, -4: -1, -3: 2, -2: -1, -1: 1}
is52 = Jc == known or Jc == {-k: v for k, v in known.items()}
print("crossings in the z-projection:", Dc["n"], " determinant:", K.determinant(Dc["pd"]), " Jones:", K.jones_str(Jc), " equals 5_2:", is52)
# isotopy margin: smallest distance between axis points more than 40 samples apart, in A
N = len(coarse); d = np.linalg.norm(coarse[:, None] - coarse[None], axis=2)
idx = np.abs(np.subtract.outer(np.arange(N), np.arange(N))); idx = np.minimum(idx, N - idx)
reach = d[idx >= 40].min() * seg["scale"]
print("axis clearance %.1f A, chain offset from the axis at most 2.3 A: isotopy margin %.1f A" % (reach, reach - 4.6))

print("\n== 2. the drawn chain with its closure")
Q = (CA - CA.mean(0)) @ rot(*view).T
t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; cs = CubicSpline(t, Q)
u = np.linspace(0, t[-1], 2600); F = cs(u); res_of = np.interp(u, t, np.arange(n))
clos = np.linspace(Q[-1], Q[0], 40, endpoint=False)[1:]; closed = np.vstack([F, clos]); nf = len(F)
D = K.diagram(closed); signs = [c["sign"] for c in D["crossings"]]
onc = [c for c in D["crossings"] if c["pi"] >= nf - 1 or c["pj"] >= nf - 1]
far = [c for c in D["crossings"] if abs(res_of[min(int(c["pi"]), nf - 1)] - res_of[min(int(c["pj"]), nf - 1)]) > 6]
print("crossings in the drawing:", D["n"], " on the closure segment:", len(onc), " between parts more than six residues apart:", len(far))
print("smallest depth separation at those crossings: %.2f A, smallest crossing angle %.1f degrees" % (min(c["dz"] for c in far), min(c["angle"] for c in far)))
ok = True; ks = set()
for tv in (2, 3, 5, 7):
    af = abs(alex_eval(D["pd"], signs, tv)); ac = abs(alex_eval(Dc["pd"], [c["sign"] for c in Dc["crossings"]], tv))
    k = round(np.log(af / ac) / np.log(tv)); ks.add(k)
    ok &= (af == ac * tv ** k) if k >= 0 else (af * tv ** (-k) == ac)
    print(f"  t = {tv}: |Alexander(chain)| = {af}, |Alexander(axis)| = {ac}, ratio t^{k}")
det = abs(alex_eval(D["pd"], signs, -1))
print("Alexander polynomials agree up to a unit:", ok and len(ks) == 1, " determinant of the chain diagram:", det)

print("\n== checks")
assert is52 and len(onc) == 0 and ok and len(ks) == 1 and det == 7 and reach - 4.6 > 0
print("The closed backbone is the knot 5_2; its crossing number is 5. KEY = 5")
print("Expected wrong answers: 3 (trefoil assumed), 0 (unknot), the number of crossings drawn (%d)." % D["n"])
