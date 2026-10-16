"""Verification of the answer key: the component survives 5 complete loading blocks (5.53 blocks).

Self-contained, Python standard library only.  Run: python3 verify_key.py

Model behind the figure.  Basquin fit sigma_a = A N^(-1/k) through the gridline crossings (5e4 cycles, 310 MPa)
and (2e6 cycles, 230 MPa): k = ln(40)/ln(310/230) = 12.358, A = 310 * (5e4)^(1/k) = 744.0 MPa; knee at
N_e = 1e7 cycles, fatigue limit sigma_e = A N_e^(-1/k) = 201.9 MPa, horizontal beyond the knee.  Failure
points drawn at 1.4e4, 3e4, 7e4, 1.5e5, 3.5e5, 7e5, 1.4e6, 3.5e6, 7e6 cycles on the fit, run-outs at 2e7
and 5e7.  Axes: cycles with 1-2-5 gridlines from 1e4 to 1e8, stress linear with gridlines every 10 MPa.
Question.  Blocks of 5000 cycles at 320 MPa and 5,000,000 cycles at 180 MPa, R = -1; linear damage rule,
Haibach extension below the fatigue limit (exponent 2k - 1 through the knee).  Complete blocks survived.

Route A: closed form with the fitted k and A.
Route B: regenerate the drawn curve numerically, locate the crossings of every horizontal gridline by
  bisection (confirming which crossings are exact and how far the others miss a vertical line), refit from the
  two exact crossings, and recompute the damage with the lives evaluated by root finding on the curve.
Also: the tempting wrong crossings, the wrong damage rules, and the rounding robustness of the integer.
"""
import math
NE = 1e7; BLOCK = [(5000, 320.0), (5_000_000, 180.0)]
XL = sorted(v * m for v in (1e4, 1e5, 1e6, 1e7) for m in (1, 2, 5)) + [1e8]
def fit(n1, s1, n2, s2):
    k = math.log(n2 / n1) / math.log(s1 / s2); return k, s1 * n1 ** (1 / k)
def life(k, A, s, se=None, rule="haibach"):
    se = A * NE ** (-1 / k) if se is None else se
    if s >= se: return (A / s) ** k
    if rule == "haibach": return NE * (se / s) ** (2 * k - 1)
    if rule == "elementary": return (A / s) ** k
    return float("inf")
def blocks(k, A, se=None, rule="haibach"):
    return 1 / sum(n / life(k, A, s, se, rule) for n, s in BLOCK)
# ---------------- Route A
k, A = fit(5e4, 310, 2e6, 230); se = A * NE ** (-1 / k)
nA, nB = life(k, A, 320), life(k, A, 180)
dA, dB = 5000 / nA, 5_000_000 / nB
print(f"ROUTE A: k = {k:.4f}, A = {A:.2f} MPa, sigma_e = {se:.2f} MPa")
print(f"   N(320 MPa) = (A/320)^k = {nA:.4g} cycles -> damage {dA:.4f} per block")
print(f"   N(180 MPa) by Haibach = N_e (sigma_e/180)^(2k-1) = {nB:.4g} cycles -> damage {dB:.4f} per block")
print(f"   damage per block {dA + dB:.4f}, blocks to failure {1/(dA+dB):.3f}, complete blocks {math.floor(1/(dA+dB))}")
keyA = math.floor(1 / (dA + dB)); assert keyA == 5
# ---------------- Route B: numeric reconstruction from the drawn curve
def curve(n): return A * n ** (-1 / k) if n <= NE else se
def cross_x(level):
    lo, hi = 1e4, NE
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if curve(mid) > level: lo = mid
        else: hi = mid
    return lo
print("\nROUTE B: crossings of the drawn curve with every horizontal gridline (10 MPa steps):")
exact = []
for level in range(210, 351, 10):
    x = cross_x(level)
    nearest = min(XL, key=lambda v: abs(math.log10(v / x)))
    lo = max(v for v in XL if v <= x); hi = min(v for v in XL if v > x); frac = min(math.log10(x / lo), math.log10(hi / x)) / math.log10(hi / lo)
    tag = "EXACT" if frac < 1e-6 else f"{100 * frac:.0f} percent of the step from {nearest:.0e}"
    print(f"   {level} MPa at N = {x:.5g}: {tag}")
    if frac < 1e-6: exact.append((nearest, level))
assert sorted(exact) == [(5e4, 310), (2e6, 230)]; exact = sorted(exact)
kB, AB = fit(*exact[0], *exact[1])
# lives by root finding on the regenerated curve
def life_curve(s):
    lo, hi = 1e4, NE
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if curve(mid) > s: lo = mid
        else: hi = mid
    return lo
nA_B = life_curve(320); seB = curve(NE); nB_B = NE * (seB / 180) ** (2 * kB - 1)
bB = 1 / (5000 / nA_B + 5_000_000 / nB_B)
print(f"   refit from the exact crossings: k = {kB:.4f}, A = {AB:.2f}; N(320) by root finding = {nA_B:.4g}; sigma_e = {seB:.2f}; N(180) = {nB_B:.4g}; blocks = {bB:.3f} -> {math.floor(bB)}")
assert math.floor(bB) == 5 and abs(bB - 1 / (dA + dB)) < 1e-6
# ---------------- tempting wrong crossings
print("\nTEMPTING WRONG CROSSINGS (one or both exact crossings replaced by the nearest major-line crossing):")
for (a1, b1), (a2, b2) in [((1e5, 290), (2e6, 230)), ((5e4, 310), (1e6, 240)), ((1e5, 290), (1e6, 240)), ((1e4, 350), (2e6, 230)), ((1e4, 350), (1e6, 240)), ((5e4, 310), (5e5, 260)), ((5e5, 260), (2e6, 230))]:
    kk, AA = fit(a1, b1, a2, b2); b = blocks(kk, AA)
    print(f"   ({a1:.0e}, {b1}) and ({a2:.0e}, {b2}): k = {kk:.3f}, A = {AA:.1f}, blocks {b:.2f} -> {math.floor(b)}")
# ---------------- wrong damage rules and rounding robustness
print("\nWRONG RULES: no damage below the fatigue limit (Miner original):", f"{blocks(k, A, rule='original'):.2f} -> {math.floor(blocks(k, A, rule='original'))}", "; same slope below the limit (elementary):", f"{blocks(k, A, rule='elementary'):.2f} -> {math.floor(blocks(k, A, rule='elementary'))}")
print("ROUNDING ROBUSTNESS of the integer:")
for kr in (12.3, 12.36, 12.4):
    for anc in ((5e4, 310), (2e6, 230)):
        Ar = anc[1] * anc[0] ** (1 / kr); print(f"   k = {kr}, A from {anc}: blocks {blocks(kr, Ar):.3f} -> {math.floor(blocks(kr, Ar))}")
for ser in (200.0, 202.0):
    print(f"   sigma_e rounded to {ser}: blocks {blocks(k, A, se=ser):.3f} -> {math.floor(blocks(k, A, se=ser))}")
print("\nALL CHECKS PASSED: 5 complete blocks.")
