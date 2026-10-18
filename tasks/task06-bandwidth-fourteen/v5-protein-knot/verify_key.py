"""Independent check of the key for the protein knot question.

The backbone in the figure is a smooth closed curve built as follows. Take the closure of the
3-strand braid  s1^3 s2^-1 s1^-3 s2^-1  (this closure is the knot 8_20, see KnotInfo, braid
notation {1,1,1,-2,-1,-1,-1,-2}), wrap it around the z axis so that braid position becomes radius and
braid time becomes angle, perturb it with a smooth low-frequency wobble, rotate it by fixed
Euler angles and project to the plane. The figure is the orthographic projection of that curve.

This script rebuilds the curve, extracts the planar diagram (crossings, over/under, signs), and
computes from that diagram alone:
  * the Alexander polynomial (Fox calculus on the Wirtinger presentation),
  * the determinant and the number of Fox 3-colourings,
  * the Jones polynomial (Kauffman bracket state sum over all 2^n smoothings).
It then compares them with the same invariants computed from (a) the plain 8-crossing closed braid
and (b) the granny knot 3_1 # 3_1 and the square knot 3_1 # 3_1*, which share the Alexander
polynomial with 8_20. Finally it checks the diagram quality numbers of the figure.

Everything runs with numpy, scipy and sympy only. Runtime about one minute.
"""
import itertools, numpy as np, sympy as sp
from scipy.interpolate import CubicSpline

WORD = [1, 1, 1, -2, -1, -1, -1, -2]           # 8_20 as a closed 3-braid
SEED, AMP, NPT = 1, 0.6, 1800
ANG = (-0.6822596345164404, -0.565022475469942, -2.6596385992300595)
EXPECTED_JONES_8_20 = {-5: -1, -4: 1, -3: -1, -2: 2, -1: -1, 0: 2, 1: -1}   # KnotInfo, one chirality

# ---------------------------------------------------------------- curve
def braid_strand_paths(word, nstr=3, h=0.45, step=1.0):
    pos = list(range(nstr)); paths = {s: [np.array([float(s), 0.0, 0.0])] for s in range(nstr)}; y = 0.0
    for g in word:
        i = abs(g) - 1
        a = [s for s in range(nstr) if pos[s] == i][0]; b = [s for s in range(nstr) if pos[s] == i + 1][0]
        for t in np.linspace(0, 1, 13)[1:]:
            s_ = 0.5 - 0.5 * np.cos(np.pi * t); bump = np.sin(np.pi * t)
            za = h * bump * (1 if g > 0 else -1)
            paths[a].append(np.array([i + s_, y + t * step, za])); paths[b].append(np.array([i + 1 - s_, y + t * step, -za]))
        for s in range(nstr):
            if s not in (a, b): paths[s].append(np.array([float(pos[s]), y + step, 0.0]))
        pos[a], pos[b] = i + 1, i; y += step
    return paths, pos, y

def smooth(pts, n):
    pts = np.asarray(pts, float)
    keep = [0] + [i for i in range(1, len(pts)) if np.linalg.norm(pts[i] - pts[i - 1]) > 1e-9]
    pts = pts[keep]
    if np.linalg.norm(pts[0] - pts[-1]) > 1e-9: pts = np.vstack([pts, pts[:1]])
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    cs = CubicSpline(d, pts, bc_type="periodic")
    return cs(np.linspace(0, d[-1], n, endpoint=False))

def planar_closure(word, nstr, n):
    """closed braid with closure arcs in the plane z=0 (used for the reference diagrams)."""
    paths, pos, Y = braid_strand_paths(word, nstr)
    curve = []; s = 0
    for _ in range(nstr):
        k = pos[s]; d = 0.9 * (nstr - k); xk = nstr + 0.9 * (nstr - k)
        curve += paths[s] + [np.array([k, Y + d, 0.0]), np.array([xk, Y + d, 0.0]), np.array([xk, -d, 0.0]), np.array([k, -d, 0.0])]
        s = pos[s]
    assert s == 0
    return smooth(np.array(curve), n)

def figure_curve(word, seed, amp, n, R0=3.0, dr=0.8, harm=(2, 3, 4, 5, 6, 7)):
    paths, pos, Y = braid_strand_paths(word, 3)
    curve = []; s = 0; yoff = 0.0; pad = 1.0
    for _ in range(3):
        P = np.array(paths[s]) + np.array([0, yoff, 0]); curve.append(P); yoff += Y + pad
        curve.append(np.array([[pos[s], yoff - pad * 0.5, 0.0]])); s = pos[s]
    assert s == 0
    C = np.vstack(curve)
    theta = 2 * np.pi * C[:, 1] / (Y + pad); rho = R0 + dr * C[:, 0]
    sm = smooth(np.c_[rho * np.cos(theta), rho * np.sin(theta), C[:, 2]], n)
    rng = np.random.default_rng(seed)
    u = np.linspace(0, 2 * np.pi, n, endpoint=False)
    for m in harm:
        sm[:, 2] += amp * rng.normal() / np.sqrt(m) * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    rad = np.zeros(n)
    for m in harm:
        rad += 0.35 * amp * rng.normal() / np.sqrt(m) * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    r = np.linalg.norm(sm[:, :2], axis=1); f = (r + rad) / r
    sm[:, 0] *= f; sm[:, 1] *= f
    return sm

def rotmat(ax, ay, az):
    cx, sx = np.cos(ax), np.sin(ax); cy, sy = np.cos(ay), np.sin(ay); cz, sz = np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

# ---------------------------------------------------------------- diagram
def diagram(pts3):
    P = pts3[:, :2]; Z = pts3[:, 2]; N = len(P)
    A = P; B = np.roll(P, -1, axis=0)
    inter = []
    for i in range(N):
        p = A[i]; r = B[i] - A[i]
        js = np.arange(i + 2, N) if i > 0 else np.arange(2, N - 1)
        q = A[js]; s = B[js] - A[js]
        rxs = r[0] * s[:, 1] - r[1] * s[:, 0]; qp = q - p
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (qp[:, 0] * s[:, 1] - qp[:, 1] * s[:, 0]) / rxs; u = (qp[:, 0] * r[1] - qp[:, 1] * r[0]) / rxs
        ok = (np.abs(rxs) > 1e-12) & (t > 0) & (t < 1) & (u > 0) & (u < 1)
        for j, tt, uu in zip(js[ok], t[ok], u[ok]): inter.append((i, int(j), float(tt), float(uu)))
    events = []; cross = []
    for cid, (i, j, ti, tj) in enumerate(inter):
        zi = Z[i] + ti * (Z[(i + 1) % N] - Z[i]); zj = Z[j] + tj * (Z[(j + 1) % N] - Z[j])
        di = P[(i + 1) % N] - P[i]; dj = P[(j + 1) % N] - P[j]
        over_i = zi > zj
        o = di if over_i else dj; u = dj if over_i else di
        sign = 1 if (o[0] * u[1] - o[1] * u[0]) > 0 else -1
        ang = abs(np.degrees(np.arctan2(di[0] * dj[1] - di[1] * dj[0], di @ dj)))
        cross.append(dict(id=cid, pt=P[i] + ti * di, over_i=over_i, sign=sign, dz=abs(zi - zj), angle=min(ang, 180 - ang), di=di, dj=dj))
        events.append((i + ti, cid, over_i)); events.append((j + tj, cid, not over_i))
    events.sort(); n = len(cross)
    edge = {}
    for k, (par, cid, is_over) in enumerate(events): edge[(cid, is_over)] = (k, (k + 1) % (2 * n))
    pd = []
    for c in cross:
        a, cc = edge[(c["id"], False)]; bi, bo = edge[(c["id"], True)]
        o = c["di"] if c["over_i"] else c["dj"]; u = c["dj"] if c["over_i"] else c["di"]
        ang = lambda v: np.arctan2(v[1], v[0])
        items = [(ang(-u), a), (ang(u), cc), (ang(-o), bi), (ang(o), bo)]; base = ang(-u)
        items.sort(key=lambda t: (t[0] - base) % (2 * np.pi))
        pd.append(tuple(int(e) for _, e in items))
    pts = np.array([c["pt"] for c in cross])
    mind = min((np.linalg.norm(pts[a] - pts[b]) for a in range(n) for b in range(a + 1, n)), default=np.inf)
    return dict(pd=pd, signs=[c["sign"] for c in cross], writhe=sum(c["sign"] for c in cross), n=n, cross=cross,
                mindist=mind, minangle=min(c["angle"] for c in cross), mindz=min(c["dz"] for c in cross))

# ---------------------------------------------------------------- invariants
Asym, tsym = sp.symbols("A t")

def arcs_of(pd):
    E = 2 * len(pd); starts = sorted(x[2] for x in pd); arc = {}
    for k, s in enumerate(starts):
        e = s
        while True:
            arc[e] = k; e = (e + 1) % E
            if e in starts: break
    return arc

def alexander(pd, signs):
    arc = arcs_of(pd); n = len(pd); M = sp.zeros(n, n)
    for r, ((a, b, c, d), sg) in enumerate(zip(pd, signs)):
        if sg > 0: M[r, arc[b]] += 1 - tsym; M[r, arc[a]] += tsym; M[r, arc[c]] += -1
        else:      M[r, arc[b]] += 1 - tsym; M[r, arc[a]] += -1; M[r, arc[c]] += tsym
    p = sp.Poly(sp.expand(M[1:, 1:].det()), tsym)
    co = p.all_coeffs()
    while co and co[-1] == 0: co.pop()
    if co[-1] < 0: co = [-c for c in co]
    return sp.Poly(co, tsym)

def coloring_matrix(pd):
    arc = arcs_of(pd); n = len(pd); M = [[0] * n for _ in range(n)]
    for r, (a, b, c, d) in enumerate(pd):
        M[r][arc[b]] += 2; M[r][arc[a]] -= 1; M[r][arc[c]] -= 1
    return M

def determinant(pd):
    M = sp.Matrix(coloring_matrix(pd)); return abs(int(M[1:, 1:].det()))

def colorings(pd, p):
    rows = [[v % p for v in r] for r in coloring_matrix(pd)]; rk = 0; cols = len(rows)
    for c in range(cols):
        piv = next((r for r in range(rk, len(rows)) if rows[r][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][c], -1, p)
        rows[rk] = [(v * inv) % p for v in rows[rk]]
        for r in range(len(rows)):
            if r != rk and rows[r][c]:
                f = rows[r][c]; rows[r] = [(x - f * y) % p for x, y in zip(rows[r], rows[rk])]
        rk += 1
    return p ** (cols - rk)

def jones(pd, writhe):
    n = len(pd); edges = sorted({e for x in pd for e in x}); total = 0
    for state in itertools.product((0, 1), repeat=n):
        parent = {e: e for e in edges}
        def find(e):
            while parent[e] != e: parent[e] = parent[parent[e]]; e = parent[e]
            return e
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry: parent[rx] = ry
        na = 0
        for (a, b, c, d), s in zip(pd, state):
            if s == 0: union(a, b); union(c, d); na += 1
            else: union(a, d); union(b, c)
        loops = len({find(e) for e in edges})
        total += Asym ** (na - (n - na)) * (-Asym ** 2 - Asym ** -2) ** (loops - 1)
    f = sp.expand((-Asym ** 3) ** (-writhe) * sp.expand(total))
    poly = sp.Poly(sp.expand(f * Asym ** 400), Asym); out = {}
    for (k,), c in poly.terms():
        e = k - 400; assert e % 4 == 0
        out[-e // 4] = int(c)
    return dict(sorted(out.items()))

def jstr(j): return " ".join(f"{'+' if v > 0 else '-'}{abs(v)}t^{k}" for k, v in sorted(j.items()))

def mirror(j): return dict(sorted({-k: v for k, v in j.items()}.items()))

# ---------------------------------------------------------------- run
if __name__ == "__main__":
    print("== figure diagram")
    Q = figure_curve(WORD, SEED, AMP, NPT) @ rotmat(*ANG).T
    D = diagram(Q)
    span = np.ptp(Q[:, :2], axis=0).max()
    print(f"crossings in the figure: {D['n']}, writhe {D['writhe']}")
    print(f"smallest distance between two crossings: {D['mindist'] / span:.3f} of the figure width;"
          f" smallest crossing angle {D['minangle']:.1f} degrees; smallest depth separation {D['mindz'] / span:.3f} of width")
    for c in D["cross"]:
        print(f"  crossing {c['id'] + 1:2d} at ({c['pt'][0]:+.3f},{c['pt'][1]:+.3f}) sign {c['sign']:+d}")
    alex = alexander(D["pd"], D["signs"]); det = determinant(D["pd"]); col3 = colorings(D["pd"], 3); J = jones(D["pd"], D["writhe"])
    print("Alexander polynomial:", alex.as_expr())
    print("determinant:", det, " Fox 3-colourings:", col3)
    print("Jones polynomial:", jstr(J))

    print("\n== reference diagrams (planar closed braids)")
    refs = {"8_20 as closed braid": ([1, 1, 1, -2, -1, -1, -1, -2], 3),
            "granny 3_1 # 3_1": ([1, 1, 1, 2, 2, 2], 3),
            "square 3_1 # 3_1*": ([1, 1, 1, -2, -2, -2], 3),
            "trefoil 3_1": ([1, 1, 1], 2)}
    table = {}
    for name, (w, ns) in refs.items():
        Dr = diagram(planar_closure(w, ns, 1200))
        table[name] = (alexander(Dr["pd"], Dr["signs"]).as_expr(), determinant(Dr["pd"]), colorings(Dr["pd"], 3), jones(Dr["pd"], Dr["writhe"]))
        print(f"{name}: {Dr['n']} crossings, Alexander {table[name][0]}, det {table[name][1]}, 3-colourings {table[name][2]}, Jones {jstr(table[name][3])}")

    print("\n== checks")
    same_alex = alex.as_expr() == table["8_20 as closed braid"][0] == table["granny 3_1 # 3_1"][0] == table["square 3_1 # 3_1*"][0]
    print("Alexander polynomial of the figure equals that of 8_20, granny and square:", same_alex)
    print("Jones of the figure equals Jones of the closed braid 8_20:", J == table["8_20 as closed braid"][3])
    print("Jones of the figure equals KnotInfo 8_20 (either chirality):", J in (EXPECTED_JONES_8_20, mirror(EXPECTED_JONES_8_20)))
    print("Jones differs from granny and square:", J not in (table["granny 3_1 # 3_1"][3], mirror(table["granny 3_1 # 3_1"][3]), table["square 3_1 # 3_1*"][3]))
    print("3-colourings: figure", col3, " granny", table["granny 3_1 # 3_1"][2], " square", table["square 3_1 # 3_1*"][2])
    assert same_alex and J in (EXPECTED_JONES_8_20, mirror(EXPECTED_JONES_8_20)) and col3 == 9 and det == 9
    print("\nThe closed backbone is the knot 8_20. Its crossing number is 8 (KnotInfo; 8_20 is a prime, non-alternating")
    print("knot, the diagram in the figure has 12 crossings and is not minimal). KEY = 8")
