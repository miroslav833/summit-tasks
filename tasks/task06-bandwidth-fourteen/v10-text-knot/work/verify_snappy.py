"""Independent identification of the knot in the stem's table with SnapPy (hyperbolic census) and knot Floer homology."""
import sys, snappy, spherogram, numpy as np
sys.path.insert(0, ".."); import verify_key as V
rows = V.parse(V.TABLE); seq = V.gauss_from_rows(rows); pd, labels = V.pd_from_gauss(seq)
L = spherogram.Link([list(x) for x in pd]); print("crossings", len(L.crossings))
M = L.exterior(); print("identify:", M.identify(), "volume", round(M.volume(), 6))
M9 = spherogram.Link("9_18").exterior(); print("9_18 for comparison: identify", M9.identify(), "volume", round(M9.volume(), 6))

Vm = np.array(L.seifert_matrix(), float); ev = np.linalg.eigvalsh(Vm + Vm.T); print("signature from Seifert matrix:", int((ev > 1e-9).sum() - (ev < -1e-9).sum()))
