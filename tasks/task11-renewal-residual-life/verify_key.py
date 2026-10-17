# Limiting mean residual life of a renewal process with log-logistic inter-arrival times, over the mean.
# Run: python3 verify_key.py (needs numpy and scipy)
import math, numpy as np
from scipy.integrate import quad
# Step 1: parameters from the two gridline crossings the curve passes through
t1, S1 = 6.0, 0.02
t2, S2 = 20.0, 0.0005
k = math.log((1/S2 - 1) / (1/S1 - 1)) / math.log(t2 / t1)
lam = t1 / (1/S1 - 1)**(1/k)
print(f"k = {k:.4f}, lambda = {lam:.4f}  (from (t/lam)^k = 1/S - 1 at the two crossings)")
S = lambda t: 1.0 / (1.0 + (t / lam)**k)
print(f"check: S({t1:g}) = {S(t1):.4f}, S({t2:g}) = {S(t2):.4f}")
labelled = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100]
print("curve at every labelled t and the distance to the nearest gridline (lines at 1, 2, 5 of each decade):")
for t in labelled:
    y = S(t)
    if y < 1e-4: print(f"   t = {t:3d}: S = {y:.3e} (below the axis)"); continue
    e = 10**math.floor(math.log10(y)); mant = y / e
    cands = [c*e for c in (1, 2, 5, 10)]
    nearest = min(cands, key=lambda v: abs(math.log10(y / v)))
    print(f"   t = {t:3d}: S = {y:.4g}, nearest line {nearest:g}, off by {abs(y/nearest-1)*100:.0f} percent")
# Step 2: closed form. E[X^r] = lam^r * (pi r/k) / sin(pi r/k) for r < k.
m1 = lam * (math.pi / k) / math.sin(math.pi / k)
m2 = lam**2 * (2*math.pi / k) / math.sin(2*math.pi / k)
ratio_closed = (k / (2*math.pi)) * math.tan(math.pi / k)
print(f"Route 1, closed form: E[X] = {m1:.5f}, E[X^2] = {m2:.5f}, E[X^2]/(2 E[X]^2) = {m2/(2*m1*m1):.5f}, (k/2pi) tan(pi/k) = {ratio_closed:.5f}")
# Step 3: numerical moments from the survival function: E[X] = int S, E[X^2] = 2 int t S
I1 = quad(S, 0, np.inf, limit=500)[0]; I2 = 2 * quad(lambda t: t * S(t), 0, np.inf, limit=500)[0]
print(f"Route 2, quadrature of the survival function: E[X] = {I1:.5f}, E[X^2] = {I2:.5f}, ratio = {I2/(2*I1*I1):.5f}")
# Step 4: the same moments through the Beta function, E[X^r] = lam^r B(1 + r/k, 1 - r/k), with scipy's beta
from scipy.special import beta as B
b1 = lam * B(1 + 1/k, 1 - 1/k); b2 = lam**2 * B(1 + 2/k, 1 - 2/k)
print(f"Route 3, Beta function: E[X] = {b1:.5f}, E[X^2] = {b2:.5f}, ratio = {b2/(2*b1*b1):.5f}")
# Step 5: the limit itself from renewal theory: the equilibrium residual-life density is S(t)/m, so the limit of
# E[r(t)] is int t S(t) dt / m = E[X^2]/(2 m); checked by quadrature of t S(t)/m
m = I1; lim_r = quad(lambda t: t * S(t) / m, 0, np.inf, limit=500)[0]
print(f"Route 4, equilibrium residual-life density S(t)/m: lim E[r(t)] = {lim_r:.5f}, over m = {lim_r/m:.5f}")
print("Note: a direct simulation of r(t) at a fixed large t converges slowly here, because r has tail index k - 1 < 2 and")
print("      so infinite variance; it is not used as a check.")
print(f"Answer key: {ratio_closed:.4f}, two significant figures {ratio_closed:.2g}")
# Wrong routes
print(f"Wrong: m/2 over m = 0.5; m over m = 1; E[X^2]/(2E[X]) itself (not divided by the mean) = {m2/(2*m1):.4f}")
def ratio_of(ta, Sa, tb, Sb):
    kk = math.log((1/Sb - 1) / (1/Sa - 1)) / math.log(tb / ta)
    return kk, ((kk/(2*math.pi))*math.tan(math.pi/kk) if kk > 2 else float('inf'))
near = {}
for t in labelled:
    y = S(t)
    if 1e-4 <= y <= 0.95:
        e = 10**math.floor(math.log10(y)); near[t] = min([c*e for c in (1, 2, 5, 10)], key=lambda v: abs(math.log10(y / v)))
near[t1] = S1; near[t2] = S2
import itertools
print("Every pair of labelled abscissae read at the nearest gridline (true crossings kept at their true values):")
for a, b in itertools.combinations(sorted(near), 2):
    if (a, b) == (t1, t2): continue
    try: kk, rr = ratio_of(a, near[a], b, near[b])
    except (ValueError, ZeroDivisionError): continue
    if kk <= 0: continue
    print(f"   ({a:g}, {near[a]:g}) with ({b:g}, {near[b]:g}): k = {kk:.3f}, ratio = {'infinite' if rr == float('inf') else f'{rr:.4f}'}")
