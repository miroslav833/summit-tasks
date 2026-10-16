import json, zipfile, pathlib, textwrap, subprocess, sys, math
HERE = pathlib.Path(__file__).parent
SLUG = "crack-growth-closure-two-load-ratios"
question = r"""The figure shows fatigue crack growth data for long cracks in a metal injection moulded Ti-6Al-7Nb alloy: the crack growth rate $da/dN$ against the stress intensity factor range $\Delta K$ on logarithmic axes, measured at the load ratios $R = 0.1$ and $R = 0.7$. The dashed line is the Paris-law fit to the straight part of the $R = 0.7$ data; the thin solid line through the $R = 0.1$ data only guides the eye. The difference between the two data sets is caused by crack closure. Assume that the crack-opening stress intensity factor $K_{op}$ has the same constant value at every load ratio at which closure occurs, independent of $K_{max}$, that closure is absent when $K_{min} \ge K_{op}$, and that the growth rate depends only on the effective range $\Delta K_{eff} = K_{max} - \max(K_{op}, K_{min})$.

A wide plate of the same material carries a constant-amplitude cyclic stress with $\sigma_{max} = 400$ MPa at $R = 0.4$. A surface pore is treated as an edge crack of initial length $a_0 = 0.20$ mm, with the geometry factor $Y = 1.12$ taken as constant, so that $K = Y \sigma \sqrt{\pi a}$. The plate fails when $K_{max}$ reaches the fracture toughness $K_{IC} = 55$ MPa$\sqrt{\mathrm{m}}$. Take the dashed Paris fit as the relation between $da/dN$ and $\Delta K_{eff}$ for the whole of the crack growth, and ignore the deviation of the data near the threshold.

Find the number of cycles from $a_0$ to failure. Give the answer to two significant figures."""
C = 1.0e-12; m = 3; Y = 1.12; a0 = 0.20e-3; smax = 400.0; R = 0.4; KIC = 55.0; Kop = 6.0
ds = smax * (1 - R); B = Y * smax * math.sqrt(math.pi); A = Y * ds * math.sqrt(math.pi)
ac = (KIC / (Y * smax)) ** 2 / math.pi; at = (Kop / R / B) ** 2
F = lambda w: -1.0 / w - Kop / (2 * w * w)
w0 = B * math.sqrt(a0) - Kop; wt = B * math.sqrt(at) - Kop
N1 = 2.0 / (C * B * B) * (F(wt) - F(w0)); N2 = 2.0 / (C * A ** 3) * (at ** -0.5 - ac ** -0.5); N = N1 + N2
Nfree = 2.0 / (C * A ** 3) * (a0 ** -0.5 - ac ** -0.5)
final_answer = r"$1.2 \times 10^{6}$ cycles"
variants = ["1.2e6 cycles", "1200000 cycles", r"$1.2 \times 10^6$", "1.2 million cycles", "1.2E+06"]
solution = rf"""Step 1: Read the closure-free growth law from the figure.
The dashed Paris fit of the $R = 0.7$ data passes through the grid intersections $da/dN = 10^{{-9}}$ m/cycle at $\Delta K = 10$ MPa$\sqrt{{\mathrm{{m}}}}$ and $da/dN = 10^{{-6}}$ m/cycle at $\Delta K = 100$ MPa$\sqrt{{\mathrm{{m}}}}$, so $m = 3$ and $C = 10^{{-9}}/10^{{3}} = 1.0 \times 10^{{-12}}$ m/cycle per (MPa$\sqrt{{\mathrm{{m}}}}$)$^{{3}}$. At $R = 0.7$, $K_{{min}} = 0.7\,K_{{max}}$ is far above any opening level that could explain the $R = 0.1$ data, so this fit is the closure-free law $da/dN = C\,\Delta K_{{eff}}^{{3}}$.

Step 2: Infer the opening level from the two data sets.
The $R = 0.1$ data are not a parallel line: they lie to the right of the $R = 0.7$ data by a gap that shrinks with $\Delta K$ and closes above $\Delta K \approx 54$ MPa$\sqrt{{\mathrm{{m}}}}$, which is the signature of a constant $K_{{op}}$. With closure, $\Delta K_{{eff}} = K_{{max}} - K_{{op}}$ and at $R = 0.1$, $K_{{max}} = \Delta K/0.9$, so points of equal growth rate satisfy $\Delta K_{{0.1}} = 0.9\,(\Delta K_{{eff}} + K_{{op}})$. Pairs of equal rate read from the plot are $\Delta K_{{eff}} = 4$ against $\Delta K_{{0.1}} = 9$, $14$ against $18$, $24$ against $27$, $34$ against $36$ and $44$ against $45$, each giving $K_{{op}} = \Delta K_{{0.1}}/0.9 - \Delta K_{{eff}} = 6$ MPa$\sqrt{{\mathrm{{m}}}}$. The merging point confirms it: closure vanishes at $R = 0.1$ when $K_{{min}} = \Delta K/9$ reaches $K_{{op}}$, that is at $\Delta K = 54$ MPa$\sqrt{{\mathrm{{m}}}}$.

Step 3: The decisive step: at $R = 0.4$ closure is present at first and disappears during the growth.
With $K_{{max}} = Y \sigma_{{max}} \sqrt{{\pi a}} = {B:.1f}\sqrt{{a}}$ (MPa$\sqrt{{\mathrm{{m}}}}$, $a$ in m), the initial crack has $K_{{max}} = {B*math.sqrt(a0):.2f}$ and $K_{{min}} = 0.4\,K_{{max}} = {0.4*B*math.sqrt(a0):.2f}$ MPa$\sqrt{{\mathrm{{m}}}}$, below $K_{{op}} = 6$: the crack closes during part of every cycle and $\Delta K_{{eff}} = K_{{max}} - 6 = {B*math.sqrt(a0)-Kop:.2f}$ MPa$\sqrt{{\mathrm{{m}}}}$ at $a_0$, above the threshold of the closure-free data. $K_{{min}}$ grows with the crack and reaches $K_{{op}}$ when $K_{{max}} = K_{{op}}/R = 15$ MPa$\sqrt{{\mathrm{{m}}}}$, at $a_t = \dfrac{{1}}{{\pi}}\left(\dfrac{{15}}{{1.12 \times 400}}\right)^{{2}} = {at*1e3:.3f}$ mm. Beyond $a_t$ the crack is closure-free and $\Delta K_{{eff}} = \Delta K = Y \Delta\sigma \sqrt{{\pi a}}$ with $\Delta\sigma = {ds:.0f}$ MPa. The life is the sum of the two parts; ignoring the closure altogether, or keeping $\Delta K_{{eff}} = K_{{max}} - K_{{op}}$ after $a_t$ (where it would exceed $\Delta K$), both give wrong lives.

Step 4: Critical crack length.
Failure occurs when $K_{{max}} = K_{{IC}}$: $a_c = \dfrac{{1}}{{\pi}}\left(\dfrac{{55}}{{1.12 \times 400}}\right)^{{2}} = {ac*1e3:.3f}$ mm (with $\Delta\sigma$ in place of $\sigma_{{max}}$ one would get $13.3$ mm, which is wrong). The closure-free part runs from $\Delta K = {A*math.sqrt(at):.2f}$ to $\Delta K = {A*math.sqrt(ac):.1f}$ MPa$\sqrt{{\mathrm{{m}}}}$, inside the straight part of the data.

Step 5: Integrate the two parts.
Part 1, $a_0 \le a \le a_t$, with $w = K_{{max}} - K_{{op}} = {B:.1f}\sqrt{{a}} - 6$: substituting $u = \sqrt{{a}}$, $da = 2u\,du$, and $w = {B:.1f}\,u - 6$,
$$N_1 = \int_{{a_0}}^{{a_t}} \frac{{da}}{{C\,w^{{3}}}} = \frac{{2}}{{C\,B^{{2}}}} \int_{{w_0}}^{{w_t}} \frac{{w + K_{{op}}}}{{w^{{3}}}}\,dw = \frac{{2}}{{C\,B^{{2}}}} \left[ -\frac{{1}}{{w}} - \frac{{K_{{op}}}}{{2 w^{{2}}}} \right]_{{w_0}}^{{w_t}},$$
with $B = {B:.1f}$, $w_0 = {B*math.sqrt(a0):.2f} - 6 = {w0:.2f}$ and $w_t = 15 - 6 = {wt:.0f}$ MPa$\sqrt{{\mathrm{{m}}}}$. The bracket is $({F(wt):.5f}) - ({F(w0):.5f}) = {F(wt)-F(w0):.5f}$ (MPa$\sqrt{{\mathrm{{m}}}}$)$^{{-1}}$ and $2/(C B^{{2}}) = {2/(C*B*B):.4e}$, so $N_1 = {N1:.4g}$ cycles.
Part 2, $a_t \le a \le a_c$, closure-free Paris law with $Y \Delta\sigma \sqrt{{\pi}} = {A:.1f}$:
$$N_2 = \frac{{2}}{{C\,(Y \Delta\sigma \sqrt{{\pi}})^{{3}}}}\left(a_t^{{-1/2}} - a_c^{{-1/2}}\right) = {2/(C*A**3):.0f} \times ({at**-0.5:.2f} - {ac**-0.5:.2f}) = {N2:.4g} \text{{ cycles}}.$$
Total: $N = N_1 + N_2 = {N:.4g} \approx 1.2 \times 10^{{6}}$ cycles.

Step 6: Conclusion.
The plate survives $1.2 \times 10^{{6}}$ cycles. Ignoring closure (the dashed fit with $\Delta K$ throughout) gives ${Nfree:.2g}$; keeping $\Delta K_{{eff}} = K_{{max}} - K_{{op}}$ up to $a_c$ gives $8.9 \times 10^{{5}}$; treating $K_{{op}}$ as the fixed fraction of $K_{{max}}$ that holds at $a_0$ gives $2.2 \times 10^{{6}}$; computing $a_c$ from $\Delta\sigma$ gives $1.3 \times 10^{{6}}$.

Answer: $1.2 \times 10^{{6}}$ cycles."""
rubric = [
    dict(id="c1", description=r"Gives $1.2 \times 10^{6}$ cycles (two significant figures; any equivalent numerical form).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Reads the closure-free law as $m = 3$, $C = 1.0 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^3$ from the $R = 0.7$ fit, and infers the constant opening level $K_{op} = 6$ MPa$\sqrt{\mathrm{m}}$ from the converging $R = 0.1$ data (equal-rate pairs or the merging point near $\Delta K = 54$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Recognises that at $R = 0.4$ closure is present from $a_0$ and disappears when $K_{min}$ reaches $K_{op}$, at $K_{max} = 15$ MPa$\sqrt{\mathrm{m}}$ ($a_t = 0.357$ mm), and integrates the two parts separately.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Obtains the critical crack length $a_c = 4.80$ mm from $K_{max} = Y \sigma_{max} \sqrt{\pi a_c} = K_{IC}$ with $\sigma_{max} = 400$ MPa.", points=1, isFinalAnswer=False),
]
wrong = [r"$1.0 \times 10^{6}$ cycles", r"$8.9 \times 10^{5}$ cycles", r"$2.2 \times 10^{6}$ cycles", r"$8.3 \times 10^{6}$ cycles", r"$1.3 \times 10^{6}$ cycles"]
references = r"""Crack closure and the effective stress intensity range: W. Elber, The significance of fatigue crack closure, in Damage Tolerance in Aircraft Structures, ASTM STP 486 (1971), 230-242. The power-law relation between growth rate and stress intensity range: P. C. Paris and F. Erdogan, A critical analysis of crack propagation laws, Journal of Basic Engineering 85 (1963), 528-534. The uploaded file verification_notes.txt states the growth law and closure model from which the figure was generated (so the fit and the opening level are exact), lists every plotted point, derives the opening level from the equal-rate pairs and the merging point, finds the transition length at $R = 0.4$, computes the critical crack length and the two-part life by closed forms and by two numerical integrations, and computes the values reached by the wrong routes; the program is embedded with its output."""
necessity = "The closure-free Paris constants and the opening level, which is encoded in how the R = 0.1 data converge towards the R = 0.7 data, are given only by the plot; nothing in the text states the growth law or the opening level."
verify_field = "Section 1 of verification_notes.txt gives the growth law and closure model that generated the figure and the coordinates of every plotted point, so the fit can be checked against the plot (the R = 0.7 fit passes through 1e-9 m/cycle at 10 MPa sqrt m and 1e-6 at 100; the R = 0.1 points at 9, 18, 27, 36, 45 have the same rates as the R = 0.7 points at 4, 14, 24, 34, 44, giving K_op = 6 from each pair). Section 2 derives the transition at K_max = 15 MPa sqrt m (a_t = 0.357 mm) at R = 0.4. Section 3 computes a_c = 4.80 mm and the life 1,196,532 cycles as the sum of two closed forms, checked by composite Simpson integration and by scipy quad. Section 4 lists the wrong routes with their values. Section 5 embeds the program verify_key.py with its output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (log-log plot generated from the stated growth law and closure model)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 2}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert "1.2" in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", verify_field)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "”", "​"): assert ch not in text, name
    assert abs(N - 1196532) < 1
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    fig = (HERE / "work" / "figure_data.txt").read_text()
    assert "ALL CHECKS PASSED" in out
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fatigue crack growth life from the two-load-ratio da/dN plot (constant opening level)

Answer key: 1.2 x 10^6 cycles (1,196,532 cycles before rounding).

1. The figure. Generated by draw_figure.py from the law da/dN = C dK_eff^3 (1 - (dK_th,eff/dK_eff)^4) with
   C = 1.0e-12 m/cycle per (MPa sqrt m)^3, dK_th,eff = 2.5 MPa sqrt m, and the closure model K_op = 6.0 MPa sqrt m at every
   load ratio while K_min < K_op (no closure once K_min >= K_op). The R = 0.7 series is closure-free over the plotted
   range (closure would need K_max < 6/0.7 = 8.6, i.e. dK < 2.6). The R = 0.1 series has dK_eff = K_max - 6 = dK/0.9 - 6
   while dK < 54 and merges with the R = 0.7 series above dK = 54. The dashed line is the Paris part da/dN = C dK^3 of
   the R = 0.7 data, through (10, 1e-9) and (100, 1e-6); the thin solid line is the closure model through the R = 0.1
   points. Equal-rate pairs: R = 0.7 at dK = 4, 14, 24, 34, 44 and R = 0.1 at dK = 9, 18, 27, 36, 45, so
   K_op = dK(0.1)/0.9 - dK(0.7) = 6 from each pair. Plotted points:
{textwrap.indent(fig.split(chr(10) + "wrote")[0], "   ")}
2. At R = 0.4: K_max = Y sigma_max sqrt(pi a) = 794.06 sqrt(a); at a0 K_max = 11.23 and K_min = 4.49 < 6, so closure is
   present; K_min reaches K_op when K_max = 6/0.4 = 15, at a_t = (15/(1.12 x 400))^2/pi = 0.3568 mm; beyond a_t the
   crack is closure-free. dK_eff at a0 is 5.23, above the intrinsic threshold.
3. Life: a_c = (K_IC/(Y sigma_max))^2/pi = 4.7975 mm. Part 1 (closure): with w = K_max - K_op and the substitution
   u = sqrt(a), N1 = (2/(C B^2)) [-1/w - K_op/(2 w^2)] from w0 = 5.2297 to w_t = 9 = 484,538 cycles. Part 2
   (closure-free): N2 = 2/(C (Y ds sqrt(pi))^3) (a_t^-1/2 - a_c^-1/2) = 711,994 cycles. N = 1,196,532 cycles; composite
   Simpson on the piecewise law and scipy quad give the same value to better than 1e-8 relative. Keeping the
   near-threshold knee factor would give 1,209,824 (+1.1 percent); the stem says to use the Paris fit, so the key is the
   closed-form value. At two significant figures the key is 1.2e6; a reading of K_op as 5.5 or 6.5 would give 1.1e6 or
   1.3e6, which is why the equal-rate pairs sit on grid lines.
4. Wrong routes (values printed by the program): closure ignored gives 1.0e6; closure kept up to a_c (transition
   ignored) gives 8.9e5; K_op taken as the fixed fraction of K_max that holds at a0 gives 2.2e6; the R = 0.1 data
   treated as a parallel line a factor 2 to the right gives 8.3e6; a_c from delta sigma gives 1.3e6.

5. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only, scipy optional)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

6. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

{textwrap.indent((HERE / "draw_figure.py").read_text(), "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: fatigue crack growth life with a constant opening level read from two load ratios", "",
             "Engineering (materials), subdomain: " + task["task"]["subdomain"] + ". This folder was first used for the mathematics task on the fractional chromatic number (Summit SUM-MVBCQZWW, returned too easy); that package and its revision are archived in work/v1 and work/v2-math. Two earlier engineering versions (closure as a fixed fraction of K_max, 0.30 and 0.55) are archived in work/eng-v1 and work/eng-v2; both were solved by every local run.", "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", verify_field, "", "## Screen", "", screen]
    (HERE / "README.md").write_text("\n".join(lines) + "\n"); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    screen = (HERE / "work" / "screen.md").read_text() if (HERE / "work" / "screen.md").exists() else "(filled in after the screen)"
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(screen); build_zip()
