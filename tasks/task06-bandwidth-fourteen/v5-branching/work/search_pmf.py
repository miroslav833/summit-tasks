"""Offspring pmf of a negative binomial (shape r, mean m) plotted on a log axis with 1-2-5 gridlines, k = 0..12.
Find (m, r) with exactly two points on gridline values and every other point at least DELTA (log ratio) from any
gridline value; key = 1/(1 - f'(q)). Scan rule: no single wrong pair (exact point + nearest-gridline reading of
another point) may give an answer that rounds to the key at two significant figures."""
import math, itertools
from scipy.optimize import brentq
K = list(range(13)); GL = sorted(c * 10.0 ** e for e in range(-6, 1) for c in (1, 2, 5) if c * 10.0 ** e <= 1)
def pmf(m, r):
    p = [(r / (r + m)) ** r]
    for k in range(1, 13): p.append(p[-1] * (r + k - 1) / k * (m / (r + m)))
    return p
def f(s, m, r): return (1 + (m / r) * (1 - s)) ** (-r)
def fp(s, m, r): return m * (1 + (m / r) * (1 - s)) ** (-r - 1)
def key(m, r):
    q = brentq(lambda s: f(s, m, r) - s, 1e-12, 1 - 1e-9); return q, fp(q, m, r), 1 / (1 - fp(q, m, r))
def logdist(v): return min(abs(math.log(v / g)) for g in GL)
def nearest(v): return min(GL, key=lambda g: abs(math.log(v / g)))
def fit(k1, y1, k2, y2):
    """solve pmf(m, r)[k1] = y1 and [k2] = y2 by a scan in r with bisection in m"""
    out = []
    def m_for(r, k, y):
        g = lambda m: pmf(m, r)[k] - y
        # pmf at k as a function of m is unimodal for k >= 1, decreasing for k = 0; scan for sign changes
        ms = [0.05 * 1.07 ** i for i in range(90)]; roots = []
        for a, b in zip(ms, ms[1:]):
            try:
                if g(a) * g(b) < 0: roots.append(brentq(g, a, b))
            except Exception: pass
        return roots
    rs = [0.15 * 1.05 ** i for i in range(80)]
    prev = {}
    for r in rs:
        for m in m_for(r, k1, y1):
            val = pmf(m, r)[k2] - y2; out.append((r, m, val))
    sols = []
    out.sort()
    for (r1, m1, v1), (r2, m2, v2) in zip(out, out[1:]):
        if v1 * v2 < 0 and abs(m1 - m2) < 0.3 * max(m1, m2):
            # refine by bisection in r along the branch
            a, b = r1, r2
            for _ in range(60):
                c = 0.5 * (a + b); ms = [m for m in m_for(c, k1, y1) if abs(m - m1) < 0.3 * max(m1, m2)]
                if not ms: break
                vc = pmf(ms[0], c)[k2] - y2
                if (vc > 0) == (v1 > 0): a, v1 = c, vc
                else: b = c
            ms = [m for m in m_for(0.5 * (a + b), k1, y1) if abs(m - m1) < 0.3 * max(m1, m2)]
            if ms: sols.append((ms[0], 0.5 * (a + b)))
    return sols
if __name__ == "__main__":
    import sys
    DELTA = 0.07
    res = []
    pairs = [(k1, k2) for k1 in (0, 1, 2) for k2 in range(k1 + 2, 13)]
    for k1, k2 in pairs:
        for y1 in [g for g in GL if 0.05 <= g <= 0.5]:
            for y2 in [g for g in GL if 1e-5 <= g < y1]:
                for m, r in fit(k1, y1, k2, y2):
                    if not (1.3 < m < 4 and 0.3 < r < 6): continue
                    p = pmf(m, r)
                    if any(v < 1e-6 for v in p): continue
                    others = [logdist(p[k]) for k in K if k not in (k1, k2)]
                    if min(others) < DELTA: continue
                    q, d, Kk = key(m, r)
                    if not (0.15 < q < 0.85): continue
                    res.append((min(others), k1, y1, k2, y2, m, r, q, d, Kk))
    res.sort(reverse=True)
    print(len(res), "candidates")
    for row in res[:30]:
        g, k1, y1, k2, y2, m, r, q, d, Kk = row
        print(f"gap {g:.3f} (log)  exact p{k1}={y1:g} p{k2}={y2:g}  m={m:.4f} r={r:.4f} q={q:.4f} f'(q)={d:.4f} key={Kk:.4f}")
    import pickle; pickle.dump(res, open("pmf_cands.pkl", "wb"))
