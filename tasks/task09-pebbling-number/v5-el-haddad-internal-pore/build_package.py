import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "el-haddad-internal-pore-cp-titanium"
question = r"""The figure shows the fatigue limit of a metal injection moulded commercially pure titanium, measured at $R = -1$ as the stress amplitude that specimens survive for $10^7$ cycles, plotted against $\sqrt{\mathrm{area}}$ of a small hole drilled into the specimen surface; both axes are logarithmic. The solid line is the El Haddad fit to the data,
$$\sigma_w = \sigma_{w0}\sqrt{\frac{a_0}{\sqrt{\mathrm{area}} + a_0}},$$
where $\sigma_{w0}$ is the fatigue limit of smooth specimens and $a_0$ is the El Haddad length, the defect size at which the long-crack threshold, with Murakami's stress intensity range for the defect, gives the smooth-specimen fatigue limit. The fitted curve passes exactly through two of the gridline crossings of the plot.

A component of the same material contains a pore with $\sqrt{\mathrm{area}} = 200\ \mu\mathrm{m}$ that lies deep inside the material, far from every surface. Take the long-crack threshold and the smooth-specimen fatigue limit of the component to be those of the specimens, and use Murakami's $\sqrt{\mathrm{area}}$ model for the stress intensity range of surface and internal defects. Estimate the fatigue limit of the component at $R = -1$, as a stress amplitude in MPa, to two significant figures."""
final_answer = "120"
variants = ["120 MPa", r"$1.2 \times 10^{2}$ MPa"]
solution = r"""Step 1: Find the two crossings.
On the $1$-$2$-$5$ grid the curve meets a vertical gridline at $20, 50, 100, 200, 500, 1000, 2000, 5000\ \mu\mathrm{m}$. It crosses the horizontal lines exactly at $(200\ \mu\mathrm{m}, 100\ \mathrm{MPa})$ and $(1000\ \mu\mathrm{m}, 50\ \mathrm{MPa})$. At the other vertical lines it misses the nearest horizontal line by a clear margin: at $20\ \mu\mathrm{m}$ it is at about $175$ MPa, below the $200$ line; at $100\ \mu\mathrm{m}$ at about $126$ MPa, above the $100$ line; at $500\ \mu\mathrm{m}$ at about $69$ MPa, between $50$ and $100$; at $2000\ \mu\mathrm{m}$ at about $36$ MPa; at $5000\ \mu\mathrm{m}$ at about $23$ MPa, above the $20$ line.

Step 2: Solve for the two parameters of the fit.
Squaring the El Haddad relation gives $\sigma_w^2(\sqrt{\mathrm{area}} + a_0) = \sigma_{w0}^2 a_0$, the same constant at both crossings, so
$$100^2 (200 + a_0) = 50^2 (1000 + a_0), \qquad a_0 = \frac{50^2 \times 1000 - 100^2 \times 200}{100^2 - 50^2} = \frac{500\,000}{7\,500} = 66.7\ \mu\mathrm{m},$$
and $\sigma_{w0} = 100\sqrt{(200 + 66.7)/66.7} = 100 \times 2 = 200$ MPa. The curve is therefore $\sigma_w = 200\sqrt{66.7/(\sqrt{\mathrm{area}} + 66.7)}$, and the smooth-specimen fatigue limit of the material is $200$ MPa. The long-crack threshold follows from the definition of $a_0$ with Murakami's surface factor, $\Delta K_{th} = 0.65\,\sigma_{w0}\sqrt{\pi a_0} = 0.65 \times 200 \times \sqrt{\pi \times 66.7 \times 10^{-6}} = 1.88\ \mathrm{MPa}\sqrt{\mathrm{m}}$ (with the stress amplitude at $R = -1$ as the stress in the range, the convention of the model).

Step 3: The El Haddad length of an internal defect.
For an internal defect Murakami's stress intensity range is $0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ instead of $0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$. The El Haddad length is defined by the threshold and the smooth limit, $a_0 = (\Delta K_{th}/(Y\sigma_{w0}))^2/\pi$, so it is not a material constant but depends on the geometry factor $Y$: with the same threshold and the same smooth limit,
$$a_{0,\mathrm{int}} = a_0 \left(\frac{0.65}{0.50}\right)^2 = 1.69 \times 66.7 = 112.7\ \mu\mathrm{m}.$$
The fatigue limit of the component with an internal pore of $\sqrt{\mathrm{area}} = 200\ \mu\mathrm{m}$ is then
$$\sigma_w = \sigma_{w0}\sqrt{\frac{a_{0,\mathrm{int}}}{200 + a_{0,\mathrm{int}}}} = 200\sqrt{\frac{112.7}{312.7}} = 200 \times 0.600 = 120\ \mathrm{MPa}.$$
The same number comes from the long-crack form, $\sigma_w = \Delta K_{th}/(0.50\sqrt{\pi(200 + 112.7) \times 10^{-6}}) = 1.881/(0.50 \times 0.03134) = 120$ MPa.

Step 4: What the shortcuts give.
Reading the surface curve at $200\ \mu\mathrm{m}$ gives $100$ MPa, the value for a surface hole of that size. Multiplying it by the ratio of the geometry factors, $0.65/0.50 = 1.3$, while keeping the surface value of $a_0$ gives $130$ MPa; that is the long-crack correction applied to a pore that is only three times the El Haddad length, where the transition term matters. The long-crack form with the internal factor and no $a_0$ at all gives $150$ MPa. Taking the crossings at $(20\ \mu\mathrm{m}, 200\ \mathrm{MPa})$ or $(100\ \mu\mathrm{m}, 100\ \mathrm{MPa})$ instead of $(200, 100)$ gives $126$ or $97$ MPa, which round to $130$ and $100$.

Step 5: Conclusion.
The component has a fatigue limit of about $120$ MPa at $R = -1$.

Answer: $120$ MPa."""
rubric = [
    dict(id="c1", description=r"Gives $120$ MPa (two significant figures).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Identifies the two crossings as $(200\ \mu\mathrm{m}, 100\ \mathrm{MPa})$ and $(1000\ \mu\mathrm{m}, 50\ \mathrm{MPa})$ and obtains $a_0 \approx 67\ \mu\mathrm{m}$ and $\sigma_{w0} = 200$ MPa (or the equivalent threshold $\Delta K_{th} \approx 1.9\ \mathrm{MPa}\sqrt{\mathrm{m}}$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Recomputes the El Haddad length for the internal geometry, $a_{0,\mathrm{int}} = (0.65/0.50)^2 a_0 \approx 113\ \mu\mathrm{m}$, instead of keeping the surface value.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Uses the internal-defect factor $0.50$ in place of the surface factor $0.65$ for the pore.", points=1, isFinalAnswer=False),
]
wrong = ["130", "100", "150", "200", "140", "110"]
references = r"""The El Haddad relation: M. H. El Haddad, T. H. Topper and K. N. Smith, Prediction of non propagating cracks, Engineering Fracture Mechanics 11 (1979), 573-584. The diagram of fatigue limit against defect size: H. Kitagawa and S. Takahashi, Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proceedings of the Second International Conference on Mechanical Behavior of Materials, ASM (1976), 627-631. The $\sqrt{\mathrm{area}}$ parameter and the stress intensity ranges $0.65\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for surface and $0.50\,\sigma\sqrt{\pi\sqrt{\mathrm{area}}}$ for internal defects: Y. Murakami and M. Endo, Quantitative evaluation of fatigue strength of metals containing various small defects or cracks, Engineering Fracture Mechanics 17 (1983), 1-15; Y. Murakami and M. Endo, Effects of defects, inclusions and inhomogeneities on fatigue strength, International Journal of Fatigue 16 (1994), 163-182. The setting (metal injection moulded titanium with pores as the fatigue-critical defects) is background; no data from the literature are used, the figure is generated from the fit stated in the solution. The uploaded file verification_notes.txt states the model, lists the curve values at every vertical gridline with the distance to the nearest horizontal line, derives the key by two routes, evaluates the shortcut and misreading routes, and embeds the program with its output."""
necessity = "The two parameters of the fit, the smooth-specimen fatigue limit and the El Haddad length of the material, are given only by the plotted curve; they have to be recovered from the two gridline crossings it passes through, and the text does not state them."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (Kitagawa diagram generated from the El Haddad fit stated in the solution)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "significant_figures", "digits": 2}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Section 1 of verification_notes.txt states the fit the figure was generated from (smooth limit 200 MPa, El Haddad length 66.7 um for surface defects) and lists the curve value at every vertical gridline of the 1-2-5 grid with its distance to the nearest horizontal line, showing that (200 um, 100 MPa) and (1000 um, 50 MPa) are the only exact crossings; section 2 derives the key by two routes (the El Haddad relation with the internal length 1.69 a0 = 112.7 um, and the long-crack form with the threshold 1.88 MPa sqrt(m) and the internal factor 0.50), both 120.1 MPa; section 3 evaluates the shortcut routes and the readings with a wrong crossing; section 4 embeds the program verify_key.py with its output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fatigue limit of the component with the internal pore (El Haddad fit, MIM CP titanium)

Answer key: 120 MPa (two significant figures; 120.1 MPa).

1. Model behind the figure. Surface drilled holes, R = -1, 1e7 cycles. El Haddad relation with Murakami's
   sqrt(area) as the crack size: sigma_w = 200 sqrt(66.67 / (sqrt(area) + 66.67)) MPa, sqrt(area) in um;
   equivalently DK_th = 0.65 x 200 x sqrt(pi x 66.67e-6) = 1.881 MPa sqrt(m). Axes: 1-2-5 logarithmic grid,
   x from 10 to 10000 um, y from 20 to 1000 MPa. Exact crossings (200 um, 100 MPa) and (1000 um, 50 MPa);
   the curve value at every other vertical gridline and its distance to the nearest horizontal line, as a
   fraction of the local step, are listed in the program output (the nearest misses are 15 and 19 percent
   of a step, at 5000 and 20 um). Seven data points at 30, 75, 140, 330, 700, 1500, 3500 um, none at a
   crossing.

2. Key by two routes. Route A: a0 = (50^2 x 1000 - 100^2 x 200)/(100^2 - 50^2) = 66.67 um and
   sigma_w0 = 100 sqrt((200 + a0)/a0) = 200 MPa from the two crossings; for the internal pore the El Haddad
   length is a0 (0.65/0.50)^2 = 112.67 um, and the key is 200 sqrt(112.67/312.67) = 120.06 MPa. Route B:
   DK_th = 1.881 MPa sqrt(m) from the threshold definition, a0_int = (DK_th/(0.50 x 200))^2/pi = 112.67 um,
   key = DK_th/(0.50 sqrt(pi (200 + 112.67) e-6)) = 120.06 MPa.

3. Shortcut and misreading routes: surface curve at 200 um, 100 MPa; factor 1.3 on the surface value with
   a0 kept, 130 MPa; long-crack form with no a0, 150 MPa; smooth limit, 200 MPa; crossings misread as
   (20, 200) or (50, 200) or (100, 100) with (1000, 50): 126, 139, 97 MPa; (200, 100) with (2000, 50):
   108 MPa; (200, 100) with (500, 50) or (5000, 20): no El Haddad curve fits.

4. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v5: El Haddad fit, internal pore in MIM CP titanium (Engineering replacement for SUM-MVBG0GO3)", "", "Domain: Engineering. Subdomain: " + task["task"]["subdomain"] + ". Task type: graph extraction with computation.", "",
             "## Question", "", question, "", "## Answer", "", final_answer + " MPa (two significant figures)", "", "Also accepted: " + ", ".join(variants), "", "## Image necessity", "", necessity, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "", "## Verify field", "", VERIFY_FIELD, "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
