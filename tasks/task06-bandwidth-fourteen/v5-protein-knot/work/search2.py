import numpy as np, json, knotlib as K, sys
word = [1,1,1,-2,-1,-1,-1,-2]
pts = K.build_braid_curve(word, 3)
sm = K.smooth(pts, 700)
rng = np.random.default_rng(int(sys.argv[1]))
rows = []
for trial in range(int(sys.argv[2])):
    ax, ay, az = rng.uniform(-np.pi, np.pi, 3)
    R = K.rotmat(ax, ay, az)
    Q = sm @ R.T
    D = K.diagram(Q)
    span = np.ptp(Q[:, :2], axis=0).max()
    rows.append(dict(n=D["n"], mindist=round(D["mindist"] / span, 3), minangle=round(D["minangle"], 1), mindz=round(D["mindz"], 3), ang=(ax, ay, az)))
import collections
print(collections.Counter(r["n"] for r in rows))
good = [r for r in rows if 10 <= r["n"] <= 14]
good.sort(key=lambda q: -(min(q["mindist"], 0.08) * min(q["minangle"], 40) * min(q["mindz"], 0.2)))
for q in good[:12]: print(q)
json.dump(good[:40], open(f"views_{sys.argv[1]}.json", "w"))
