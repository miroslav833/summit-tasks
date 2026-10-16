import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "kitagawa-internal-pore-titanium"
question = r"""The figure shows the fatigue limit of a metal injection moulded Ti-6Al-7Nb alloy, measured at $R = -1$ as the stress amplitude that specimens survive for $10^7$ cycles, plotted against $\sqrt{\mathrm{area}}$ of an artificial defect, a small hole drilled into the specimen surface. All specimens come from one powder lot with $0.20$ wt% oxygen and a Vickers hardness of $320$ HV. Both axes are logarithmic.

A component is made from a second powder lot with $0.38$ wt% oxygen and a hardness of $372$ HV. Sectioning of a sister part found that its largest pore, with $\sqrt{\mathrm{area}} = 600\ \mu\mathrm{m}$, lies deep inside the material, far from every surface. Use Murakami's $\sqrt{\mathrm{area}}$ model, and take the long-crack threshold stress intensity range at $R = -1$ to be the same for both lots. Estimate the fatigue limit of the component at $R = -1$, as a stress amplitude in MPa, to two significant figures."""
final_answer = "200"
variants = ["200 MPa", r"$2.0 \times 10^{2}$ MPa", "201 MPa", "201"]
solution = r"""Step 1: Read the figure.
The eight points lie at $\sqrt{\mathrm{area}} = 20, 40, 80, 160, 320, 640, 1280, 2560\ \mu\mathrm{m}$ with fatigue limits of about $382, 340, 303, 270, 212, 150, 106, 75$ MPa. On the logarithmic axes the first four points fall on a line of slope $-1/6$ and the last four on a line of slope $-1/2$; the two lines cross near $220\ \mu\mathrm{m}$. The points $(640\ \mu\mathrm{m}, 150\ \mathrm{MPa})$ and $(2560\ \mu\mathrm{m}, 75\ \mathrm{MPa})$ sit on gridlines and fix the steep branch exactly.

Step 2: Identify the two branches.
The shallow branch is the small-defect law of Murakami's model for surface defects, $\sigma_w = 1.43\,(HV + 120)\,(\sqrt{\mathrm{area}})^{-1/6}$ with $\sigma_w$ in MPa and $\sqrt{\mathrm{area}}$ in $\mu\mathrm{m}$: with $HV = 320$ it gives $629.2 \times 20^{-1/6} = 381.8$ MPa at $20\ \mu\mathrm{m}$ and $270.0$ MPa at $160\ \mu\mathrm{m}$, which is what the figure shows. The steep branch is the long-crack threshold. In the model the stress intensity range of a surface defect is $\Delta K = 0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ (with $\sigma$ the stress range at $R = -1$ counted as the amplitude, in the usual convention of the model), so the point $(640\ \mu\mathrm{m}, 150\ \mathrm{MPa})$ gives
$$\Delta K_{th} = 0.65 \times 150 \times \sqrt{\pi \times 640 \times 10^{-6}} = 0.65 \times 150 \times 0.04484 = 4.37\ \mathrm{MPa}\sqrt{\mathrm{m}},$$
and the point $(2560\ \mu\mathrm{m}, 75\ \mathrm{MPa})$ gives the same value, as it must on a line of slope $-1/2$. Beyond the knee the fatigue limit of the specimens is $\Delta K_{th} / (0.65\sqrt{\pi\sqrt{\mathrm{area}}})$ and no longer depends on the hardness.

Step 3: Which branch applies to the component.
The pore is internal, so the stress intensity range is $\Delta K = 0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ and the small-defect constant is $1.56$ instead of $1.43$. For the $372$ HV lot the small-defect branch at $600\ \mu\mathrm{m}$ would give $1.56 \times 492 \times 600^{-1/6} = 767.5 / 2.904 = 264$ MPa. The long-crack branch, with the threshold of Step 2 unchanged between the lots, gives
$$\sigma_w = \frac{\Delta K_{th}}{0.50\sqrt{\pi \times 600 \times 10^{-6}}} = \frac{4.372}{0.50 \times 0.04342} = 201\ \mathrm{MPa}.$$
The fatigue limit is the smaller of the two, so the pore lies in the long-crack regime of the component lot as well (its knee for internal defects is near $265\ \mu\mathrm{m}$), and the higher hardness of the second lot does not raise the limit.

Step 4: Assemble.
Equivalently, from the specimen value at $640\ \mu\mathrm{m}$: $\sigma_w = 150 \times (0.65/0.50) \times \sqrt{640/600} = 150 \times 1.3 \times 1.0328 = 201.4$ MPa. To two significant figures the fatigue limit of the component is $200$ MPa.

Step 5: Conclusion.
The component with the $600\ \mu\mathrm{m}$ internal pore has a fatigue limit of about $200$ MPa at $R = -1$. Keeping the surface factor $0.65$ gives $155$ MPa, scaling the long-crack branch with the hardness ratio $492/440$ gives $225$ MPa, and the small-defect law with the internal constant gives $264$ MPa; each of these misses one of the three decisions, the regime, the hardness independence of the threshold, and the internal-defect factor.

Answer: $200$ MPa."""
rubric = [
    dict(id="c1", description=r"Gives $200$ MPa (two significant figures; $201$ MPa before rounding is equivalent).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Recognises that the steep branch of the figure is the long-crack threshold and obtains $\Delta K_{th} \approx 4.4\ \mathrm{MPa}\sqrt{\mathrm{m}}$ from it (for instance from the point $640\ \mu\mathrm{m}$, $150$ MPa with the factor $0.65$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Uses the internal-defect factor $0.50$ in place of the surface factor $0.65$ (the fatigue limit of the internal pore is $1.3$ times the surface value at the same $\sqrt{\mathrm{area}}$).", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States that the $600\ \mu\mathrm{m}$ pore lies in the long-crack regime, so the hardness of the second lot does not change the result (the small-defect value $264$ MPa is not the limit).", points=1, isFinalAnswer=False),
]
wrong = ["150", "230", "260", "240", "220", "170"]
references = r"""The $\sqrt{\mathrm{area}}$ model, with the small-defect law $\sigma_w = C\,(HV + 120)\,(\sqrt{\mathrm{area}})^{-1/6}$ ($C = 1.43$ for surface and $1.56$ for internal defects), the stress intensity factors $\Delta K = 0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for surface and $0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for internal defects, and the transition to the long-crack threshold for large defects: Y. Murakami and M. Endo, Quantitative evaluation of fatigue strength of metals containing various small defects or cracks, Engineering Fracture Mechanics 17 (1983), 1-15, and Y. Murakami and M. Endo, Effects of defects, inclusions and inhomogeneities on fatigue strength, International Journal of Fatigue 16 (1994), 163-182. The diagram of fatigue limit against defect size with its two regimes: H. Kitagawa and S. Takahashi, Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proceedings of the Second International Conference on Mechanical Behavior of Materials, ASM (1976), 627-631; M. H. El Haddad, T. H. Topper and K. N. Smith, Prediction of non propagating cracks, Engineering Fracture Mechanics 11 (1979), 573-584. Fatigue of metal injection moulded titanium alloys with interstitial oxygen as the hardness lever: a background setting, no data from the literature are used. The uploaded file verification_notes.txt states the model the figure was generated from, derives the key by two routes (closed form from the gridline point, and a least-squares fit of the long-crack branch through the regenerated points), checks the regime for the component lot, evaluates the wrong routes, and embeds the program with its output."""
necessity = "The long-crack threshold of the alloy and the position of the knee between the small-defect law and the long-crack regime exist only in the plotted data; the text gives hardnesses and the pore size but not the threshold, so the fatigue limit cannot be computed without reading the steep branch of the figure."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (Kitagawa diagram generated from the model stated in the solution)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 2}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Section 1 of verification_notes.txt states the model the figure was generated from (small-defect law with 320 HV, long-crack branch fixed by the gridline point 640 um, 150 MPa) and lists the eight plotted values; section 2 derives the key by two routes, the closed form 150 x 0.65/0.50 x sqrt(640/600) = 201 MPa and a least-squares fit of the slope -1/2 branch through the regenerated points followed by the regime check for the 372 HV lot (small-defect value 264 MPa against long-crack value 201 MPa); section 3 evaluates the wrong routes; section 4 embeds the program verify_key.py with its output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fatigue limit of the component with the internal pore (Kitagawa diagram of MIM Ti-6Al-7Nb)

Answer key: 200 MPa (two significant figures; 201.4 MPa before rounding).

1. Model behind the figure. Specimen lot: 0.20 wt% O, 320 HV, surface drilled holes, R = -1, 1e7 cycles.
   Small-defect branch (Murakami, surface): sigma_w = 1.43 (HV + 120) (sqrt(area))^(-1/6), sqrt(area) in um.
   Long-crack branch (surface): sigma_w = DK_th / (0.65 sqrt(pi sqrt(area))), sqrt(area) in m, with DK_th
   fixed by the gridline point (640 um, 150 MPa): DK_th = 4.372 MPa sqrt(m). The plotted fatigue limit is
   the smaller of the two. Plotted points (sqrt(area) um, MPa): (20, 381.9), (40, 340.2), (80, 303.1),
   (160, 270.0), (320, 212.1), (640, 150.0), (1280, 106.1), (2560, 75.0). Knee of the specimen lot: 219 um.

2. Key by two routes. Route A: the component's pore (600 um, internal) is read off the long-crack branch
   with the internal factor 0.50 in place of 0.65: sigma = 150 x (0.65/0.50) x sqrt(640/600) = 201.4 MPa.
   Route B: regenerate the points, fit the slope -1/2 branch through (640, 1280, 2560) by least squares
   (DK_th = 4.372 MPa sqrt(m)), then for the 372 HV lot compare the small-defect value with the internal
   constant, 1.56 x 492 x 600^(-1/6) = 264.3 MPa, with the long-crack value 4.372 / (0.50 sqrt(pi 600e-6)) =
   201.4 MPa; the smaller applies, and the knee of the component lot for internal defects is at 266 um, so
   600 um is in the long-crack regime. Both routes: 201.4 MPa, 200 MPa to two significant figures.

3. Wrong routes (section 3 of the program output): surface factor kept, 155 MPa; long-crack branch scaled
   with the hardness ratio 492/440, 225 MPa; small-defect law with the internal constant, 264 MPa; with the
   surface constant, 242 MPa; small-defect law at the specimen hardness, 217 MPa; long-crack branch with
   surface factor and hardness scaling, 173 MPa.

4. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v3: Kitagawa diagram, internal pore in MIM Ti-6Al-7Nb (Engineering replacement for SUM-MVBG0GO3)", "", "Domain: Engineering. Subdomain: " + task["task"]["subdomain"] + ". Task type: graph extraction with computation.", "",
             "## Question", "", question, "", "## Answer", "", final_answer + " MPa (two significant figures)", "", "Also accepted: " + ", ".join(variants), "", "## Image necessity", "", necessity, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", VERIFY_FIELD, "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
