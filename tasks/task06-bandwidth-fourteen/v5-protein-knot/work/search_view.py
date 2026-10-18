import numpy as np, json, knotlib as K, itertools
word = [1,1,1,-2,-1,-1,-1,-2]
pts = K.build_braid_curve(word, 3)
sm = K.smooth(pts, 1600)
ref = K.diagram(sm)
Jref = K.jones(ref["pd"], ref["writhe"])
print("reference n", ref["n"], K.jones_str(Jref))
best = []
rng = np.random.default_rng(1)
for trial in range(4000):
    ax, ay, az = rng.uniform(-np.pi, np.pi, 3)
    R = K.rotmat(ax, ay, az)
    Q = sm @ R.T
    D = K.diagram(Q)
    if not (11 <= D["n"] <= 13): continue
    span = np.ptp(Q[:, :2], axis=0).max()
    q = dict(n=D["n"], mindist=D["mindist"] / span, minangle=D["minangle"], mindz=D["mindz"], ang=(ax, ay, az))
    if q["mindist"] < 0.06 or q["minangle"] < 30 or q["mindz"] < 0.12: continue
    best.append(q)
best.sort(key=lambda q: -(q["mindist"] * q["minangle"]))
for q in best[:15]: print(q)
json.dump(best[:30], open("views.json", "w"))
