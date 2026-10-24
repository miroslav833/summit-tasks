"""Variant with a hidden reduction: 12-crossing diagram of 10_132 (hidden.pkl), residue dressing, stem_<tag>.txt."""
import pickle, json, random, sys, numpy as np, knotlib as K, glsig
import os; cands = {c["seed"]: c for c in pickle.load(open(os.environ.get("HIDDEN", "hidden.pkl"), "rb"))}
for s, c in cands.items():
    F, fid, colour = glsig.checkerboard(c["pd"]); w = sum(1 for k in colour if colour[k] == 0)
    print("seed", s, "crossings", c["n"], "face split", w, "/", len(F) - w)
if len(sys.argv) < 3: sys.exit()
seed, tag = int(sys.argv[1]), sys.argv[2]; pd = cands[seed]["pd"]; n = len(pd); n2 = 2 * n
def gauss_from_pd(pd):
    ev = {}
    for cid, (a, b, c, d) in enumerate(pd):
        s = K.crossing_sign_from_pd((a, b, c, d), n2); ev[a] = (cid, "U", s); ev[d if s == 1 else b] = (cid, "O", s)
    return [ev[e] for e in range(n2)]
g = gauss_from_pd(pd); rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 5); NRES = 184
while True:
    steps = [rnd.randint(4, 10) for _ in range(n2 - 1)]; res = [8]
    for s in steps: res.append(res[-1] + s)
    if res[-1] <= NRES - 7: break
events = [dict(pos=k, crossing=g[k][0], over=(g[k][1] == "O"), sign=g[k][2], residue=res[k]) for k in range(n2)]
rows = []
for cid in range(n):
    ev = [e for e in events if e["crossing"] == cid]; o = [e for e in ev if e["over"]][0]; u = [e for e in ev if not e["over"]][0]
    rows.append(dict(id=cid, over=o["residue"], under=u["residue"], sign=o["sign"], first=min(o["residue"], u["residue"])))
rows.sort(key=lambda r: r["first"])
for k, r in enumerate(rows): r["label"] = k + 1
json.dump(dict(seed=seed, n=n, nres=NRES, pd=pd, events=events, rows=rows), open(f"instance_{tag}.json", "w"), indent=1)
table = "\n".join(f"{r['label']} & {r['over']} & {r['under']} & {'+1' if r['sign'] > 0 else '-1'} \\\\" for r in rows)
stem = open("../stem.txt").read()
import re
stem = stem.replace("$192$", f"${NRES}$").replace("exactly $13$ times", f"exactly ${n}$ times")
stem = re.sub(r"\\hline\n.*?\\end\{tabular\}", "\\\\hline\n" + table.replace("\\", "\\\\") + "\n\\\\end{tabular}", stem, flags=re.S)
open(f"../stem_{tag}.txt", "w").write(stem); print(stem)
print("passages:", " ".join(f"{e['residue']}:{[r['label'] for r in rows if r['id']==e['crossing']][0]}{'O' if e['over'] else 'U'}" for e in events))
print("writhe", sum(K.signs_from_pd(pd)), "sigma", glsig.gl_signature(pd, 0)[0], glsig.gl_signature(pd, 1)[0], "det", K.determinant(pd))
