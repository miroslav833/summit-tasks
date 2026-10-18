"""Ruin probability psi(u) of the Cramer-Lundberg model with Lomax claims S(t) = (1 + t/s)^(-a), safety loading theta.
psi solves psi(u) = rho*Fbar_I(u) + rho * int_0^u psi(u-y) f_I(y) dy, rho = 1/(1+theta), I ~ Lomax(s, a-1)."""
import math, numpy as np
def lomax_sf(t, s, a): return (1 + t / s) ** (-a)
def psi_renewal(u, s, a, theta, h):
    """product integration on a grid of step h (trapezoid on the convolution with the exact cdf increments)"""
    rho = 1 / (1 + theta); b = a - 1
    n = int(round(u / h)); x = np.arange(n + 1) * h
    FI = 1 - lomax_sf(x, s, b)                 # cdf of I on the grid
    dF = np.diff(FI)                           # mass of I in each cell
    psi = np.zeros(n + 1); psi[0] = rho
    for k in range(1, n + 1):
        # int_0^{x_k} psi(x_k - y) dF_I(y) ~ sum_j dF_j * (psi(x_k - y_j) + psi(x_k - y_{j+1}))/2, the j = k-1 cell uses psi(0) and psi(h)? implicit
        j = np.arange(k)
        a1 = psi[k - j]; a2 = psi[k - j - 1]
        # the term with j = 0 involves psi[k] itself (implicit): dF_0 * (psi[k] + psi[k-1]) / 2
        rest = np.sum(dF[1:k] * (psi[k - j[1:]] + psi[k - j[1:] - 1]) / 2)
        rhs = rho * lomax_sf(x[k], s, b) + rho * (rest + dF[0] * psi[k - 1] / 2)
        psi[k] = rhs / (1 - rho * dF[0] / 2)
    return psi[-1]
def psi_extrap(u, s, a, theta):
    vals = [psi_renewal(u, s, a, theta, h) for h in (0.02, 0.01, 0.005)]
    # second-order Richardson on the last two
    return vals, (4 * vals[2] - vals[1]) / 3
def shortcuts(u, s, a, theta):
    rho = 1 / (1 + theta); mu = s / (a - 1)
    out = {}
    out["exponential claims, same mean"] = rho * math.exp(-(1 - rho) * u / mu)
    out["heavy-tail asymptotic"] = rho / (1 - rho) * lomax_sf(u, s, a - 1)
    if a > 3:
        m2 = 2 * s * s / ((a - 1) * (a - 2)); m3 = 6 * s ** 3 / ((a - 1) * (a - 2) * (a - 3))
        lam_c = 1.0                                   # De Vylder: match three moments of the surplus with exp claims
        # De Vylder: beta' = 3 m2/m3, lambda' = 9 lam m2^3 / (2 m3^2), c' = c - lam m1 + 3 lam m2^2/(2 m3)
        lam = 1.0; c = (1 + theta) * lam * mu
        bp = 3 * m2 / m3; lp = 9 * lam * m2 ** 3 / (2 * m3 ** 2); cp = c - lam * mu + 3 * lam * m2 ** 2 / (2 * m3)
        thp = cp * bp / lp - 1
        out["De Vylder"] = 1 / (1 + thp) * math.exp(-thp * bp * u / (1 + thp))
    return out
if __name__ == "__main__":
    s, a, theta = 2.0, 3.0, 0.25
    for u in (5, 10, 20):
        vals, ex = psi_extrap(u, s, a, theta); print(u, [round(v, 5) for v in vals], round(ex, 5), {k: round(v, 4) for k, v in shortcuts(u, s, a, theta).items()})
