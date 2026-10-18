"""Verification of the answer key: fatigue crack growth life of the MIM Ti-6Al-7Nb edge-cracked plate loaded at R = 0.4,
with the intrinsic growth law and the (constant) crack-opening level read from the figure.

Self-contained, python3 standard library only (scipy is used for one extra numerical integration when installed).
Run: python3 verify_key.py

Model that generated the figure (so the key is exact):
  intrinsic (closure-free) law   da/dN = C * dK_eff^m * (1 - (dK_th,eff / dK_eff)^4),  C = 1.0e-12 m/cycle per (MPa sqrt m)^3,
                                 m = 3, dK_th,eff = 2.5 MPa sqrt m;  the dashed line is the Paris fit da/dN = C dK^3 of the
                                 R = 0.7 data, through (10, 1e-9) and (100, 1e-6).
  closure: K_op = 6.0 MPa sqrt m, the same value at every load ratio, whenever K_min < K_op; no closure once K_min >= K_op;
           dK_eff = K_max - max(K_op, K_min).
  R = 0.7 data: closure only below K_max = K_op/0.7 = 8.6, i.e. dK < 2.6, below the first plotted point: the R = 0.7 curve is
                the intrinsic curve over the whole plotted range.
  R = 0.1 data: closure while K_min = dK/9 < 6, i.e. dK < 54: there dK_eff = K_max - K_op = dK/0.9 - 6 and the applied
                range at a given rate is dK = 0.9 (dK_eff + 6); the two data sets merge above dK = 54.  Pairs at equal
                rates: dK_eff = 4, 14, 24, 34, 44 against dK(R = 0.1) = 9, 18, 27, 36, 45, so K_op = dK/0.9 - dK_eff = 6
                from any pair.
Question data: edge crack in a wide plate, Y = 1.12 (constant), a0 = 0.20 mm, sigma_max = 400 MPa, R = 0.4,
  K_IC = 55 MPa sqrt m, failure when K_max = K_IC.
Decisive step: at R = 0.4 closure is present while K_min = 0.4 K_max < 6, i.e. K_max < 15 MPa sqrt m, which is the case
  from a0 (K_max = 11.23) up to the transition length a_t = (15/(Y sigma_max))^2/pi = 0.357 mm; beyond a_t the crack is
  closure-free.  The life is the sum of the two parts, each with its own closed form.
"""
import math

C = 1.0e-12; m = 3; dK_th_eff = 2.5; Kop = 6.0
Y = 1.12; a0 = 0.20e-3; smax = 400.0; R = 0.4; KIC = 55.0
smin = R * smax; ds = smax - smin
B = Y * smax * math.sqrt(math.pi)          # K_max = B sqrt(a)
A = Y * ds * math.sqrt(math.pi)            # dK = A sqrt(a)
ac = (KIC / (Y * smax)) ** 2 / math.pi
at = (Kop / R / B) ** 2
print(f"sigma_max = {smax} MPa, sigma_min = {smin} MPa, delta sigma = {ds} MPa; K_max = {B:.2f} sqrt(a), delta K = {A:.2f} sqrt(a) (a in m)")
print(f"a_c = (K_IC/(Y sigma_max))^2/pi = {ac*1e3:.4f} mm; K_max at a0 = {B*math.sqrt(a0):.3f} MPa sqrt m, K_min at a0 = {R*B*math.sqrt(a0):.3f} < K_op = {Kop}: closure present at a0")
print(f"transition: K_min = K_op when K_max = K_op/R = {Kop/R:.1f} MPa sqrt m, a_t = {at*1e3:.4f} mm; dK_eff at a0 = {B*math.sqrt(a0)-Kop:.3f} (above the intrinsic threshold {dK_th_eff}), at a_t = {B*math.sqrt(at)-Kop:.2f}; closure-free dK from {A*math.sqrt(at):.2f} to {A*math.sqrt(ac):.2f}")
assert a0 < at < ac and B * math.sqrt(a0) - Kop > dK_th_eff

# ---------- (1) closed forms ----------
def F(w): return -1.0 / w - Kop / (2 * w * w)
w0 = B * math.sqrt(a0) - Kop; wt = B * math.sqrt(at) - Kop
N1 = 2.0 / (C * B * B) * (F(wt) - F(w0))
N2 = 2.0 / (C * A ** 3) * (at ** -0.5 - ac ** -0.5)
N = N1 + N2
print(f"ROUTE 1 (closed forms): part 1 (closure, dK_eff = K_max - K_op = B sqrt(a) - {Kop}): N1 = (2/(C B^2)) [-1/w - K_op/(2 w^2)] from w0 = {w0:.4f} to w_t = {wt:.4f} = {N1:.1f}")
print(f"                        part 2 (closure-free, dK_eff = dK): N2 = 2/(C A^3) [a_t^(-1/2) - a_c^(-1/2)] = {N2:.1f}")
print(f"                        N = N1 + N2 = {N:.1f} cycles = {N:.4e}")

# ---------- (2) numerical integration of the piecewise law (composite Simpson in log a, each part) ----------
def dkeff(a):
    kmax = B * math.sqrt(a); kmin = R * kmax
    return kmax - max(Kop, kmin)
def simpson(f, t0, t1, n=20000):
    h = (t1 - t0) / n
    return (f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))) * h / 3
g = lambda t: math.exp(t) / (C * dkeff(math.exp(t)) ** m)
N_num = simpson(g, math.log(a0), math.log(at)) + simpson(g, math.log(at), math.log(ac))
print(f"ROUTE 2 (Simpson on the piecewise law): N = {N_num:.1f} cycles")
assert abs(N_num - N) / N < 1e-8
try:
    from scipy.integrate import quad
    N3 = quad(lambda a: 1.0 / (C * dkeff(a) ** m), a0, at)[0] + quad(lambda a: 1.0 / (C * dkeff(a) ** m), at, ac)[0]
    print(f"ROUTE 3 (scipy quad): N = {N3:.1f} cycles")
    assert abs(N3 - N) / N < 1e-8
except ImportError:
    print("scipy not installed, quad skipped")

# ---------- (3) the knee factor, which the stem says to ignore ----------
gk = lambda t: math.exp(t) / (C * dkeff(math.exp(t)) ** m * (1 - (dK_th_eff / dkeff(math.exp(t))) ** 4))
Nk = simpson(gk, math.log(a0), math.log(at)) + simpson(gk, math.log(at), math.log(ac))
print(f"with the near-threshold knee factor kept in the law: N = {Nk:.1f} cycles ({(Nk/N-1)*100:+.2f} percent; the stem says to use the Paris fit)")

def sig(x, n):
    e = math.floor(math.log10(abs(x))); return round(x / 10 ** (e - n + 1)) * 10 ** (e - n + 1)
print(f"ANSWER KEY (2 s.f.): {sig(N, 2):.2g} cycles = {sig(N, 2)/1e6:.1f} x 10^6  (3 s.f. would be {sig(N, 3):.3g})")

# ---------- (4) wrong routes ----------
Nfree = 2.0 / (C * A ** 3) * (a0 ** -0.5 - ac ** -0.5)
print(f"wrong route A, closure ignored (intrinsic law with dK throughout): N = {Nfree:.4e} -> {sig(Nfree, 2):.2g}")
wc = B * math.sqrt(ac) - Kop
Nthr = 2.0 / (C * B * B) * (F(wc) - F(w0))
print(f"wrong route B, closure kept throughout (dK_eff = K_max - K_op up to a_c, transition ignored): N = {Nthr:.4e} -> {sig(Nthr, 2):.2g}")
k = Kop / (B * math.sqrt(a0)); U = (1 - k) / (1 - R)
Nfrac = Nfree / U ** 3
print(f"wrong route C, K_op taken as the fixed fraction {k:.3f} of K_max that holds at a0 (U = {U:.3f} throughout): N = {Nfrac:.4e} -> {sig(Nfrac, 2):.2g}")
U01 = 0.5
Nr01 = Nfree / U01 ** 3
print(f"wrong route D, the R = 0.1 data treated as a parallel Paris line a factor 2 to the right (U = 0.5): N = {Nr01:.4e} -> {sig(Nr01, 2):.2g}")
ac_ds = (KIC / (Y * ds)) ** 2 / math.pi
N_acds = N1 + 2.0 / (C * A ** 3) * (at ** -0.5 - ac_ds ** -0.5)
print(f"wrong route E, a_c computed with delta sigma instead of sigma_max (a_c = {ac_ds*1e3:.2f} mm): N = {N_acds:.4e} -> {sig(N_acds, 2):.2g}")
for kread in (5.5, 6.5):
    at_ = (kread / R / B) ** 2; w0_ = B * math.sqrt(a0) - kread; wt_ = B * math.sqrt(at_) - kread
    Fk = lambda w: -1.0 / w - kread / (2 * w * w)
    Nk_ = 2.0 / (C * B * B) * (Fk(wt_) - Fk(w0_)) + 2.0 / (C * A ** 3) * (at_ ** -0.5 - ac ** -0.5)
    print(f"sensitivity: K_op read as {kread}: N = {Nk_:.4e} -> {sig(Nk_, 2):.2g}")
print("ALL CHECKS PASSED.")
