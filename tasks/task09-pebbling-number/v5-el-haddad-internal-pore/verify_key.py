"""Verification of the answer key: fatigue limit of the component with the internal pore, 120 MPa (2 s.f.; 120.1 MPa).

Self-contained, Python standard library only.  Run: python3 verify_key.py

Model behind the figure (metal injection moulded CP titanium, surface drilled holes, R = -1, 1e7 cycles):
  El Haddad relation with Murakami's sqrt(area) as the crack size,
      sigma_w(s) = sigma_w0 * sqrt(a0 / (s + a0)),   s = sqrt(area) in um,
  with sigma_w0 = 200 MPa (smooth fatigue limit, stress amplitude) and a0 = 200/3 um = 66.67 um for surface
  defects (Y = 0.65).  Equivalently DK_th = 0.65 * sigma_w0 * sqrt(pi a0) = 1.882 MPa sqrt(m) and
  sigma_w(s) = DK_th / (0.65 sqrt(pi (s + a0))).
  The curve passes exactly through the gridline crossings (200 um, 100 MPa) and (1000 um, 50 MPa) of the
  1-2-5 logarithmic grid and through no other crossing; the nearest misses are listed below.
Component: internal pore, sqrt(area) = 200 um, same material.  For an internal defect Y = 0.50, so the El
  Haddad length that reproduces the same smooth limit and the same threshold is
      a0_int = (DK_th / (0.50 sigma_w0))^2 / pi = a0 * (0.65/0.50)^2 = 1.69 a0 = 112.67 um,
  and the key is sigma_w0 * sqrt(a0_int / (200 + a0_int)) = 120.1 MPa.

Route A: from the two crossings, a0 = (50^2 * 1000 - 100^2 * 200) / (100^2 - 50^2) = 66.67 um,
  sigma_w0 = 100 * sqrt((200 + a0)/a0) = 200 MPa, then the key as above.
Route B: DK_th from the crossing (1000 um, 50 MPa) with the long-crack form, a0 from the smooth limit,
  then the internal value from DK_th / (0.50 sqrt(pi (s + a0_int))).
"""
import math
S1, Y1, S2, Y2 = 200.0, 100.0, 1000.0, 50.0
a0 = (Y2 ** 2 * S2 - Y1 ** 2 * S1) / (Y1 ** 2 - Y2 ** 2); sw0 = Y1 * math.sqrt((S1 + a0) / a0)
def curve(s, a=a0, w=sw0): return w * math.sqrt(a / (s + a))
print(f"a0 (surface) = {a0:.4f} um, sigma_w0 = {sw0:.4f} MPa")
DK = 0.65 * sw0 * math.sqrt(math.pi * a0 * 1e-6)
print(f"DK_th = 0.65 * sigma_w0 * sqrt(pi a0) = {DK:.4f} MPa sqrt(m)")
assert abs(curve(S1) - Y1) < 1e-9 and abs(curve(S2) - Y2) < 1e-9
# ---------------- Route A
a0i = a0 * (0.65 / 0.50) ** 2; keyA = sw0 * math.sqrt(a0i / (200 + a0i))
print(f"\nROUTE A: a0_int = 1.69 a0 = {a0i:.3f} um; key = 200 * sqrt({a0i:.3f}/(200 + {a0i:.3f})) = {keyA:.2f} MPa -> {round(keyA, -1):.0f} MPa (2 s.f.)")
# ---------------- Route B
a0i_B = (DK / (0.50 * sw0)) ** 2 / math.pi * 1e6
keyB = DK / (0.50 * math.sqrt(math.pi * (200 + a0i_B) * 1e-6))
print(f"ROUTE B: a0_int from the threshold = {a0i_B:.3f} um; key = DK_th / (0.50 sqrt(pi (200 + a0_int))) = {keyB:.2f} MPa")
assert abs(keyA - keyB) < 1e-9 and round(keyA, -1) == 120
# ---------------- crossings and near misses on the 1-2-5 grid
lines = sorted(set(v * m for v in (1, 10, 100, 1000) for m in (1, 2, 5)))
print("\nCURVE AT THE VERTICAL GRIDLINES (1-2-5 grid): value, nearest horizontal line, distance as a fraction of the log step")
for x in (20, 50, 100, 200, 500, 1000, 2000, 5000):
    y = curve(x); lo = max(l for l in lines if l <= y); hi = min(l for l in lines if l > y)
    step = math.log10(hi / lo); dlo, dhi = math.log10(y / lo), math.log10(hi / y)
    g = lo if dlo < dhi else hi; f = min(dlo, dhi) / step
    print(f"   x = {x:5d} um: {y:7.2f} MPa, nearest line {g}, {100 * f:.0f} percent of the step{'   EXACT' if f < 1e-9 else ''}")
# ---------------- decoy readings
print("\nDECOY READINGS (one crossing replaced by the nearest tempting crossing), answer by the correct method:")
def params(s1, y1, s2, y2):
    a = (y2 ** 2 * s2 - y1 ** 2 * s1) / (y1 ** 2 - y2 ** 2)
    return (a, y1 * math.sqrt((s1 + a) / a)) if a > 0 else (a, None)
for (s1, y1, s2, y2) in [(20, 200, 1000, 50), (100, 100, 1000, 50), (50, 200, 1000, 50), (200, 100, 500, 50), (200, 100, 2000, 50), (200, 100, 5000, 20)]:
    a, w = params(s1, y1, s2, y2)
    if a <= 0: print(f"   crossings ({s1}, {y1}) and ({s2}, {y2}): no El Haddad curve fits"); continue
    k = w * math.sqrt(1.69 * a / (200 + 1.69 * a))
    print(f"   crossings ({s1}, {y1}) and ({s2}, {y2}): a0 = {a:.1f} um, sigma_w0 = {w:.1f} MPa, answer {k:.1f} MPa -> {round(k, -1):.0f}")
# ---------------- wrong routes
print("\nWRONG ROUTES:")
print(f"   surface curve read at 200 um (ignores the internal position): {curve(200):.1f} MPa -> 100")
print(f"   internal factor 0.65/0.50 applied to the surface value, a0 kept: {1.3 * curve(200):.1f} MPa -> 130")
print(f"   smooth limit with no defect correction: {sw0:.1f} MPa -> 200")
print(f"   long-crack form only, internal factor, a0 ignored: {DK / (0.50 * math.sqrt(math.pi * 200e-6)):.1f} MPa -> 150")
print("\nALL CHECKS PASSED: key 120 MPa (120.1 MPa).")
