"""Model behind the crack-growth task.  Everything in the figure is generated from these choices.

Material: a powder-injection-moulded alpha/beta titanium alloy (invented data).
Crack growth law in the Paris regime:  da/dN = C * (dK_eff)^n,  dK_eff = U(R) * dK.
Closure: U(R) linear in R between the two tested ratios, with the R = 0.5 data closure-free (U = 1).
Fit anchors (on gridline intersections) for the straight lines in the figure:
   R = 0.5 : (dK = 5,  1e-9 m/cycle) and (dK = 50,  1e-6 m/cycle)   -> n = 3, C = 8e-12
   R = 0.1 : (dK = 10, 1e-9 m/cycle) and (dK = 100, 1e-6 m/cycle)   -> U(0.1) = 1/2
Component: single-edge through-crack in a plate of width W, remote stress range dsigma at ratio R_c,
Y(a/W) polynomial (standard SENT), failure when K_max = K_IC.
"""
import math

C = 8e-12          # m/cycle (MPa sqrt m)^-n
n = 3
U01 = 0.5          # closure factor at R = 0.1
U05 = 1.0          # R = 0.5 taken closure-free
dKth_eff = 2.5     # MPa sqrt m, intrinsic threshold (used only for the near-threshold points in the figure)

W = 0.020          # m
a0 = 0.0006        # m, initial crack depth from a surface pore
dsigma = 250.0     # MPa, stress range in service
Rc = 0.3           # service load ratio
KIC = 60.0         # MPa sqrt m


def U_of_R(R):
    return U01 + (U05 - U01) * (R - 0.1) / (0.5 - 0.1)


def Y(a):
    x = a / W
    return 1.12 - 0.231 * x + 10.55 * x ** 2 - 21.72 * x ** 3 + 30.39 * x ** 4


def dK(a, ds=dsigma):
    return Y(a) * ds * math.sqrt(math.pi * a)


def dadN(a, U, ds=dsigma):
    return C * (U * dK(a, ds)) ** n


def a_crit(smax, lo=1e-6, hi=W * 0.999):
    """K_max = Y smax sqrt(pi a) = KIC, solved by bisection (K increases with a for this Y)."""
    f = lambda a: Y(a) * smax * math.sqrt(math.pi * a) - KIC
    assert f(lo) < 0 < f(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
