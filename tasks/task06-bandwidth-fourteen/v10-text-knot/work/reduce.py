"""Reduced 10-crossing diagram from the 13-crossing one (remove the kink and the R2 pair in the Gauss code),
with table labels kept; faces, Goeritz matrix, correction term and signature for the written solution."""
import json, numpy as np, knotlib as K, glsig
inst = json.load(open("instance.json")); rows = {r["id"]: r for r in inst["rows"]}; ev = inst["events"]
lab = lambda cid: rows[cid]["label"]
seq = [(lab(e["crossing"]), "O" if e["over"] else "U", e["sign"], e["residue"]) for e in ev]
print("Gauss word (table labels):", " ".join(f"{c}{o}" for c, o, s, r in seq))
def reduce_once(seq):
    n2 = len(seq)
    for k in range(n2):                       # R1: same crossing at consecutive positions
        if seq[k][0] == seq[(k + 1) % n2][0]:
            c = seq[k][0]; print("kink at crossing", c, "residues", seq[k][3], seq[(k+1)%n2][3]); return [x for x in seq if x[0] != c]
    for k in range(n2):                       # R2: two crossings adjacent twice with the same over/under on each pass
        a, b = seq[k], seq[(k + 1) % n2]
        if a[0] == b[0] or a[1] != b[1]: continue
        for m in range(n2):
            if m == k: continue
            c, d = seq[m], seq[(m + 1) % n2]
            if {c[0], d[0]} == {a[0], b[0]} and c[1] == d[1] and c[1] != a[1]:
                print("R2 pair: crossings", a[0], b[0], "residues", a[3], b[3], "and", c[3], d[3]); return [x for x in seq if x[0] not in (a[0], b[0])]
    return None
cur = seq
while True:
    nxt = reduce_once(cur)
    if nxt is None: break
    cur = nxt
print("reduced Gauss word:", " ".join(f"{c}{o}" for c, o, s, r in cur), "| crossings", len(cur) // 2)
# PD from the signed Gauss code: edge k runs from passage k to passage k+1
def pd_from_gauss(seq):
    n2 = len(seq); byc = {}
    for k, (c, o, s, r) in enumerate(seq): byc.setdefault(c, {})[o] = k
    pd = []; labels = []
    for c, d in byc.items():
        a = d["U"]; cc = (a + 1) % n2; oin = d["O"]; oout = (oin + 1) % n2; s = seq[a][2]
        b, dd = (oout, oin) if s == 1 else (oin, oout)
        pd.append((a, b, cc, dd)); labels.append(c)
    return pd, labels
pd, labels = pd_from_gauss(cur); n = len(pd)
assert K.signs_from_pd(pd) == [cur[[k for k, x in enumerate(cur) if x[0] == c and x[1] == "U"][0]][2] for c in labels]
F = glsig.faces(pd); print("faces", len(F), "(= n + 2, planar)")
signs = K.signs_from_pd(pd); print("writhe", sum(signs), "det", K.determinant(pd), "alexander", K.alexander(pd, signs).as_expr())
print("jones", K.jones_str(K.jones(pd, sum(signs))))
for w in (0, 1):
    s, info = glsig.gl_signature(pd, w)
    print(f"white={w}: {info['white_faces']} white faces, sign(G')={info['signG']}, mu={info['mu']}, sigma={s}, |det G'|={info['det']}")
    print(info["goeritz"].astype(int))
# face description for the solution: each face as the cyclic list of (crossing label, corner) and the edges (residue intervals)
Fs, fid, colour = glsig.checkerboard(pd)
res = [x[3] for x in cur]
for k, f in enumerate(Fs):
    edges = []
    for (x, p) in f:
        e = pd[x][(p + 1) % 4]; edges.append(f"{res[e]}-{res[(e + 1) % (2 * n)]}")
    print("face", k, "colour", colour[k], "crossings", [labels[x] for x, p in f], "edges (residue to residue)", edges)
json.dump(dict(reduced_gauss=[(c, o, s, r) for c, o, s, r in cur], pd=pd, labels=labels), open("reduced.json", "w"), indent=1)
