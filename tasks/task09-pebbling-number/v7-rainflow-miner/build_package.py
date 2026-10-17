import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "rainflow-repeating-history-titanium"
question = r"""The figure shows one period of the stress history that a metal injection moulded Ti-6Al-7Nb component sees in service: $24$ reversals, all of them on the gridlines, repeated without change period after period. The S-N curve of the material for fully reversed loading is $\sigma_a = 450\,N^{-1/8}$, with $\sigma_a$ the stress amplitude in MPa and $N$ the cycles to failure, and it has no fatigue limit in the range of interest.

Count the cycles of one period with the rainflow method for repeating histories of ASTM E1049, in which the period is rearranged to begin at its largest peak and every closed loop is one full cycle. Neglect the mean stress of the cycles. Use the linear damage rule with failure at a damage sum of one. How many complete periods of the history does the component survive? Give an integer."""
final_answer = "7"
variants = ["7 periods", "seven"]
solution = r"""Step 1: Read the period off the figure.
The $24$ reversals are, in MPa: $-175, 150, -150, 375, 150, 325, -175, 300, -50, 325, 150, 325, 300, 350, -125, 275, -200, 400, -200, 375, 50, 150, -200, 375$. The largest peak is $400$ at reversal $18$ and the lowest valley is $-200$ (reversals $17$, $19$ and $23$).

Step 2: Rearrange the period to start at the largest peak.
Because the history repeats, reversal $24$ ($375$) is followed by reversal $1$ ($-175$). Starting at the peak of $400$ and going once round the period gives the sequence $400, -200, 375, 50, 150, -200, 375, -175, 150, -150, 375, 150, 325, -175, 300, -50, 325, 150, 325, 300, 350, -125, 275, -200, 400$, which ends where it began. On such a sequence every rainflow cycle closes, so there are no half cycles.

Step 3: Rainflow count.
Applying the three-point rule (a range $Y$ formed by two successive reversals is a cycle, and its two reversals are removed, as soon as the following range $X$ satisfies $X \ge Y$) along the rearranged sequence extracts the twelve cycles, as ranges with their means: $25$ (mean $312.5$), $100$ ($100$), $175$ ($237.5$) twice, $300$ ($0$), $350$ ($125$), $400$ ($75$), $525$ ($87.5$), $550$ ($100$), $575$ ($87.5$) twice, and finally the largest loop $600$ (mean $100$) between the peak $400$ and the valley $-200$. The small loops are the nested excursions $300\,/\,325$ at reversals $12$ to $13$, $150\,/\,50$ at $21$ to $22$, the two $150\,/\,325$ excursions, and so on; the four cycles of range $525$ to $600$ are the big swings between the valleys near $-200$ and the peaks near $375$. The count is $12$ cycles, one for each pair of reversals, as it must be for a closed period of $24$ reversals.

Step 4: Damage per period.
With $N = (450/\sigma_a)^{8}$ and $\sigma_a$ half the range: range $600$, $\sigma_a = 300$, $N = 1.5^{8} = 25.6$, damage $0.0390$; range $575$, $\sigma_a = 287.5$, $N = 36.0$, two cycles, damage $0.0555$; range $550$, $\sigma_a = 275$, $N = 51.4$, damage $0.0195$; range $525$, $\sigma_a = 262.5$, $N = 74.6$, damage $0.0134$; range $400$, $N = 657$, damage $0.0015$; range $350$, $N = 1\,912$, damage $0.0005$; range $300$, $N = 6\,561$, damage $0.0002$; the ranges of $175$ and below contribute less than $10^{-5}$ together. The damage per period is $D = 0.1296$.

Step 5: Periods to failure.
$1/D = 7.72$, so the damage sum reaches one during the eighth period, and the component survives $7$ complete periods.

Step 6: What the other procedures give.
Counting the period as given, from reversal $1$ to $24$, with the ASTM rule for a non-repeating history leaves a residue of half cycles (the $550$ range counts only one half) and gives $D = 0.120$, that is $8.3$ periods, $8$; counting that residue as full cycles gives $5.1$ periods, $5$; ignoring the residue gives $23$; range-pair counting of successive reversals gives $11$; the largest range alone gives $25$.

Answer: $7$ complete periods."""
rubric = [
    dict(id="c1", description=r"Gives $7$ (complete periods).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Obtains the rainflow count of the period as twelve full cycles with the four largest ranges $600$ (once), $575$ (twice), $550$ and $525$ (once each), or an equivalent list in amplitudes.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Obtains a damage per period of about $0.130$ (within $3$ percent), with the range-$600$ cycle contributing about $0.039$ and the two range-$575$ cycles about $0.056$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Treats the period as repeating: starts the count at the $400$ MPa peak (or equivalently closes the loop across the period boundary) so that no half cycles remain.", points=1, isFinalAnswer=False),
]
wrong = ["8", "11", "5", "23", "25", "6"]
references = r"""Cycle counting: ASTM E1049-85 (reapproved 2017), Standard Practices for Cycle Counting in Fatigue Analysis, ASTM International, section 5.4.4 (rainflow counting) and section 5.4.5 (simplified rainflow counting for repeating histories); the original method: M. Matsuishi and T. Endo, Fatigue of metals subjected to varying stress, Japan Society of Mechanical Engineers, Fukuoka (1968); the equivalence of the three-point and four-point formulations: I. Rychlik, A new definition of the rainflow cycle counting method, International Journal of Fatigue 9 (1987), 119-121. Damage accumulation: A. Palmgren, Die Lebensdauer von Kugellagern, Zeitschrift des Vereines Deutscher Ingenieure 68 (1924), 339-341, and M. A. Miner, Cumulative damage in fatigue, Journal of Applied Mechanics 12 (1945), A159-A164. The power law: O. H. Basquin, The exponential law of endurance tests, Proceedings of the American Society for Testing Materials 10 (1910), 625-630. The history is invented for the question and the figure is drawn from it. The uploaded file verification_notes.txt lists the history, the rearranged period, the full cycle list obtained by two independently written counters (the ASTM three-point rule and a four-point algorithm), the damage of every cycle, the periods to failure, and the results of the wrong procedures, with the program embedded."""
necessity = "The sequence of the 24 reversals, which decides how the loops nest and therefore which cycles the rainflow count produces, exists only in the figure; the text gives the material curve and the counting rule but not the history."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Fatigue and fracture of titanium alloys",
    "modality": "image_reference", "taskType": "graph_extraction_computation",
    "imageCreationTool": "matplotlib (stress history drawn from the reversal list stated in the solution)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Section 1 of verification_notes.txt lists the 24 reversals of the period and the sequence rearranged to start at the 400 MPa peak; section 2 gives the full cycle list (twelve cycles with ranges 600, 575, 575, 550, 525, 400, 350, 300, 175, 175, 100, 25) obtained by two independently written counters, the ASTM three-point rule and a four-point algorithm, with the life and damage of every cycle, the damage per period 0.1296 and the periods to failure 7.72; section 3 gives the results of the wrong procedures (8, 11, 5, 23, 25 periods); section 4 embeds the program verify_key.py with its output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: complete periods survived under the repeating stress history (rainflow, MIM Ti-6Al-7Nb)

Answer key: 7 complete periods (failure during the eighth, 7.72 periods).

1. History (one period, 24 reversals, MPa, as drawn): -175, 150, -150, 375, 150, 325, -175, 300, -50, 325,
   150, 325, 300, 350, -125, 275, -200, 400, -200, 375, 50, 150, -200, 375. Material: sigma_a = 450 N^(-1/8).
   Rearranged to start at the largest peak (400, reversal 18), going once round the period: 400, -200, 375,
   50, 150, -200, 375, -175, 150, -150, 375, 150, 325, -175, 300, -50, 325, 150, 325, 300, 350, -125, 275,
   -200, 400.

2. Cycle list (ASTM E1049 three-point rule on the rearranged period; the four-point algorithm written
   separately gives the identical list): ranges 600 (mean 100) once, 575 (87.5) twice, 550 (100), 525 (87.5),
   400 (75), 350 (125), 300 (0), 175 (237.5) twice, 100 (100), 25 (312.5): twelve full cycles. Damage per
   cycle with N = (450/amplitude)^8: 0.03902, 0.02776 each, 0.01945, 0.01341, 0.00152, 0.00052, 0.00015, and
   below 1e-5 for the rest; D = 0.12960 per period; 1/D = 7.716; 7 complete periods.

3. Wrong procedures (section 3 of the output): the half-cycle variant applied to the period as given, 8.34
   (8); range pair counting, 11.2 (11); residue counted as full cycles, 5.09 (5); residue ignored, 23.1 (23);
   largest range alone, 25.6 (25).

4. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v7: rainflow count of a repeating history, MIM Ti-6Al-7Nb (Engineering replacement candidate for SUM-MVBG0GO3)", "", "Domain: Engineering. Subdomain: " + task["task"]["subdomain"] + ". Task type: graph extraction with computation.", "",
             "## Question", "", question, "", "## Answer", "", final_answer + " (complete periods)", "", "Also accepted: " + ", ".join(variants), "", "## Image necessity", "", necessity, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "", "## Verify field", "", VERIFY_FIELD, "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
