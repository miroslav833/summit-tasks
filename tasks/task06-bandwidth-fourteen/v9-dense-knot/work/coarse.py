"""Coarse knotted axis curve for the dense protein: closure of the 3-braid s1^3 s2 s1^-1 s2 (5_2)."""
import numpy as np, knotlib as K, torus2, sys, json
WORD = [1, 1, 1, 2, -1, 2]
def check_type():
    D = K.diagram(K.smooth(K.build_braid_curve(WORD, 3), 900))
    J = K.jones(D["pd"], D["writhe"]); print("planar closure: crossings", D["n"], "det", K.determinant(D["pd"]), "Jones", K.jones_str(J))
    return J
if __name__ == "__main__":
    J = check_type()
    # known V(5_2) (one chirality): -t^-6 + t^-5 - t^-4 + 2t^-3 - t^-2 + t^-1 ; mirror: t^6 ... 
    known = {-6: -1, -5: 1, -4: -1, -3: 2, -2: -1, -1: 1}
    print("matches 5_2:", J == known or J == {-k: v for k, v in known.items()})
    sm = torus2.curve(WORD, seed=int(sys.argv[1]) if len(sys.argv) > 1 else 2, amp=0.35, R0=3.0, dr=0.9, n=1600)
    D0 = K.diagram(sm); J0 = K.jones(D0["pd"], D0["writhe"]) if D0["n"] <= 14 else None
    print("torus curve top view: crossings", D0["n"], "Jones ok", J0 == J)
    np.save("coarse.npy", sm)
