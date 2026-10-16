"""Verification of the answer key: position r of the black vertex of valency 2 for the chiral
plane tree in the figure (passport 4,2,1,1,1 | 2,2,2,2,1), normalised with the black vertex of
valency 4 at 0 and the white vertex of valency 1 at 1.  Key: r = 0.1399 + 2.699 i.

Self-contained: python3 with sympy, mpmath and numpy.  Run: python3 verify_key.py
  (1) the derivation: P' = 9c x^3 (x-r) Q with P - 1 = c (x-1) Q^2 gives Q + 2(x-1)Q' = 9x^3(x-r),
      so Q lies in a one-parameter family; P(r) = 0 then gives (r+3)(25r^3-30r^2+189r-168) = 0;
  (2) for each of the four roots the dessin P^{-1}([0,1]) is traced numerically and its two edge
      permutations are compared with the permutations read off the coordinates of image.png;
      exactly one root, r = 0.1399 + 2.699 i, gives the figure's tree; the conjugate root gives
      its mirror image, the real roots give the two mirror-symmetric trees of the passport;
  (3) all plane trees with the passport are enumerated: four, two chiral (a mirror pair) and two
      mirror-symmetric, and the figure's tree is one of the chiral pair.
"""
import math, itertools
import numpy as np
import sympy as sp
import mpmath as mp

# ---------- (1) the derivation ----------
x, r, t, c = sp.symbols("x r t c")
q3, q2, q1, q0 = sp.symbols("q3 q2 q1 q0")
Q = x**4 + q3*x**3 + q2*x**2 + q1*x + q0
ident = sp.Poly(sp.expand(Q + 2*(x - 1)*sp.diff(Q, x) - 9*x**3*(x - r)), x)
sol = sp.solve(ident.all_coeffs(), [q2, q1, q0, r], dict=True)[0]
print("Q + 2(x-1)Q' = 9x^3(x-r) forces:", {k: sp.simplify(v.subs(q3, t)) for k, v in sol.items()}, "with t = q3")
Qt = Q.subs(sol).subs(q3, t); rt = sol[r].subs(q3, t)
P = c*(x - 1)*Qt**2 + 1
csol = sp.solve(P.subs(x, 0), c)[0]
print("P(0) = 0 gives c =", csol)
cond = sp.factor(sp.numer(sp.together(P.subs(c, csol).subs(x, rt))))
print("P(r) = 0 factors as", cond)
condr = sp.factor(sp.numer(sp.together(cond.subs(t, (8 - 9*r)/7))))
print("in terms of r:", condr)
assert sp.Poly(25*r**3 - 30*r**2 + 189*r - 168, r).as_expr() in [f for f, _ in sp.factor_list(condr)[1]]
mp.mp.dps = 40
roots = [mp.mpc(v) for v in sp.Poly(25*r**3 - 30*r**2 + 189*r - 168, r).nroots(n=40)] + [mp.mpc(-3)]
print("the four roots r:", [mp.nstr(v, 10) for v in roots])

# ---------- helpers ----------
def canon_from(sb, sw, start):
    label = {start: 0}; order = [start]; seq = []; i = 0
    while i < len(order):
        e = order[i]; i += 1
        for perm in (sb, sw):
            f = perm[e]
            if f not in label: label[f] = len(order); order.append(f)
            seq.append(label[f])
    return tuple(seq)
canon = lambda sb, sw: min(canon_from(sb, sw, s) for s in range(len(sb)))
def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen: continue
        k, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; k += 1
        out.append(k)
    return sorted(out, reverse=True)
inv = lambda p: [p.index(i) for i in range(len(p))]

# the figure: coordinates used to draw image.png (counterclockwise order at the centre:
# white leaf, long chain, short arm, short arm)
V = {"c": ("b", 0.00, 0.00), "w0": ("w", 1.00, 0.05),
     "w2": ("w", 0.10, 1.00), "b2": ("b", -0.15, 2.00), "w4": ("w", 0.05, 3.00), "b3": ("b", -0.10, 4.00),
     "w1": ("w", -1.00, -0.30), "b1": ("b", -2.00, -0.55), "w3": ("w", 0.35, -0.95), "b4": ("b", 0.60, -1.95)}
E = [("c", "w0"), ("c", "w2"), ("w2", "b2"), ("b2", "w4"), ("w4", "b3"), ("c", "w1"), ("w1", "b1"), ("c", "w3"), ("w3", "b4")]
sb_F = [0]*9; sw_F = [0]*9
for v, (col, x0, y0) in V.items():
    inc = [i for i, e in enumerate(E) if v in e]
    def ang(i):
        o = E[i][0] if E[i][1] == v else E[i][1]
        return math.atan2(V[o][2] - y0, V[o][1] - x0) % (2*math.pi)
    inc.sort(key=ang)
    tgt = sb_F if col == "b" else sw_F
    for k, i in enumerate(inc): tgt[i] = inc[(k+1) % len(inc)]
FIG = canon(sb_F, sw_F); MIRROR = canon(inv(sb_F), inv(sw_F))
print("figure: sigma_black =", sb_F, "sigma_white =", sw_F, "; chiral:", FIG != MIRROR)
assert FIG != MIRROR

# ---------- (2) trace the dessin for each root ----------
def dessin(rv):
    rv = complex(rv); tv = (8 - 9*rv)/7
    Qc = np.array([1, tv, 6*tv/5, 8*tv/5, 16*tv/5], dtype=complex)
    cv = 25/(256*tv**2)
    Pc = cv*np.polymul(np.array([1, -1]), np.polymul(Qc, Qc)); Pc[-1] += 1
    Pf = lambda z: np.polyval(Pc, z); dP = np.polyder(Pc); dPf = lambda z: np.polyval(dP, z)
    blacks = np.roots(Pc); whites = np.roots(Pc - np.array([0]*9 + [1]))
    # cluster multiple roots
    def cluster(rs):
        out = []
        for z in rs:
            for o in out:
                if abs(o[0] - z) < 1e-3: o[1] += 1; o[0] = (o[0]*(o[1]-1) + z)/o[1]; break
            else: out.append([z, 1])
        return sorted(out, key=lambda o: -o[1])
    B = cluster(blacks); W = cluster(whites)
    a = np.array([o[0] for o in B]); alpha = [o[1] for o in B]; b = np.array([o[0] for o in W]); beta = [o[1] for o in W]
    pts = np.concatenate([a, b]); scale = min(abs(u - v) for u, v in itertools.combinations(pts, 2))
    edges = []
    for j, w in enumerate(b):
        m = beta[j]; kappa = np.polyval(np.polyder(Pc, m), w)/math.factorial(m)
        base = (np.pi - np.angle(kappa))/m
        for k in range(m):
            th = base + 2*np.pi*k/m
            z = w + min(0.05*scale, (0.01/abs(kappa))**(1.0/m))*np.exp(1j*th); tt = Pf(z).real; dt = 0.01
            while tt > 1e-5:
                tn = max(tt - dt, 0.0); zn = z
                for _ in range(60): zn = zn - (Pf(zn) - tn)/dPf(zn)
                if abs(Pf(zn) - tn) > 1e-9 or abs(zn - z) > 0.15*scale:
                    dt /= 2; continue
                z, tt = zn, tn; dt = min(dt*1.5, 0.01)
            i = int(np.argmin(np.abs(a - z))); edges.append((j, th, i, np.angle(z - a[i])))
    sb = [0]*9; sw = [0]*9
    for j in range(len(b)):
        es = sorted([e for e in range(9) if edges[e][0] == j], key=lambda e: edges[e][1] % (2*np.pi))
        for k, e in enumerate(es): sw[e] = es[(k+1) % len(es)]
    for i in range(len(a)):
        es = sorted([e for e in range(9) if edges[e][2] == i], key=lambda e: edges[e][3] % (2*np.pi))
        assert len(es) == alpha[i]
        for k, e in enumerate(es): sb[e] = es[(k+1) % len(es)]
    return sb, sw, a, alpha, b, beta, edges

hit = None
for rv in roots:
    sb, sw, a, alpha, b, beta, edges = dessin(rv)
    cf = canon(sb, sw)
    tag = "the figure" if cf == FIG else ("mirror image of the figure" if cf == MIRROR else "another tree (mirror-symmetric)" if cf == canon(inv(sb), inv(sw)) else "another tree")
    print(f"r = {mp.nstr(rv, 8)}: passport {cycles(sb)} | {cycles(sw)} -> {tag}")
    if cf == FIG:
        hit = rv
        print("   black vertices:", [f"{z:.4f}" for z in a], "white vertices:", [f"{z:.4f}" for z in b])
        for e in sorted(edges, key=lambda e: e[1]):
            print(f"   edge: white {b[e[0]]:.4f} -- black {a[e[2]]:.4f}")
assert hit is not None and mp.im(hit) > 0
print("CHECK 2: the figure's tree is the dessin for r = %s + %s i (four significant figures: %s + %s i)"
      % (mp.nstr(mp.re(hit), 10), mp.nstr(mp.im(hit), 10), mp.nstr(mp.re(hit), 4), mp.nstr(mp.im(hit), 4)))

# ---------- (3) enumeration ----------
def ordered_trees(n):
    if n == 0:
        yield (); return
    def comps(m):
        if m == 0:
            yield []; return
        for first in range(m):
            for rest in comps(m - 1 - first): yield [first] + rest
    for sizes in comps(n):
        for subs in itertools.product(*[list(ordered_trees(s)) for s in sizes]): yield tuple(subs)
def perms_from_ordered(tr):
    sb, sw, counter = {}, {}, [0]
    def visit(node, colour, parent_edge):
        child_edges = []
        for sub in node:
            e = counter[0]; counter[0] += 1; child_edges.append((e, sub))
        order = ([parent_edge] if parent_edge is not None else []) + [e for e, _ in child_edges]
        target = sb if colour == "b" else sw
        for i, e in enumerate(order): target[e] = order[(i+1) % len(order)]
        for e, sub in child_edges: visit(sub, "w" if colour == "b" else "b", e)
    visit(tr, "b", None); n = counter[0]
    return [sb[i] for i in range(n)], [sw[i] for i in range(n)]
seen = {}
for tr in ordered_trees(9):
    sb, sw = perms_from_ordered(tr)
    if cycles(sb) == [4, 2, 1, 1, 1] and cycles(sw) == [2, 2, 2, 2, 1]: seen.setdefault(canon(sb, sw), (sb, sw))
print(f"plane trees with passport (4,2,1,1,1 | 2,2,2,2,1): {len(seen)}")
for cf, (sb, sw) in seen.items():
    print("  ", "chiral" if canon(inv(sb), inv(sw)) != cf else "mirror-symmetric", "<- the figure" if cf == FIG else "<- mirror image of the figure" if cf == MIRROR else "")
assert len(seen) == 4 and FIG in seen and MIRROR in seen
print("CHECK 3: four trees, the figure and its mirror image are the chiral pair")
print("ALL CHECKS PASSED. r = 0.1399 + 2.699 i")
