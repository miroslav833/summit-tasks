# Expected number of renewals by time t = 6 for a renewal process with log-logistic inter-arrival times,
# the parameters taken from two gridline crossings of the drawn survival function.
# Run: python3 verify_key.py   (needs numpy and scipy)
import math
import numpy as np
from scipy.integrate import quad

# Step 1: the two gridline crossings the curve passes through, and the parameters they fix
t1, S1 = 6.0, 0.02
t2, S2 = 20.0, 0.0005
k = math.log((1/S2 - 1) / (1/S1 - 1)) / math.log(t2 / t1)
lam = t1 / (1/S1 - 1)**(1/k)
print(f"k = {k:.4f}  (root of (20/6)^k = 1999/49 = {1999/49:.3f}), lambda = {lam:.4f}")
print(f"check: S({t1:g}) = {1/(1+(t1/lam)**k):.4f}, S({t2:g}) = {1/(1+(t2/lam)**k):.6f}")
for kk in (3.0, 3.05, 3.08, 3.0803):
    print(f"   hand iteration: k = {kk}: (20/6)^k = {(20/6)**kk:.2f} (target {1999/49:.2f})")

labelled = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100]
S = lambda t: 1.0 / (1.0 + (t / lam)**k)
print("curve at every labelled t and the distance to the nearest gridline (lines at 1, 2, 5 of each decade):")
for t in labelled:
    y = S(t)
    if y < 1e-4:
        print(f"   t = {t:3d}: S = {y:.3e} (below the axis)"); continue
    e = 10**math.floor(math.log10(y))
    nearest = min([c*e for c in (1, 2, 5, 10)], key=lambda v: abs(math.log10(y / v)))
    print(f"   t = {t:3d}: S = {y:.4g}, nearest line {nearest:g}, off by {abs(y/nearest-1)*100:.0f} percent")

KEY3 = "2.705"                 # the answer the question asks for: E[N(6)] rounded to 3 decimals
def verdict(v):
    r = f"{v:.3f}"
    return "rounds to 2.705" if r == KEY3 else f"rounds to {r}, wrong"

F = lambda t: 1.0 - S(t)
f = lambda t: (k/lam) * (t/lam)**(k-1) / (1.0 + (t/lam)**k)**2
T = 6.0

# Route 1: the renewal equation M = F + M * f, solved on a uniform grid by product integration
def renewal_M(T, n):
    h = T / n
    t = np.linspace(0, T, n + 1)
    Fv = F(t); fv = f(t)
    M = np.zeros(n + 1)
    for i in range(1, n + 1):
        w = np.full(i + 1, h); w[0] = w[-1] = h / 2
        M[i] = Fv[i] + np.dot(w[1:] * fv[1:i+1], M[i-1::-1])
    return M[-1]
for n in (1000, 2000, 4000, 8000):
    v = renewal_M(T, n); print(f"Route 1, renewal equation on {n:5d} intervals: M({T:g}) = {v:.6f}  {verdict(v)}")
M1 = renewal_M(T, 8000)

# Route 2: the convolution series M(t) = sum_{j>=1} F^{*j}(t), the convolutions taken numerically
def series_M(T, n=4000, jmax=40):
    h = T / n
    t = np.linspace(0, T, n + 1)
    fv = f(t)
    dens = fv.copy()          # density of the first arrival
    total = 0.0
    for j in range(1, jmax + 1):
        w = np.full(n + 1, h); w[0] = w[-1] = h / 2
        total += np.dot(w, dens)          # P(S_j <= T)
        new = np.zeros(n + 1)             # convolve dens with f
        for i in range(1, n + 1):
            wi = np.full(i + 1, h); wi[0] = wi[-1] = h / 2
            new[i] = np.dot(wi[1:] * fv[1:i+1], dens[i-1::-1])
        dens = new
        if np.dot(np.full(n+1, h), dens) < 1e-12: break
    return total
M2 = series_M(T)
print(f"Route 2, convolution series sum_j P(S_j <= {T:g}): M({T:g}) = {M2:.6f}  {verdict(M2)}")

# Route 3: simulation
rng = np.random.default_rng(20261017)
N = 400000
U = rng.random((N, 30))
X = lam * (U / (1 - U))**(1/k)          # log-logistic inverse cdf
counts = (np.cumsum(X, axis=1) <= T).sum(axis=1)
se = counts.std() / math.sqrt(N)
print(f"Route 3, simulation of {N} paths: E[N({T:g})] = {counts.mean():.4f} (standard error {se:.4f})  {verdict(counts.mean())}")

# The discretisation trap: the discrete (Lotka) renewal recursion with cell masses converges only
# like O(h) from below, so a hand-sized step lands in the wrong bin unless it is refined or extrapolated.
def lotka(T, h):
    n = int(round(T/h)); t = np.linspace(0, T, n+1)
    Fv = F(t); p = np.diff(Fv); M = np.zeros(n+1)
    for i in range(1, n+1):
        M[i] = Fv[i] + sum(p[j-1]*M[i-j] for j in range(1, i+1))
    return M[-1]
# The same quantity by the trapezoidal product rule on dF, implicit in M_i: second order, right on a coarse grid
def trap_dF(T, h):
    n = int(round(T/h)); t = np.linspace(0, T, n+1); Fv = F(t); dF = np.diff(Fv); M = np.zeros(n+1)
    for i in range(1, n+1):
        acc = sum(dF[j-1]*(M[i-j] + M[i-j+1])/2 for j in range(2, i+1))
        M[i] = (Fv[i] + acc + dF[0]*M[i-1]/2) / (1 - dF[0]/2)
    return M[-1]
print("Scheme comparison, trapezoidal product rule on dF (second order, implicit):")
for h in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
    v = trap_dF(T, h); print(f"   h = {h:<6}: M({T:g}) = {v:.4f}  {verdict(v)}")
print("   Even this second-order scheme needs h = 0.0625 before it rounds to 2.705, so no scheme survives a")
print("   single coarse run: the step has to be refined or two steps extrapolated.")

# Midpoint / lattice rule: converges to the same limit from ABOVE, and a coarse Richardson step overshoots
def midpoint(T, h):
    n = int(round(T/h))
    q0 = F(h/2); q = [F(j*h + h/2) - F(j*h - h/2) for j in range(1, n+1)]
    G = [F(j*h + h/2) for j in range(0, n+1)]
    M = np.zeros(n+1)
    for j in range(1, n+1):
        M[j] = (G[j] + sum(q[i-1]*M[j-i] for i in range(1, j+1))) / (1 - q0)
    return M[-1]
print("Midpoint / lattice rule (converges from above):")
mv = {}
for h in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
    mv[h] = midpoint(T, h)
    print(f"   h = {h:<7}: M({T:g}) = {mv[h]:.4f}  {verdict(mv[h])}")
rich = mv[0.5] + (mv[0.5]-mv[1.0])/3
print(f"   Richardson on its two coarsest values overshoots: {rich:.4f}  {verdict(rich)}")
print("   The schemes straddle the answer, and only a well refined or correctly extrapolated one rounds to 2.705.")

print("Discretisation trap, discrete renewal recursion with right-endpoint cell masses:")
prev = None
for h in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
    v = lotka(T, h)
    extra = f"   Richardson with the previous step: {2*v-prev:.4f}  {verdict(2*v-prev)}" if prev is not None else ""
    print(f"   h = {h:<7}: M({T:g}) = {v:.4f}  {verdict(v)}{extra}")
    prev = v
print("   The scheme converges from below at first order: no step down to 0.03125 rounds to 2.705, and")
print("   of the Richardson pairs only (0.0625, 0.03125) does; the earlier pairs stop at 2.700 and 2.704.")

# The rounding trap: forcing k to the round value 3
k3, l3 = 3.0, 4.0**(1/3)
S3 = lambda t: 1.0/(1.0 + (t/l3)**k3)
print(f"Rounding trap: with k = 3 and lambda = 4^(1/3) = {l3:.4f}, S(6) = {S3(6):.6f} against the drawn 0.0200")
print(f"   (nine per cent low) and S(10) = {S3(10):.6f} against the curve's {1/(1+(10/lam)**k):.6f}.")
def M_params(kk, ll, T, n=4000):
    Fx = lambda t: 1.0 - 1.0/(1.0 + (t/ll)**kk)
    fx = lambda t: (kk/ll)*(t/ll)**(kk-1)/(1.0 + (t/ll)**kk)**2
    h = T/n; t = np.linspace(0, T, n+1); Fv = Fx(t); fv = fx(t); M = np.zeros(n+1)
    for i in range(1, n+1):
        w = np.full(i+1, h); w[0] = w[-1] = h/2
        M[i] = Fv[i] + np.dot(w[1:]*fv[1:i+1], M[i-1::-1])
    return M[-1]
mk3 = M_params(k3, l3, T); print(f"   That law would give M(6) = {mk3:.4f}  {verdict(mk3)}")
print("   The key is unchanged under honest rounding of the true parameters:")
for kk, ll in ((3.08, 1.696), (3.1, 1.70), (3.08, 1.70), (3.07, 1.70), (3.08, 1.69)):
    vv = M_params(kk, ll, T); print(f"      k = {kk}, lambda = {ll}: M(6) = {vv:.4f}  {verdict(vv)}")

print(f"Answer key: {M1:.6f}, which is {M1:.3f} at 3 decimals; the 3-decimal bin runs 2.7045 to 2.7055, so the key sits {M1-2.7045:.5f} above its lower edge")

# The shortcuts that do not work
m = lam * (math.pi/k) / math.sin(math.pi/k)
E2 = lam**2 * (2*math.pi/k) / math.sin(2*math.pi/k)
print(f"E[X] = {m:.5f}, E[X^2] = {E2:.5f} (both finite, r < k; the first divergent integer moment is the fourth)")
print(f"Wrong route: elementary renewal theorem alone, t/m = {T/m:.4f}  {verdict(T/m)}")
asy = T/m + (E2-2*m*m)/(2*m*m)
print(f"Wrong route: asymptotic expansion t/m + (E[X^2] - 2m^2)/(2m^2) = {asy:.4f}  {verdict(asy)}")
print(f"   (it is still 1.8 percent above the true value at t = {T:g}, because t is only about 3 mean gaps)")
print(f"Wrong route: t/m - 1/2 = {T/m - 0.5:.4f}  {verdict(T/m - 0.5)}")
print(f"Wrong route: F({T:g}) = {F(T):.4f}, the probability of at least one renewal, not their expected number")

def M_from(ta, Sa, tb, Sb):
    kk = math.log((1/Sb - 1) / (1/Sa - 1)) / math.log(tb / ta)
    ll = ta / (1/Sa - 1)**(1/kk)
    Sx = lambda t: 1.0/(1.0 + (t/ll)**kk)
    Fx = lambda t: 1.0 - Sx(t)
    fx = lambda t: (kk/ll) * (t/ll)**(kk-1) / (1.0 + (t/ll)**kk)**2
    n = 4000; h = T/n; t = np.linspace(0, T, n+1); Fv = Fx(t); fv = fx(t); M = np.zeros(n+1)
    for i in range(1, n+1):
        w = np.full(i+1, h); w[0] = w[-1] = h/2
        M[i] = Fv[i] + np.dot(w[1:]*fv[1:i+1], M[i-1::-1])
    return kk, M[-1]
print("Near-miss readings (the named crossing at 6 paired with a crossing the curve does not pass through):")
for b, Sb in [(8, 0.01), (10, 0.005), (15, 0.001), (30, 0.0002), (4, 0.05), (3, 0.2), (2, 0.5), (10, 0.004), (2, 0.4)]:
    kk, v = M_from(6, 0.02, b, Sb)
    print(f"   (6, 0.02) with ({b:g}, {Sb:g}): k = {kk:.3f}, M({T:g}) = {v:.4f}  {verdict(v)}")
