"""Verification for the text-only knotted-backbone task (key 11). Self-contained: python3 with numpy.

Reads the crossing table from stem.txt (or the copy below), builds the signed Gauss code from the residue order,
checks that it is a planar knot diagram, and computes
  the Alexander polynomial (exact integer evaluations), the determinant, the signature (Gordon-Litherland formula
  from the Goeritz matrix) and the Jones polynomial (Kauffman bracket state sum).
Alexander polynomial, determinant and signature coincide with those of the mirror image of 9_18 (the trap answer 9).
No Reidemeister I or II move is visible in the table, but a Reidemeister III move on the triangle bounded by
crossings 10, 11, 12 exposes a II pair (12, 13); the resulting 11-crossing diagram is alternating and reduced, so by
the Kauffman-Murasugi-Thistlethwaite theorem the crossing number is 11. The Jones polynomial has span 11 (that of
9_18 has span 9), which confirms the lower bound independently. Key: 11 (the knot is 11a246)."""
import re, sys, itertools, pathlib
from fractions import Fraction
import numpy as np

TABLE = """1 & 79 & 8 & +1
2 & 14 & 139 & +1
3 & 122 & 19 & +1
4 & 26 & 127 & +1
5 & 131 & 35 & +1
6 & 39 & 118 & +1
7 & 111 & 43 & +1
8 & 53 & 104 & +1
9 & 100 & 61 & +1
10 & 150 & 65 & +1
11 & 71 & 91 & +1
12 & 160 & 83 & +1
13 & 146 & 96 & -1"""


def parse(text):
    rows = []
    for m in re.finditer(r"^\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*([+-]?1)", text, re.M):
        rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    return rows

def gauss_from_rows(rows):
    ev = []
    for lab, over, under, sign in rows:
        ev.append((over, lab, "O", sign)); ev.append((under, lab, "U", sign))
    ev.sort()
    assert len(set(e[0] for e in ev)) == len(ev), "a residue appears twice"
    return ev   # chain order from the N terminus; the closure returns from the last passage to the first

def pd_from_gauss(seq):
    """PD code X[a,b,c,d] (a incoming under edge, then counterclockwise), edge k ends at passage k and starts at passage k-1.
    Positive crossing: the under direction is the over direction rotated counterclockwise, so the over strand
    runs from the west edge d to the east edge b."""
    n2 = len(seq); byc = {}
    for k, (res, lab, o, s) in enumerate(seq): byc.setdefault(lab, {})[o] = (k, s)
    pd, labels = [], []
    for lab in sorted(byc):
        (a, s), (oin, _) = byc[lab]["U"], byc[lab]["O"]
        c, oout = (a + 1) % n2, (oin + 1) % n2
        b, d = (oout, oin) if s == 1 else (oin, oout)
        pd.append((a, b, c, d)); labels.append(lab)
    return pd, labels

def faces(pd):
    n = len(pd); pos = {}
    for x, X in enumerate(pd):
        for p, e in enumerate(X): pos.setdefault(e, []).append((x, p))
    seen, F = set(), []
    for x in range(n):
        for p in range(4):
            if (x, p) in seen: continue
            face, cur = [], (x, p)
            while cur not in seen:
                seen.add(cur); face.append(cur); cx, cp = cur; e = pd[cx][(cp + 1) % 4]
                ends = pos[e]; cur = ends[0] if ends[1] == (cx, (cp + 1) % 4) else ends[1]
            F.append(face)
    return F

def signs(pd):
    n2 = 2 * len(pd); return [1 if (d + 1) % n2 == b else -1 for a, b, c, d in pd]

def bareiss(M):
    """Exact determinant of an integer matrix."""
    M = [row[:] for row in M]; n = len(M); sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None: return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]

def alexander_at(pd, t):
    """Alexander polynomial evaluated at the integer t, up to sign and a power of t. Arcs are the under-strand
    segments between consecutive undercrossings; Wirtinger relation at a positive crossing x_out = x_over x_in x_over^-1
    gives the row (1 - t) a_over + t a_in - a_out, at a negative crossing in and out swap."""
    n = len(pd); n2 = 2 * n; sg = signs(pd)
    under_in = [a for a, b, c, d in pd]
    arc = [None] * n2; k = 0
    starts = sorted(set((a + 1) % n2 for a in under_in))     # an arc starts at every outgoing under edge
    arc_id = {}
    for s in starts: arc_id[s] = len(arc_id)
    cur = None
    for step in range(2 * n2):
        e = step % n2
        if e in arc_id: cur = arc_id[e]
        if cur is not None: arc[e] = cur
    rows = []
    for (a, b, c, d), s in zip(pd, sg):
        over = arc[b]; assert arc[b] == arc[d]
        ain, aout = arc[a], arc[c]
        row = [0] * n
        if s == 1: row[over] += 1 - t; row[ain] += t; row[aout] -= 1
        else: row[over] += 1 - t; row[aout] += t; row[ain] -= 1
        rows.append(row)
    minor = [r[1:] for r in rows[1:]]
    return bareiss(minor)

def kauffman_jones(pd):
    """Jones polynomial V(t) as {exponent: coefficient} by the Kauffman bracket state sum."""
    n = len(pd); n2 = 2 * n; w = sum(signs(pd))
    br = {}   # Laurent polynomial in A
    for state in itertools.product((0, 1), repeat=n):
        parent = list(range(n2))
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(x, y): parent[find(x)] = find(y)
        na = 0
        for (a, b, c, d), s in zip(pd, state):
            if s == 0: union(a, b); union(c, d); na += 1     # A smoothing joins a-b and c-d
            else: union(a, d); union(b, c)
        loops = len(set(find(x) for x in range(n2)))
        # A^(na - nb) (-A^2 - A^-2)^(loops - 1)
        term = {na - (n - na): 1}
        for _ in range(loops - 1):
            new = {}
            for e, cf in term.items():
                new[e + 2] = new.get(e + 2, 0) - cf; new[e - 2] = new.get(e - 2, 0) - cf
            term = new
        for e, cf in term.items(): br[e] = br.get(e, 0) + cf
    # f = (-A^3)^(-w) <D>, then A = t^(-1/4)
    V = {}
    for e, cf in br.items():
        if cf == 0: continue
        ee = e - 3 * w; cf2 = cf * ((-1) ** (w % 2))
        assert ee % 4 == 0; V[-ee // 4] = V.get(-ee // 4, 0) + cf2
    return {k: v for k, v in sorted(V.items()) if v != 0}

def gl_signature(pd, white_colour=0):
    """Gordon-Litherland: sigma = sign(Goeritz) - mu. Corners (x,p) lie between positions p and p+1 of crossing x;
    eta(c) = +1 when the white regions are at corners 1 and 3, else -1; the oriented smoothing merges corners 0 and 2
    at a negative crossing and corners 1 and 3 at a positive one; type II crossings are those where the white
    regions are not the merged pair."""
    n = len(pd); n2 = 2 * n; F = faces(pd); fid = {c: k for k, f in enumerate(F) for c in f}
    colour = {0: 0}; adj = {k: set() for k in range(len(F))}
    for x in range(n):
        for p in range(4):
            f1, f2 = fid[(x, p)], fid[(x, (p - 1) % 4)]; adj[f1].add(f2); adj[f2].add(f1)
    stack = [0]
    while stack:
        f = stack.pop()
        for g in adj[f]:
            if g not in colour: colour[g] = 1 - colour[f]; stack.append(g)
            else: assert colour[g] != colour[f], "not checkerboard"
    W = [k for k in range(len(F)) if colour[k] == white_colour]; widx = {k: i for i, k in enumerate(W)}
    G = [[0] * len(W) for _ in W]; mu = 0; detail = []
    for x, (a, b, c, d) in enumerate(pd):
        f = [fid[(x, p)] for p in range(4)]
        white02 = colour[f[0]] == white_colour
        eta, wi, wj = (-1, f[0], f[2]) if white02 else (1, f[1], f[3])
        positive = (d + 1) % n2 == b
        typeII = white02 != (not positive)
        if typeII: mu += eta
        i, j = widx[wi], widx[wj]
        if i != j: G[i][j] -= eta; G[j][i] -= eta; G[i][i] += eta; G[j][j] += eta
        detail.append((x, eta, "II" if typeII else "I", i, j))
    Gp = np.array([row[1:] for row in G[1:]], float)
    ev = np.linalg.eigvalsh(Gp) if len(Gp) else np.array([])
    assert np.all(np.abs(ev) > 1e-6), "Goeritz matrix singular?"
    sG = int((ev > 0).sum() - (ev < 0).sum())
    return sG - mu, dict(white=W, faces=F, colour=colour, G=np.array(G, int), mu=mu, signG=sG, detail=detail,
                         detG=round(abs(np.linalg.det(Gp))) if len(Gp) else 1)

def reduce_gauss(seq):
    """Remove Reidemeister-1 kinks and Reidemeister-2 pairs visible in the Gauss code; returns the reduced sequence
    and the list of moves."""
    seq = list(seq); moves = []
    while True:
        n2 = len(seq); done = False
        for k in range(n2):
            if seq[k][1] == seq[(k + 1) % n2][1]:
                moves.append(("R1", seq[k][1])); seq = [e for e in seq if e[1] != seq[k][1]]; done = True; break
        if done: continue
        for k in range(n2):
            a, b = seq[k], seq[(k + 1) % n2]
            if a[1] == b[1] or a[2] != b[2]: continue
            for m in range(n2):
                c, d = seq[m], seq[(m + 1) % n2]
                if m != k and {c[1], d[1]} == {a[1], b[1]} and c[2] == d[2] != a[2]:
                    moves.append(("R2", a[1], b[1])); seq = [e for e in seq if e[1] not in (a[1], b[1])]; done = True; break
            if done: break
        if not done: return seq, moves

def poly_str(V): return " ".join(f"{'+' if c > 0 else '-'} {abs(c)}t^{e}" for e, c in sorted(V.items()))

def r3_move(seq, pd, labels, triangle):
    """Reidemeister III on the triangular face bounded by the given crossing labels: on each of the three strands the
    two consecutive passages through the triangle swap places. Returns the new sequence (residues keep their passages)."""
    n2 = len(seq); F = faces(pd)
    tri = [f for f in F if sorted(labels[x] for x, p in f) == sorted(triangle)]
    assert len(tri) == 1, "triangle not found"; f = tri[0]
    edges = [pd[x][(p + 1) % 4] for x, p in f]
    strands = [(seq[(e - 1) % n2], seq[e]) for e in edges]
    kinds = ["".join(sorted((a[2], b[2]))) for a, b in strands]
    assert any(k in ("OO", "UU") for k in kinds), "no strand passes over or under both others: not a III move"
    new = list(seq)
    for e in edges: a, b = (e - 1) % n2, e % n2; new[a], new[b] = new[b], new[a]
    return new

def alternating(seq):
    w = [o for r, l, o, s in seq]; return all(w[i] != w[(i + 1) % len(w)] for i in range(len(w)))

def nugatory(seq):
    """crossing labels whose two passages cut the Gauss word into two closed halves (every crossing of one half
    appears twice in it): such a crossing is removable."""
    out = []
    for lab in sorted(set(l for r, l, o, s in seq)):
        i, j = [k for k, x in enumerate(seq) if x[1] == lab]
        inner = [x[1] for x in seq[i + 1:j]]
        if all(inner.count(c) == 2 for c in set(inner)): out.append(lab)
    return out

if __name__ == "__main__":
    text = TABLE
    p = pathlib.Path(__file__).with_name("stem.txt")
    if p.exists():
        rows_stem = parse(p.read_text()); assert rows_stem == parse(TABLE), "stem table differs from the embedded table"
    rows = parse(text); assert len(rows) == 13
    seq = gauss_from_rows(rows)
    print("Passages along the chain (residue:crossing O/U):", " ".join(f"{r}:{l}{o}" for r, l, o, s in seq))
    pd, labels = pd_from_gauss(seq); n = len(pd)
    F = faces(pd); assert len(F) == n + 2, "not a planar diagram"
    print(f"13-crossing diagram: {len(F)} faces = n + 2, planar; writhe {sum(signs(pd))}; alternating: {alternating(seq)}")
    A918 = lambda t: 4 * t**4 - 10 * t**3 + 13 * t**2 - 10 * t + 4
    vals = {t: alexander_at(pd, t) for t in (2, 3, 5, 7)}; ok = True
    for t, v in vals.items():
        q = Fraction(abs(v), A918(t)); ok &= (q.denominator == 1 and q.numerator in [t**k for k in range(14)]) or (q.numerator == 1 and q.denominator in [t**k for k in range(14)])
    det = abs(alexander_at(pd, -1))
    print(f"Alexander polynomial at t = 2, 3, 5, 7: {vals}; {'equals' if ok else 'DIFFERS FROM'} 4t^4 - 10t^3 + 13t^2 - 10t + 4 (the polynomial of 9_18) up to a unit; determinant {det}")
    assert ok and det == 41
    s0, i0 = gl_signature(pd, 0); s1, i1 = gl_signature(pd, 1)
    print(f"Signature (Gordon-Litherland): colour class 0 ({len(i0['white'])} regions): sign(G') {i0['signG']}, mu {i0['mu']}, sigma {s0}; class 1 ({len(i1['white'])} regions): sign(G') {i1['signG']}, mu {i1['mu']}, sigma {s1}")
    print("Goeritz matrix (class 1, first region deleted):"); print(i1["G"][1:, 1:])
    print("Crossing data (label, eta, type, regions):", [(labels[x], e, ty, i, j) for x, e, ty, i, j in i1["detail"]])
    assert s0 == s1 == 4
    print("9_18 has signature -4 and its mirror image +4: Alexander polynomial, determinant and signature all agree with the mirror image of 9_18. This is the trap (answer 9).")
    red, moves = reduce_gauss(seq); print("Reidemeister I/II moves visible in the table:", moves, "(none)" if not moves else "")
    assert not moves
    new = r3_move(seq, pd, labels, (10, 11, 12))
    new_idx = [(k, l, o, s) for k, (r, l, o, s) in enumerate(new)]
    pd2, lab2 = pd_from_gauss(new_idx); assert len(faces(pd2)) == n + 2
    print("After the Reidemeister III move on the triangle of crossings 10, 11, 12 (strand 150-160 passes over both 10 and 12, so it slides across crossing 11):")
    print("   Gauss word", " ".join(f"{l}{o}" for r, l, o, s in new), "(planar)")
    red2, moves2 = reduce_gauss(new_idx); print("   visible moves now:", moves2, "-> crossings", len(red2) // 2)
    assert moves2 == [("R2", 12, 13)] and len(red2) == 22
    pdr, labr = pd_from_gauss(red2); assert len(faces(pdr)) == len(pdr) + 2
    print("Reduced 11-crossing diagram:", " ".join(f"{l}{o}" for r, l, o, s in red2))
    print(f"   alternating: {alternating(red2)}; nugatory crossings: {nugatory(red2)}; writhe {sum(signs(pdr))}")
    assert alternating(red2) and not nugatory(red2)
    for name, P in (("13-crossing diagram", pd), ("11-crossing diagram", pdr)):
        V = kauffman_jones(P); print(f"Jones polynomial of the {name}: {poly_str(V)}; span {max(V) - min(V)}")
        assert max(V) - min(V) == 11
    print("Jones polynomial of 9_18: -t^-11 + 2t^-10 - 4t^-9 + 6t^-8 - 7t^-7 + 7t^-6 - 6t^-5 + 5t^-4 - 2t^-3 + t^-2 (span 9); the knot is not 9_18 or its mirror image.")
    print("A reduced alternating diagram has the minimal number of crossings (Kauffman, Murasugi, Thistlethwaite 1987), so the crossing number is 11; the Jones span 11 gives the lower bound 11 independently (span V <= crossing number for every knot).")
    print("KEY: minimal crossing number 11 (the knot is 11a246).")
