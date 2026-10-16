"""Verification of the answer key: fatigue limit of the component with the internal pore, 200 MPa (2 s.f.; 201 MPa).

Self-contained, Python standard library only.  Run: python3 verify_key.py

The figure is generated from the model below (model.py / draw_figure.py use the same numbers), so every
plotted point is exact.

Model behind the figure (0.20 wt% O lot, 320 HV, surface drilled holes, R = -1, 1e7 cycles):
  small-defect branch (Murakami):  sigma_w = 1.43 (HV + 120) / (sqrt(area))^(1/6)   [MPa, sqrt(area) in um]
  long-crack branch:               sigma_w = DK_th / (0.65 sqrt(pi sqrt(area)))      [sqrt(area) in m]
  plotted fatigue limit = the smaller of the two.  DK_th is fixed by the gridline point (640 um, 150 MPa).
Component: 0.38 wt% O lot, 372 HV, largest pore internal, sqrt(area) = 600 um, R = -1, same long-crack
threshold.  Key = DK_th / (0.50 sqrt(pi * 600e-6)).

Route A: closed form from the defining point (640 um, 150 MPa): sigma = 150 * 0.65/0.50 * sqrt(640/600).
Route B: regenerate the eight plotted points from the model, recover DK_th by a least-squares fit of
  slope -1/2 through the points that lie on the long-crack branch, check the regime of the component's
  pore for the 372 HV lot, and evaluate the key numerically.  The wrong routes are evaluated as well.
"""
import math
HV_SPEC = 320; HV_COMP = 372
P_AREA = 640e-6; P_SIGMA = 150.0            # the gridline point that fixes the long-crack branch
DK_TH = P_SIGMA * 0.65 * math.sqrt(math.pi * P_AREA)
def small(hv, s_um, c=1.43): return c * (hv + 120) / s_um ** (1 / 6)
def longcrack(s_um, Y=0.65): return DK_TH / (Y * math.sqrt(math.pi * s_um * 1e-6))
POINTS = [20, 40, 80, 160, 320, 640, 1280, 2560]
print(f"DK_th from the point (640 um, 150 MPa): {DK_TH:.4f} MPa sqrt(m)")
print("plotted points (sqrt(area) um, fatigue limit MPa, branch):")
plotted = []
for s in POINTS:
    a, b = small(HV_SPEC, s), longcrack(s); v = min(a, b); plotted.append((s, v))
    print(f"   {s:5d}  {v:7.2f}   {'small-defect' if a < b else 'long-crack'}   (small {a:.2f}, long-crack {b:.2f})")
# knee of the specimen lot
lo, hi = 100.0, 1000.0
for _ in range(100):
    mid = math.sqrt(lo * hi)
    if small(HV_SPEC, mid) < longcrack(mid): lo = mid
    else: hi = mid
print(f"knee of the 320 HV lot (surface defects): sqrt(area) = {lo:.1f} um, {longcrack(lo):.1f} MPa")
# ---------------- Route A
keyA = P_SIGMA * (0.65 / 0.50) * math.sqrt(P_AREA / 600e-6)
print(f"\nROUTE A: key = 150 * 0.65/0.50 * sqrt(640/600) = {keyA:.2f} MPa -> {round(keyA, -1):.0f} MPa (2 s.f.)")
# ---------------- Route B
lc = [(s, v) for s, v in plotted if s >= 640]
# fit log(sigma) = c - 0.5 log(s): c = mean(log sigma + 0.5 log s)
c = sum(math.log(v) + 0.5 * math.log(s) for s, v in lc) / len(lc)
dk_fit = math.exp(c) * 0.65 * math.sqrt(math.pi * 1e-6)
print(f"ROUTE B: least-squares level of the slope -1/2 branch through {[s for s, v in lc]} um gives DK_th = {dk_fit:.4f} MPa sqrt(m)")
assert abs(dk_fit - DK_TH) < 1e-9
s_small_comp = small(HV_COMP, 600, c=1.56); s_long_comp = dk_fit / (0.50 * math.sqrt(math.pi * 600e-6))
print(f"   component, 372 HV lot, internal pore 600 um: small-defect branch (1.56, internal) {s_small_comp:.1f} MPa, long-crack branch (Y = 0.50) {s_long_comp:.1f} MPa; the smaller applies: {min(s_small_comp, s_long_comp):.2f} MPa")
keyB = min(s_small_comp, s_long_comp)
assert abs(keyA - keyB) < 1e-9 and round(keyB, -1) == 200
# knee of the component lot (internal defects)
lo, hi = 50.0, 2000.0
for _ in range(100):
    mid = math.sqrt(lo * hi)
    if small(HV_COMP, mid, 1.56) < dk_fit / (0.5 * math.sqrt(math.pi * mid * 1e-6)): lo = mid
    else: hi = mid
print(f"   knee of the 372 HV lot for internal defects: sqrt(area) = {lo:.1f} um; 600 um lies beyond it, in the long-crack regime")
print(f"ROUTE B: key = {keyB:.2f} MPa -> 200 MPa (2 s.f.)")
# ---------------- wrong routes
print("\nWRONG ROUTES:")
print(f"   surface factor 0.65 kept for the internal pore (reads the curve at 600 um): {longcrack(600):.1f} MPa -> 150")
print(f"   long-crack branch scaled with hardness (492/440) and internal factor: {keyA * (HV_COMP + 120) / (HV_SPEC + 120):.1f} MPa -> 230")
print(f"   small-defect law, internal constant 1.56, 372 HV: {small(HV_COMP, 600, 1.56):.1f} MPa -> 260")
print(f"   small-defect law, surface constant 1.43, 372 HV: {small(HV_COMP, 600, 1.43):.1f} MPa -> 240")
print(f"   small-defect law, surface constant, specimen hardness: {small(HV_SPEC, 600, 1.43):.1f} MPa -> 220")
print(f"   long-crack branch at 600 um, surface factor, scaled with hardness: {longcrack(600) * (HV_COMP + 120) / (HV_SPEC + 120):.1f} MPa -> 170")
print("\nALL CHECKS PASSED: key 200 MPa (201.4 MPa before rounding).")
