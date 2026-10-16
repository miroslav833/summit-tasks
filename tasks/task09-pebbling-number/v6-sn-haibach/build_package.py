import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "sn-curve-haibach-block-loading-titanium"
question = r"""The figure shows the S-N curve of a metal injection moulded Ti-6Al-7Nb alloy at $R = -1$: stress amplitude on a linear axis against cycles to failure on a logarithmic axis. The solid line is a Basquin fit $\sigma_a = A\,N^{-1/k}$ to the failures; it passes exactly through two of the gridline crossings of the plot, both between $10^4$ and $10^7$ cycles. At the knee at $N_e = 10^7$ cycles the fit meets the fatigue limit, and the specimens beyond the knee ran out.

A component of this material is loaded in repeated blocks at $R = -1$. Each block consists of $5\,000$ cycles at a stress amplitude of $320$ MPa followed by $5\,000\,000$ cycles at $180$ MPa. Use the linear damage rule with failure at a damage sum of one, and extend the S-N curve below the fatigue limit by Haibach's rule, a second Basquin line through the knee with the exponent $2k - 1$ in place of $k$. How many complete blocks does the component survive? Give an integer."""
final_answer = "5"
variants = ["5 blocks", "five"]
solution = r"""Step 1: Find the two crossings.
The vertical gridlines are at $1, 2, 5$ times each decade of cycles and the horizontal gridlines every $10$ MPa. Following the fitted curve across the horizontal lines, it meets a vertical line exactly at $(5 \times 10^4\ \text{cycles}, 310\ \text{MPa})$ and at $(2 \times 10^6\ \text{cycles}, 230\ \text{MPa})$. Everywhere else it crosses a horizontal line between two vertical lines: at $290$ MPa it is at about $1.14 \times 10^5$, past the $10^5$ line; at $240$ MPa at about $1.18 \times 10^6$, past the $10^6$ line; at $260$ MPa at about $4.4 \times 10^5$, short of the $5 \times 10^5$ line; at $350$ MPa at about $1.1 \times 10^4$.

Step 2: The Basquin parameters.
From the two crossings, $k = \ln(2 \times 10^6 / 5 \times 10^4) / \ln(310/230) = \ln 40 / \ln 1.3478 = 3.689 / 0.2985 = 12.36$, and $A = 310 \times (5 \times 10^4)^{1/12.36} = 310 \times 2.400 = 744$ MPa. The fatigue limit at the knee is $\sigma_e = A\,N_e^{-1/k} = 744 \times 10^{-7/12.36} = 744 \times 0.2714 = 201.9$ MPa.

Step 3: Life at the two amplitudes of the block.
At $320$ MPa, above the fatigue limit, $N = (A/320)^{k} = (2.325)^{12.36} = 3.38 \times 10^4$ cycles. At $180$ MPa, below the fatigue limit, Haibach's extension gives $N = N_e\,(\sigma_e/180)^{2k-1} = 10^7 \times (1.1218)^{23.72} = 10^7 \times 15.25 = 1.52 \times 10^8$ cycles.

Step 4: Damage per block and the number of blocks.
$D = 5\,000 / 3.38 \times 10^4 + 5 \times 10^6 / 1.52 \times 10^8 = 0.148 + 0.033 = 0.181$ per block, so failure after $1/0.181 = 5.53$ blocks. The component survives $5$ complete blocks.

Step 5: What the other readings and rules give.
Taking the crossings at the major lines, $(10^5, 290)$ and $(10^6, 240)$, gives $k = 12.17$, $A = 747$ MPa and $4.63$ blocks, that is $4$; either one of them with the correct other crossing gives $4.9$ or $4.8$ blocks, again $4$. Pairing $(5 \times 10^5, 260)$ with $(2 \times 10^6, 230)$ gives $6.3$ blocks, that is $6$. Ignoring the cycles below the fatigue limit gives $6.75$ blocks, that is $6$; extending the Basquin line below the limit with the same exponent $k$ gives $3.7$ blocks, that is $3$. The integer $5$ is unchanged by rounding $k$ to $12.3$ or $12.4$ or the fatigue limit to $200$ or $202$ MPa.

Answer: $5$ complete blocks."""
rubric = [
    dict(id="c1", description=r"Gives $5$ (complete blocks).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Identifies the two crossings as $(5 \times 10^4, 310\ \text{MPa})$ and $(2 \times 10^6, 230\ \text{MPa})$ and obtains $k \approx 12.4$ (equivalently a Basquin exponent of about $-0.081$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Obtains the fatigue limit at the knee, about $202$ MPa, and the Haibach life at $180$ MPa of about $1.5 \times 10^8$ cycles (within $10$ percent).", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Obtains a damage of about $0.18$ per block, with about $0.15$ from the $320$ MPa cycles and $0.03$ from the $180$ MPa cycles.", points=1, isFinalAnswer=False),
]
wrong = ["4", "6", "3", "7", "9"]
references = r"""The power law for the finite-life region: O. H. Basquin, The exponential law of endurance tests, Proceedings of the American Society for Testing Materials 10 (1910), 625-630. The linear damage rule: A. Palmgren, Die Lebensdauer von Kugellagern, Zeitschrift des Vereines Deutscher Ingenieure 68 (1924), 339-341, and M. A. Miner, Cumulative damage in fatigue, Journal of Applied Mechanics 12 (1945), A159-A164. The extension of the S-N curve below the fatigue limit with the exponent $2k - 1$: E. Haibach, Modifizierte lineare Schadensakkumulations-Hypothese zur Beruecksichtigung des Dauerfestigkeitsabfalls mit fortschreitender Schaedigung, Technische Mitteilung TM 50/70, Laboratorium fuer Betriebsfestigkeit, Darmstadt (1970); see also E. Haibach, Betriebsfestigkeit, third edition, Springer (2006), chapter 3. The setting (metal injection moulded titanium alloy) is background; the figure is generated from the fit stated in the solution and no literature data are used. The uploaded file verification_notes.txt states the fit, lists where the drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, derives the block count by two routes, and evaluates the wrong crossings, the wrong damage rules and the rounding robustness of the integer, with the program embedded."""
necessity = "The Basquin parameters and the fatigue limit at the knee exist only in the plotted curve; they have to be recovered from the two gridline crossings the curve passes through, and the text states neither the exponent nor the fatigue limit."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (S-N diagram generated from the Basquin fit stated in the solution)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Section 1 of verification_notes.txt states the fit the figure was generated from (k = 12.36, A = 744 MPa, knee at 1e7 cycles, fatigue limit 201.9 MPa) and lists where the drawn curve crosses every horizontal gridline with the distance to the nearest vertical line, showing that (5e4, 310) and (2e6, 230) are the only exact crossings; section 2 derives the block count by two routes (closed form, and a numerical reconstruction of the curve with the crossings and lives found by bisection), both 5.53 blocks; section 3 evaluates the wrong crossings (4 or 6 blocks), the wrong damage rules (6 and 3) and the rounding robustness of the integer; section 4 embeds the program verify_key.py with its output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: complete loading blocks survived (S-N curve of MIM Ti-6Al-7Nb, Haibach extension)

Answer key: 5 complete blocks (failure after 5.53 blocks).

1. Model behind the figure. Basquin fit sigma_a = A N^(-1/k) through the gridline crossings (5e4 cycles,
   310 MPa) and (2e6 cycles, 230 MPa): k = 12.358, A = 744.0 MPa; knee at 1e7 cycles, fatigue limit
   201.9 MPa, horizontal beyond the knee. Axes: cycles 1e4 to 1e8 with 1-2-5 gridlines, stress linear with
   gridlines every 10 MPa. Nine failure points on the fit (1.4e4 to 7e6 cycles), run-outs at 2e7 and 5e7.
   The program output lists where the curve crosses every horizontal line and the distance to the nearest
   vertical line as a fraction of the local step: the only exact crossings are the two above; the closest
   misses are 14 percent of a step at 260 MPa (5e5), 16 percent at 330 and 350 MPa, 19 percent at 280 and
   290 MPa (1e5), 24 percent at 240 MPa (1e6).

2. Key by two routes. Route A (closed form): N(320) = (744.0/320)^12.358 = 3.377e4 cycles, damage 0.1480 per
   block; sigma_e = 201.9 MPa; N(180) = 1e7 (201.9/180)^(23.72) = 1.525e8 cycles, damage 0.0328; total
   0.1808 per block, 5.53 blocks, 5 complete. Route B: the drawn curve is regenerated, the crossings located
   by bisection, the fit redone from the two exact crossings and the lives found by root finding on the
   curve: 5.53 blocks.

3. Wrong crossings and wrong rules (section 3 of the output): the major-line pair (1e5, 290) and (1e6, 240)
   gives k = 12.17 and 4.63 blocks (4); each of them combined with the correct other crossing gives 4.92 or
   4.76 blocks (4); (1e4, 350) with (1e6, 240) gives 4.62 (4); (5e5, 260) with (2e6, 230) gives 6.30 (6);
   (1e4, 350) with (2e6, 230) and (5e4, 310) with (5e5, 260) give 5.25 and 6.00, which floor to 5. No damage
   below the fatigue limit: 6.75 blocks (6); same exponent below the limit: 3.72 blocks (3). Rounding k to
   12.3 or 12.4 (A refitted from either crossing) or the fatigue limit to 200 or 202 MPa leaves the integer
   at 5.

4. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v6: S-N curve with Haibach extension, block loading of MIM Ti-6Al-7Nb (Engineering replacement for SUM-MVBG0GO3)", "", "Domain: Engineering. Subdomain: " + task["task"]["subdomain"] + ". Task type: graph extraction with computation.", "",
             "## Question", "", question, "", "## Answer", "", final_answer + " (complete blocks)", "", "Also accepted: " + ", ".join(variants), "", "## Image necessity", "", necessity, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "", "## Verify field", "", VERIFY_FIELD, "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
