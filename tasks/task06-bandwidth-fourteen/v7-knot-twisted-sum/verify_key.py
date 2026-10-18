"""Check of the key for the twisted connected sum figure (task06 v7).

The backbone is a planar diagram built from the closed 2-braid s1^5 (the knot 5_1) and the closed
3-braid s1^2 s2^-1 s1 s2^-2 (the knot 6_3) joined through a neck with one crossing, then warped by a
smooth planar map (which keeps the diagram combinatorics), given a small depth wobble and drawn as a
tube. This script rebuilds the same curve (work/twisted_sum.py, work/render3.py parameters seed 11,
amplitude 0.035), extracts the crossings, and checks from the diagram alone:

  1. the diagram has 12 crossings and is alternating;
  2. exactly one crossing is nugatory (the Gauss word between its two visits is closed), so the
     diagram is not reduced and Tait's count does not apply to it;
  3. removing the neck twist (the same construction with a straight neck) gives an 11-crossing
     diagram that is alternating and has no nugatory crossing, hence reduced; by the
     Kauffman-Murasugi-Thistlethwaite theorem a reduced alternating diagram has minimal crossing
     number, so the knot has crossing number 11;
  4. consistency: the Jones polynomial of the figure's diagram equals V(5_1) V(6_3) (computed from
     the two closed braids), its span is 11, and the determinant is 65 = 5 x 13.
Run from the task folder: python3 verify_key.py (numpy, scipy, sympy). About two minutes.
"""
import sys, os, numpy as np, sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
import knotlib as K, altcheck as A, twisted_sum as T

t = sp.symbols("t")
def poly(j): return sp.expand(sum(c * t ** k for k, c in j.items()))

def figure_curve(seed=11, amp=0.035):
    rng = np.random.default_rng(seed)
    C = K.smooth(T.build(1, True, True), 3000)
    X = C[:, :2].copy(); L = np.ptp(X, axis=0).max(); W = np.zeros_like(X)
    for _ in range(5):
        kx, ky = rng.uniform(-1.2, 1.2, 2) * 2 * np.pi / L; ph = rng.uniform(0, 2 * np.pi, 2); a = rng.normal(0, amp * L, 2)
        W[:, 0] += a[0] * np.cos(kx * X[:, 0] + ky * X[:, 1] + ph[0]); W[:, 1] += a[1] * np.cos(kx * X[:, 0] + ky * X[:, 1] + ph[1])
    th = rng.uniform(-0.5, 0.5); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    X = (X + W) @ R.T; Z = C[:, 2].copy(); u = np.linspace(0, 2 * np.pi, len(C), endpoint=False)
    for m in range(1, 5): Z += 0.10 * rng.normal() * np.cos(m * u + rng.uniform(0, 2 * np.pi))
    return np.c_[X, Z]

if __name__ == "__main__":
    print("== the figure")
    D = K.diagram(figure_curve())
    gauss = A.gauss(D)
    print("crossings:", D["n"], " writhe:", D["writhe"])
    print("Gauss word (crossing, O/U):", " ".join(f"{c + 1}{'O' if o else 'U'}" for c, o in gauss))
    alt = A.alternating(D); nug = A.nugatory(D)
    print("alternating:", alt, " nugatory crossings:", [c + 1 for c in nug])
    J = K.jones(D["pd"], D["writhe"]); det = K.determinant(D["pd"])
    print("Jones:", K.jones_str(J), " span:", max(J) - min(J), " determinant:", det)

    print("\n== the same construction with a straight neck (the nugatory crossing removed)")
    D0 = K.diagram(K.smooth(T.build(1, True, False), 3000))
    alt0 = A.alternating(D0); nug0 = A.nugatory(D0); J0 = K.jones(D0["pd"], D0["writhe"])
    print("crossings:", D0["n"], " alternating:", alt0, " nugatory:", [c + 1 for c in nug0], " Jones span:", max(J0) - min(J0), " determinant:", K.determinant(D0["pd"]))

    print("\n== the two summands from their closed braids")
    D51 = K.diagram(K.smooth(K.build_braid_curve([1] * 5, 2), 900)); V51 = K.jones(D51["pd"], D51["writhe"])
    D63 = K.diagram(K.smooth(K.build_braid_curve([1, 1, -2, 1, -2, -2], 3), 900)); V63 = K.jones(D63["pd"], D63["writhe"])
    print("5_1: crossings", D51["n"], "alternating", A.alternating(D51), "reduced", not A.nugatory(D51), "det", K.determinant(D51["pd"]), "Jones", K.jones_str(V51))
    print("6_3: crossings", D63["n"], "alternating", A.alternating(D63), "reduced", not A.nugatory(D63), "det", K.determinant(D63["pd"]), "Jones", K.jones_str(V63))
    products = {sp.expand(poly(V51).subs(t, a) * poly(V63).subs(t, b)) for a in (t, 1 / t) for b in (t, 1 / t)}
    print("Jones(figure) = V(5_1) V(6_3) up to mirror:", poly(J) in products)

    print("\n== checks")
    assert D["n"] == 12 and alt and len(nug) == 1
    assert D0["n"] == 11 and alt0 and not nug0 and poly(J0) == poly(J)
    assert max(J) - min(J) == 11 and det == 65 and poly(J) in products
    print("12 crossings, alternating, one nugatory crossing; after removing it 11 crossings, alternating, reduced.")
    print("Reduced alternating diagrams are minimal (Kauffman, Murasugi, Thistlethwaite 1987), so c(K) = 11. KEY = 11")
    print("The naive count of the drawn crossings gives 12, the expected wrong answer.")
