"""Enumerate all Hamiltonian paths of the 3x3x3 cubic lattice (compact 27-mer conformations).
Stores for each path its contact map (set of non-bonded adjacent position pairs) and keeps
one path per distinct contact map (as a canonical representative). Saves cube_paths.npz."""
import numpy as np, itertools, pickle, time, sys
sites = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
idx = {s: i for i, s in enumerate(sites)}
adj = [[idx[(x + dx, y + dy, z + dz)] for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
        if 0 <= x + dx < 3 and 0 <= y + dy < 3 and 0 <= z + dz < 3] for (x, y, z) in sites]
N = 27
# symmetry: 48 cube symmetries as permutations of sites
def perms():
    out = []
    for p in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            m = []
            for (x, y, z) in sites:
                v = [x, y, z]; w = [v[p[0]], v[p[1]], v[p[2]]]
                w = [c if s == 1 else 2 - c for c, s in zip(w, sg)]
                m.append(idx[tuple(w)])
            out.append(tuple(m))
    return out
SYM = perms()
paths = []
t0 = time.time()
# start only from one representative of each site orbit: corner (0,0,0), edge (1,0,0), face (1,1,0), centre (1,1,1)
starts = [idx[(0,0,0)], idx[(1,0,0)], idx[(1,1,0)], idx[(1,1,1)]]
sys.setrecursionlimit(10000)
def dfs(path, used):
    if len(path) == N:
        paths.append(tuple(path)); return
    last = path[-1]
    for nb in adj[last]:
        if not used[nb]:
            used[nb] = True; path.append(nb); dfs(path, used); path.pop(); used[nb] = False
for s in starts:
    used = [False] * 27; used[s] = True
    dfs([s], used)
print("paths from representative starts:", len(paths), round(time.time() - t0), "s")
# canonical form under symmetry (and keep direction: a path and its reverse are different foldings
# of a sequence unless the sequence is a palindrome; keep both directions as separate entries)
seen = {}
for p in paths:
    key = min(tuple(m[i] for i in p) for m in SYM)
    if key not in seen: seen[key] = p
canon = list(seen.values())
print("distinct up to symmetry (direction kept):", len(canon))
# contact maps
pos_of = np.zeros((len(canon), 27), int)
pairs = [(i, j) for i in range(N) for j in range(i + 2, N)]
pair_index = {pr: k for k, pr in enumerate(pairs)}
M = np.zeros((len(canon), len(pairs)), bool)
for r, p in enumerate(canon):
    where = {site: k for k, site in enumerate(p)}
    for k, site in enumerate(p):
        for nb in adj[site]:
            j = where[nb]
            if j > k + 1: M[r, pair_index[(k, j)]] = True
print("contacts per structure: min", M.sum(1).min(), "max", M.sum(1).max())
np.savez_compressed("cube_paths.npz", M=M, paths=np.array(canon), pairs=np.array(pairs))
print("saved", round(time.time() - t0), "s")
