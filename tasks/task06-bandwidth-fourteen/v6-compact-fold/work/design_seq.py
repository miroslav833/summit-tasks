"""Search HP sequences (27-mer on the 3x3x3 cube, compact conformations only) with:
 - hand bound B (parity/site-degree bound) equal to the true optimum E*,
 - a unique optimal structure up to symmetry (direction kept),
 - many structures at E*-1 (the trap level).
Prints the hand bound components so the written proof can be drafted."""
import numpy as np, sys, itertools
d = np.load("cube_paths.npz"); M = d["M"]; paths = d["paths"]; pairs = [tuple(p) for p in d["pairs"]]
N = 27
pair_index = {pr: k for k, pr in enumerate(pairs)}
def energy_all(seq):
    s = np.array([c == "H" for c in seq])
    v = np.array([s[i] and s[j] for i, j in pairs])
    return M[:, v].sum(1)
def hand_bound(seq):
    """Odd positions (1-based) sit on the 14 even sites (8 corners deg 3, 6 faces deg 5); even positions
    on the 13 odd sites (12 edges deg 4, 1 centre deg 6). Contacts join an odd-position H to an
    even-position H. Free valence of a position = site degree minus its chain bonds (2, or 1 at an end)."""
    s = [c == "H" for c in seq]
    odd = [p for p in range(N) if p % 2 == 0 and s[p]]    # 0-based even index = 1-based odd position
    even = [p for p in range(N) if p % 2 == 1 and s[p]]
    def bonds(p): return 1 if p in (0, N - 1) else 2
    # odd positions: at most 6 on faces (deg 5), rest corners (deg 3); give faces to the ends first (more valence)
    fo = sorted([5 - bonds(p) for p in odd], reverse=True)[:6]; co = sorted([3 - bonds(p) for p in odd], reverse=True)[6:] if len(odd) > 6 else []
    B_odd = sum(fo) + sum(co)
    # even positions: at most 1 at centre (deg 6), rest edges (deg 4)
    fe = sorted([6 - bonds(p) for p in even], reverse=True)[:1]; ce = sorted([4 - bonds(p) for p in even], reverse=True)[1:] if len(even) > 1 else []
    B_even = sum(fe) + sum(ce)
    return min(B_odd, B_even), B_odd, B_even
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
nH = int(sys.argv[2]) if len(sys.argv) > 2 else 12
found = []
for trial in range(int(sys.argv[3]) if len(sys.argv) > 3 else 3000):
    pos = rng.choice(N, nH, replace=False)
    seq = "".join("H" if i in pos else "P" for i in range(N))
    E = energy_all(seq); Es = E.max(); n1 = int((E == Es).sum()); n2 = int((E == Es - 1).sum())
    B, Bo, Be = hand_bound(seq)
    if n1 == 1 and B == Es and n2 >= 20:
        found.append((seq, Es, B, Bo, Be, n1, n2))
        print(seq, "E*", Es, "bound", B, "(odd", Bo, "even", Be, ") optima", n1, "at E*-1:", n2, flush=True)
print("found", len(found))
