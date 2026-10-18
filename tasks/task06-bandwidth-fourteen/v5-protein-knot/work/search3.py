import numpy as np, json, knotlib as K, torus_curve as T, sys, collections
word = [1,1,1,-2,-1,-1,-1,-2]
seed = int(sys.argv[1]); wob = float(sys.argv[2]); ntr = int(sys.argv[3])
sm = T.torus_closure(word, wobble=wob, seed=seed, n=700)
rng = np.random.default_rng(seed)
rows = []
for trial in range(ntr):
    ax, ay, az = rng.uniform(-np.pi, np.pi, 3)
    Q = sm @ K.rotmat(ax, ay, az).T
    D = K.diagram(Q)
    span = np.ptp(Q[:, :2], axis=0).max()
    rows.append(dict(n=D["n"], mindist=round(float(D["mindist"] / span), 3), minangle=round(float(D["minangle"]), 1), mindz=round(float(D["mindz"]), 3), ang=[float(ax), float(ay), float(az)], seed=seed, wob=wob))
print(sorted(collections.Counter(r["n"] for r in rows).items()))
good = [r for r in rows if 10 <= r["n"] <= 14]
good.sort(key=lambda q: -(min(q["mindist"], 0.08) * min(q["minangle"], 40) * min(q["mindz"], 0.25)))
for q in good[:8]: print(q)
json.dump(good[:40], open(f"views3_{seed}_{wob}.json", "w"))
