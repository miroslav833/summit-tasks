import itertools, math, warnings
warnings.filterwarnings("ignore")
from search_nb import *
def near_misses(m, r, true_pts, tol=0.035):
    """readings a solver could mistake for crossings: at each labelled s the nearest gridline value, if within tol"""
    out = []
    for s in S:
        v = f(s, m, r); y = min(Y, key=lambda y: abs(v - y))
        if (s, y) in true_pts: continue
        if abs(v - y) <= tol: out.append((s, y, abs(v - y)))
    return out
def answer_from(p1, p2):
    outs = []
    for m, r in solve_pair(p1, p2):
        if m <= 1.0 or r <= 0: continue
        try: q, d, K = key(m, r); outs.append(K)
        except Exception: pass
    return outs
good = []
for g, p1, p2, m, r, q, d, K in res:
    if g < 0.012: continue
    if min(abs(q - y) for y in [0.1*i for i in range(11)]) < 0.03: continue        # q would sit on a gridline
    true = {p1, p2}; nm = near_misses(m, r, true)
    cands = [(s, y) for s, y, _ in nm] + list(true)
    collide = []; wrong = []
    for a, b in itertools.combinations(cands, 2):
        if {a, b} == true or a[0] == b[0]: continue
        for K2 in answer_from(a, b):
            wrong.append((a, b, round(K2, 3)))
            if round(K2, 1) == round(K, 1): collide.append((a, b, round(K2, 3)))
    good.append((len(collide), g, p1, p2, m, r, q, d, K, nm, collide, wrong))
good.sort(key=lambda x: (x[0], -x[1]))
for c, g, p1, p2, m, r, q, d, K, nm, collide, wrong in good[:8]:
    print(f"collisions {c} gap {g:.4f} true {p1} {p2} m={m:.4f} r={r:.4f} q={q:.4f} f'(q)={d:.4f} key={K:.4f} -> {round(K,1)}")
    print("    near misses:", [(s, y, round(e, 3)) for s, y, e in nm])
    print("    wrong-pair answers:", sorted(set(w[2] for w in wrong))[:20])
    if collide: print("    COLLIDING:", collide[:5])
