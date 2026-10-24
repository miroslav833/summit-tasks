"""Goeritz data of the variant diagram as given (no reduction), for the written solution."""
import sys; sys.path.insert(0, ".."); import verify_key as V, numpy as np
tag = sys.argv[1]; white = int(sys.argv[2])
stem = open(f"../stem_{tag}.txt").read(); rows = V.parse(stem); seq = V.gauss_from_rows(rows); pd, labels = V.pd_from_gauss(seq); n = len(pd); n2 = 2 * n
s, info = V.gl_signature(pd, white); F, colour = info["faces"], info["colour"]
res = [x[0] for x in seq]
W = info["white"]
print("white regions (index: crossings in trace order; edges as residue pairs):")
for i, k in enumerate(W):
    f = F[k]; cr = [labels[x] for x, p in f]; ed = [f"{res[(pd[x][(p+1)%4]-1)%n2]}-{res[pd[x][(p+1)%4]]}" for x, p in f]
    print(f"  W{i}: crossings {cr}, edges {ed}")
print("other class:", [[labels[x] for x, p in F[k]] for k in range(len(F)) if colour[k] != white])
print("crossing: eta, type, white regions:", [(labels[x], e, ty, f"W{i}", f"W{j}") for x, e, ty, i, j in info["detail"]])
print("eta -1 at", sorted(labels[x] for x, e, ty, i, j in info["detail"] if e == -1), "| eta +1 at", sorted(labels[x] for x, e, ty, i, j in info["detail"] if e == 1))
print("type II:", [(labels[x], e) for x, e, ty, i, j in info["detail"] if ty == "II"], "mu", info["mu"])
G = info["G"][1:, 1:]; print("Goeritz (W0 deleted):"); print(G); ev = np.linalg.eigvalsh(G.astype(float)); print("eigenvalues", np.round(ev, 3), "sign", info["signG"], "det", round(np.linalg.det(G.astype(float))), "sigma", s)
