"""Find an optimal history by the search in rmin.py, keep the chain of states, then check every transition with a
separate, plain implementation of the three backward moves (no code shared with the search)."""
import pickle, glob, sys
from rmin import canon, splits, lb, done
def path(seqs, k):
    start = canon(seqs); fail = {}
    def go(state, k):
        if done(state): return [state]
        if k == 0 or fail.get(state, -1) >= k or lb(state) > k: return None
        for nxt in splits(state):
            p = go(nxt, k - 1)
            if p: return [state] + p
        fail[state] = k; return None
    return go(start, k)
# ---- independent checker ----
def compatible_merge_ok(rows):
    return rows
def reduce_once(rows):
    """one independent reduction pass: drop columns with a minority value on <= 1 specified rows (a single mutation
    or monomorphic), remove a row whose specified entries all agree with another row (coalescence)"""
    m = len(rows[0]) if rows else 0
    keep = []
    for j in range(m):
        vals = [r[j] for r in rows if r[j] is not None]
        if min(vals.count(0), vals.count(1)) >= 2: keep.append(j)
    rows = [tuple(r[j] for j in keep) for r in rows]
    out = []
    for i, r in enumerate(rows):
        absorbed = any(k != i and all(a is None or a == b for a, b in zip(r, s)) and (r != s or k < i) for k, s in enumerate(rows))
        if not absorbed and any(x is not None for x in r): out.append(r)
    return out
def full_reduce(rows):
    rows = list(rows)
    while True:
        new = reduce_once(rows)
        if new == rows: return rows
        rows = new
def same_up_to_flips(a, b):
    """equal as multisets of rows after flipping columns and permuting rows (columns keep their order)"""
    if len(a) != len(b): return False
    if not a: return True
    if len(a[0]) != len(b[0]): return False
    def norm(rows):
        cols = list(zip(*rows)); nc = []
        for c in cols:
            f = next(x for x in c if x is not None); nc.append(tuple(None if x is None else x ^ f for x in c))
        return sorted(zip(*nc), key=lambda r: tuple(-1 if x is None else x for x in r))
    return norm(a) == norm(b)
def check(chain):
    rec = 0
    for s, t in zip(chain, chain[1:]):
        ok = False
        for i, r in enumerate(s):
            spec = [j for j, x in enumerate(r) if x is not None]
            for b in spec[1:]:
                L = tuple(x if j < b else None for j, x in enumerate(r)); R = tuple(x if j >= b else None for j, x in enumerate(r))
                cand = full_reduce(list(s[:i]) + [L, R] + list(s[i + 1:]))
                if same_up_to_flips(cand, list(t)): ok = True; break
            if ok: break
        assert ok, "a step is not one recombination followed by mutations and coalescences"
        rec += 1
    assert len(full_reduce(list(chain[-1]))) <= 1
    return rec
if __name__ == "__main__":
    M = pickle.load(open(sorted(glob.glob(sys.argv[1]))[0], "rb")); k = int(sys.argv[2])
    ch = path(M, k); assert ch is not None, "no history with that many recombinations"
    print("history found; states along the way:")
    for st in ch: print("   ", ["".join("*" if x is None else str(x) for x in r) for r in st])
    print("independent check: recombinations used =", check(ch))
    print("no history with", k - 1, ":", path(M, k - 1) is None)
