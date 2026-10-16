"""Verification of the answer key: fatigue crack growth life of the MIM Ti-6Al-7Nb edge-cracked plate loaded at R = 0.4,
with the growth law read from the figure (two long-crack data sets at R = 0.1 and R = 0.7).

Self-contained, python3 standard library only (scipy is used for one extra numerical integration when installed).
Run: python3 verify_key.py

Model that generated the figure (so the key is exact):
  intrinsic (closure-free) law   da/dN = C * dK_eff^m * (1 - (dK_th,eff / dK_eff)^4),  C = 1.0e-12 m/cycle per (MPa sqrt m)^3,
                                 m = 3, dK_th,eff = 2.5 MPa sqrt m;  the dashed Paris fits are da/dN = C dK_eff^3.
  closure: K_op = 0.30 K_max at every load ratio with K_min < K_op; no closure once K_min >= K_op.
  R = 0.7 data: K_min = 0.7 K_max > K_op, so dK_eff = dK (the R = 0.7 curve is the intrinsic curve).
  R = 0.1 data: dK_eff = K_max - K_op = 0.70 K_max = (0.70/0.90) dK = U dK with U = 7/9; the R = 0.1 curve is the
                intrinsic curve shifted right by the factor 1/U = 9/7 = 1.2857 in dK.
Question data: edge crack in a wide plate, Y = 1.12 (constant), a0 = 0.20 mm, sigma_max = 400 MPa, R = 0.4,
  K_IC = 55 MPa sqrt m, failure when K_max = K_IC.
Decisive step: at R = 0.4, K_min = 0.40 K_max > K_op = 0.30 K_max, so the crack is closure-free and the R = 0.7
  (intrinsic) Paris constants apply unchanged; the R = 0.1 curve, or an interpolation between the curves, is wrong.
"""
import math

C = 1.0e-12; m = 3; dK_th_eff = 2.5; kop_ratio = 0.30
Y = 1.12; a0 = 0.20e-3; smax = 400.0; R = 0.4; KIC = 55.0
smin = R * smax; ds = smax - smin
U01 = (1 - kop_ratio) / (1 - 0.1)          # dK_eff / dK at R = 0.1
print(f"closure: K_op/K_max = {kop_ratio}; at R = 0.1 U = dK_eff/dK = {U01:.4f}, curve shift factor 1/U = {1/U01:.4f}")
print(f"at R = 0.4: K_min/K_max = {R} >= K_op/K_max = {kop_ratio}: closure-free, intrinsic constants C = {C:g}, m = {m}")

# ---------- critical crack length and initial dK ----------
ac = (KIC / (Y * smax)) ** 2 / math.pi
dK0 = Y * ds * math.sqrt(math.pi * a0); dKc = Y * ds * math.sqrt(math.pi * ac)
print(f"sigma_max = {smax} MPa, sigma_min = {smin} MPa, delta sigma = {ds} MPa")
print(f"a_c = (K_IC/(Y sigma_max))^2/pi = {ac*1e3:.4f} mm;  dK at a0 = {dK0:.3f} MPa sqrt m, at a_c = {dKc:.2f} MPa sqrt m")
print(f"thresholds: intrinsic {dK_th_eff} MPa sqrt m, apparent at R = 0.1 {dK_th_eff/U01:.3f} MPa sqrt m; dK at a0 is above both")
assert dK0 > dK_th_eff / U01

# ---------- (1) closed form, m = 3 ----------
def life_closed(Ceff):
    return 2.0 / ((m - 2) * Ceff * (Y * ds * math.sqrt(math.pi)) ** m) * (a0 ** (-(m - 2) / 2) - ac ** (-(m - 2) / 2))
N = life_closed(C)
print(f"ROUTE 1 (closed form): N = 2/((m-2) C (Y ds sqrt(pi))^m) [a0^(-1/2) - ac^(-1/2)] = {N:.1f} cycles = {N:.4e}")

# ---------- (2) numerical integration of the Paris law (composite Simpson in log a) ----------
def dadn(a, Ceff): return Ceff * (Y * ds * math.sqrt(math.pi * a)) ** m
def life_simpson(Ceff, n=20000):
    # integrate dN = da / (da/dN) with substitution a = exp(t)
    t0, t1 = math.log(a0), math.log(ac); h = (t1 - t0) / n
    f = lambda t: math.exp(t) / dadn(math.exp(t), Ceff)
    s = f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))
    return s * h / 3
N2 = life_simpson(C)
print(f"ROUTE 2 (Simpson, 20000 intervals): N = {N2:.1f} cycles")
assert abs(N2 - N) / N < 1e-9
try:
    from scipy.integrate import quad
    N3, err = quad(lambda a: 1.0 / dadn(a, C), a0, ac)
    print(f"ROUTE 3 (scipy quad): N = {N3:.1f} cycles (abs err {err:.1e})")
    assert abs(N3 - N) / N < 1e-9
except ImportError:
    print("scipy not installed, quad skipped")

# ---------- (3) check that the growth law with the knee term changes nothing above dK = 6 ----------
def dadn_knee(a, Ceff, U=1.0):
    dKeff = U * Y * ds * math.sqrt(math.pi * a)
    return Ceff * dKeff ** m * (1 - (dK_th_eff / dKeff) ** 4)
def life_simpson_knee(U=1.0, n=20000):
    t0, t1 = math.log(a0), math.log(ac); h = (t1 - t0) / n
    f = lambda t: math.exp(t) / dadn_knee(math.exp(t), C, U)
    s = f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))
    return s * h / 3
Nk = life_simpson_knee()
print(f"with the near-threshold knee factor kept in the law: N = {Nk:.1f} cycles ({(Nk/N-1)*100:+.2f} percent; the stem says to use the Paris fit)")

def sig3(x):
    e = math.floor(math.log10(abs(x))); return round(x / 10 ** (e - 2)) * 10 ** (e - 2)
key = sig3(N)
print(f"ANSWER KEY (3 s.f.): {key:.3g} cycles = {key/1e6:.2f} x 10^6")

# ---------- (4) wrong routes ----------
N_r01 = life_closed(C * U01 ** m)
print(f"wrong route A, R = 0.1 fit applied at R = 0.4 (C_eff = C U^3 = {C*U01**m:.3e}): N = {N_r01:.4e} -> {sig3(N_r01):.3g}")
N_interp = life_closed(C * U01 ** (m * 0.5))
print(f"wrong route B, log-linear interpolation of the two curves in R (shift factor U^(1/2)): N = {N_interp:.4e} -> {sig3(N_interp):.3g}")
ac_ds = (KIC / (Y * ds)) ** 2 / math.pi
N_acds = 2.0 / ((m - 2) * C * (Y * ds * math.sqrt(math.pi)) ** m) * (a0 ** (-0.5) - ac_ds ** (-0.5))
print(f"wrong route C, a_c computed with delta sigma instead of sigma_max (a_c = {ac_ds*1e3:.2f} mm): N = {N_acds:.4e} -> {sig3(N_acds):.3g}")
N_noY = 2.0 / ((m - 2) * C * (ds * math.sqrt(math.pi)) ** m) * (a0 ** (-0.5) - ((KIC / smax) ** 2 / math.pi) ** (-0.5))
print(f"wrong route D, Y omitted everywhere: N = {N_noY:.4e} -> {sig3(N_noY):.3g}")
N_dKmax = life_closed(C) * (ds / smax) ** m
print(f"wrong route E, K_max range used instead of delta K (sigma_max in place of delta sigma): N = {N_dKmax:.4e} -> {sig3(N_dKmax):.3g}")
print("ALL CHECKS PASSED.")
