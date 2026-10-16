import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "crack-growth-closure-life-titanium"
question = r"""The figure shows fatigue crack growth data for a powder injection moulded alpha plus beta titanium alloy: the crack growth rate $\mathrm{d}a/\mathrm{d}N$ against the stress intensity factor range $\Delta K$ on logarithmic axes, measured on compact tension specimens at the load ratios $R = 0.1$ (filled circles) and $R = 0.5$ (open squares). The two straight lines are the Paris fits of the data above the threshold region, the solid line for $R = 0.5$ and the dashed line for $R = 0.1$. Each line passes exactly through its two crosses, and every cross sits on an intersection of gridlines.

Take the following as given. Crack growth in this alloy is governed by the effective range $\Delta K_{\mathrm{eff}} = U \, \Delta K$, where the closure factor $U$ depends only on the load ratio, and in the Paris regime $\mathrm{d}a/\mathrm{d}N = C \, (\Delta K_{\mathrm{eff}})^{n}$ with the same $C$ and $n$ at every load ratio. The $R = 0.5$ data are free of crack closure, so $U = 1$ at $R = 0.5$, and $U$ varies linearly with $R$ between $R = 0.1$ and $R = 0.5$.

A plate of this alloy of width $W = 20$ mm carries a remote tensile stress that cycles with the stress range $\Delta\sigma = 250$ MPa at the load ratio $R = 0.3$. A surface pore has started a through-thickness edge crack of depth $a_0 = 0.6$ mm. The stress intensity factor of the edge crack is $K = Y \sigma \sqrt{\pi a}$ with $Y = 1.12 - 0.231\,(a/W) + 10.55\,(a/W)^2 - 21.72\,(a/W)^3 + 30.39\,(a/W)^4$. The plate fails when the maximum stress intensity factor in a cycle reaches the fracture toughness $K_{\mathrm{IC}} = 60$ MPa$\sqrt{\mathrm{m}}$. Neglect the threshold, so that the Paris law applies from $a_0$ onwards.

How many load cycles does the plate survive from the crack depth $a_0$ to failure? Give the number of cycles to two significant figures."""
final_answer = r"$1.1 \times 10^{5}$"
variants = ["1.1e5", "110000", "110,000", r"$1.1 \cdot 10^{5}$", "1.1e5 cycles", "110000 cycles", "0.11 million cycles"]
solution = r"""Step 1: Read the Paris constants from the $R = 0.5$ line.
The solid line passes through $(\Delta K, \mathrm{d}a/\mathrm{d}N) = (5, 10^{-9})$ and $(50, 10^{-6})$, in MPa$\sqrt{\mathrm{m}}$ and m/cycle. A factor $10$ in $\Delta K$ gives a factor $10^{3}$ in rate, so $n = \log(10^{3}) / \log(10) = 3$. Since $U = 1$ at $R = 0.5$, $C = 10^{-9} / 5^{3} = 8 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^{3}$.

Step 2: Read the closure factor at $R = 0.1$ from the dashed line.
The dashed line passes through $(10, 10^{-9})$ and $(100, 10^{-6})$, so it has the same slope $n = 3$ and reaches a given rate at twice the $\Delta K$ of the $R = 0.5$ line. The same rate means the same $\Delta K_{\mathrm{eff}}$, so $U(0.1) \cdot 10 = 1 \cdot 5$ and $U(0.1) = 0.5$.

Step 3: Closure factor at the service load ratio.
With $U$ linear in $R$ between $U(0.1) = 0.5$ and $U(0.5) = 1$, at $R = 0.3$ (the midpoint) $U = 0.5 + \dfrac{0.3 - 0.1}{0.5 - 0.1}\,(1 - 0.5) = 0.75$. The growth law in service is therefore $\mathrm{d}a/\mathrm{d}N = 8 \times 10^{-12}\,(0.75\,\Delta K)^{3}$ with $\Delta K = Y \Delta\sigma \sqrt{\pi a}$.

Step 4: Critical crack depth.
The maximum stress in the cycle is $\sigma_{\max} = \Delta\sigma / (1 - R) = 250 / 0.7 = 357.1$ MPa. Failure occurs when $Y \sigma_{\max} \sqrt{\pi a} = K_{\mathrm{IC}} = 60$ MPa$\sqrt{\mathrm{m}}$. At $a = 4.40$ mm, $a/W = 0.220$, $Y = 1.4197$, $\sqrt{\pi a} = 0.11757$ $\sqrt{\mathrm{m}}$ and $K_{\max} = 59.6$; at $a = 4.50$ mm, $Y = 1.4326$, $\sqrt{\pi a} = 0.11890$ and $K_{\max} = 60.8$. Interpolating, $a_c = 4.43$ mm ($a_c/W = 0.222$, $Y = 1.424$).

Step 5: Integrate the growth law.
$N = \displaystyle\int_{a_0}^{a_c} \frac{\mathrm{d}a}{C\,(U Y \Delta\sigma \sqrt{\pi a})^{3}} = \frac{1}{C\,(U \Delta\sigma)^{3}\,\pi^{3/2}} \int_{a_0}^{a_c} \frac{\mathrm{d}a}{Y^{3} a^{3/2}}$, and $C\,(U\Delta\sigma)^{3}\,\pi^{3/2} = 8 \times 10^{-12} \cdot 187.5^{3} \cdot 5.5683 = 2.9364 \times 10^{-4}$ m$^{-1/2}$.
With the substitution $a = u^{2}$ the integral becomes $\displaystyle\int_{u_0}^{u_c} \frac{2\,\mathrm{d}u}{Y^{3} u^{2}}$ with $u_0 = \sqrt{0.0006} = 0.02449$ and $u_c = \sqrt{0.004432} = 0.06657$. Simpson's rule on eight panels ($h = 0.005260$) uses the integrand values $2/(Y^{3}u^{2})$ at $a = 0.600, 0.885, 1.226, 1.622, 2.073, 2.580, 3.142, 3.759, 4.432$ mm, where $Y = 1.1220, 1.1287, 1.1409, 1.1604, 1.1887, 1.2275, 1.2784, 1.3430, 1.4238$ and the integrand is $2359.9, 1571.1, 1098.5, 789.2, 574.3, 419.1, 304.7, 219.6, 156.4$; the rule gives $32.38$ (the exact value of the integral is $32.36$). Hence $N = 32.36 / (2.9364 \times 10^{-4}) = 1.10 \times 10^{5}$ cycles.

Step 6: Result.
The plate survives $1.1 \times 10^{5}$ cycles. Using the $R = 0.1$ line as it stands ($U = 0.5$) gives $3.7 \times 10^{5}$ cycles, using the $R = 0.5$ line as it stands ($U = 1$) gives $4.6 \times 10^{4}$, and holding $Y$ at $1.12$ throughout gives $1.3 \times 10^{5}$; only the closure factor interpolated to $R = 0.3$ together with the varying $Y$ gives the stated result.

Answer: $1.1 \times 10^{5}$ cycles."""
rubric = [
    dict(id="c1", description=r"Gives $1.1 \times 10^{5}$ cycles (110000 to two significant figures).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Reads the Paris exponent $n = 3$ and the constant $C = 8 \times 10^{-12}$ m/cycle per (MPa$\sqrt{\mathrm{m}}$)$^{3}$ from the $R = 0.5$ line.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Obtains the closure factor $U(0.1) = 0.5$ from the horizontal shift between the two lines and interpolates to $U = 0.75$ at $R = 0.3$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Finds the critical crack depth $a_c = 4.4$ mm (accept 4.3 to 4.5 mm) from $K_{\max} = K_{\mathrm{IC}}$ with $\sigma_{\max} = \Delta\sigma/(1 - R) = 357$ MPa.", points=1, isFinalAnswer=False),
    dict(id="c5", description=r"Integrates $\mathrm{d}a/\mathrm{d}N = C (U Y \Delta\sigma \sqrt{\pi a})^{3}$ from $a_0$ to $a_c$ with $Y$ varying along the integration (numerically or by a stated quadrature), not held constant.", points=1, isFinalAnswer=False),
]
wrong = [r"$3.7 \times 10^{5}$", r"$4.6 \times 10^{4}$", r"$2.0 \times 10^{5}$", r"$1.3 \times 10^{5}$"]
references = r"""Crack closure and the effective stress intensity range: W. Elber, The significance of fatigue crack closure, in Damage Tolerance in Aircraft Structures, ASTM STP 486 (1971), 230-242. The Paris relation: P. C. Paris and F. Erdogan, A critical analysis of crack propagation laws, Journal of Basic Engineering 85 (1963), 528-534. The edge-crack geometry factor used in the stem is the standard single-edge-notch polynomial, for instance in H. Tada, P. C. Paris and G. R. Irwin, The Stress Analysis of Cracks Handbook, 3rd edition, ASME Press (2000). Closure effects and load-ratio dependence of crack growth in titanium alloys: R. O. Ritchie, Mechanisms of fatigue-crack propagation in ductile and brittle solids, International Journal of Fracture 100 (1999), 55-83. The uploaded file verification_notes.txt gives the model from which the figure was generated (the two fit lines are exact, through the marked anchors), recomputes the Paris constants and the closure factors from the anchors, solves for the critical crack depth, integrates the growth law by two independent routes (scipy adaptive quadrature; mpmath tanh-sinh quadrature at 30 digits plus a composite Simpson rule with Richardson extrapolation), evaluates every plausible wrong route, and embeds the program with its output."""
necessity = "The Paris constants and the closure factor at R = 0.1 exist only in the figure: the stem gives no value of C, n or U, and the answer depends on reading the two fit lines (their slope, and the horizontal shift of the R = 0.1 line relative to the R = 0.5 line) off the logarithmic axes."
verify_field = "Section 2 of verification_notes.txt gives the model that generated the figure (the solid fit through (5, 1e-9) and (50, 1e-6), the dashed fit through (10, 1e-9) and (100, 1e-6), hence n = 3, C = 8e-12 and U(0.1) = 0.5, U(0.3) = 0.75); section 3 gives the critical crack depth 4.43 mm; section 4 gives the life 110212 cycles by scipy quadrature and independently by mpmath tanh-sinh quadrature and a composite Simpson rule, and shows the value is 4.3 percent away from the nearest two-significant-figure rounding boundary; section 5 lists the plausible wrong routes with their values; section 6 embeds the program verify_key.py with its full output."
SCREEN = """Screen 2026-10-17, figure plus stem only, no web, no code: Opus 3/3 correct, each in about two minutes and 45k tokens (anchors read exactly, n = 3, C = 8e-12, U(0.1) = 0.5 from the factor-2 shift, U(0.3) = 0.75, a_c = 4.43 mm from sigma_max = 357 MPa, then the substitution u = a^(-1/2) and a nine-point Simpson rule giving 1.10e5). Sonnet 1/1 correct by the same route in 2.5 minutes. Tally: Opus 3/3, Sonnet 1/1. Too easy; held back, the owner decides."""
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (original plot generated from a stated crack-growth model; Python script kept)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 2}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}


def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert "1.1 \\times 10^{5}" in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", verify_field), ("screen", SCREEN)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"):
            assert ch not in text, name
    print("package checks passed")


def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "Both routes agree" in out, "verify_key_output.txt is not a complete run"
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fatigue life of the edge-cracked titanium plate

Answer key: 1.1e5 cycles (two significant figures); exact model value 110212 cycles.

1. What the figure is.  The plot is generated from a stated model, not measured: da/dN = C (U dK)^n
   with n = 3, C = 8e-12 m/cycle per (MPa sqrt m)^3, U(0.5) = 1 and U(0.1) = 1/2.  The data symbols
   are model values with a near-threshold knee (intrinsic threshold 2.5 MPa sqrt m) and 6 percent
   log-normal scatter; the two straight lines are the exact Paris fits and pass through the anchors
   marked with crosses, all on gridline intersections.  The figure script draw_figure.py is kept.

2. Reading the figure.  Solid line (R = 0.5) through (5, 1e-9) and (50, 1e-6): n = 3, C = 8e-12.
   Dashed line (R = 0.1) through (10, 1e-9) and (100, 1e-6): same slope, same rate at twice dK, so
   U(0.1) = 0.5.  Linear in R: U(0.3) = 0.75.  Service law da/dN = 8e-12 (0.75 Y dsigma sqrt(pi a))^3.

3. Critical crack depth.  sigma_max = dsigma / (1 - R) = 357.14 MPa; Y sigma_max sqrt(pi a) = 60 at
   a_c = 4.4318 mm (a/W = 0.2216, Y = 1.4238), by bisection in both routes.

4. Life.  N = integral from 0.6 mm to a_c of da / (C (U Y dsigma sqrt(pi a))^3).  Route A (scipy
   quad): 110211.90.  Route B (mpmath tanh-sinh at 30 digits): 110211.9005; composite Simpson on 2000
   and 4000 panels with Richardson extrapolation: 110211.90.  Two significant figures: 1.1e5.  The
   exact value lies 4.3 percent from the nearest rounding boundary (1.05e5 and 1.15e5), so a careful
   hand quadrature (Simpson on eight panels in sqrt(a) gives 110260) rounds to the same key.

5. Plausible wrong routes (each differs from the key at two significant figures):
   R = 0.1 line as it stands (U = 0.5): 3.7e5.   R = 0.5 line as it stands (U = 1): 4.6e4.
   Elber's U = 0.5 + 0.4 R = 0.62: 2.0e5.   Y held at 1.12: 1.3e5.
   a_c from dsigma instead of sigma_max (6.27 mm): 114706, which still rounds to 1.1e5, so this slip
   alone is not penalised by the key.

6. Program verify_key.py (run with {pyver}, scipy and mpmath from the venv; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")


def build_readme():
    lines = ["# task07: fatigue life from a crack-growth plot with closure", "", "Domain: Engineering. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer + " cycles (two significant figures; exact model value 110212)", "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", verify_field, "", "## Screen", "", SCREEN]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")


def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")


if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
