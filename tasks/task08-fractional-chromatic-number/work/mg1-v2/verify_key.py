# M/G/1 queue with Weibull service times read from a plot: standard deviation of the steady-state waiting time.
# Run: python3 verify_key.py (needs numpy and scipy)
import math, itertools, numpy as np
from scipy.integrate import quad
G = math.gamma
LAM = 0.25                       # Poisson arrival rate, given in the question
LAB = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]
LINES = sorted(c * 10.0**e for e in range(-5, 1) for c in (1, 2, 5))

# Step 1: the two gridline crossings fix eta and beta, since ln(1/S(t)) = (t/eta)^beta
t1, S1, t2, S2 = 2.5, 0.5, 10.0, 0.002
def fit(ta, Sa, tb, Sb):
    b = math.log(math.log(1/Sb) / math.log(1/Sa)) / math.log(tb/ta)
    return ta / math.log(1/Sa)**(1/b), b
eta, beta = fit(t1, S1, t2, S2)
S = lambda t: math.exp(-(t/eta)**beta)
print(f"beta = {beta:.5f}, eta = {eta:.5f}; check S({t1:g}) = {S(t1):.5f}, S({t2:g}) = {S(t2):.6f}")
print("curve at every labelled t inside the frame (lines at 1, 2, 5 of each decade, frame 1e-4 to 1):")
for t in LAB:
    y = S(t)
    if y < 1e-4: print(f"   t = {t:4g}: S = {y:.2e}, below the frame"); continue
    v = min(LINES, key=lambda v: abs(math.log(y/v)))
    print(f"   t = {t:4g}: S = {y:.4g}, nearest line {v:g}, off by {max(y/v, v/y)*100-100:.1f} percent")

# Step 2: the key by the Takacs moment formulas
def key(eta, beta, lam=LAM, full=False):
    m1, m2, m3 = (eta**n * G(1 + n/beta) for n in (1, 2, 3))
    rho = lam * m1
    if rho >= 1: return math.inf
    w1 = lam * m2 / (2 * (1 - rho))
    w2 = 2 * w1 * w1 + lam * m3 / (3 * (1 - rho))
    out = math.sqrt(w2 - w1 * w1)
    return (out, m1, m2, m3, rho, w1, w2) if full else out
sd, m1, m2, m3, rho, w1, w2 = key(eta, beta, full=True)
print(f"Route 1, Gamma-function moments: E[S] = {m1:.5f}, E[S^2] = {m2:.5f}, E[S^3] = {m3:.5f}, rho = {rho:.5f}")
print(f"   E[W] = {w1:.5f}, E[W^2] = {w2:.5f}, Var W = {w2 - w1*w1:.5f}, sd W = {sd:.5f}")

# Route 2: moments by quadrature of the survival function, E[S^n] = n int t^(n-1) S(t) dt
q = [n * quad(lambda t: t**(n-1) * S(t), 0, np.inf, limit=500)[0] for n in (1, 2, 3)]
r2 = LAM * q[0]; a = LAM*q[1]/(2*(1-r2)); b = 2*a*a + LAM*q[2]/(3*(1-r2))
print(f"Route 2, quadrature: E[S^n] = {q[0]:.5f}, {q[1]:.5f}, {q[2]:.5f}, sd W = {math.sqrt(b - a*a):.5f}")

# Route 3: Pollaczek-Khinchine as a geometric sum. W = R_1 + ... + R_N with P(N = n) = (1 - rho) rho^n and R_i
# i.i.d. with the equilibrium density S(t)/E[S]; Var W = E[N] Var R + Var N E[R]^2
ER = quad(lambda t: t * S(t), 0, np.inf, limit=500)[0] / q[0]
ER2 = quad(lambda t: t * t * S(t), 0, np.inf, limit=500)[0] / q[0]
EN = r2 / (1 - r2); VN = r2 / (1 - r2)**2
print(f"Route 3, geometric sum of equilibrium residuals: E[R] = {ER:.5f}, E[R^2] = {ER2:.5f}, E[W] = {EN*ER:.5f}, "
      f"sd W = {math.sqrt(EN*(ER2 - ER*ER) + VN*ER*ER):.5f}")

# Route 4: simulation of the Lindley recursion W_{n+1} = max(0, W_n + S_n - A_n), in batches
rng = np.random.default_rng(20261017)
sds = []
for batch in range(20):
    n = 2_000_000
    x = eta * rng.weibull(beta, n) - rng.exponential(1/LAM, n)
    U = np.concatenate(([0.0], np.cumsum(x)))
    W = U - np.minimum.accumulate(U)
    sds.append(W[200_000:].std())
sds = np.array(sds)
print(f"Route 4, Lindley simulation (20 batches of 2e6 customers): sd W = {sds.mean():.3f} +/- {sds.std()/math.sqrt(len(sds)):.3f}")
print(f"Answer key: {sd:.4f}, two significant figures {float(f'{sd:.2g}')}")

# Wrong routes
print(f"Wrong: sd W taken equal to E[W] (exponential waiting time) = {w1:.3f}")
print(f"Wrong: M/M/1 with the same mean, sd of the queueing delay = {math.sqrt(rho*(2-rho))*m1/(1-rho):.3f}")
print(f"Wrong: E[W^2] without the factor 2, sd = {math.sqrt(max(w1*w1 + LAM*m3/(3*(1-rho)) - w1*w1, 0)):.3f}")
print(f"Wrong: sd of the sojourn time W + S instead = {math.sqrt(w2 - w1*w1 + m2 - m1*m1):.3f}")

# Every pair of labelled abscissae read at the nearest gridline, the two true crossings kept
pts = {}
for t in LAB:
    y = S(t)
    if 1e-4 <= y <= 0.95: pts[t] = min(LINES, key=lambda v: abs(math.log(y/v)))
pts[t1], pts[t2] = S1, S2
print("Near-miss readings (each pair of labelled t at the nearest line):")
for ta, tb in itertools.combinations(sorted(pts), 2):
    if (ta, tb) == (t1, t2) or pts[tb] >= pts[ta] or pts[ta] >= 1: continue
    e, b_ = fit(ta, pts[ta], tb, pts[tb])
    k = key(e, b_)
    tag = "unstable, rho >= 1" if not math.isfinite(k) else f"sd W = {k:.4g} -> {float(f'{k:.2g}')}"
    print(f"   ({ta:g}, {pts[ta]:g}) with ({tb:g}, {pts[tb]:g}): beta = {b_:.3f}, eta = {e:.3f}, {tag}")
