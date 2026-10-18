import math, itertools
from scipy.optimize import brentq
from ruin import lomax_sf, psi_extrap, shortcuts
T = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100]
GL = [c * 10.0 ** e for e in range(-5, 1) for c in (1, 2, 5) if c * 10.0 ** e <= 1]
def fit(t1, y1, t2, y2):
    # a ln(1 + t/s) = -ln y; ratio eliminates a: ln(1+t1/s)/ln(1+t2/s) = ln y1 / ln y2
    R = math.log(y1) / math.log(y2)
    g = lambda ls: math.log(1 + t1 / math.exp(ls)) / math.log(1 + t2 / math.exp(ls)) - R
    out = []
    grid = [x / 10 for x in range(-40, 61)]
    for a_, b_ in zip(grid, grid[1:]):
        if g(a_) * g(b_) < 0:
            s = math.exp(brentq(g, a_, b_)); a = -math.log(y1) / math.log(1 + t1 / s); out.append((s, a))
    return out
def logdist(v): return min(abs(math.log10(v / g)) for g in GL)
res = []
for (t1, t2) in itertools.combinations(T, 2):
    for y1 in GL:
        for y2 in GL:
            if y2 >= y1 or y1 > 0.5: continue
            for s, a in fit(t1, y1, t2, y2):
                if not (2.6 < a < 4.2 and 0.8 < s < 12): continue
                vis = [t for t in T if lomax_sf(t, s, a) > 1e-4 and t not in (t1, t2)]
                if len(vis) < 7: continue
                gap = min(logdist(lomax_sf(t, s, a)) for t in vis)
                if gap < 0.06: continue                     # at least 0.06 decade (15 percent) off every gridline
                if abs(a - round(a)) < 0.08 or abs(a * 2 - round(a * 2)) < 0.05: continue   # not a round shape
                res.append((gap, t1, y1, t2, y2, s, a))
res.sort(reverse=True)
for r in res[:15]: print("gap %.3f  crossings (%g, %g) (%g, %g)  s=%.4f a=%.4f" % r)
import pickle; pickle.dump(res, open("cands.pkl", "wb"))
