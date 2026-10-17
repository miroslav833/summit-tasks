"""Verification of the answer key: E[T | extinction] = 1.9 (two significant figures; 1.911 to four) for the
Galton-Watson process in the figure.

Run: python3 verify_key.py   (needs numpy and scipy only for the cross-checks; the main route is plain python)
  (1) parameters: f(0) = (1 + m/r)^(-r) = 0.4 and f(0.4) = (1 + 0.6 m/r)^(-r) = 0.5, solved by bisection on r;
      the curve is checked against every other labelled s (distance to the nearest gridline printed);
  (2) extinction probability q: the root of f(s) = s in (0, 1), by bisection;
  (3) route A, closed form: conditioned on extinction the process is a Galton-Watson process with offspring
      generating function f(q s)/q, subcritical with mean f'(q), so E[T | extinction] = 1/(1 - f'(q));
  (4) route B, independent: the generating function of T solves G(s) = s f(G(s)); P(T = n, extinction) are its
      coefficients (Lagrange inversion: P(T = n) = (1/n) [z^(n-1)] f(z)^n), summed as sum n P(T=n) / sum P(T=n);
  (5) route C, Monte Carlo: simulate the process, keep the runs that die out, average T;
  (6) the answers from the near-miss readings (a solver who takes a wrong second crossing).
"""
import math, random
def f(s, m, r): return (1 + (m / r) * (1 - s)) ** (-r)
def fp(s, m, r): return m * (1 + (m / r) * (1 - s)) ** (-r - 1)
def bisect(g, a, b, it=200):
    ga = g(a)
    for _ in range(it):
        c = 0.5 * (a + b); gc = g(c)
        if (gc > 0) == (ga > 0): a, ga = c, gc
        else: b = c
    return 0.5 * (a + b)
def fit(p1, p2):
    """negative binomial through (s1, y1) and (s2, y2): for each r the first point fixes m; bisect r on the second"""
    (s1, y1), (s2, y2) = p1, p2
    def m_of(r): return r * (y1 ** (-1 / r) - 1) / (1 - s1)
    def g(lr): r = math.exp(lr); return f(s2, m_of(r), r) - y2
    grid = [x / 20 for x in range(-80, 81)]; out = []
    for a, b in zip(grid, grid[1:]):
        if g(a) * g(b) < 0:
            lr = bisect(g, a, b); r = math.exp(lr); out.append((m_of(r), r))
    return out

# ---------- (1) parameters ----------
(m, r), = fit((0.0, 0.4), (0.4, 0.5))
print(f"(1) parameters from the crossings (0, 0.4) and (0.4, 0.5): m = {m:.8f}, r = {r:.8f}")
grid = [round(0.1 * j, 1) for j in range(11)]
for i in range(11):
    s = round(0.1 * i, 1); v = f(s, m, r); y = min(grid, key=lambda y: abs(v - y))
    print(f"    s = {s:.1f}: f(s) = {v:.5f}, nearest gridline {y:.1f}, distance {abs(v - y):.5f}" + ("  <- exact crossing" if abs(v - y) < 1e-9 and s < 1 else ""))
assert abs(f(0.0, m, r) - 0.4) < 1e-12 and abs(f(0.4, m, r) - 0.5) < 1e-12

# ---------- (2) extinction probability ----------
q = bisect(lambda s: f(s, m, r) - s, 0.0, 0.99)
print(f"\n(2) mean m = {m:.6f} > 1, so the process is supercritical; extinction probability q = {q:.8f} (f(q) - q = {f(q, m, r) - q:.1e})")

# ---------- (3) route A ----------
d = fp(q, m, r); A = 1 / (1 - d)
print(f"\n(3) route A: f'(q) = {d:.8f}, E[T | extinction] = 1/(1 - f'(q)) = {A:.8f}")

# ---------- (4) route B ----------
# offspring probabilities of the negative binomial: p_k = C(r+k-1, k) (r/(r+m))^r (m/(r+m))^k
N = 4000; p0 = (r / (r + m)) ** r; ratio = m / (r + m)
p = [p0]
for k in range(1, N): p.append(p[-1] * (r + k - 1) / k * ratio)
# P(T = n) = (1/n) [z^(n-1)] f(z)^n; compute by the recursion on h_n(z) = f(z)^n is costly, so use the equivalent
# branching recursion: T = 1 + sum of T_i over X children; P(T = n) via the convolution powers of the law of T.
M = 400                                  # T up to 400 carries all but a negligible part of the extinct mass
P = [0.0] * (M + 1)                      # P[n] = P(T = n)
# Lagrange: P(T = n) = (1/n) * coefficient of z^(n-1) in f(z)^n. Compute f(z)^n coefficients up to degree n-1 by
# repeated multiplication on the fly using the log-derivative recursion for powers of a power series.
def power_coeffs(n, deg):
    """coefficients a_0..a_deg of f(z)^n, f(z) = sum p_k z^k, by the J.C.P. Miller recursion"""
    a = [0.0] * (deg + 1); a[0] = p[0] ** n
    for k in range(1, deg + 1):
        acc = 0.0
        for j in range(1, k + 1): acc += (n * j - k + j) * p[j] * a[k - j]
        a[k] = acc / (k * p[0])
    return a
for n in range(1, M + 1):
    P[n] = power_coeffs(n, n - 1)[n - 1] / n
mass = sum(P); mean_T = sum(n * P[n] for n in range(M + 1)) / mass
print(f"\n(4) route B (Lagrange inversion, T up to {M}): P(extinction) = sum P(T = n) = {mass:.6f} (q = {q:.6f}); E[T | extinction] = {mean_T:.6f}")
assert abs(mass - q) < 1e-4 and abs(mean_T - A) < 1e-3

# ---------- (5) route C ----------
random.seed(12345)
import numpy as np
rng = np.random.default_rng(2026)
def sample_T(cap=2000):
    alive, total = 1, 1
    while alive:
        # negative binomial with shape r and mean m as a gamma-Poisson mixture
        kids = int(rng.poisson(rng.gamma(r, m / r, size=alive)).sum())
        total += kids; alive = kids
        if total > cap: return None
    return total
runs = 200000; ext = []
for _ in range(runs):
    t = sample_T()
    if t is not None: ext.append(t)
mc = sum(ext) / len(ext); se = (np.std(ext) / math.sqrt(len(ext)))
print(f"\n(5) route C (Monte Carlo, {runs} runs): extinct fraction {len(ext) / runs:.4f}; E[T | extinction] = {mc:.4f} +- {se:.4f}")
assert abs(mc - A) < 4 * se + 0.005

print(f"\nKEY: {A:.4f}, to two significant figures {A:.2g}")

# ---------- (6) near misses ----------
print("\n(6) answers a solver gets with a wrong second crossing (first crossing (0, 0.4) as stated):")
for s2 in [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9]:
    v = f(s2, m, r); y = min(grid[1:-1], key=lambda y: abs(v - y))
    for mm, rr in fit((0.0, 0.4), (s2, y)):
        if mm <= 1: print(f"    ({s2}, {y}): m = {mm:.3f} <= 1, extinction certain"); continue
        qq = bisect(lambda s: f(s, mm, rr) - s, 0.0, 0.999); dd = fp(qq, mm, rr)
        print(f"    ({s2}, {y}) [curve is {abs(v - y):.3f} off]: m = {mm:.3f}, r = {rr:.3f}, q = {qq:.3f}, answer {1 / (1 - dd):.3f}")
print(f"    forgetting to condition, E[T; extinction] = q/(1 - f'(q)) = {q * A:.3f}; the unconditional E[T] is infinite")
