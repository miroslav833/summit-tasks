import numpy as np, json, knotlib as K, torus2, sys
word = [1,1,1,-2,-1,-1,-1,-2]
seed, amp, ntr = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
sm = torus2.curve(word, seed, amp=amp, n=700)
# knot check from top view first
D0 = K.diagram(sm)
J = K.jones(D0["pd"], D0["writhe"]) if D0["n"] <= 14 else None
print("top n", D0["n"], "jones ok" if J == {-5:-1,-4:1,-3:-1,-2:2,-1:-1,0:2,1:-1} else ("jones DIFFERENT" if J else "too many to check"))
rng = np.random.default_rng(seed + 7)
rows = []
for trial in range(ntr):
    ang = np.array([rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), rng.uniform(-np.pi, np.pi)])
    Q = sm @ K.rotmat(*ang).T
    D = K.diagram(Q)
    if not (11 <= D["n"] <= 13): continue
    span = np.ptp(Q[:, :2], axis=0).max()
    rows.append(dict(n=D["n"], mindist=round(float(D["mindist"] / span), 3), minangle=round(float(D["minangle"]), 1), mindz=round(float(D["mindz"] / span), 3), ang=[float(a) for a in ang], seed=seed, amp=amp))
rows.sort(key=lambda q: -(min(q["mindist"], 0.09) * min(q["minangle"], 45) * min(q["mindz"], 0.06)))
print(len(rows), "candidates")
for q in rows[:5]: print(q)
json.dump(rows[:30], open(f"views5_{seed}_{amp}.json", "w"))
