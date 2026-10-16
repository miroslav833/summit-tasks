"""Verification of the answer key: fatigue limit of the component with the internal pore, 200 MPa (2 s.f.; 200.0 MPa).

Self-contained, Python standard library only.  Run: python3 verify_key.py

The figure is generated from the model below (draw_figure.py uses the same numbers), so every plotted
point is exact.

Model behind the figure (0.20 wt% O lot, 320 HV, surface drilled holes, R = -1, 1e7 cycles):
  small-defect branch (Murakami):  sigma_w = 1.43 (HV + 120) / (sqrt(area))^(1/6)   [MPa, sqrt(area) in um]
  long-crack branch:               sigma_w = DK_th / (0.65 sqrt(pi sqrt(area)))      [sqrt(area) in m]
  plotted fatigue limit = the smaller of the two.  DK_th is chosen so that the component value is exactly
  200.0 MPa: DK_th = 200 * 0.50 * sqrt(pi * 600e-6) = 4.3416 MPa sqrt(m).
Component: 0.38 wt% O lot, 372 HV, largest pore internal, sqrt(area) = 600 um, R = -1, same long-crack
threshold.  Key = DK_th / (0.50 sqrt(pi * 600e-6)) = 200.0 MPa.

Route A: closed form from any plotted long-crack point (s, v): key = v * (0.65/0.50) * sqrt(s/600).
Route B: regenerate the plotted points, recover DK_th by a least-squares fit of slope -1/2 through the
  points on the long-crack branch, check the regime of the component's pore for the 372 HV lot, evaluate.
Reading sensitivity: the key is linear in the reading of the steep branch, so a reading error of x percent
  moves the key by x percent; the band that rounds to 200 is 195 to 205, i.e. readings within 2.5 percent.
  Linear interpolation between the neighbouring gridlines of the logarithmic axis (a common misreading) is
  evaluated for every plotted point.
"""
import math
HV_SPEC = 320; HV_COMP = 372; S_COMP = 600e-6
DK_TH = 200.0 * 0.50 * math.sqrt(math.pi * S_COMP)
def small(hv, s_um, c=1.43): return c * (hv + 120) / s_um ** (1 / 6)
def longcrack(s_um, Y=0.65, dk=DK_TH): return dk / (Y * math.sqrt(math.pi * s_um * 1e-6))
POINTS = [25, 50, 90, 170, 480, 650, 850, 1100]
print(f"DK_th (fixed so that the component value is 200.0 MPa): {DK_TH:.4f} MPa sqrt(m)")
print("plotted points (sqrt(area) um, fatigue limit MPa, branch):")
plotted = []
for s in POINTS:
    a, b = small(HV_SPEC, s), longcrack(s); v = min(a, b); plotted.append((s, v))
    print(f"   {s:5d}  {v:7.2f}   {'small-defect' if a < b else 'long-crack'}   (small {a:.2f}, long-crack {b:.2f})")
lo, hi = 100.0, 1000.0
for _ in range(100):
    mid = math.sqrt(lo * hi)
    if small(HV_SPEC, mid) < longcrack(mid): lo = mid
    else: hi = mid
print(f"knee of the 320 HV lot (surface defects): sqrt(area) = {lo:.1f} um, {longcrack(lo):.1f} MPa")
# ---------------- Route A from each long-crack point
print("\nROUTE A: key from each plotted long-crack point, v * 0.65/0.50 * sqrt(s/600):")
for s, v in plotted:
    if s >= 480: print(f"   ({s} um, {v:.2f} MPa) -> {v * 1.3 * math.sqrt(s / 600):.2f} MPa")
keyA = 200.0
# ---------------- Route B
lc = [(s, v) for s, v in plotted if s >= 480]
c = sum(math.log(v) + 0.5 * math.log(s) for s, v in lc) / len(lc)
dk_fit = math.exp(c) * 0.65 * math.sqrt(math.pi * 1e-6)
print(f"ROUTE B: least-squares level of the slope -1/2 branch through {[s for s, v in lc]} um gives DK_th = {dk_fit:.4f} MPa sqrt(m)")
assert abs(dk_fit - DK_TH) < 1e-9
s_small_comp = small(HV_COMP, 600, c=1.56); s_long_comp = dk_fit / (0.50 * math.sqrt(math.pi * S_COMP))
print(f"   component, 372 HV lot, internal pore 600 um: small-defect branch (1.56, internal) {s_small_comp:.1f} MPa, long-crack branch (Y = 0.50) {s_long_comp:.1f} MPa; the smaller applies: {min(s_small_comp, s_long_comp):.2f} MPa")
keyB = min(s_small_comp, s_long_comp); assert abs(keyB - 200.0) < 1e-9
lo, hi = 50.0, 2000.0
for _ in range(100):
    mid = math.sqrt(lo * hi)
    if small(HV_COMP, mid, 1.56) < dk_fit / (0.5 * math.sqrt(math.pi * mid * 1e-6)): lo = mid
    else: hi = mid
print(f"   knee of the 372 HV lot for internal defects: sqrt(area) = {lo:.1f} um; 600 um lies beyond it")
print("ROUTE B: key = 200.00 MPa -> 200 MPa (2 s.f.)")
# ---------------- reading sensitivity: linear interpolation between decade gridlines
def linear_misread(v):
    # linear interpolation between the two neighbouring gridlines (minor gridlines at 2..9 times the decade)
    d = 10 ** math.floor(math.log10(v)); k = math.floor(v / d); lo_, hi_ = k * d, (k + 1) * d
    frac = (math.log10(v) - math.log10(lo_)) / (math.log10(hi_) - math.log10(lo_))
    return lo_ + frac * (hi_ - lo_)
print("\nREADING: value read by linear interpolation between the neighbouring gridlines of the logarithmic y axis, and the key it gives:")
for s, v in lc:
    m = linear_misread(v); print(f"   true {v:.1f} at {s} um -> linear read {m:.1f} -> key {m * 1.3 * math.sqrt(s / 600):.1f} MPa")
print("   band of readings of the 650 um point that still round to 200:", f"{195 / (1.3 * math.sqrt(650 / 600)):.1f} to {205 / (1.3 * math.sqrt(650 / 600)):.1f} MPa (true {longcrack(650):.1f})")
# ---------------- wrong routes
print("\nWRONG ROUTES:")
print(f"   surface factor 0.65 kept for the internal pore: {longcrack(600):.1f} MPa -> 150")
print(f"   long-crack branch scaled with hardness (492/440), internal factor: {200.0 * (HV_COMP + 120) / (HV_SPEC + 120):.1f} MPa -> 220")
print(f"   small-defect law, internal constant 1.56, 372 HV: {small(HV_COMP, 600, 1.56):.1f} MPa -> 260")
print(f"   small-defect law, surface constant 1.43, 372 HV: {small(HV_COMP, 600, 1.43):.1f} MPa -> 240")
print(f"   small-defect law, surface constant, specimen hardness: {small(HV_SPEC, 600, 1.43):.1f} MPa -> 220")
print(f"   long-crack branch, surface factor, scaled with hardness: {longcrack(600) * (HV_COMP + 120) / (HV_SPEC + 120):.1f} MPa -> 170")
print("\nALL CHECKS PASSED: key 200 MPa (200.0 MPa).")
