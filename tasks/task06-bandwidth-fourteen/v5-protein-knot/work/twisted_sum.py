"""Alternating diagram of 5_1 # 6_3 with one extra (nugatory) crossing in the neck.
build(neck_sign, mirror2, twist=True, wobble=0, seed=0) -> closed 3D polyline (unsmoothed, z=0 except crossings)."""
import numpy as np, knotlib as K, altcheck as A

def closure_curve(word, nstr, gap, h=0.45):
    """planar closed braid with closure arcs spaced by `gap`; returns point list (closed, not repeated)."""
    pos = list(range(nstr)); paths = {s: [np.array([float(s), 0.0, 0.0])] for s in range(nstr)}; y = 0.0
    for g in word:
        i = abs(g) - 1
        a = [s for s in range(nstr) if pos[s] == i][0]; b = [s for s in range(nstr) if pos[s] == i + 1][0]
        for t in np.linspace(0, 1, 13)[1:]:
            s_ = 0.5 - 0.5 * np.cos(np.pi * t); bump = np.sin(np.pi * t); za = h * bump * (1 if g > 0 else -1)
            paths[a].append(np.array([i + s_, y + t, za])); paths[b].append(np.array([i + 1 - s_, y + t, -za]))
        for s in range(nstr):
            if s not in (a, b): paths[s].append(np.array([float(pos[s]), y + 1, 0.0]))
        pos[a], pos[b] = i + 1, i; y += 1
    Y = y; curve = []; s = 0
    for _ in range(nstr):
        k = pos[s]; d = gap * (nstr - k) * 0.5; xk = nstr - 1 + gap * (nstr - k)
        # go up from (k, Y) to (k, Y+d), right to xk, down to -d, left to (k, -d), up to (k, 0)
        seg = [np.array([k, Y + d, 0.0]), np.array([xk, Y + d, 0.0]), np.array([xk, -d, 0.0]), np.array([k, -d, 0.0])]
        curve += paths[s] + seg; s = pos[s]
    assert s == 0
    return np.array(curve)

def densify(P, step=0.08):
    out = []
    for a, b in zip(P, np.roll(P, -1, axis=0)):
        n = max(1, int(np.linalg.norm(b - a) / step))
        for t in np.linspace(0, 1, n, endpoint=False): out.append(a + t * (b - a))
    return np.array(out)

def build(neck_sign=1, mirror2=False, twist=True, h=0.45):
    A1 = densify(closure_curve([1] * 5, 2, gap=3.2))                 # 5_1, strands at x=0,1; closure arcs at x=4.2 and 7.4
    B = densify(closure_curve([1, 1, -2, 1, -2, -2], 3, gap=0.9))   # 6_3 (blocks 2,1,1,2)
    if mirror2: B[:, 2] *= -1
    # scale and place B inside the region between x=1 and x=4.2 of A1
    B = B * 0.42; B[:, 2] /= 0.42 * 1.0 / 1.0   # keep z bumps at full height
    B[:, 2] *= 1.0
    bx = (B[:, 0].min() + B[:, 0].max()) / 2; by = (B[:, 1].min() + B[:, 1].max()) / 2
    B[:, 0] += 2.55 - bx; B[:, 1] += 2.5 - by
    # cut points: inner closure arc of A1 (x = 4.2, vertical) at y0; outer arc of B (its max x) at y0
    y0 = 2.5
    def cut(P, xsel, y0):
        """indices of the two points nearest (x, y0+-0.25) on the vertical arc x=xsel"""
        up = np.argmin(np.hypot(P[:, 0] - xsel, P[:, 1] - (y0 + 0.3))); lo = np.argmin(np.hypot(P[:, 0] - xsel, P[:, 1] - (y0 - 0.3)))
        return up, lo
    a_up, a_lo = cut(A1, 4.2, y0)
    xb = B[:, 0].max(); b_up, b_lo = cut(B, xb, y0)
    def arc(P, start, end):
        """points of closed list P going forward from start to end (inclusive)"""
        n = len(P); out = []; i = start
        while True:
            out.append(P[i]);
            if i == end: break
            i = (i + 1) % n
        return out
    # the inner arc of A1 is traversed downward (closure goes right at top, then down): check direction
    # we need A traversed from one cut end all the way round to the other; choose the long way.
    def long_arc(P, i, j):
        a1 = arc(P, i, j); a2 = arc(P, j, i)
        return (a1, i, j) if len(a1) > len(a2) else (a2, j, i)
    Aarc, a_s, a_e = long_arc(A1, a_up, a_lo)   # starts at a_s, ends at a_e
    Barc, b_s, b_e = long_arc(B, b_up, b_lo)
    # neck: from A end to B start, then B end to A start. For a crossing, pair A-lower with B-upper.
    def is_upper(P, i, y0): return P[i][1] > y0
    if twist:
        if is_upper(A1, a_e, y0) == is_upper(B, b_s, y0):      # same side: reverse B traversal
            Barc = Barc[::-1]; b_s, b_e = b_e, b_s
    else:
        if is_upper(A1, a_e, y0) != is_upper(B, b_s, y0):
            Barc = Barc[::-1]; b_s, b_e = b_e, b_s
    def neck(p, q, zsign):
        pts = []
        for t in np.linspace(0, 1, 14, endpoint=False):
            r = p + t * (q - p); r = r.copy(); r[2] = zsign * h * np.sin(np.pi * t) if twist else 0.0; pts.append(r)
        return pts
    curve = Aarc + neck(A1[a_e], B[b_s], neck_sign) + Barc + neck(B[b_e], A1[a_s], -neck_sign)
    return np.array(curve)

if __name__ == "__main__":
    V51 = K.jones(*[(lambda D: (D["pd"], D["writhe"]))(K.diagram(K.smooth(K.build_braid_curve([1]*5, 2), 900)))][0])
    D63 = K.diagram(K.smooth(K.build_braid_curve([1, 1, -2, 1, -2, -2], 3), 900)); V63 = K.jones(D63["pd"], D63["writhe"])
    import sympy as sp
    t = sp.symbols("t")
    def poly(j): return sum(c * t ** k for k, c in j.items())
    prod = sp.expand(poly(V51) * poly(V63)); prodm = sp.expand(poly(V51).subs(t, 1 / t) * poly(V63))
    print("V(5_1)V(6_3) =", prod)
    for twist in (True, False):
        for ns in (1, -1):
            for m2 in (False, True):
                C = build(ns, m2, twist)
                D = K.diagram(C)
                J = K.jones(D["pd"], D["writhe"]); Jp = sp.expand(poly(J))
                print(f"twist={twist} neck={ns} mirror2={m2}: n={D['n']} alternating={A.alternating(D)} nugatory={A.nugatory(D)} det={K.determinant(D['pd'])} jones_ok={Jp in (prod, prodm)} span={max(J)-min(J)}")
