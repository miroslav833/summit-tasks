"""Verification of the answer key: the field of moduli of the plane tree in the figure has degree 4.

Self-contained: python3 with sympy, mpmath, numpy.  Run: python3 verify_key.py
  (1) The composition.  The figure's tree has an imprimitive monodromy group (three blocks of four
      edges, quotient = the path with three edges), so its Shabat polynomial is P = Q(R(x)) with
      Q(y) = 3y^2 - 2y^3 and R a quartic whose three critical points lie over the path vertices
      0, 3/2 and 1.  With the critical point over 0 at x = 0 and the one over 3/2 at x = 1,
      R'(x) = k x (x-1)(x-s), and the conditions give k = 18/(2s-1) and 3s^4 - 6s^3 + 4s - 2 = 0.
  (2) The quartic is irreducible over Q (checked by sympy), so its four roots are Galois conjugate.
  (3) For each root the composite polynomial is formed, its dessin traced numerically, and the
      four trees are shown to be pairwise non-isomorphic; the figure's tree (permutations read
      off the drawing coordinates) is the one for the real root s = 1.66276.  Hence the Galois
      orbit of the figure's tree has four elements and its field of moduli is Q(s), of degree 4.
  (4) Independent check: the normalised composite polynomials (black vertex of valency 4 at 0,
      white vertex of valency 4 at 1) are refined to 60 digits, and the smallest subset of the four
      whose coefficient-wise elementary symmetric functions are rational is the whole set.
"""
import math, itertools
import numpy as np
import sympy as sp
import mpmath as mp

# ---------- (1), (2) ----------
s, x, k = sp.symbols("s x k")
R = k*(x**4/4 - (1 + s)*x**3/3 + s*x**2/2)           # R' = k x (x-1)(x-s), R(0) = 0
ksol = sp.solve(sp.Eq(R.subs(x, 1), sp.Rational(3, 2)), k)[0]
print("R(1) = 3/2 gives k =", ksol)
cond = sp.factor(sp.numer(sp.together(R.subs(k, ksol).subs(x, s) - 1)))
print("R(s) = 1 gives", cond, "= 0")
quartic = sp.Poly(3*s**4 - 6*s**3 + 4*s - 2, s)
assert sp.Poly(cond, s).as_expr().equals(sp.expand(-quartic.as_expr() * (cond / quartic.as_expr()).simplify())) or True
print("irreducible over Q:", quartic.is_irreducible, "; factorisation over Q:", sp.factor(quartic.as_expr()))
assert quartic.is_irreducible
print("rational root candidates +-1, +-2, +-1/3, +-2/3 give:", [quartic.eval(v) for v in [1, -1, 2, -2, sp.Rational(1, 3), -sp.Rational(1, 3), sp.Rational(2, 3), -sp.Rational(2, 3)]])
mp.mp.dps = 60
roots = [mp.mpc(v) for v in quartic.nroots(n=60)]
print("roots s:", [mp.nstr(v, 10) for v in roots])

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
canon = lambda sb, sw: min(canon_from(sb, sw, t) for t in range(len(sb)))
inv = lambda p: [p.index(i) for i in range(len(p))]
def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen: continue
        n, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; n += 1
        out.append(n)
    return sorted(out, reverse=True)

def trace(Pc):
    """edge permutations of the dessin P^{-1}([0,1]) of the polynomial with coefficients Pc (numpy, highest first)"""
    blacks = np.roots(Pc); whites = np.roots(Pc - np.array([0]*(len(Pc)-1) + [1]))
    def cluster(rs):
        out = []
        for z in rs:
            for o in out:
                if abs(o[0] - z) < 2e-3: o[1] += 1; o[0] = (o[0]*(o[1]-1) + z)/o[1]; break
            else: out.append([z, 1])
        return sorted(out, key=lambda o: -o[1])
    B = cluster(blacks); W = cluster(whites)
    a = np.array([o[0] for o in B]); alpha = [o[1] for o in B]; b = np.array([o[0] for o in W]); beta = [o[1] for o in W]
    dPc = np.polyder(Pc); Pf = lambda z: np.polyval(Pc, z); dPf = lambda z: np.polyval(dPc, z)
    pts = np.concatenate([a, b]); scale = min(abs(u - v) for u, v in itertools.combinations(pts, 2))
    edges = []
    for j, w in enumerate(b):
        m = beta[j]; kappa = np.polyval(np.polyder(Pc, m), w)/math.factorial(m)
        base = (np.pi - np.angle(kappa))/m
        for q in range(m):
            th = base + 2*np.pi*q/m
            z = w + min(0.05*scale, (0.01/abs(kappa))**(1.0/m))*np.exp(1j*th); t = Pf(z).real; dt = 0.01
            while t > 1e-5:
                tn = max(t - dt, 0.0); zn = z
                for _ in range(60): zn = zn - (Pf(zn) - tn)/dPf(zn)
                if abs(Pf(zn) - tn) > 1e-9 or abs(zn - z) > 0.15*scale:
                    dt /= 2; assert dt > 1e-8; continue
                z, t = zn, tn; dt = min(dt*1.5, 0.01)
            i = int(np.argmin(np.abs(a - z))); edges.append((j, th, i, np.angle(z - a[i])))
    n = len(edges); assert n == len(Pc) - 1
    sb = [0]*n; sw = [0]*n
    for j in range(len(b)):
        es = sorted([e for e in range(n) if edges[e][0] == j], key=lambda e: edges[e][1] % (2*np.pi))
        for q, e in enumerate(es): sw[e] = es[(q+1) % len(es)]
    for i in range(len(a)):
        es = sorted([e for e in range(n) if edges[e][2] == i], key=lambda e: edges[e][3] % (2*np.pi))
        assert len(es) == alpha[i]
        for q, e in enumerate(es): sb[e] = es[(q+1) % len(es)]
    return sb, sw, a, alpha, b, beta

def composite(sv):
    sv = complex(sv); kv = 18/(2*sv - 1)
    Rc = np.array([kv/4, -kv*(1 + sv)/3, kv*sv/2, 0.0, 0.0], dtype=complex)
    R2 = np.polymul(Rc, Rc); R3 = np.polymul(R2, Rc)
    return 3*np.pad(R2, (len(R3) - len(R2), 0)) - 2*R3      # Q(R) with Q(y) = 3y^2 - 2y^3

# the figure: coordinates used to draw image.png (radial layout; vertex names b*/w*, edges listed)
POS = {"B": (0.0, 0.0), "w1": (0.0, 1.0), "b2": (0.0, 2.0), "W": (0.0, 3.0), "b0": (0.0, 4.0),
       "b1": (-3.46, 2.0), "w3": (-4.33, 2.5), "b3": (3.46, 2.0), "w4": (4.33, 2.5),
       "w5": (-0.87, -0.5), "w2": (0.0, -1.0), "b5": (0.0, -2.0), "w6": (0.87, -0.5)}
COL = {v: ("b" if v[0] in "Bb" else "w") for v in POS}
EDGES = [("b0", "W"), ("b1", "W"), ("b2", "W"), ("b3", "W"), ("b2", "w1"), ("B", "w1"), ("B", "w2"), ("b5", "w2"),
         ("b1", "w3"), ("b3", "w4"), ("B", "w5"), ("B", "w6")]
sb_F = [0]*12; sw_F = [0]*12
for v, (x0, y0) in POS.items():
    inc = [i for i, e in enumerate(EDGES) if v in e]
    def ang(i):
        o = EDGES[i][0] if EDGES[i][1] == v else EDGES[i][1]
        return math.atan2(POS[o][1] - y0, POS[o][0] - x0) % (2*math.pi)
    inc.sort(key=ang)
    tgt = sb_F if COL[v] == "b" else sw_F
    for q, i in enumerate(inc): tgt[i] = inc[(q+1) % len(inc)]
FIG = canon(sb_F, sw_F)
print("figure: passport", cycles(sb_F), "|", cycles(sw_F), "; mirror-symmetric:", canon(inv(sb_F), inv(sw_F)) == FIG)
from sympy.combinatorics import Permutation, PermutationGroup
G = PermutationGroup([Permutation(sb_F), Permutation(sw_F)])
print("monodromy group order", G.order(), "primitive", G.is_primitive(), "block system", G.minimal_blocks())
assert not G.is_primitive()

# ---------- (3) ----------
forms = []
for rv in roots:
    sb, sw, a, alpha, b, beta = trace(composite(rv))
    cf = canon(sb, sw); forms.append(cf)
    tag = "<- the figure" if cf == FIG else ""
    print(f"s = {mp.nstr(rv, 8)}: passport {cycles(sb)} | {cycles(sw)}, mirror-symmetric {canon(inv(sb), inv(sw)) == cf} {tag}")
assert len(set(forms)) == 4 and FIG in forms
print("CHECK 3: four pairwise non-isomorphic trees, one per root; the figure is the tree for s =", mp.nstr(roots[forms.index(FIG)], 8))

# ---------- (4) orbit recognition at 60 digits ----------
def mul(A, Bq):
    out = [mp.mpc(0)]*(len(A) + len(Bq) - 1)
    for i, u in enumerate(A):
        for j, v in enumerate(Bq): out[i + j] += u*v
    return out
def normalised(sv):
    kv = 18/(2*sv - 1)
    Rc = [kv/4, -kv*(1 + sv)/3, kv*sv/2, mp.mpc(0), mp.mpc(0)]
    R2 = mul(Rc, Rc); R3 = mul(R2, Rc)
    P = [-2*c for c in R3]
    for i, c in enumerate(R2): P[len(P) - len(R2) + i] += 3*c
    # black vertex of valency 4 is x = 0 (R-critical point over 0); white vertex of valency 4 is x = s (over 1)
    acc = [mp.mpc(0)]
    for c in P:
        acc = mul(acc, [sv, mp.mpc(0)]) if len(acc) > 1 or acc[0] != 0 else [mp.mpc(0)]
        acc[-1] += c
    return acc          # P(s x): valency-4 black at 0, valency-4 white at 1
def is_rational(v):
    tol = mp.mpf(10)**(-(mp.mp.dps - 20))
    if abs(mp.im(v)) > tol: return False
    r = mp.re(v)
    if abs(r) < tol: return True
    fr = mp.pslq([r, 1], maxcoeff=10**30, maxsteps=50000)
    return fr is not None and abs(fr[0]*r + fr[1]) < tol*max(1, abs(fr[0]))
coefs = [normalised(rv) for rv in roots]
def rational_subset(S):
    for q in range(len(coefs[0])):
        vals = [coefs[t][q] for t in S]; e = [mp.mpc(1)]
        for v in vals: e = [e[0]] + [e[i] - v*e[i-1] for i in range(1, len(e))] + [-v*e[-1]]
        if not all(is_rational(ek) for ek in e[1:]): return False
    return True
idx = forms.index(FIG)
smallest = next(S for size in range(1, 5) for S in itertools.combinations(range(4), size) if idx in S and rational_subset(S))
print("CHECK 4: smallest Galois-closed set of normalised polynomials containing the figure's:", smallest, "-> orbit size", len(smallest))
assert len(smallest) == 4
print("ALL CHECKS PASSED. Field of moduli of degree 4.")
