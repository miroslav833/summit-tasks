"""Knot tools for the protein-knot task.

build_braid_curve(word)  closed 3D polyline for the closure of a 3-strand braid word
                         (generators 1,2 with sign), closure arcs in the plane z=0.
smooth(pts, n)           periodic cubic spline resample.
diagram(pts3, R)         rotate by R, project on x,y, find crossings, return a PD code,
                         writhe, and the crossing list.
jones(pd, writhe)        Jones polynomial by the Kauffman bracket state sum (dict power->coef, in t).
alexander(pd)            Alexander polynomial via Fox calculus (sympy Poly, normalised).
colorings(pd, p)         number of Fox p-colourings.
determinant(pd)          knot determinant.
"""
import numpy as np, itertools, sympy as sp
from scipy.interpolate import CubicSpline

def build_braid_curve(word, nstr=3, h=0.35, step=1.0):
    """word: list of nonzero ints, +i = sigma_i (strand i goes over strand i+1, left to right
    as seen from +z)... sign only fixes which strand is on top. Returns closed polyline (N,3)."""
    pos = list(range(nstr))            # pos[s] = x position of strand s (strand identity by start x)
    paths = {s: [np.array([float(s), 0.0, 0.0])] for s in range(nstr)}
    y = 0.0
    for g in word:
        i = abs(g) - 1
        a = [s for s in range(nstr) if pos[s] == i][0]
        b = [s for s in range(nstr) if pos[s] == i + 1][0]
        ts = np.linspace(0, 1, 9)[1:]
        for t in ts:
            yy = y + t * step
            s_ = 0.5 - 0.5 * np.cos(np.pi * t)         # smooth 0..1
            bump = np.sin(np.pi * t)
            za = h * bump * (1 if g > 0 else -1)
            zb = -za
            paths[a].append(np.array([i + s_, yy, za]))
            paths[b].append(np.array([i + 1 - s_, yy, zb]))
        for s in range(nstr):
            if s not in (a, b):
                paths[s].append(np.array([float(pos[s]), y + step, 0.0]))
        pos[a], pos[b] = i + 1, i
        y += step
    Y = y
    # closure: strand ending at position k returns on the right at x = nstr + 0.8*(k+1)... nested
    # strand at position k turns at height Y + 0.8*(nstr-k) and returns to its own start x=s at bottom.
    # For a planar closure we need end position k to connect to start x = k; the permutation of a
    # knot braid is a full cycle, the strands just continue. Build loops: from (k, Y) up to (k, Y+d_k),
    # right to x_k, down to -d_k, left to (k, -d_k), up to (k, 0). d_k = 0.8*(nstr-k), x_k = nstr+0.8*(nstr-k)... 
    # outermost loop belongs to the smallest k, so d and x grow as k decreases.
    segs = {}
    for s in range(nstr):
        k = pos[s]                 # end position
        d = 0.9 * (nstr - k); xk = nstr + 0.9 * (nstr - k)
        # the loop lands at bottom position k as well (we re-enter at x=k); so it continues to the
        # strand that starts at k.
        loop = [np.array([k, Y + d, 0.0]), np.array([xk, Y + d, 0.0]), np.array([xk, -d, 0.0]), np.array([k, -d, 0.0])]
        segs[s] = loop
    # assemble closed curve: start strand 0, follow to end pos k, loop, continue with strand starting at k
    curve = []; s = 0
    for _ in range(nstr):
        curve += paths[s]
        curve += segs[s]
        s = pos[s]
    assert s == 0, "braid closure is not a knot (more than one component)"
    return np.array(curve)

def smooth(pts, n=1500, tension=None):
    pts = np.asarray(pts, float)
    # remove consecutive duplicates
    keep = [0] + [i for i in range(1, len(pts)) if np.linalg.norm(pts[i] - pts[i - 1]) > 1e-9]
    pts = pts[keep]
    if np.linalg.norm(pts[0] - pts[-1]) > 1e-9:
        pts = np.vstack([pts, pts[:1]])
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    cs = CubicSpline(d, pts, bc_type="periodic")
    u = np.linspace(0, d[-1], n, endpoint=False)
    return cs(u)

def rotmat(ax, ay, az):
    cx, sx = np.cos(ax), np.sin(ax); cy, sy = np.cos(ay), np.sin(ay); cz, sz = np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def seg_intersections(P):
    """P: (N,2) closed polyline. Returns list of (i, j, ti, tj) with segments i<j intersecting
    properly (not adjacent)."""
    N = len(P)
    A = P; B = np.roll(P, -1, axis=0)
    out = []
    for i in range(N):
        p = A[i]; r = B[i] - A[i]
        js = np.arange(i + 2, N) if i > 0 else np.arange(2, N - 1)
        q = A[js]; s = B[js] - A[js]
        rxs = r[0] * s[:, 1] - r[1] * s[:, 0]
        qp = q - p
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (qp[:, 0] * s[:, 1] - qp[:, 1] * s[:, 0]) / rxs
            u = (qp[:, 0] * r[1] - qp[:, 1] * r[0]) / rxs
        ok = (np.abs(rxs) > 1e-12) & (t > 0) & (t < 1) & (u > 0) & (u < 1)
        for j, tt, uu in zip(js[ok], t[ok], u[ok]):
            out.append((i, int(j), float(tt), float(uu)))
    return out

def diagram(pts3):
    """pts3: closed 3D polyline, already rotated; projection is (x,y), depth z (larger = nearer).
    Returns dict with pd (list of 4-tuples), writhe, crossings (list), arcs count, quality stats."""
    P = pts3[:, :2]; Z = pts3[:, 2]
    N = len(P)
    inter = seg_intersections(P)
    # events along the curve: parameter position = segment index + t
    events = []   # (param, crossing id, is_over)
    cross = []
    for cid, (i, j, ti, tj) in enumerate(inter):
        zi = Z[i] + ti * (Z[(i + 1) % N] - Z[i]); zj = Z[j] + tj * (Z[(j + 1) % N] - Z[j])
        di = P[(i + 1) % N] - P[i]; dj = P[(j + 1) % N] - P[j]
        pt = P[i] + ti * di
        over_is_i = zi > zj
        # sign: with over direction o and under direction u, positive if (u x o) ... standard:
        # crossing is positive when rotating the over strand ccw by <180 aligns with under? Use the
        # right-hand rule: sign = sign( (over_dir x under_dir)_z ) ... for a positive crossing, the
        # under strand goes from right to left when looking along the over strand => cross(over, under) > 0.
        o = di if over_is_i else dj; u = dj if over_is_i else di
        sign = 1 if (o[0] * u[1] - o[1] * u[0]) > 0 else -1
        ang = abs(np.degrees(np.arctan2(di[0] * dj[1] - di[1] * dj[0], di @ dj)))
        cross.append(dict(id=cid, pt=pt, pi=i + ti, pj=j + tj, over_i=over_is_i, sign=sign,
                          dz=abs(zi - zj), angle=min(ang, 180 - ang)))
        events.append((i + ti, cid, over_is_i)); events.append((j + tj, cid, not over_is_i))
    events.sort()
    # arcs: edge labels. Walk along the curve; an edge label increments at every crossing passage
    # (PD edges), 2n edges for n crossings.
    n = len(cross)
    edge_of_event = {}
    for k, (par, cid, is_over) in enumerate(events):
        edge_of_event[(cid, is_over)] = (k, (k + 1) % (2 * n))   # incoming edge k, outgoing k+1
    # PD code: X[a,b,c,d], a incoming under edge, then counterclockwise.
    pd = []
    for c in cross:
        cid = c["id"]
        a, cc = edge_of_event[(cid, False)]
        bin_, bout = edge_of_event[(cid, True)]
        # geometry: under direction u, over direction o. ccw from incoming-under direction (-u)...
        # Edges around the crossing: incoming under at direction -u (pointing away from crossing),
        # outgoing under at +u, incoming over at -o, outgoing over at +o.
        i, j = int(c["pi"]) % N, int(c["pj"]) % N
        di = P[(i + 1) % N] - P[i]; dj = P[(j + 1) % N] - P[j]
        o = di if c["over_i"] else dj; u = dj if c["over_i"] else di
        def ang(v): return np.arctan2(v[1], v[0])
        items = [(ang(-u), a), (ang(u), cc), (ang(-o), bin_), (ang(o), bout)]
        base = ang(-u)
        items.sort(key=lambda t: (t[0] - base) % (2 * np.pi))
        pd.append(tuple(int(e) for _, e in items))
    writhe = sum(c["sign"] for c in cross)
    # quality: min distance between crossing points, min angle, min dz
    pts = np.array([c["pt"] for c in cross]) if cross else np.zeros((0, 2))
    mind = min((np.linalg.norm(pts[a] - pts[b]) for a in range(n) for b in range(a + 1, n)), default=np.inf)
    return dict(pd=pd, writhe=writhe, crossings=cross, n=n, mindist=mind,
                minangle=min((c["angle"] for c in cross), default=90), mindz=min((c["dz"] for c in cross), default=np.inf))

# ---------- invariants from a PD code ----------
A = sp.symbols("A")

def kauffman_bracket(pd):
    """State sum over 2^n smoothings. Returns sympy expression in A."""
    n = len(pd)
    edges = sorted({e for x in pd for e in x})
    total = 0
    for state in itertools.product((0, 1), repeat=n):
        parent = {e: e for e in edges}
        def find(e):
            while parent[e] != e:
                parent[e] = parent[parent[e]]; e = parent[e]
            return e
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry: parent[rx] = ry
        na = 0
        for (a, b, c, d), s in zip(pd, state):
            if s == 0: union(a, b); union(c, d); na += 1     # A-smoothing
            else: union(a, d); union(b, c)                     # B-smoothing
        loops = len({find(e) for e in edges})
        total += A ** (na - (n - na)) * (-A ** 2 - A ** -2) ** (loops - 1)
    return sp.expand(total)

def jones(pd, writhe):
    t = sp.symbols("t")
    f = sp.expand((-A ** 3) ** (-writhe) * kauffman_bracket(pd))
    # substitute A = t^(-1/4)
    poly = sp.Poly(sp.expand(f * A ** 200), A)   # shift to make exponents nonnegative
    out = {}
    for (k,), c in poly.terms():
        e = k - 200
        assert e % 4 == 0, "odd exponent, not a knot?"
        out[sp.Rational(-e, 4)] = int(c)
    return {int(k): v for k, v in sorted(out.items())}

def jones_str(j):
    return " ".join(f"{'+' if v > 0 else '-'}{abs(v)}t^{k}" for k, v in sorted(j.items()))

def crossing_sign_from_pd(x, n2=None):
    """Sign of a crossing X[a,b,c,d] (a incoming under edge, then counterclockwise), edges 0..2n-1 cyclic.
    The over strand runs d -> b when b == d + 1 (mod 2n), which with the under strand running a -> c gives
    cross(over, under) > 0: a positive (right-handed) crossing. Otherwise the over strand runs b -> d: negative."""
    a, b, c, d = x
    if n2 is None: n2 = 2 * _N2_HINT[0] if _N2_HINT[0] else None
    if n2 is None: raise ValueError("pass n2 = number of edges")
    return 1 if (d + 1) % n2 == b else -1
_N2_HINT = [0]

def signs_from_pd(pd):
    n2 = 2 * len(pd); return [crossing_sign_from_pd(x, n2) for x in pd]

def alexander(pd, signs):
    """pd as above; signs: list of +1/-1 per crossing. Over arc = the over strand's edges; arcs are
    maximal runs of edges between undercrossings. Fox calculus rows."""
    t = sp.symbols("t")
    n = len(pd); E = 2 * n
    # arc id for each edge: arcs break at under-crossings; incoming under edge a ends an arc, outgoing c starts one.
    starts = sorted(x[2] for x in pd)      # edges that begin arcs
    arc_of = {}
    for s_idx, s in enumerate(starts):
        e = s
        while True:
            arc_of[e] = s_idx
            e = (e + 1) % E
            if e in starts: break
    M = sp.zeros(n, n)
    for r, ((a, b, c, d), sg) in enumerate(zip(pd, signs)):
        over = arc_of[b]; ain = arc_of[a]; aout = arc_of[c]
        if sg > 0:
            M[r, over] += 1 - t; M[r, ain] += t; M[r, aout] += -1
        else:
            M[r, over] += 1 - t; M[r, ain] += -1; M[r, aout] += t
    minor = M[1:, 1:].det()
    p = sp.Poly(sp.expand(minor), t)
    if p.is_zero: return p
    # normalise: divide by t^k, make constant term positive
    coeffs = p.all_coeffs()
    while coeffs and coeffs[-1] == 0: coeffs.pop()
    if coeffs[-1] < 0: coeffs = [-c for c in coeffs]
    return sp.Poly(coeffs, t)

def coloring_matrix(pd):
    n = len(pd); E = 2 * n
    starts = sorted(x[2] for x in pd)
    arc_of = {}
    for s_idx, s in enumerate(starts):
        e = s
        while True:
            arc_of[e] = s_idx; e = (e + 1) % E
            if e in starts: break
    M = sp.zeros(n, n)
    for r, (a, b, c, d) in enumerate(pd):
        M[r, arc_of[b]] += 2; M[r, arc_of[a]] -= 1; M[r, arc_of[c]] -= 1
    return M

def determinant(pd):
    M = coloring_matrix(pd)
    return abs(int(M[1:, 1:].det()))

def colorings(pd, p):
    M = coloring_matrix(pd)
    rank = sp.Matrix(M).applyfunc(lambda v: v % p)
    # rank over GF(p) by elimination
    rows = [[int(v) % p for v in M.row(i)] for i in range(M.rows)]
    rk = 0; cols = M.cols
    for c in range(cols):
        piv = next((r for r in range(rk, len(rows)) if rows[r][c] % p), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], -1, p)
        rows[rk] = [(v * inv) % p for v in rows[rk]]
        for r in range(len(rows)):
            if r != rk and rows[r][c]:
                f = rows[r][c]; rows[r] = [(x - f * y) % p for x, y in zip(rows[r], rows[rk])]
        rk += 1
    return p ** (cols - rk)
