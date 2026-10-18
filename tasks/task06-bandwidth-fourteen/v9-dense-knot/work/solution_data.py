"""Coarse-grained diagram of the fold in the figure's view with the residue positions of each
crossing; used for the written solution and the verification notes."""
import numpy as np, json, knotlib as K, altcheck as A
from render_dense import rot
view = json.load(open("image_view.json"))["view"]
seg = json.load(open("segments.json")); n = seg["n"]
coarse = np.load("coarse_open.npy")                     # open axis polyline (A), chain order
s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(coarse, axis=0), axis=1))]
per = {"loop": 3.25, "helix": 1.5, "strand": 3.3}       # axis length per residue used in decorate.py
res_s = np.zeros(n); pos = 0.0
for g in seg["segments"]:
    nres = g["last"] - g["first"] + 1; length = nres * per[g["kind"]]
    for k in range(nres): res_s[g["first"] - 1 + k] = pos + length / nres * (k + 0.5)
    pos += length
def kind_of(r):
    for g in seg["segments"]:
        if g["first"] <= r <= g["last"]: return [g["kind"], g["first"], g["last"]]
Q = (coarse - coarse.mean(0)) @ rot(*view).T
clos = np.linspace(Q[-1], Q[0], 30, endpoint=False)[1:]; closed = np.vstack([Q, clos])
D = K.diagram(closed); signs = [c["sign"] for c in D["crossings"]]
g = A.gauss(D)
out = dict(view=view, crossings=[], gauss=" ".join(f"{c + 1}{'O' if o else 'U'}" for c, o in g), writhe=D["writhe"],
           det=K.determinant(D["pd"]), alexander=str(K.alexander(D["pd"], signs).as_expr()),
           jones=K.jones_str(K.jones(D["pd"], D["writhe"])), nugatory=[c + 1 for c in A.nugatory(D)])
def res_at(p):
    if p >= len(Q) - 1: return None
    sp = s[int(p)] + (p - int(p)) * (s[min(int(p) + 1, len(s) - 1)] - s[int(p)])
    return int(np.argmin(np.abs(res_s - sp))) + 1
for c in D["crossings"]:
    ri, rj = res_at(c["pi"]), res_at(c["pj"])
    over, under = (ri, rj) if c["over_i"] else (rj, ri)
    out["crossings"].append(dict(id=c["id"] + 1, over=over, under=under, sign=c["sign"],
                                 over_kind=kind_of(over) if over else "closure", under_kind=kind_of(under) if under else "closure"))
json.dump(out, open("solution_data.json", "w"), indent=1)
print("crossings", len(out["crossings"]), "det", out["det"], "alexander", out["alexander"], "nugatory", out["nugatory"])
print("Gauss:", out["gauss"])
for c in out["crossings"]:
    ok_, uk_ = c["over_kind"], c["under_kind"]
    print(f"crossing {c['id']:2d}: residue {c['over']} ({ok_[0]} {ok_[1]}-{ok_[2]}) over residue {c['under']} ({uk_[0]} {uk_[1]}-{uk_[2]}), sign {c['sign']:+d}")
