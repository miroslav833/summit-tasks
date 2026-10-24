"""Find the hidden reduction of the variant diagram: a Reidemeister III move (on a triangular face with one strand
passing over or under the other two) after which a Reidemeister II pair becomes visible in the Gauss code."""
import sys, json; sys.path.insert(0, ".."); import verify_key as V
tag = sys.argv[1]; stem = open(f"../stem_{tag}.txt").read(); rows = V.parse(stem); seq = V.gauss_from_rows(rows)
pd, labels = V.pd_from_gauss(seq); n = len(pd); n2 = 2 * n
print("diagram:", " ".join(f"{r}:{l}{o}" for r, l, o, s in seq)); print("faces", len(V.faces(pd)))
red, moves = V.reduce_gauss(seq); print("visible R1/R2 reductions:", moves)
# triangular faces: corners (x,p); the face's edges are pd[x][(p+1)%4]
def r3_candidates(pd, labels, seq):
    out = []
    for f in V.faces(pd):
        if len(f) != 3: continue
        crossings = [labels[x] for x, p in f]
        edges = [pd[x][(p + 1) % 4] for x, p in f]
        # each edge e runs from passage e to passage e+1; the strand through the face at edge e visits two of the triangle's crossings consecutively
        strands = []
        for e in edges:
            a, b = seq[(e - 1) % n2], seq[e]; strands.append((a[1], a[2], b[1], b[2]))   # (crossing, O/U, crossing, O/U)
        kinds = ["".join(sorted((s[1], s[3]))) for s in strands]
        ok = any(k in ("OO", "UU") for k in kinds)
        out.append(dict(crossings=crossings, edges=edges, strands=strands, r3=ok))
    return out
cands = r3_candidates(pd, labels, seq)
for c in cands: print("triangle", c["crossings"], "strands", c["strands"], "R3 possible" if c["r3"] else "no R3 (mixed)")
def apply_r3(seq, edges):
    """swap the two consecutive passages on each of the three strands bounding the triangle"""
    seq = list(seq)
    for e in edges:
        a, b = (e - 1) % n2, e % n2; seq[a], seq[b] = seq[b], seq[a]
    return seq
for c in cands:
    if not c["r3"]: continue
    new = apply_r3(seq, c["edges"])
    # residues move with the passages, so re-sort is wrong: keep the sequence order as the new chain order
    pd2, lab2 = V.pd_from_gauss([(k, l, o, s) for k, (r, l, o, s) in enumerate(new)])
    planar = len(V.faces(pd2)) == n + 2
    red2, moves2 = V.reduce_gauss([(k, l, o, s) for k, (r, l, o, s) in enumerate(new)])
    print("after R3 on triangle", c["crossings"], "planar" if planar else "NOT planar", "| reductions:", moves2, "-> crossings", len(red2) // 2,
          "| Gauss:", " ".join(f"{l}{o}" for r, l, o, s in new))
    if planar and len(red2) // 2 == 10:
        J = V.kauffman_jones(pd2); print("   Jones after R3:", V.poly_str(J))
        pdr, labr = V.pd_from_gauss([(k, l, o, s) for k, (r, l, o, s) in enumerate(red2)])
        print("   reduced Gauss:", " ".join(f"{l}{o}" for r, l, o, s in red2), "| Jones:", V.poly_str(V.kauffman_jones(pdr)), "| sigma", V.gl_signature(pdr, 0)[0])
