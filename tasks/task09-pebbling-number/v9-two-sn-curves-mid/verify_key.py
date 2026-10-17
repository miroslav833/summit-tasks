"""Verification of the answer key: the component survives 7 complete loading blocks (7.68 blocks).

Self-contained, Python standard library only.  Run: python3 verify_key.py

Model behind the figure.  Two Basquin fits sigma_a = A N^(-1/k), knee at N_e = 1e7 with the fatigue limit
sigma_e = A N_e^(-1/k), horizontal beyond the knee.
  R = -1 (solid):  through the gridline crossings (1e5, 240) and (5e5, 210): k1 = 12.053, A1 = 623.8, sigma_e1 = 163.8.
  R = 0.1 (dashed): through the gridline crossings (2e4, 200) and (1e6, 150): k2 = 13.598, A2 = 414.3, sigma_e2 = 126.6.
  The curves are drawn from 1.3e4 cycles, where they are at 284.3 and 206.4 MPa, so neither end nor knee lies on a gridline.
Axes: cycles with 1-2-5 gridlines from 1e4 to 1e8, stress linear with gridlines every 10 MPa.
Question.  Blocks of 20,000 cycles at 220 MPa (R = -1), 10,000 cycles at 170 MPa (R = 0.1), 2,000,000 cycles
at 140 MPa (R = -1).  Linear damage, Haibach extension below a fatigue limit (exponent 2k - 1 through the knee).

Route A: closed form with the fitted parameters.
Route B: regenerate both drawn curves, locate the crossings of every horizontal gridline by bisection
  (confirming the exact crossings and how far the others miss), refit, and evaluate the lives by root finding.
Also: tempting wrong crossings on either curve, wrong damage rules, rounding robustness of the integer.
"""
import math
NE = 1e7
BLOCK = [(20000, 220.0, -1), (10000, 170.0, 0.1), (2_000_000, 140.0, -1)]
XL = sorted(v * m for v in (1e4, 1e5, 1e6, 1e7) for m in (1, 2, 5)) + [1e8]
def fit(n1, s1, n2, s2):
    k = math.log(n2 / n1) / math.log(s1 / s2); return k, s1 * n1 ** (1 / k)
def blocks(p1, p2, rule="haibach", se_over=None):
    D = 0
    for n, s, R in BLOCK:
        k, a = p1 if R == -1 else p2
        se = a * NE ** (-1 / k)
        if se_over and R in se_over: se = se_over[R]
        if s >= se: D += n / (a / s) ** k
        elif rule == "haibach": D += n / (NE * (se / s) ** (2 * k - 1))
        elif rule == "elementary": D += n / (a / s) ** k
    return 1 / D
P1, P2 = fit(1e5, 240, 5e5, 210), fit(2e4, 200, 1e6, 150)
(k1, A1), (k2, A2) = P1, P2; se1, se2 = A1 * NE ** (-1 / k1), A2 * NE ** (-1 / k2)
print(f"ROUTE A: R = -1: k1 = {k1:.4f}, A1 = {A1:.2f}, sigma_e1 = {se1:.2f};  R = 0.1: k2 = {k2:.4f}, A2 = {A2:.2f}, sigma_e2 = {se2:.2f}")
parts = []
for n, s, R in BLOCK:
    k, a, se = (k1, A1, se1) if R == -1 else (k2, A2, se2)
    N = (a / s) ** k if s >= se else NE * (se / s) ** (2 * k - 1)
    parts.append(n / N); print(f"   {n} cycles at {s} MPa, R = {R}: {'Basquin' if s >= se else 'Haibach'} life {N:.4g}, damage {n / N:.5f}")
D = sum(parts); bA = 1 / D
print(f"   damage per block {D:.5f}, blocks to failure {bA:.3f}, complete blocks {math.floor(bA)}")
assert math.floor(bA) == 7
# ---------------- Route B
def curve(p, n):
    k, a = p; se = a * NE ** (-1 / k); return a * n ** (-1 / k) if n <= NE else se
def cross_x(p, level):
    lo, hi = 1.3e4, NE
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if curve(p, mid) > level: lo = mid
        else: hi = mid
    return lo
print("\nROUTE B: crossings of the drawn curves with the horizontal gridlines (distance to the nearest vertical line as a fraction of the step):")
exact = {}
for name, p, lo_level, hi_level in (("R = -1", P1, 170, 280), ("R = 0.1", P2, 130, 200)):
    exact[name] = []
    for level in range(lo_level, hi_level + 1, 10):
        x = cross_x(p, level); nearest = min(XL, key=lambda v: abs(math.log10(v / x)))
        lo = max(v for v in XL if v <= x); hi = min(v for v in XL if v > x); frac = min(math.log10(x / lo), math.log10(hi / x)) / math.log10(hi / lo)
        print(f"   {name}: {level} MPa at N = {x:.5g}: {'EXACT' if frac < 1e-6 else f'{100 * frac:.0f} percent from {nearest:.0e}'}")
        if frac < 1e-6: exact[name].append((nearest, level))
assert sorted(exact["R = -1"]) == [(1e5, 240), (5e5, 210)] and sorted(exact["R = 0.1"]) == [(2e4, 200), (1e6, 150)]
P1b, P2b = fit(*sorted(exact["R = -1"])[0], *sorted(exact["R = -1"])[1]), fit(*sorted(exact["R = 0.1"])[0], *sorted(exact["R = 0.1"])[1])
def life_curve(p, s):
    lo, hi = 1.3e4, NE
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if curve(p, mid) > s: lo = mid
        else: hi = mid
    return lo
D_B = 20000 / life_curve(P1b, 220) + 10000 / life_curve(P2b, 170) + 2_000_000 / (NE * (curve(P1b, NE) / 140) ** (2 * P1b[0] - 1))
print(f"   refit and root finding: blocks = {1 / D_B:.3f} -> {math.floor(1 / D_B)}")
assert abs(1 / D_B - bA) < 1e-6
# ---------------- decoys
print("\nTEMPTING WRONG CROSSINGS:")
for d in [((1e5, 240), (1e6, 200)), ((2e5, 230), (5e5, 210)), ((2e5, 230), (1e6, 200)), ((5e4, 250), (5e5, 210)), ((1e5, 240), (2e6, 190))]:
    b = blocks(fit(*d[0], *d[1]), P2); print(f"   R = -1 read as {d[0]} and {d[1]}: blocks {b:.2f} -> {math.floor(b)}")
for d in [((1e5, 180), (1e6, 150)), ((2e4, 200), (5e5, 160)), ((1e5, 180), (5e5, 160)), ((2e4, 200), (2e5, 170)), ((5e4, 190), (1e6, 150))]:
    b = blocks(P1, fit(*d[0], *d[1])); print(f"   R = 0.1 read as {d[0]} and {d[1]}: blocks {b:.2f} -> {math.floor(b)}")
print("\nWRONG RULES: no damage below the limit:", f"{blocks(P1, P2, 'original'):.2f} -> {math.floor(blocks(P1, P2, 'original'))}", "; same exponent below the limit:", f"{blocks(P1, P2, 'elementary'):.2f} -> {math.floor(blocks(P1, P2, 'elementary'))}")
print("ROUNDING ROBUSTNESS:")
for dk1 in (-0.05, 0.05):
    for dk2 in (-0.05, 0.05):
        for anc1 in ((1e5, 240), (5e5, 210)):
            for anc2 in ((2e4, 200), (1e6, 150)):
                kk1, kk2 = k1 + dk1, k2 + dk2; b = blocks((kk1, anc1[1] * anc1[0] ** (1 / kk1)), (kk2, anc2[1] * anc2[0] ** (1 / kk2)))
                assert math.floor(b) == 7
print("   k1 and k2 each rounded by +-0.05 with A refitted from either crossing: all 16 cases give 7")
for so in ({-1: 160.0}, {-1: 170.0}, {0.1: 120.0}, {0.1: 130.0}, {-1: 160.0, 0.1: 130.0}):
    b = blocks(P1, P2, se_over=so); print(f"   fatigue limits rounded to {so}: blocks {b:.3f} -> {math.floor(b)}"); assert math.floor(b) == 7
print("\nALL CHECKS PASSED: 7 complete blocks.")
