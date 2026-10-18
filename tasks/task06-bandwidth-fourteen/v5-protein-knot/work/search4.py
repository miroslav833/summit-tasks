import numpy as np, json, knotlib as K, torus_curve as T, sys, collections
word = [1,1,1,-2,-1,-1,-1,-2]
seed, wob, ntr = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
sm = T.torus_closure(word, wobble=wob, seed=seed, n=700)
rng = np.random.default_rng(seed + 100)
def curl(Q):
    """min radius of curvature of the projected curve, relative to span"""
    P = Q[:, :2]; span = np.ptp(P, axis=0).max()
    d1 = np.gradient(P, axis=0); d2 = np.gradient(d1, axis=0)
    num = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]); den = (d1 ** 2).sum(1) ** 1.5 + 1e-12
    kappa = num / den
    return (1 / (kappa.max() + 1e-12)) / span
rows = []
for trial in range(ntr):
    ang = rng.uniform(-np.pi, np.pi, 3)
    Q = sm @ K.rotmat(*ang).T
    D = K.diagram(Q)
    if not (11 <= D["n"] <= 13): continue
    span = np.ptp(Q[:, :2], axis=0).max()
    rows.append(dict(n=D["n"], mindist=round(float(D["mindist"] / span), 3), minangle=round(float(D["minangle"]), 1), mindz=round(float(D["mindz"] / span), 3), curl=round(float(curl(Q)), 3), ang=[float(a) for a in ang], seed=seed, wob=wob))
rows.sort(key=lambda q: -(min(q["mindist"], 0.09) * min(q["minangle"], 45) * min(q["mindz"], 0.06) * min(q["curl"], 0.04)))
for q in rows[:6]: print(q)
json.dump(rows[:30], open(f"views4_{seed}_{wob}.json", "w"))
