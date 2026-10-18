"""Random instances for the recombination question, with the classical bounds and the natural construction."""
import random, itertools, sys, time, pickle
from rmin import rmin, canon
def incompatible(a, b):
    return len({(x, y) for x, y in zip(a, b)}) == 4
def hk_bound(M):
    m = len(M[0]); cols = [tuple(r[j] for r in M) for j in range(m)]
    iv = sorted([(j, i) for i in range(m) for j in range(i + 1, m) if incompatible(cols[i], cols[j])])   # (right, left)
    cnt, last = 0, -1
    for right, left in iv:
        if left >= last: cnt += 1; last = right
    return cnt
def hap_bound(M):
    """Myers-Griffiths style: for every interval of sites, distinct haplotypes - (sites + 1); best composite over a partition into intervals"""
    m = len(M[0])
    def local(i, j):
        sub = {tuple(r[i:j + 1]) for r in M}; return max(0, len(sub) - (j - i + 1) - 1)
    best = [0] * (m + 1)
    for j in range(1, m + 1):
        best[j] = max(best[i] + local(i, j - 1) for i in range(j))
    return best[m]
def hap_subset_bound(M):
    """haplotype bound over every subset S of positions: distinct rows on S - |S| - 1"""
    m = len(M[0]); best = 0
    for mask in range(1, 1 << m):
        S = [j for j in range(m) if mask >> j & 1]
        best = max(best, len({tuple(r[j] for j in S) for r in M}) - len(S) - 1)
    return best
def mosaic_cost(row, core):
    """minimum number of switches to write row as a concatenation of segments of core rows"""
    m = len(row); INF = 10 ** 9
    f = [0 if c[0] == row[0] else INF for c in core]
    for j in range(1, m):
        g = min(f) + 1
        f = [min(f[k], g) if core[k][j] == row[j] else INF for k in range(len(core))]
    return min(f)
def compatible_set(rows):
    m = len(rows[0]); cols = [tuple(r[j] for r in rows) for j in range(m)]
    return not any(incompatible(cols[i], cols[j]) for i in range(m) for j in range(i + 1, m))
def natural_upper(M):
    """best 'compatible core plus mosaics' construction: a set of rows with no four-gamete pair forms a tree, every
    other row is built as a mosaic of rows already present (core first, then earlier mosaics)"""
    n = len(M); best = None
    for size in range(n, 0, -1):
        for core in itertools.combinations(range(n), size):
            rows = [M[i] for i in core]
            if not compatible_set(rows): continue
            rest = [i for i in range(n) if i not in core]
            # order the rest greedily by cheapest mosaic
            pool = list(rows); tot = 0; left = list(rest)
            while left:
                c, i = min((mosaic_cost(M[i], pool), i) for i in left)
                tot += c; pool.append(M[i]); left.remove(i)
            if best is None or tot < best: best = tot
        if best is not None and size < n - 4: break
    return best
def simulate(n, m, k, rnd):
    """forward: one ancestor; events in random order: 2m mutations at distinct sites, k recombinations, 3n splits;
    sample n distinct rows, keep m informative columns (both alleles at least twice) in their order"""
    M2 = 2 * m
    pop = [[0] * M2]; sites = list(range(M2)); rnd.shuffle(sites); events = ["mut"] * M2 + ["rec"] * k + ["dup"] * (3 * n)
    rnd.shuffle(events)
    for e in events:
        if e == "dup": pop.append(list(rnd.choice(pop)))
        elif e == "mut":
            s = sites.pop(); r = rnd.choice(pop); r[s] = 1
        else:
            if len(pop) < 2: pop.append(list(rnd.choice(pop))); continue
            a, b = rnd.sample(pop, 2); bp = rnd.randrange(1, M2); pop.append(a[:bp] + b[bp:])
    rows = list({tuple(r) for r in pop})
    if len(rows) < n: return None
    rows = rnd.sample(rows, n)
    keep = [j for j in range(M2) if 2 <= sum(r[j] for r in rows) <= n - 2]
    if len(keep) < m: return None
    keep = sorted(rnd.sample(keep, m))
    M = [tuple(r[j] for j in keep) for r in rows]
    return M if len(set(M)) == n else None
if __name__ == "__main__":
    n, m, k, seed, budget = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    rnd = random.Random(seed); t0 = time.time(); out = open(f"log_{n}_{m}_{k}_{seed}.txt", "a"); i = 0
    while time.time() - t0 < budget:
        M = simulate(n, m, k, rnd); i += 1
        if M is None: continue
        hk, hb = hk_bound(M), max(hap_bound(M), hap_subset_bound(M))
        if max(hk, hb) >= k: continue
        st = {}; R = rmin(M, kmax=8, stats=st)
        if R is None or R < max(hk, hb) + 1: continue
        U = natural_upper(M)
        flag = "TRAP" if U is not None and U >= R + 1 and max(hk, hb) <= R - 1 else ""
        print(i, f"n={n} m={len(M[0])} R={R} HK={hk} hap={hb} natural={U} states={st.get('states')} {flag}", file=out, flush=True)
        if flag: pickle.dump(M, open(f"inst_{n}_{m}_{k}_{seed}_{i}.pkl", "wb"))
