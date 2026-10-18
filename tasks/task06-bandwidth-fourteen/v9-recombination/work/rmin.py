"""Exact minimum number of recombinations (infinite-sites model) for a set of binary sequences.
Backward search over sets of sequences with wildcards (None = unspecified), Lyngso-Song-Hein style:
  safe steps (cost 0, applied greedily): drop columns that are not polymorphic among specified values;
    drop a column where the minor allele occurs once (a mutation); remove a sequence that is subsumed by another
    (every specified value agrees) -> coalescence; drop columns that are entirely unspecified.
  recombination (cost 1): split one sequence at a breakpoint into a prefix (suffix unspecified) and a suffix
    (prefix unspecified).
Iterative deepening on the recombination count with a memo of states already shown to need more than k."""
import sys, itertools
from functools import lru_cache
sys.setrecursionlimit(100000)

def canon(seqs):
    """apply the safe reductions and return a canonical tuple (sorted rows, columns normalised)"""
    rows = [tuple(r) for r in seqs]
    changed = True
    while changed:
        changed = False
        if not rows: break
        m = len(rows[0])
        # columns
        keep = []
        for j in range(m):
            col = [r[j] for r in rows if r[j] is not None]
            ones = sum(col); zeros = len(col) - ones
            if ones >= 2 and zeros >= 2: keep.append(j)
        if len(keep) < m:
            rows = [tuple(r[j] for j in keep) for r in rows]; changed = True
        # subsumed rows (coalescence): remove r if some other row s agrees with r on every position where r is specified
        n = len(rows); out = []; removed = [False] * n
        for i in range(n):
            for k in range(n):
                if i == k or removed[k]: continue
                r, s = rows[i], rows[k]
                if all(a is None or (b is not None and a == b) for a, b in zip(r, s)):
                    # r is subsumed by s; for identical rows keep the first
                    if r != s or i > k: removed[i] = True; break
        if any(removed):
            rows = [r for i, r in enumerate(rows) if not removed[i]]; changed = True
        # all-wildcard rows
        nr = [r for r in rows if any(x is not None for x in r)]
        if len(nr) < len(rows): rows = nr; changed = True
    # canonical form: normalise each column so the first specified value is 0, then sort rows, then sort columns
    if not rows or not rows[0]: return ()
    m = len(rows[0])
    cols = []
    for j in range(m):
        col = [r[j] for r in rows]
        first = next(x for x in col if x is not None)
        cols.append(tuple(None if x is None else x ^ first for x in col))
    rows = [tuple(c[i] for c in cols) for i in range(len(rows))]
    return tuple(sorted(rows, key=lambda r: tuple(-1 if x is None else x for x in r)))

def done(state): return len(state) <= 1

def splits(state):
    """all recombination moves: for each row and each breakpoint between two specified sites"""
    seen = set()
    for i, r in enumerate(state):
        spec = [j for j, x in enumerate(r) if x is not None]
        for t in range(1, len(spec)):
            b = spec[t]                          # breakpoint just before position b
            left = tuple(x if j < b else None for j, x in enumerate(r))
            right = tuple(x if j >= b else None for j, x in enumerate(r))
            new = list(state[:i]) + [left, right] + list(state[i + 1:])
            c = canon(new)
            if c not in seen: seen.add(c); yield c

def lb(state):
    """Hudson-Kaplan bound on a state with wildcards: a column pair is incompatible when the rows specified at both
    columns show all four gametes; the number of pairwise disjoint incompatible intervals bounds R_min"""
    if len(state) <= 1: return 0
    m = len(state[0]); iv = []
    for i in range(m):
        for j in range(i + 1, m):
            g = {(r[i], r[j]) for r in state if r[i] is not None and r[j] is not None}
            if len(g) == 4: iv.append((j, i))
    iv.sort(); cnt, last = 0, -1
    for right, left in iv:
        if left >= last: cnt += 1; last = right
    return cnt

def rmin(seqs, kmax=12, stats=None):
    start = canon(seqs)
    fail = {}                                     # state -> largest k known insufficient
    count = [0]
    def ok(state, k):
        count[0] += 1
        if done(state): return True
        if k == 0: return False
        if fail.get(state, -1) >= k: return False
        if lb(state) > k: fail[state] = max(fail.get(state, -1), k); return False
        for nxt in splits(state):
            if ok(nxt, k - 1): return True
        fail[state] = max(fail.get(state, -1), k)
        return False
    for k in range(kmax + 1):
        if ok(start, k):
            if stats is not None: stats["states"] = count[0]; stats["memo"] = len(fail)
            return k
    return None

def parse(lines): return [tuple(int(c) for c in l.strip()) for l in lines if l.strip()]

if __name__ == "__main__":
    tests = {
        "compatible (tree)": ["000", "100", "110", "111"],
        "one four-gamete pair": ["00", "01", "10", "11"],
        "two disjoint incompatibilities": ["0000", "0101", "1010", "1111"],
    }
    for name, t in tests.items(): print(name, rmin(parse(t)))
