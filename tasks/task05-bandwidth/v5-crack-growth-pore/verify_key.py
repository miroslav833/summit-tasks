# Propagation life of a crack growing from a surface pore: constants from two points on the fitted curve,
# then two independent integrations. Run: python3 verify_key.py (needs numpy and scipy)
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
Kth = 4.0        # long-crack threshold, MPa m^0.5 (stated in the question and marked in the figure)
x1, y1 = 6.0, 2.0e-9    # the fitted curve passes exactly through this gridline crossing (Delta K, da/dN)
x2, y2 = 20.0, 1.0e-7   # and through this one
# Step 1: m and C from the two points of the Klesnil-Lukas law y = C (x^m - Kth^m)
ratio = lambda mm: (x2**mm - Kth**mm) / (x1**mm - Kth**mm) - y2 / y1
m = brentq(ratio, 2.0, 5.0)
C = y1 / (x1**m - Kth**m)
print(f"m = {m:.4f}  (root of (20^m - 4^m)/(6^m - 4^m) = 50), C = {C:.4e} m/cycle (MPa m^0.5)^-m")
print(f"check: C (6^m - 4^m) = {C*(x1**m-Kth**m):.3e}, C (20^m - 4^m) = {C*(x2**m-Kth**m):.3e}")
# Hand route for m: a few iterations of the ratio
for mm in (2.9, 2.95, 2.96, 2.959):
    print(f"   m = {mm}: ratio = {(x2**mm-Kth**mm)/(x1**mm-Kth**mm):.2f} (target 50)")
Y = 0.65         # Murakami surface-defect factor
dsw = 500.0      # smooth-specimen fatigue limit, stress range, MPa, R = 0.1
ds = 450.0       # applied stress range, MPa
ai = 50e-6       # initial crack size (sqrt(area) of the pore), m
af = 0.5e-3      # final crack size, m
a0 = (Kth / (Y * dsw))**2 / np.pi
dK = lambda a: Y * ds * np.sqrt(np.pi * a)
Kth_a = lambda a: Kth * np.sqrt(a / (a + a0))
rate = lambda a: C * (dK(a)**m - Kth_a(a)**m)
print(f"a0 = {a0*1e6:.2f} um")
print(f"Delta K at the pore = {dK(ai):.3f} MPa m^0.5, long-crack threshold {Kth}, size-corrected threshold {Kth_a(ai):.3f}")
print(f"Kitagawa fatigue limit (stress range) for a 50 um pore = {dsw*np.sqrt(a0/(ai+a0)):.1f} MPa")
N1, err = quad(lambda a: 1.0 / rate(a), ai, af, limit=200)
print(f"Route 1, adaptive quadrature: N = {N1:.1f} (error estimate {err:.1e})")
u = np.linspace(np.log(ai), np.log(af), 9); a = np.exp(u); g = a / rate(a); h = u[1] - u[0]
print("Simpson nodes (a in um, integrand a/(da/dN) in cycles):")
for ak, gk in zip(a, g): print(f"   a = {ak*1e6:8.2f} um   g = {gk:12.1f}")
N2 = h / 3 * (g[0] + g[-1] + 4 * g[1:-1:2].sum() + 2 * g[2:-1:2].sum())
print(f"Route 2, Simpson in ln a, 8 intervals: N = {N2:.1f}")
u = np.linspace(np.log(ai), np.log(af), 2001); a = np.exp(u); g = a / rate(a); h = u[1] - u[0]
N3 = h / 3 * (g[0] + g[-1] + 4 * g[1:-1:2].sum() + 2 * g[2:-1:2].sum())
print(f"Route 2, Simpson in ln a, 2000 intervals: N = {N3:.1f}")
print(f"Answer key: {N1:.3e} cycles (two significant figures: {float(f'{N1:.2g}'):.0f})")
def life_from(xa, ya, xb, yb, paris=False):
    if paris:
        mm = np.log10(yb / ya) / np.log10(xb / xa); CC = ya / xa**mm
    else:
        mm = brentq(lambda t: (xb**t - Kth**t) / (xa**t - Kth**t) - yb / ya, 2.0, 5.0); CC = ya / (xa**mm - Kth**mm)
    f = lambda a: 1.0 / (CC * (dK(a)**mm - Kth_a(a)**mm))
    return mm, CC, quad(f, ai, af, limit=200)[0]
for lab, args in [("decoy crossings (8, 5e-9) and (20, 1e-7)", (8, 5e-9, 20, 1e-7)),
                  ("decoy crossings (10, 1e-8) and (100, 1e-5)", (10, 1e-8, 100, 1e-5)),
                  ("decoy crossings (5, 1e-9) and (20, 1e-7)", (5, 1e-9, 20, 1e-7)),
                  ("decoy crossings (10, 1e-8) and (20, 1e-7)", (10, 1e-8, 20, 1e-7)),
                  ("decoy crossings (7, 5e-9) and (30, 5e-7)", (7, 5e-9, 30, 5e-7)),
                  ("right first point, decoy second (6, 2e-9) and (10, 1e-8)", (6, 2e-9, 10, 1e-8))]:
    mm, CC, N = life_from(*args); print(f"Misreading: {lab}: m = {mm:.3f}, C = {CC:.3e}, N = {N:.3e}")
mm, CC, N = life_from(6, 2e-9, 20, 1e-7, paris=True)
print(f"Wrong route: both points treated as Paris-law points (threshold ignored in the fit): m = {mm:.3f}, C = {CC:.3e}, N = {N:.3e}")
print("Wrong route: pure Paris integral with the right C and m, no threshold:", f"{quad(lambda a: 1/(C*dK(a)**m), ai, af)[0]:.3e}")
a_s = (Kth / (Y * ds))**2 / np.pi
print("Wrong route: long-crack threshold kept; Delta K at the pore is below 4.0 so growth is predicted not to start;",
      f"starting the integral where Delta K reaches 4.0 (a = {a_s*1e6:.1f} um) gives",
      f"{quad(lambda a: 1/(C*(dK(a)**m-Kth**m)), a_s*1.000001, af)[0]:.3e}")
a0amp = (Kth / (Y * dsw / 2))**2 / np.pi
print("Wrong route: a0 from the stress amplitude instead of the range:",
      f"{quad(lambda a: 1/(C*(dK(a)**m-(Kth*np.sqrt(a/(a+a0amp)))**m)), ai, af)[0]:.3e}")
