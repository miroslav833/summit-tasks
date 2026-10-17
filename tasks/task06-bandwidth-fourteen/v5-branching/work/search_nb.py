"""Negative-binomial offspring f(s) = (1 + (m/r)(1-s))^(-r): find (m, r) whose curve passes exactly through two
gridline crossings at labelled s in {0, 0.1, ..., 0.9} (gridlines every 0.1 on both axes) and stays at least
`gap` away from every horizontal gridline at all other labelled s. Supercritical (m > 1). Report q, f'(q) and the
key 1/(1 - f'(q)) (expected total progeny given extinction), plus the answers from every near-miss pair."""
import itertools, math
from scipy.optimize import brentq, fsolve
S = [round(0.1*i, 1) for i in range(10)]; Y = [round(0.1*j, 1) for j in range(1, 10)]
def f(s, m, r): return (1 + (m/r)*(1-s))**(-r)
def fp(s, m, r): return m*(1 + (m/r)*(1-s))**(-r-1)
def solve_pair(p1, p2):
    (s1, y1), (s2, y2) = p1, p2
    def eqs(x):
        m, lr = x; r = math.exp(lr); return [f(s1, m, r) - y1, f(s2, m, r) - y2]
    sols = set()
    for m0 in (1.2, 1.6, 2.2, 3.0, 4.5):
        for lr0 in (-1.5, -0.5, 0.5, 1.5, 2.5):
            try:
                x, info, ier, _ = fsolve(eqs, [m0, lr0], full_output=True)
                if ier == 1 and max(abs(v) for v in eqs(x)) < 1e-12 and x[0] > 0: sols.add((round(x[0], 9), round(math.exp(x[1]), 9)))
            except Exception: pass
    return sols
def key(m, r):
    q = brentq(lambda s: f(s, m, r) - s, 0.0, 1 - 1e-9 if m > 1 else 0.5) if m > 1 else None
    d = fp(q, m, r); return q, d, 1/(1-d)
res = []
pts = [(s, y) for s in S for y in Y]
for p1, p2 in itertools.combinations(pts, 2):
    if p1[0] == p2[0] or not (p1[0] < p2[0] and p1[1] < p2[1]): continue
    for m, r in solve_pair(p1, p2):
        if m <= 1.15 or m > 4 or r < 0.3 or r > 30: continue
        try: q, d, K = key(m, r)
        except Exception: continue
        if not (0.15 < q < 0.85): continue
        gaps = []
        for s in S:
            if s in (p1[0], p2[0]): continue
            v = f(s, m, r); gaps.append(min(abs(v - y) for y in [0.0] + Y + [1.0]))
        res.append((min(gaps), p1, p2, m, r, q, d, K))
res.sort(reverse=True)
for g, p1, p2, m, r, q, d, K in res[:25]:
    print(f"gap {g:.4f}  crossings {p1} {p2}  m={m:.4f} r={r:.4f}  q={q:.4f} f'(q)={d:.4f}  key={K:.4f}  naive 1/(1-m)={1/(1-m):.2f}")
