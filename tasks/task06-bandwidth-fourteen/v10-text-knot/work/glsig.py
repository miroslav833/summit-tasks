"""Gordon-Litherland signature from a PD code (faces, checkerboard colouring, Goeritz matrix, correction term).
Convention fixed by testing against Seifert-matrix signatures of the table knots (see test at the bottom)."""
import numpy as np
def faces(pd):
    n = len(pd); pos = {}
    for x, X in enumerate(pd):
        for p, e in enumerate(X): pos.setdefault(e, []).append((x, p))
    seen = set(); F = []
    for x in range(n):
        for p in range(4):
            if (x, p) in seen: continue
            face = []; cur = (x, p)
            while cur not in seen:
                seen.add(cur); face.append(cur); cx, cp = cur; e = pd[cx][(cp + 1) % 4]
                ends = pos[e]; other = ends[0] if ends[1] == (cx, (cp + 1) % 4) else ends[1]
                if ends[0] == ends[1]: raise ValueError("loop edge")
                cur = (other[0], other[1])
            F.append(face)
    assert len(F) == n + 2, ("faces", len(F), n)
    return F
def checkerboard(pd):
    F = faces(pd); fid = {c: k for k, f in enumerate(F) for c in f}
    n = len(pd); colour = {0: 0}; adj = {k: set() for k in range(len(F))}
    for x in range(n):
        for p in range(4):
            f1, f2 = fid[(x, p)], fid[(x, (p - 1) % 4)]   # faces on the two sides of edge pd[x][p]
            adj[f1].add(f2); adj[f2].add(f1)
    stack = [0]
    while stack:
        f = stack.pop()
        for g in adj[f]:
            if g not in colour: colour[g] = 1 - colour[f]; stack.append(g)
            elif colour[g] == colour[f]: raise ValueError("not checkerboard")
    return F, fid, colour
def gl_signature(pd, white=0, e1=1, e2=1):
    # sigma(K) = sign(Goeritz) - mu with eta = +1 when the white regions sit at corners 1,3 (test: 84/84 table knots)
    n = len(pd); n2 = 2 * n; F, fid, colour = checkerboard(pd)
    W = [k for k in range(len(F)) if colour[k] == white]; widx = {k: i for i, k in enumerate(W)}
    G = np.zeros((len(W), len(W))); mu = 0
    for x, (a, b, c, d) in enumerate(pd):
        f = [fid[(x, p)] for p in range(4)]
        if colour[f[0]] == white: eta, wi, wj = -1, f[0], f[2]
        else: eta, wi, wj = 1, f[1], f[3]
        positive = (d + 1) % n2 == b
        merged_02 = not positive          # oriented smoothing merges corners 0,2 when the crossing is negative
        white_02 = (colour[f[0]] == white)
        typeII = (white_02 != merged_02)
        if typeII: mu += eta
        i, j = widx[wi], widx[wj]
        if i != j: G[i, j] -= eta; G[j, i] -= eta; G[i, i] += eta; G[j, j] += eta
    Gp = G[1:, 1:]; ev = np.linalg.eigvalsh(Gp) if len(Gp) else np.array([])
    sG = int((ev > 1e-9).sum() - (ev < -1e-9).sum())
    return e1 * sG - e2 * mu, dict(white_faces=len(W), goeritz=Gp, mu=mu, signG=sG, det=round(abs(np.linalg.det(Gp))) if len(Gp) else 1)
if __name__ == "__main__":
    import spherogram
    names = [f"{n}_{k}" for n, cnt in ((3,1),(4,1),(5,2),(6,3),(7,7),(8,21),(9,49)) for k in range(1, cnt+1)]
    combos = {(w, e1, e2): 0 for w in (0, 1) for e1 in (1, -1) for e2 in (1, -1)}; total = 0
    for nm in names:
        L = spherogram.Link(nm); pd = [tuple(x) for x in L.PD_code()]
        V = np.array(L.seifert_matrix(), float); ev = np.linalg.eigvalsh(V + V.T); sig = int((ev > 1e-9).sum() - (ev < -1e-9).sum())
        total += 1
        for key in combos:
            s, info = gl_signature(pd, *key); combos[key] += (s == sig)
    for key, ok in combos.items(): print("white", key[0], "e1", key[1], "e2", key[2], ":", ok, "/", total)
