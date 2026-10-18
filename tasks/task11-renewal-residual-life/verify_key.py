# Variance of the number of renewals by time t = 3 for a renewal process with log-logistic inter-arrival
# times, the parameters taken from two gridline crossings of the drawn survival function.
# Run: python3 verify_key.py   (needs numpy)
import math
import numpy as np

# Step 1: the two gridline crossings the curve passes through, and the parameters they fix
t1, S1 = 6.0, 0.02
t2, S2 = 20.0, 0.0005
k = math.log((1/S2 - 1) / (1/S1 - 1)) / math.log(t2 / t1)
lam = t1 / (1/S1 - 1)**(1/k)
print(f"k = {k:.6f}, lambda = {lam:.6f}")
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

T = 3.0
KEY3 = "0.520"
def verdict(v):
    r = f"{v:.3f}"
    return "rounds to 0.520" if r == KEY3 else f"rounds to {r}, wrong"

def laws(kk, ll):
    F = lambda t: 1.0 - 1.0/(1.0 + (t/ll)**kk)
    f = lambda t: (kk/ll)*(t/ll)**(kk-1)/(1.0 + (t/ll)**kk)**2
    return F, f

# Route 1: renewal function M = F + M*f by product integration, then E[N^2] = M + 2 (M * dM)
def var_route1(kk, ll, n):
    F, f = laws(kk, ll)
    h = T/n; t = np.linspace(0, T, n+1); Fv = F(t); fv = f(t); M = np.zeros(n+1)
    for i in range(1, n+1):
        w = np.full(i+1, h); w[0] = w[-1] = h/2
        M[i] = Fv[i] + np.dot(w[1:]*fv[1:i+1], M[i-1::-1])
    m = np.gradient(M, h); w = np.full(n+1, h); w[0] = w[-1] = h/2
    EN2 = M[-1] + 2*np.dot(w*m, M[::-1])
    return EN2 - M[-1]**2, M[-1], EN2
# Route 2: convolution series P(N >= n) = F_n(T), E[N] = sum F_n, E[N^2] = sum (2n - 1) F_n
def var_route2(n=6000, jmax=12):
    F, f = laws(k, lam)
    h = T/n; t = np.linspace(0, T, n+1); fv = f(t)
    dens = fv.copy(); Fn = []
    for j in range(1, jmax+1):
        w = np.full(n+1, h); w[0] = w[-1] = h/2
        Fn.append(float(np.dot(w, dens)))
        new = np.zeros(n+1)
        for i in range(1, n+1):
            wi = np.full(i+1, h); wi[0] = wi[-1] = h/2
            new[i] = np.dot(wi[1:]*fv[1:i+1], dens[i-1::-1])
        dens = new
    EN = sum(Fn); EN2 = sum((2*j+1)*x for j, x in enumerate(Fn))
    return EN2 - EN**2, EN, EN2, Fn

for n in (1000, 2000, 4000, 8000):
    v, M3, EN2 = var_route1(k, lam, n)
    print(f"Route 1, renewal equation and E[N^2] = M + 2 M*dM on {n:5d} intervals: Var = {v:.6f}  {verdict(v)}  (M = {M3:.6f})")
V1, M3, EN2 = var_route1(k, lam, 8000)
V2, EN, EN2b, Fn = var_route2()
print("Route 2, convolution series: F_n(3) = " + ", ".join(f"{x:.6f}" for x in Fn[:6]))
print(f"   E[N] = {EN:.6f}, E[N^2] = sum (2n-1) F_n = {EN2b:.6f}, Var = {V2:.6f}  {verdict(V2)}")
rng = np.random.default_rng(20261018)
N = 1_000_000
cnt = np.zeros(N, dtype=np.int64); s = np.zeros(N)
for _ in range(30):
    U = rng.random(N); s += lam*(U/(1-U))**(1/k); cnt += (s <= T)
mv = cnt.mean(); vv = cnt.var(ddof=1)
se = math.sqrt(((cnt - mv)**4).mean() - vv**2) / math.sqrt(N)
print(f"Route 3, simulation of {N} paths: E[N] = {mv:.4f}, Var = {vv:.4f} (standard error {se:.4f})")

print("Discretisation trap, the variance by the coupled trapezoid scheme on dF (M = F + M*dF, A = M + A*dF, Var = 2A - M - M^2):")
def coupled(h):
    F, _ = laws(k, lam)
    n = int(round(T/h)); t = np.linspace(0, T, n+1); Fv = F(t); d = np.diff(Fv)
    M = np.zeros(n+1); A = np.zeros(n+1)
    for i in range(1, n+1):
        aM = sum(d[j-1]*(M[i-j] + M[i-j+1])/2 for j in range(2, i+1))
        M[i] = (Fv[i] + aM + d[0]*M[i-1]/2) / (1 - d[0]/2)
        aA = sum(d[j-1]*(A[i-j] + A[i-j+1])/2 for j in range(2, i+1))
        A[i] = (M[i] + aA + d[0]*A[i-1]/2) / (1 - d[0]/2)
    return 2*A[-1] - M[-1] - M[-1]**2
cv = {}
for h in (0.75, 0.5, 0.25, 0.125, 0.0625):
    cv[h] = coupled(h); print(f"   h = {h:<7}: Var = {cv[h]:.5f}  {verdict(cv[h])}")
for a, b in ((0.5, 0.25), (0.25, 0.125), (0.125, 0.0625)):
    r = (4*cv[b] - cv[a])/3; print(f"   Richardson (second order) on ({a}, {b}): {r:.5f}  {verdict(r)}")

print("Midpoint lattice convolution (each cell's mass at its midpoint), the variance from sum (2n-1) F_n:")
def midpoint_var(h):
    F, _ = laws(k, lam)
    n = int(round(T/h)); p = np.array([F((j+1)*h) - F(j*h) for j in range(n)])   # mass of cell j, placed at (j+1/2)h
    # distribution of S_n on the half-integer lattice; P(S_n <= T) counts sums whose position <= T
    G = []; cur = p.copy(); off = 1   # positions (j + off/2) h
    for nn in range(1, 8):
        pos = (np.arange(len(cur)) + nn*0.5)*h
        G.append(float(cur[pos <= T + 1e-12].sum()) + 0.5*float(cur[np.isclose(pos, T)].sum())*0)
        cur = np.convolve(cur, p)
    EN = sum(G); EN2 = sum((2*j+1)*x for j, x in enumerate(G))
    return EN2 - EN**2
for h in (0.5, 0.25, 0.125):
    v = midpoint_var(h); print(f"   h = {h:<6}: Var = {v:.5f}  {verdict(v)}")

print("Parameter rounding:")
for kk, ll, tag in ((3.0803, 1.6960, "5 significant figures"), (3.080, 1.696, "4 significant figures"),
                    (3.08, 1.70, "3 significant figures"), (3.0, 4**(1/3), "k forced to 3")):
    v, _, _ = var_route1(kk, ll, 4000); print(f"   {tag:22s} k = {kk:.4f}, lambda = {ll:.4f}: Var = {v:.6f}  {verdict(v)}")

m = lam*(math.pi/k)/math.sin(math.pi/k); E2 = lam**2*(2*math.pi/k)/math.sin(2*math.pi/k); s2 = E2 - m*m
F, _ = laws(k, lam); F3 = F(T)
print(f"E[X] = {m:.5f}, Var X = {s2:.5f}")
print("Wrong routes:")
print(f"   Poisson guess Var = E[N] = {M3:.4f}  {verdict(M3)}")
print(f"   asymptotic sigma^2 t / mu^3 = {s2*T/m**3:.4f}  {verdict(s2*T/m**3)}")
print(f"   E[N^2] without subtracting E[N]^2 = {EN2:.4f}  {verdict(EN2)}")
print(f"   E[N^2] = M + 2 (M * dF) instead of M + 2 (M * dM): Var = {M3 + 2*(M3 - F3) - M3**2:.4f}  {verdict(M3 + 2*(M3 - F3) - M3**2)}")
print(f"   E[N^2] = sum n F_n instead of sum (2n - 1) F_n: Var = {EN - EN**2:.4f}  {verdict(EN - EN**2)}")
print(f"   Bernoulli guess F(3) (1 - F(3)) = {F3*(1-F3):.4f}  {verdict(F3*(1-F3))}")
print(f"Answer key: Var[N(3)] = {V1:.6f}, which is {V1:.3f} at 3 decimals; the bin runs 0.5195 to 0.5205, so the key sits {0.5205-V1:.5f} below its upper edge")
