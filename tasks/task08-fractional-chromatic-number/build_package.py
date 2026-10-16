import json, zipfile, pathlib, textwrap, subprocess, sys, math
HERE = pathlib.Path(__file__).parent
SLUG = "crack-growth-closure-two-load-ratios"
question = r"""The figure shows fatigue crack growth data for long cracks in a metal injection moulded Ti-6Al-7Nb alloy: the crack growth rate $da/dN$ against the stress intensity factor range $\Delta K$ on logarithmic axes, measured at the load ratios $R = 0.1$ and $R = 0.7$. The dashed lines are the Paris-law fits to the straight parts of the two data sets. The difference between the two data sets is caused by crack closure. Assume that the crack-opening stress intensity factor $K_{op}$ is the same fixed fraction of $K_{max}$ at every load ratio at which closure occurs, that closure is absent when $K_{min} \ge K_{op}$, and that the growth rate depends only on the effective range $\Delta K_{eff} = K_{max} - \max(K_{op}, K_{min})$.

A wide plate of the same material carries a constant-amplitude cyclic stress with $\sigma_{max} = 400$ MPa at $R = 0.4$. A surface pore is treated as an edge crack of initial length $a_0 = 0.20$ mm, with the geometry factor $Y = 1.12$ taken as constant, so that $K = Y \sigma \sqrt{\pi a}$. The plate fails when $K_{max}$ reaches the fracture toughness $K_{IC} = 55$ MPa$\sqrt{\mathrm{m}}$. Use the Paris fits for the whole of the crack growth and ignore the deviation of the data near the threshold.

Find the number of cycles from $a_0$ to failure. Give the answer to three significant figures."""
# numbers
C = 1.0e-12; m = 3; Y = 1.12; a0 = 0.20e-3; smax = 400.0; R = 0.4; KIC = 55.0; k = 0.55
ds = smax * (1 - R); ac = (KIC / (Y * smax)) ** 2 / math.pi
U04 = (1 - k) / (1 - R); Ceff = C * U04 ** 3
A = Y * ds * math.sqrt(math.pi); pref = 2.0 / (Ceff * A ** 3); N = pref * (a0 ** -0.5 - ac ** -0.5)
Nfree = 2.0 / (C * A ** 3) * (a0 ** -0.5 - ac ** -0.5)
dK0 = Y * ds * math.sqrt(math.pi * a0); dKc = Y * ds * math.sqrt(math.pi * ac)
final_answer = r"$2.47 \times 10^{6}$ cycles"
variants = ["2.47e6 cycles", "2470000 cycles", r"$2.47 \times 10^6$", "2.47 million cycles", "2.47E+06"]
solution = rf"""Step 1: Read the two Paris fits from the figure.
Both dashed lines have the same slope. The fit to the $R = 0.7$ data passes through the grid intersections $da/dN = 10^{{-9}}$ m/cycle at $\Delta K = 10$ MPa$\sqrt{{\mathrm{{m}}}}$ and $da/dN = 10^{{-6}}$ m/cycle at $\Delta K = 100$ MPa$\sqrt{{\mathrm{{m}}}}$, so its exponent is $m = \log(10^{{3}})/\log(10) = 3$ and its coefficient is $C = 10^{{-9}}/10^{{3}} = 1.0 \times 10^{{-12}}$ m/cycle per (MPa$\sqrt{{\mathrm{{m}}}}$)$^{{3}}$. The fit to the $R = 0.1$ data is the same line displaced to the right by a factor of $2$: it passes through $10^{{-9}}$ m/cycle at $\Delta K = 20$ and $10^{{-6}}$ m/cycle at $\Delta K = 200$ MPa$\sqrt{{\mathrm{{m}}}}$, and the two thresholds ($\approx 2.5$ and $\approx 5$ MPa$\sqrt{{\mathrm{{m}}}}$) are displaced by the same factor.

Step 2: Infer the closure level.
Write $K_{{op}} = k\,K_{{max}}$. A load ratio with $K_{{min}} \ge K_{{op}}$ has $\Delta K_{{eff}} = \Delta K$. The data set to the left (faster growth at a given $\Delta K$) is the one in which the whole range is effective, so the $R = 0.7$ curve is the closure-free curve, $da/dN = C\,\Delta K_{{eff}}^{{3}}$, and $k < 0.7$. At $R = 0.1$, $\Delta K = 0.9\,K_{{max}}$ and $\Delta K_{{eff}} = (1 - k)\,K_{{max}}$, so $\Delta K_{{eff}} = U_{{0.1}}\,\Delta K$ with $U_{{0.1}} = (1-k)/0.9$. Equal growth rates occur at equal $\Delta K_{{eff}}$, so the displacement of the $R = 0.1$ curve is $1/U_{{0.1}} = 2$, giving $U_{{0.1}} = 0.5$ and $k = 1 - 0.9 \times 0.5 = 0.55$.

Step 3: The decisive step: at $R = 0.4$ closure is present, and neither measured curve applies as it stands.
At $R = 0.4$, $K_{{min}} = 0.40\,K_{{max}} < K_{{op}} = 0.55\,K_{{max}}$, so the crack closes during part of every cycle and $\Delta K_{{eff}} = K_{{max}} - K_{{op}} = 0.45\,K_{{max}}$. With $\Delta K = 0.6\,K_{{max}}$ this is $\Delta K_{{eff}} = U_{{0.4}}\,\Delta K$ with $U_{{0.4}} = 0.45/0.60 = 0.75$. The growth law of the plate is therefore $da/dN = C\,(0.75\,\Delta K)^{{3}} = C_{{eff}}\,\Delta K^{{3}}$ with $C_{{eff}} = 0.75^{{3}} \times 10^{{-12}} = {Ceff:.4e}$ m/cycle per (MPa$\sqrt{{\mathrm{{m}}}}$)$^{{3}}$. Taking the crack to be closure-free at $R = 0.4$ (the $R = 0.7$ fit), using the $R = 0.1$ fit, or interpolating between the two curves in $R$ all give wrong lives.

Step 4: Stress range, critical crack length and the range of $\Delta K$.
$\sigma_{{min}} = R\,\sigma_{{max}} = 160$ MPa and $\Delta \sigma = \sigma_{{max}} - \sigma_{{min}} = {ds:.0f}$ MPa. Failure occurs when $K_{{max}} = Y \sigma_{{max}} \sqrt{{\pi a_c}} = K_{{IC}}$, so $a_c = \dfrac{{1}}{{\pi}}\left(\dfrac{{K_{{IC}}}}{{Y \sigma_{{max}}}}\right)^{{2}} = \dfrac{{1}}{{\pi}}\left(\dfrac{{55}}{{1.12 \times 400}}\right)^{{2}} = {ac*1e3:.3f}$ mm (with $\Delta\sigma$ in place of $\sigma_{{max}}$ one would get $13.3$ mm, which is wrong). The applied range grows from $\Delta K(a_0) = 1.12 \times {ds:.0f} \times \sqrt{{\pi \times 0.20 \times 10^{{-3}}}} = {dK0:.2f}$ MPa$\sqrt{{\mathrm{{m}}}}$ to $\Delta K(a_c) = {dKc:.1f}$ MPa$\sqrt{{\mathrm{{m}}}}$; the effective range runs from ${U04*dK0:.2f}$ to ${U04*dKc:.1f}$ MPa$\sqrt{{\mathrm{{m}}}}$, above the intrinsic threshold and inside the straight part of the data.

Step 5: Integrate the Paris law.
With $da/dN = C_{{eff}} (Y \Delta\sigma \sqrt{{\pi a}})^{{m}}$ and $m = 3$,
$$N = \int_{{a_0}}^{{a_c}} \frac{{da}}{{C_{{eff}}\,(Y \Delta\sigma \sqrt{{\pi}})^{{3}}\, a^{{3/2}}}} = \frac{{2}}{{C_{{eff}}\,(Y \Delta\sigma \sqrt{{\pi}})^{{3}}}}\left(a_0^{{-1/2}} - a_c^{{-1/2}}\right).$$
Here $Y \Delta\sigma \sqrt{{\pi}} = 1.12 \times {ds:.0f} \times \sqrt{{\pi}} = {A:.1f}$ MPa$\sqrt{{\mathrm{{m}}}}\,$m$^{{-1/2}}$, its cube is ${A**3:.4e}$, and $2/(C_{{eff}} \times {A**3:.4e}) = {pref:.0f}$ cycles$\,$m$^{{1/2}}$. With $a_0^{{-1/2}} = (0.20 \times 10^{{-3}})^{{-1/2}} = {a0**-0.5:.2f}$ m$^{{-1/2}}$ and $a_c^{{-1/2}} = ({ac*1e3:.3f} \times 10^{{-3}})^{{-1/2}} = {ac**-0.5:.2f}$ m$^{{-1/2}}$,
$$N = {pref:.0f} \times ({a0**-0.5:.2f} - {ac**-0.5:.2f}) = {N:.4g} \approx 2.47 \times 10^{{6}} \text{{ cycles}}.$$

Step 6: Conclusion.
The plate survives $2.47 \times 10^{{6}}$ cycles. The closure-free law (the $R = 0.7$ fit used directly) gives ${Nfree:.3g}$, which is the life one obtains by assuming that closure has vanished at $R = 0.4$; the $R = 0.1$ fit gives $8.33 \times 10^{{6}}$; a log-linear interpolation between the two curves at $R = 0.4$ gives $2.94 \times 10^{{6}}$; computing $a_c$ from $\Delta\sigma$ gives $2.72 \times 10^{{6}}$.

Answer: $2.47 \times 10^{{6}}$ cycles."""
rubric = [
    dict(id="c1", description=r"Gives $2.47 \times 10^{6}$ cycles (three significant figures; any equivalent numerical form).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Reads the Paris fit of the $R = 0.7$ data as $m = 3$ and $C = 1.0 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^3$, and infers the closure level $K_{op}/K_{max} = 0.55$ (equivalently $U = 0.5$ at $R = 0.1$) from the displacement factor $2$ between the two curves.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Recognises that closure is still present at $R = 0.4$ because $K_{min} = 0.40\,K_{max}$ is below $K_{op} = 0.55\,K_{max}$, and derives $\Delta K_{eff} = 0.75\,\Delta K$ (equivalently $C_{eff} = 4.22 \times 10^{-13}$) for the plate.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Obtains the critical crack length $a_c = 4.80$ mm from $K_{max} = Y \sigma_{max} \sqrt{\pi a_c} = K_{IC}$ with $\sigma_{max} = 400$ MPa.", points=1, isFinalAnswer=False),
]
wrong = [r"$1.04 \times 10^{6}$ cycles", r"$8.33 \times 10^{6}$ cycles", r"$2.94 \times 10^{6}$ cycles", r"$3.62 \times 10^{6}$ cycles", r"$2.72 \times 10^{6}$ cycles"]
references = r"""Crack closure and the effective stress intensity range: W. Elber, The significance of fatigue crack closure, in Damage Tolerance in Aircraft Structures, ASTM STP 486 (1971), 230-242. The power-law relation between growth rate and stress intensity range: P. C. Paris and F. Erdogan, A critical analysis of crack propagation laws, Journal of Basic Engineering 85 (1963), 528-534. The uploaded file verification_notes.txt states the growth law and closure model from which the figure was generated (so the fits are exact), lists every plotted point, derives the closure level from the displacement of the two curves and the effective range at $R = 0.4$, computes the critical crack length and the life by the closed form and by two numerical integrations, and computes the values reached by the wrong routes; the program is embedded with its output."""
necessity = "The Paris constants, the slope, the thresholds and the displacement between the two load ratios, from which the closure level follows, are given only by the plot; nothing in the text states the growth law or the closure level."
verify_field = "Section 1 of verification_notes.txt gives the growth law and closure model that generated the figure and the coordinates of every plotted point, so the fits can be checked against the plot (the R = 0.7 fit passes through 1e-9 m/cycle at 10 MPa sqrt m and 1e-6 at 100; the R = 0.1 fit through the same rates at 20 and 200). Section 2 derives K_op/K_max = 0.55 from the displacement factor 2 of the two curves and the effective range 0.75 delta K at R = 0.4, where K_min is below K_op. Section 3 computes a_c = 4.80 mm and the life 2,466,809 cycles by the closed form, by composite Simpson integration and by scipy quad. Section 4 lists the wrong routes with their values. Section 5 embeds the program verify_key.py with its output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (log-log plot generated from the stated growth law and closure model)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 3}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert "2.47" in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", verify_field)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "”", "​"): assert ch not in text, name
    assert abs(N - 2466809) < 1
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    fig = (HERE / "work" / "figure_data.txt").read_text()
    assert "ALL CHECKS PASSED" in out
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fatigue crack growth life from the two-load-ratio da/dN plot

Answer key: 2.47 x 10^6 cycles (2,466,809 cycles before rounding).

1. The figure. Generated by draw_figure.py from the law da/dN = C dK_eff^3 (1 - (dK_th,eff/dK_eff)^4) with
   C = 1.0e-12 m/cycle per (MPa sqrt m)^3, dK_th,eff = 2.5 MPa sqrt m, and the closure model K_op = 0.55 K_max (no
   closure once K_min >= K_op). The R = 0.7 series is closure-free (dK_eff = dK). The R = 0.1 series has
   dK_eff = (1 - 0.55) K_max = (0.45/0.90) dK = 0.5 dK, so it is the intrinsic curve displaced to the right by the
   factor 2. The dashed lines are the pure Paris parts, da/dN = C dK^3 (R = 0.7) and C (0.5 dK)^3 (R = 0.1); the
   R = 0.7 fit passes through (10, 1e-9) and (100, 1e-6), the R = 0.1 fit through (20, 1e-9) and (200, 1e-6).
   Plotted points:
{textwrap.indent(fig.split(chr(10) + "wrote")[0], "   ")}
2. Closure level from the plot: equal growth rates at equal dK_eff, so the displacement factor is 1/U with
   U = dK_eff/dK at R = 0.1; 1/U = 2 gives U = 0.5 and K_op/K_max = 1 - 0.9 U = 0.55. At R = 0.4,
   K_min/K_max = 0.40 < 0.55, so closure is present: dK_eff = K_max - K_op = 0.45 K_max = 0.75 dK, and the growth law
   of the plate is da/dN = C (0.75 dK)^3 = 4.2188e-13 dK^3.
3. Life: sigma_max 400 MPa, R 0.4, delta sigma 240 MPa, Y 1.12, a0 0.20 mm, K_IC 55 MPa sqrt m.
   a_c = (K_IC/(Y sigma_max))^2/pi = 4.7975 mm. dK runs from 6.74 to 33.0 MPa sqrt m (dK_eff from 5.05 to 24.8), above
   the intrinsic threshold and inside the straight part. N = 2/(C_eff (Y ds sqrt(pi))^3) (a0^-1/2 - a_c^-1/2)
   = 2,466,809 cycles (closed form); composite Simpson with 20000 intervals and scipy quad give the same value to
   better than 1e-9 relative. Keeping the near-threshold knee factor in the law would give 2,505,221 (+1.56 percent);
   the stem says to use the Paris fits, so the key is the closed-form value.
4. Wrong routes (values printed by the program): closure assumed absent at R = 0.4 (R = 0.7 fit used directly) gives
   1.04e6; the R = 0.1 fit gives 8.33e6; a log-linear interpolation between the curves gives 2.94e6; Elber's
   U = 0.5 + 0.4 R in place of the closure level in the figure gives 3.62e6; a_c from delta sigma gives 2.72e6;
   sigma_max used in place of delta sigma gives 5.33e5.

5. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only, scipy optional)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

6. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

{textwrap.indent((HERE / "draw_figure.py").read_text(), "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: fatigue crack growth life with closure read from two load ratios", "",
             "Engineering (materials), subdomain: " + task["task"]["subdomain"] + ". This folder was first used for the mathematics task on the fractional chromatic number (Summit SUM-MVBCQZWW, returned too easy); that package and its revision are archived in work/v1 and work/v2-math. Mathematics is closed for new tasks (see AQ_Summit/domains-for-new-task.md).", "",
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
