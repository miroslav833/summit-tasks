"""Pick the 13-crossing diagram (seed 3), assign residue numbers to the 26 passages along the chain, write
instance.json and stem.txt. Residues increase along the chain from N to C; the closure N..C adds no crossing."""
import pickle, json, random, numpy as np, knotlib as K, glsig
cands = {c["seed"]: c for c in pickle.load(open("bigdiag_13.pkl", "rb"))}
C = cands[3]; pd, g = C["pd"], C["gauss"]; n = len(pd); n2 = 2 * n
rnd = random.Random(11); NRES = 192
steps = [rnd.randint(4, 9) for _ in range(n2)]
start = 9; res = [start]
for s in steps[:-1]: res.append(res[-1] + s)
assert res[-1] <= NRES - 8, res[-1]
events = [dict(pos=k, crossing=g[k][0], over=(g[k][1] == "O"), sign=g[k][2], residue=res[k]) for k in range(n2)]
rows = []
for cid in range(n):
    ev = [e for e in events if e["crossing"] == cid]; assert len(ev) == 2
    o = [e for e in ev if e["over"]][0]; u = [e for e in ev if not e["over"]][0]
    rows.append(dict(id=cid, over=o["residue"], under=u["residue"], sign=o["sign"], first=min(o["residue"], u["residue"])))
rows.sort(key=lambda r: r["first"])
for k, r in enumerate(rows): r["label"] = k + 1
signs = K.signs_from_pd(pd)
inst = dict(seed=3, n=n, nres=NRES, pd=pd, signs=signs, writhe=sum(signs), events=events, rows=rows,
            gauss=" ".join(f"{g[k][0]+1}{g[k][1]}" for k in range(n2)))
json.dump(inst, open("instance.json", "w"), indent=1)
lines = []
for r in rows:
    lines.append(f"{r['label']} & {r['over']} & {r['under']} & {'+1' if r['sign'] > 0 else '-1'} \\\\")
table = "\n".join(lines)
stem = f"""A structure prediction model returned a model of a ${NRES}$-residue protein. To examine its topology, the $C_\\alpha$ trace was coarse-grained (each helix replaced by its axis, each strand and loop by a smooth curve through its residues) and projected onto a plane. The direction of projection was chosen so that the straight segment joining the two termini crosses no part of the chain; that segment is added to close the chain into a closed curve, so the closed curve consists of the chain from residue $1$ to residue ${NRES}$ followed by the segment back to residue $1$.

In the projection the chain crosses itself exactly $13$ times. Every crossing is listed in the table below by the two residues at which the two parts of the chain meet: the residue on the part in front (over) and the residue on the part behind (under). The chain is oriented from residue $1$ to residue ${NRES}$. The sign of a crossing is $+1$ when the direction of the under strand is obtained from the direction of the over strand by a counterclockwise rotation of less than $180$ degrees, and $-1$ otherwise. There are no other crossings.

\\begin{{tabular}}{{cccc}}
crossing & over (residue) & under (residue) & sign \\\\
\\hline
{table}
\\end{{tabular}}

The closed curve is a knot. What is the minimal crossing number of this knot, that is, the smallest number of crossings in any diagram of its knot type? Give a single integer.
"""
open("../stem.txt", "w").write(stem)
print(stem); print("events along chain:", " ".join(f"{e['residue']}{'O' if e['over'] else 'U'}{e['crossing']+1}" for e in events))
print("writhe", sum(signs), "sigma", glsig.gl_signature(pd, 0)[0], "det", K.determinant(pd))
