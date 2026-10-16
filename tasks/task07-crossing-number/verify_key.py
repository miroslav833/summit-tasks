"""Verification of the answer key: fatigue life of the edge-cracked plate, 1.1e5 cycles (two significant
figures; the exact model value is printed).

Self-contained.  Route A needs scipy; route B uses only the standard library and mpmath (both in the
venv).  Run: python3 verify_key.py

The figure is generated from the model stated here, so the key is a property of the model:
  da/dN = C (U dK)^n with the R = 0.5 fit through (5, 1e-9) and (50, 1e-6): n = 3, C = 8e-12;
  the R = 0.1 fit through (10, 1e-9) and (100, 1e-6): same n, shifted by a factor 2 in dK, so U(0.1) = 1/2
  with U(0.5) = 1; U linear in R gives U(0.3) = 3/4.
  Component: edge crack, W = 20 mm, a0 = 0.6 mm, dsigma = 250 MPa, R = 0.3, so sigma_max = 250/0.7 MPa,
  Y(a/W) = 1.12 - 0.231 x + 10.55 x^2 - 21.72 x^3 + 30.39 x^4, failure at K_max = K_IC = 60 MPa sqrt(m).
  N = integral from a0 to a_c of da / (C (U Y dsigma sqrt(pi a))^n).

Route A: a_c by bisection, N by scipy.integrate.quad.
Route B: a_c by bisection in mpmath at 30 digits, N by mpmath.quad (tanh-sinh) and, as a third check,
         a composite Simpson rule on 2000 and 4000 panels with Richardson extrapolation.
Both routes also evaluate the plausible wrong routes (R = 0.1 line as it stands, R = 0.5 line as it
stands, Elber's U = 0.5 + 0.4R, constant Y = 1.12, a_c from dsigma instead of sigma_max).
"""
import math

# ---- the model (every number the solver reads or is given) ----
ANCH05 = ((5.0, 1e-9), (50.0, 1e-6))     # R = 0.5 fit anchors (dK in MPa sqrt m, da/dN in m/cycle)
ANCH01 = ((10.0, 1e-9), (100.0, 1e-6))   # R = 0.1 fit anchors
W = 0.020; a0 = 0.0006; dsigma = 250.0; Rc = 0.3; KIC = 60.0

# ---- reading the figure: n, C, U(0.1) ----
(k1, r1), (k2, r2) = ANCH05
n = math.log(r2 / r1) / math.log(k2 / k1)
C = r1 / k1 ** n
(q1, s1), (q2, s2) = ANCH01
n01 = math.log(s2 / s1) / math.log(q2 / q1)
U01 = (k1 / q1)  # same rate at dK = 5 (R = 0.5) and dK = 10 (R = 0.1): U(0.1) * 10 = 1 * 5
U05 = 1.0
print("Paris exponent from the R = 0.5 anchors: n =", n, "; from the R = 0.1 anchors:", n01)
print("C =", C, "m/cycle per (MPa sqrt m)^n")
print("closure factor U(0.1) =", U01, "(horizontal shift of the two parallel fits), U(0.5) = 1")


def U_of_R(R):
    return U01 + (U05 - U01) * (R - 0.1) / (0.5 - 0.1)


U = U_of_R(Rc)
print("U at the service ratio R = 0.3 (linear interpolation):", U)
smax = dsigma / (1 - Rc)
print("sigma_max = dsigma / (1 - R) =", smax, "MPa")


def Y(a):
    x = a / W
    return 1.12 - 0.231 * x + 10.55 * x ** 2 - 21.72 * x ** 3 + 30.39 * x ** 4


def a_crit(s, lo=1e-6, hi=W * 0.999):
    f = lambda a: Y(a) * s * math.sqrt(math.pi * a) - KIC
    assert f(lo) < 0 < f(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return 0.5 * (lo + hi)


ac = a_crit(smax)
print("a_c from K_max = K_IC: %.6f mm (a/W = %.4f, Y = %.4f)" % (ac * 1e3, ac / W, Y(ac)))
print("dK at a0: %.4f MPa sqrt m; dK_eff at a0: %.4f; initial rate %.4e m/cycle" % (Y(a0) * dsigma * math.sqrt(math.pi * a0), U * Y(a0) * dsigma * math.sqrt(math.pi * a0), C * (U * Y(a0) * dsigma * math.sqrt(math.pi * a0)) ** n))


def integrand(a, U=U, ds=dsigma, Yf=Y):
    return 1.0 / (C * (U * Yf(a) * ds * math.sqrt(math.pi * a)) ** n)


# ================= Route A =================
from scipy.integrate import quad
print("\nRoute A (scipy quad)")
NA = quad(integrand, a0, ac, limit=200)[0]
print("N = %.2f cycles" % NA)

# ================= Route B =================
import mpmath as mp
mp.mp.dps = 30
print("\nRoute B (mpmath, independent arithmetic)")


def Ymp(a):
    x = a / mp.mpf(W)
    return mp.mpf("1.12") - mp.mpf("0.231") * x + mp.mpf("10.55") * x ** 2 - mp.mpf("21.72") * x ** 3 + mp.mpf("30.39") * x ** 4


def a_crit_mp(s):
    f = lambda a: Ymp(a) * s * mp.sqrt(mp.pi * a) - KIC
    lo, hi = mp.mpf("1e-6"), mp.mpf(W) * mp.mpf("0.999")
    for _ in range(120):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return (lo + hi) / 2


Cmp = mp.mpf(r1) / mp.mpf(k1) ** 3
Ump = mp.mpf(3) / 4
acmp = a_crit_mp(mp.mpf(dsigma) / (1 - mp.mpf(Rc)))
print("a_c (mpmath): %s mm" % mp.nstr(acmp * 1000, 8))
fmp = lambda a: 1 / (Cmp * (Ump * Ymp(a) * dsigma * mp.sqrt(mp.pi * a)) ** 3)
NB = mp.quad(fmp, [mp.mpf(a0), acmp])
print("N (tanh-sinh) = %s cycles" % mp.nstr(NB, 10))


def simpson(f, lo, hi, panels):
    h = (hi - lo) / panels
    s = f(lo) + f(hi)
    for i in range(1, panels):
        s += (4 if i % 2 else 2) * f(lo + i * h)
    return s * h / 3


S1 = simpson(lambda a: integrand(float(a)), float(a0), float(acmp), 2000)
S2 = simpson(lambda a: integrand(float(a)), float(a0), float(acmp), 4000)
print("N (Simpson 2000 / 4000 panels, Richardson) = %.2f / %.2f / %.2f" % (S1, S2, S2 + (S2 - S1) / 15))
assert abs(NA - float(NB)) / NA < 1e-6
print("Both routes agree: N = %.0f cycles, which is 1.1e5 to two significant figures." % NA)
print("Distance of the exact value from the nearest rounding boundary (1.05e5 or 1.15e5): %.1f%%" % (100 * min(NA - 1.05e5, 1.15e5 - NA) / NA))

# ================= plausible wrong routes =================
print("\nPlausible wrong routes (route A integrator)")
wrong = {
    "R = 0.1 line used as it stands (U = 0.5)": quad(lambda a: integrand(a, U=0.5), a0, ac, limit=200)[0],
    "R = 0.5 line used as it stands (U = 1)": quad(lambda a: integrand(a, U=1.0), a0, ac, limit=200)[0],
    "Elber's U = 0.5 + 0.4 R = 0.62": quad(lambda a: integrand(a, U=0.5 + 0.4 * Rc), a0, ac, limit=200)[0],
    "Y held at 1.12": quad(lambda a: integrand(a, Yf=lambda x: 1.12), a0, ac, limit=200)[0],
    "a_c from dsigma instead of sigma_max (a_c = %.3f mm)" % (a_crit(dsigma) * 1e3): quad(integrand, a0, a_crit(dsigma), limit=200)[0],
    "no closure correction and no interpolation, dK_eff = dK with the R = 0.1 constants (C/8)": quad(lambda a: 1.0 / (C / 8 * (Y(a) * dsigma * math.sqrt(math.pi * a)) ** n), a0, ac, limit=200)[0],
}
for k, v in wrong.items():
    print("   %s: N = %.0f (%.2g)" % (k, v, v))
