"""Verification of the answer key: the component survives 7 complete repetitions of the history (7.72).

Self-contained, Python standard library only.  Run: python3 verify_key.py

History (one period, 24 reversals, MPa, as drawn): see HIST below.  Material: sigma_a = 450 N^(-1/8) (MPa).
Counting: rainflow for repeating histories (ASTM E1049-85, section 5.4.5): the period is rearranged to start at
its largest peak and every closed cycle is a full cycle.  Mean stress neglected.  Linear damage, failure at 1.

Route A: the three-point rainflow rule of ASTM E1049 applied to the rearranged history.
Route B: an independently written four-point algorithm (a cycle is extracted whenever an inner range is
  enclosed by its two neighbours), with the largest cycle closed from the residue.
Both give the same cycle list; the damage per period and the number of repetitions follow.
Wrong procedures evaluated: the half-cycle variant applied to the period as given (ASTM 5.4.4), simple range
  pair counting, residue counted as full cycles, residue ignored, and the largest range alone.
"""
import math
from collections import Counter
HIST = [-175, 150, -150, 375, 150, 325, -175, 300, -50, 325, 150, 325, 300, 350, -125, 275, -200, 400, -200, 375, 50, 150, -200, 375]
A, K = 450.0, 8.0
def life(amp): return (A / amp) ** K
def peaks_valleys(x):
    pv = [x[0]]
    for i in range(1, len(x) - 1):
        if (x[i] - x[i - 1]) * (x[i + 1] - x[i]) < 0: pv.append(x[i])
    pv.append(x[-1]); return pv
def rotate_to_max(pv):
    i = max(range(len(pv)), key=lambda j: pv[j]); seq = pv[i:] + pv[:i] + [pv[i]]
    out = [seq[0]]
    for v in seq[1:]:
        if v != out[-1]: out.append(v)
    return out
def astm_repeating(x):
    pts = rotate_to_max(peaks_valleys(x)); stack = []; cycles = []
    for p in pts:
        stack.append(p)
        while len(stack) >= 3:
            X = abs(stack[-1] - stack[-2]); Y = abs(stack[-2] - stack[-3])
            if X < Y: break
            cycles.append((Y, (stack[-2] + stack[-3]) / 2, 1.0)); del stack[-3:-1]
    assert all(v == max(pts) for v in stack) and len(stack) <= 2, ("residue left", stack)
    return cycles
def four_point_repeating(x):
    seq = rotate_to_max(peaks_valleys(x)); cycles = []; changed = True
    while changed:
        changed = False
        for i in range(len(seq) - 3):
            a, b, c, d = seq[i:i + 4]
            if abs(c - b) <= abs(b - a) and abs(c - b) <= abs(d - c):
                cycles.append((abs(c - b), (b + c) / 2, 1.0)); del seq[i + 1:i + 3]; changed = True; break
    if len(seq) == 3 and seq[0] == seq[2]:
        cycles.append((abs(seq[1] - seq[0]), (seq[0] + seq[1]) / 2, 1.0)); seq = [seq[0]]
    assert all(v == seq[0] for v in seq) and len(seq) <= 2, ("residue left", seq)
    return cycles
def astm_as_given(x):
    pts = peaks_valleys(x); stack = []; cycles = []
    for p in pts:
        stack.append(p)
        while len(stack) >= 3:
            X = abs(stack[-1] - stack[-2]); Y = abs(stack[-2] - stack[-3])
            if X < Y: break
            if len(stack) == 3: cycles.append((Y, (stack[0] + stack[1]) / 2, 0.5)); stack.pop(0)
            else: cycles.append((Y, (stack[-2] + stack[-3]) / 2, 1.0)); del stack[-3:-1]
    for i in range(len(stack) - 1): cycles.append((abs(stack[i + 1] - stack[i]), (stack[i] + stack[i + 1]) / 2, 0.5))
    return cycles
def summary(c):
    s = Counter()
    for r, m, n in c: s[(r, m)] += n
    return dict(sorted(s.items(), reverse=True))
def damage(c): return sum(n / life(r / 2) for r, m, n in c if r > 0)
pv = peaks_valleys(HIST); assert pv == HIST and len(HIST) == 24 and HIST.count(max(HIST)) == 1
print("history (24 reversals):", HIST)
print("rearranged to start at the largest peak (400):", rotate_to_max(HIST))
cA, cB = astm_repeating(HIST), four_point_repeating(HIST)
print("\nROUTE A (ASTM three-point rule on the rearranged period), cycles (range, mean): count")
for (r, m), n in summary(cA).items(): print(f"   range {r:4.0f}  mean {m:7.1f}  count {n}   amplitude {r/2:6.1f}  N = {life(r/2):.4g}  damage {n / life(r/2):.5f}")
print("ROUTE B (four-point algorithm):", "identical cycle list" if summary(cA) == summary(cB) else "DIFFERENT")
assert summary(cA) == summary(cB) and sum(n for _, _, n in cA) == 12
D = damage(cA); print(f"\ndamage per period D = {D:.5f}; repetitions to failure 1/D = {1/D:.3f}; complete repetitions {math.floor(1/D)}")
assert math.floor(1 / D) == 7
print("\nWRONG PROCEDURES:")
w = {}
w["half-cycle variant on the period as given (ASTM 5.4.4)"] = damage(astm_as_given(HIST))
w["range pair counting (every successive reversal pair a half cycle)"] = sum(0.5 / life(abs(pv[i+1] - pv[i]) / 2) for i in range(len(pv) - 1))
w["half-cycle variant with the residue counted as full cycles"] = sum((1.0 if n == 0.5 else n) / life(r / 2) for r, m, n in astm_as_given(HIST))
w["half-cycle variant with the residue ignored"] = sum(n / life(r / 2) for r, m, n in astm_as_given(HIST) if n == 1.0)
w["largest range only, once per period"] = 1 / life((max(pv) - min(pv)) / 2)
for k, v in w.items(): print(f"   {k}: D = {v:.5f}, repetitions {1/v:.2f} -> {math.floor(1/v)}")
print("   half-cycle variant cycle list:", summary(astm_as_given(HIST)))
print("\nALL CHECKS PASSED: 7 complete repetitions.")
