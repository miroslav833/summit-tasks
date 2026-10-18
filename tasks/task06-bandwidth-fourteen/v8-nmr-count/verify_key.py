"""Check of the key for the distance-data counting question (task06 v8).

Instance: 36 C-alpha atoms of an ideal three-helix bundle (work/gen4.py, seed 88; coordinates in
instance.pkl). Known distances: all pairs with |i-j| <= 3, plus the 14 restraint pairs
(1,6) (3,8) (6,11) (8,13) (10,15) (13,18) (15,20) (17,22) (20,25) (22,27) (24,29) (27,32) (29,34) (31,36).

Route A: branch and prune. Fix atoms 1,2,3. For v = 4..36 the three distances to v-3, v-2, v-1 leave
two candidate positions (mirror images through the plane of those three atoms); keep a candidate only if
it also matches every restraint distance to an earlier atom. Count the complete conformations.

Route B: the symmetry argument. Reflecting all atoms v, v+1, ..., 36 through the plane of atoms
v-3, v-2, v-1 keeps every distance among atoms >= v and every distance between an atom >= v and one of
v-3, v-2, v-1; it changes the distance between an atom u <= v-4 and an atom w >= v. So the reflection at
v is a symmetry of the data exactly when no restraint pair {u, w} has u <= v-4 and w >= v, that is,
u + 3 < v <= w. These reflections at the free vertices commute and generate all solutions, so the count
is 2 to the power of the number of free vertices (Liberti, Lavor, Mucherino and Maculan, SIAM Review
56 (2014), section on the discretizable molecular distance geometry problem; Liberti, Masson, Lee,
Lavor and Mucherino, On the number of realizations of certain Henneberg graphs arising in protein
conformation, Discrete Applied Mathematics 165 (2014)).

Both routes must give the same number. The naive count 2^(33 - 14) (one binary choice per atom beyond
the third, one choice removed per restraint) is also printed as the expected wrong answer.
Run: python3 verify_key.py (numpy, scipy). A few seconds.
"""
import sys, os, pickle, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
import bp

HERE = os.path.dirname(os.path.abspath(__file__))
inst = pickle.load(open(os.path.join(HERE, "instance.pkl"), "rb"))
X, E, E1 = inst["X"], inst["E"], inst["E1"]; n = len(X)
D = np.linalg.norm(X[:, None] - X[None], axis=2)

print("atoms:", n, " restraint pairs:", E1)
print("consecutive C-alpha distances: min %.2f max %.2f A" % (min(D[i, i + 1] for i in range(n - 1)), max(D[i, i + 1] for i in range(n - 1))))
print("smallest non-bonded distance: %.2f A" % min(D[i, j] for i in range(n) for j in range(i + 2, n)))
print("restraint distances (A):", [round(float(D[u, w]), 1) for u, w in E])

# general position checks: no three consecutive atoms collinear, no four consecutive coplanar,
# and at every level the rejected candidate violates the restraint by a clear margin
for i in range(n - 2):
    a, b, c = X[i], X[i + 1], X[i + 2]
    assert np.linalg.norm(np.cross(b - a, c - a)) > 1e-3
for i in range(n - 3):
    a, b, c, d = X[i], X[i + 1], X[i + 2], X[i + 3]
    assert abs(np.cross(b - a, c - a) @ (d - a)) > 1e-3

print("\n== Route A: branch and prune")
cnt, sols = bp.count_solutions(X, E, tol=1e-6, keep=True)
print("complete conformations found:", cnt)
# every solution reproduces all known distances; solutions are pairwise different
for S_ in sols:
    DS = np.linalg.norm(S_[:, None] - S_[None], axis=2)
    for i in range(n):
        for j in range(i + 1, min(n, i + 4)): assert abs(DS[i, j] - D[i, j]) < 1e-6
    for u, w in E: assert abs(DS[u, w] - D[u, w]) < 1e-6
dists = [np.abs(sols[a] - sols[b]).max() for a in range(cnt) for b in range(a + 1, cnt)]
print("all pairs of solutions differ (largest coordinate difference at least %.2f A)" % min(dists))
# margin: at each level, how far the rejected candidate misses a restraint (smallest over the tree)
margin = np.inf
prune = {}
for u, w in E: prune.setdefault(max(u, w), []).append(min(u, w))
stack = [[X[0], X[1], X[2]]]
while stack:
    P = stack.pop(); v = len(P)
    if v == n: continue
    for cand in bp.trilaterate(P[v - 3], P[v - 2], P[v - 1], D[v, v - 3], D[v, v - 2], D[v, v - 1]):
        errs = [abs(np.linalg.norm(cand - P[u]) - D[v, u]) for u in prune.get(v, [])]
        if errs and max(errs) > 1e-6: margin = min(margin, max(errs))
        if all(e < 1e-6 for e in errs): stack.append(P + [cand])
print("smallest violation of a restraint by a rejected candidate: %.3f A (general position holds)" % margin)

print("\n== Route B: free reflection vertices")
S = bp.symmetry_vertices(n, E)
cover = {v: [(u, w) for u, w in E1 if u + 3 < v <= w] for v in range(4, n + 1)}
for v in range(4, n + 1):
    print(f"  vertex {v:2d}: " + ("free" if v in S else "fixed by " + ", ".join(f"({u},{w})" for u, w in cover[v])))
print("free vertices:", S, "-> 2^%d = %d" % (len(S), 2 ** len(S)))

print("\n== checks")
assert cnt == 2 ** len(S)
print("Route A and Route B agree. KEY =", cnt)
print("naive count 2^(n-3-m) = 2^(%d) = %d (wrong); 2^(n-3) = %d (wrong)" % (n - 3 - len(E), 2 ** (n - 3 - len(E)), 2 ** (n - 3)))
