import numpy as np, json, knotlib as K, torus_curve as T, sys
word = [1,1,1,-2,-1,-1,-1,-2]
seed, wob = int(sys.argv[1]), float(sys.argv[2]); c0 = np.array(json.loads(sys.argv[3])); ntr = int(sys.argv[4])
sm = T.torus_closure(word, wobble=wob, seed=seed, n=700)
rng = np.random.default_rng(11)
rows = []
for trial in range(ntr):
    ang = c0 + rng.normal(0, 0.25, 3) if trial else c0
    Q = sm @ K.rotmat(*ang).T
    D = K.diagram(Q); span = np.ptp(Q[:, :2], axis=0).max()
    if 11 <= D["n"] <= 13:
        rows.append(dict(n=D["n"], mindist=round(float(D["mindist"] / span), 3), minangle=round(float(D["minangle"]), 1), mindz=round(float(D["mindz"]), 3), ang=[float(a) for a in ang], seed=seed, wob=wob))
rows.sort(key=lambda q: -(min(q["mindist"], 0.09) * min(q["minangle"], 45) * min(q["mindz"], 0.3)))
for q in rows[:6]: print(q)
json.dump(rows[:20], open(f"refine_{seed}_{wob}.json", "w"))
