import numpy as np, knotlib as K, itertools
def gauss(D):
    """Gauss sequence along the curve: list of (crossing id, is_over)."""
    ev = []
    for c in D["crossings"]:
        ev.append((c["pi"], c["id"], c["over_i"])); ev.append((c["pj"], c["id"], not c["over_i"]))
    ev.sort(); return [(cid, ov) for _, cid, ov in ev]
def alternating(D):
    g = gauss(D); return all(g[i][1] != g[(i + 1) % len(g)][1] for i in range(len(g)))
def nugatory(D):
    """crossing ids whose two visits bound a closed sub-word (every crossing inside appears twice inside)."""
    g = [cid for cid, _ in gauss(D)]; out = []
    for cid in range(D["n"]):
        i, j = [k for k, c in enumerate(g) if c == cid]
        inside = g[i + 1:j]
        if all(inside.count(c) == 2 for c in set(inside)): out.append(cid)
    return out
if __name__ == "__main__":
    # alternating 3-braid words: blocks sigma1^a sigma2^-b sigma1^c sigma2^-d ... ; find 7-crossing knots
    res = []
    for nb in (2, 4, 6):
        for blocks in itertools.product(range(1, 6), repeat=nb):
            if sum(blocks) not in (4, 5, 6, 7): continue
            word = []
            for k, b in enumerate(blocks): word += [1] * b if k % 2 == 0 else [-2] * b
            try: pts = K.build_braid_curve(word, 3)
            except AssertionError: continue
            D = K.diagram(K.smooth(pts, 900))
            if D["n"] != len(word): continue
            res.append((sum(blocks), blocks, alternating(D), nugatory(D), K.determinant(D["pd"]), K.jones_str(K.jones(D["pd"], D["writhe"]))))
    for r in sorted(res): print(r)
