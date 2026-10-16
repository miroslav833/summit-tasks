"""Verification of the answer key: fatigue crack growth life of the MIM Ti-6Al-7Nb edge-cracked plate loaded at R = 0.4,
with the growth law and the closure level read from the figure (two long-crack data sets at R = 0.1 and R = 0.7).

Self-contained, python3 standard library only (scipy is used for one extra numerical integration when installed).
Run: python3 verify_key.py

Model that generated the figure (so the key is exact):
  intrinsic (closure-free) law   da/dN = C * dK_eff^m * (1 - (dK_th,eff / dK_eff)^4),  C = 1.0e-12 m/cycle per (MPa sqrt m)^3,
                                 m = 3, dK_th,eff = 2.5 MPa sqrt m;  the dashed Paris fits are da/dN = C dK_eff^3.
  closure: K_op = 0.55 K_max at every load ratio with K_min < K_op; no closure once K_min >= K_op.
  R = 0.7 data: K_min = 0.7 K_max > K_op, so dK_eff = dK (the R = 0.7 curve is the intrinsic curve).
  R = 0.1 data: dK_eff = K_max - K_op = 0.45 K_max = (0.45/0.90) dK = 0.5 dK; the R = 0.1 curve is the intrinsic curve
                displaced to the right by the factor 2 in dK (its fit passes through (20, 1e-9) and (200, 1e-6)).
Question data: edge crack in a wide plate, Y = 1.12 (constant), a0 = 0.20 mm, sigma_max = 400 MPa, R = 0.4,
  K_IC = 55 MPa sqrt m, failure when K_max = K_IC.
Decisive step: at R = 0.4, K_min = 0.40 K_max < K_op = 0.55 K_max, so closure is present and
  dK_eff = K_max - K_op = 0.45 K_max = (0.45/0.60) dK = 0.75 dK; the growth law of the plate is da/dN = C (0.75 dK)^3.
  Neither measured curve applies directly: the R = 0.7 fit (closure-free) and the R = 0.1 fit (U = 0.5) both give
  wrong lives, and so does an interpolation between them.
"""
import math

C = 1.0e-12; m = 3; dK_th_eff = 2.5; kop_ratio = 0.55
Y = 1.12; a0 = 0.20e-3; smax = 400.0; R = 0.4; KIC = 55.0
smin = R * smax; ds = smax - smin
U01 = (1 - kop_ratio) / (1 - 0.1)
U04 = (1 - kop_ratio) / (1 - R)
print(f"closure: K_op/K_max = {kop_ratio}; at R = 0.1 U = dK_eff/dK = {U01:.4f}, curve displacement factor 1/U = {1/U01:.4f}")
print(f"at R = 0.4: K_min/K_max = {R} < K_op/K_max = {kop_ratio}: closure present, U(0.4) = (1 - {kop_ratio})/(1 - {R}) = {U04:.4f}")
print(f"growth law of the plate: da/dN = C (U dK)^3 with C_eff = C U^3 = {C * U04 ** 3:.4e} m/cycle per (MPa sqrt m)^3")

# ---------- critical crack length and the range of dK ----------
ac = (KIC / (Y * smax)) ** 2 / math.pi
dK0 = Y * ds * math.sqrt(math.pi * a0); dKc = Y * ds * math.sqrt(math.pi * ac)
print(f"sigma_max = {smax} MPa, sigma_min = {smin} MPa, delta sigma = {ds} MPa")
print(f"a_c = (K_IC/(Y sigma_max))^2/pi = {ac*1e3:.4f} mm;  dK at a0 = {dK0:.3f}, at a_c = {dKc:.2f} MPa sqrt m;  dK_eff at a0 = {U04*dK0:.3f}, at a_c = {U04*dKc:.2f}")
print(f"thresholds: intrinsic {dK_th_eff} MPa sqrt m (dK_eff at a0 is above it), apparent at R = 0.1 {dK_th_eff/U01:.2f} MPa sqrt m")
assert U04 * dK0 > dK_th_eff

# ---------- (1) closed form, m = 3 ----------
def life_closed(Ceff):
    return 2.0 / ((m - 2) * Ceff * (Y * ds * math.sqrt(math.pi)) ** m) * (a0 ** (-(m - 2) / 2) - ac ** (-(m - 2) / 2))
Ceff = C * U04 ** m
N = life_closed(Ceff)
print(f"ROUTE 1 (closed form): N = 2/((m-2) C_eff (Y ds sqrt(pi))^m) [a0^(-1/2) - ac^(-1/2)] = {N:.1f} cycles = {N:.4e}")

# ---------- (2) numerical integration (composite Simpson in log a) ----------
def dadn(a, Ceff): return Ceff * (Y * ds * math.sqrt(math.pi * a)) ** m
def life_simpson(Ceff, n=20000):
    t0, t1 = math.log(a0), math.log(ac); h = (t1 - t0) / n
    f = lambda t: math.exp(t) / dadn(math.exp(t), Ceff)
    s = f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))
    return s * h / 3
N2 = life_simpson(Ceff)
print(f"ROUTE 2 (Simpson, 20000 intervals): N = {N2:.1f} cycles")
assert abs(N2 - N) / N < 1e-9
try:
    from scipy.integrate import quad
    N3, err = quad(lambda a: 1.0 / dadn(a, Ceff), a0, ac)
    print(f"ROUTE 3 (scipy quad): N = {N3:.1f} cycles (abs err {err:.1e})")
    assert abs(N3 - N) / N < 1e-9
except ImportError:
    print("scipy not installed, quad skipped")

# ---------- (3) the knee factor, which the stem says to ignore ----------
def life_simpson_knee(U, n=20000):
    t0, t1 = math.log(a0), math.log(ac); h = (t1 - t0) / n
    def f(t):
        dKeff = U * Y * ds * math.sqrt(math.pi * math.exp(t))
        return math.exp(t) / (C * dKeff ** m * (1 - (dK_th_eff / dKeff) ** 4))
    s = f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))
    return s * h / 3
Nk = life_simpson_knee(U04)
print(f"with the near-threshold knee factor kept in the law: N = {Nk:.1f} cycles ({(Nk/N-1)*100:+.2f} percent; the stem says to use the Paris fits)")

def sig3(x):
    e = math.floor(math.log10(abs(x))); return round(x / 10 ** (e - 2)) * 10 ** (e - 2)
key = sig3(N)
print(f"ANSWER KEY (3 s.f.): {key:.3g} cycles = {key/1e6:.2f} x 10^6")

# ---------- (4) wrong routes ----------
print(f"wrong route A, closure assumed absent at R = 0.4 (R = 0.7 fit used directly): N = {life_closed(C):.4e} -> {sig3(life_closed(C)):.3g}")
print(f"wrong route B, R = 0.1 fit used (C U(0.1)^3 = {C*U01**m:.3e}): N = {life_closed(C*U01**m):.4e} -> {sig3(life_closed(C*U01**m)):.3g}")
print(f"wrong route C, log-linear interpolation of the two curves in R (displacement 2^(1/2)): N = {life_closed(C*U01**(m*0.5)):.4e} -> {sig3(life_closed(C*U01**(m*0.5))):.3g}")
Ue = 0.5 + 0.4 * R
print(f"wrong route D, Elber's U = 0.5 + 0.4 R = {Ue:.2f} instead of the closure level in the figure: N = {life_closed(C*Ue**m):.4e} -> {sig3(life_closed(C*Ue**m)):.3g}")
ac_ds = (KIC / (Y * ds)) ** 2 / math.pi
N_acds = 2.0 / ((m - 2) * Ceff * (Y * ds * math.sqrt(math.pi)) ** m) * (a0 ** (-0.5) - ac_ds ** (-0.5))
print(f"wrong route E, a_c computed with delta sigma instead of sigma_max (a_c = {ac_ds*1e3:.2f} mm): N = {N_acds:.4e} -> {sig3(N_acds):.3g}")
N_dKmax = life_closed(Ceff) * (ds / smax) ** m
print(f"wrong route F, sigma_max in place of delta sigma in the range: N = {N_dKmax:.4e} -> {sig3(N_dKmax):.3g}")
print("ALL CHECKS PASSED.")
