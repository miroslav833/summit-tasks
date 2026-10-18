import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "fatigue-test-matrix-minimum-specimens"
question = r"""A fatigue test programme on metal injection moulded Ti-6Al-7Nb varies the five factors listed in the figure, each at three levels: the powder, the specimen geometry, the space-holder content, the oxygen content and the load ratio. Every specimen is made and tested at one level of each factor. The seven level combinations listed in the lower table of the figure are not available; a specimen containing any of them cannot be made or tested.

The programme must cover every admissible pair of levels of two different factors, which is to say that for any two factors and any level of the first with any level of the second, unless that combination is one of the seven unavailable ones, at least one specimen must carry both levels. No other requirement is imposed.

Find the smallest number of specimens with which this can be done. Give a single integer."""
final_answer = "10"
variants = ["$10$", "10 specimens", "ten"]
solution = r"""Step 1: Set up the counting objects.
Write the factors as $A$ (powder), $B$ (specimen geometry), $C$ (space-holder content), $D$ (oxygen content), $E$ (load ratio), with levels $0, 1, 2$ in the order of the figure, so that the unavailable combinations are $A_0E_1$, $A_1B_0$, $A_1C_2$, $A_2B_1$, $B_1C_1$, $B_1D_1$ and $D_0E_0$. A specimen is a choice of one level per factor containing none of them; there are $105$ admissible specimens. The pairs to be covered are the $90 - 7 = 83$ admissible level pairs. Each specimen carries exactly one level pair for each of the ten factor pairs.

Step 2: The bound that comes first, and why it is not the answer.
The factor pairs $AD$, $BE$, $CD$ and $CE$ keep all $9$ of their level pairs, and one specimen covers one level pair of a given factor pair, so at least $9$ specimens are needed. Nine specimens would have to form an orthogonal array on each of these factor pairs at once, and the unavailable combinations make that impossible, as the next step shows in a way that counts.

Step 3: Lower bound $10$.
Call two admissible level pairs incompatible if no admissible specimen contains both. Consider the ten pairs
$$A_0D_0,\ A_0D_1,\ A_0D_2,\ A_1E_0,\ A_1E_2,\ A_2E_0,\ A_2E_2,\ B_0E_1,\ B_1E_1,\ B_2E_1 .$$
They are pairwise incompatible: the three $A_0D_m$ disagree on $D$ with one another and on $A$ with the $A_1E_n$ and $A_2E_n$; the $A_1E_n$ and $A_2E_n$ disagree on $A$ or on $E$ with one another; the three $B_jE_1$ disagree on $B$ with one another and on $E$ with the $A_1E_n$ and $A_2E_n$ (which have $n \in \{0, 2\}$); and $A_0D_m$ with $B_jE_1$ would put $A_0$ and $E_1$ in one specimen, which is unavailable. In words: the TiH$_2$ specimens must appear with all three oxygen levels, so there are at least three of them; the HDH and the gas-atomised specimens must each appear with the load ratios $-1$ and $0.5$, so there are at least two of each; and the load ratio $0.1$ must appear with all three geometries, on three further specimens, none of which can use TiH$_2$ powder and none of which is among the HDH or gas-atomised specimens just counted, since those carry other load ratios. That is $3 + 2 + 2 + 3 = 10$ specimens at least.

Step 4: Upper bound $10$, the decisive step.
The ten specimens
$A_0B_0C_1D_0E_2$, $A_0B_1C_2D_2E_0$, $A_0B_2C_0D_1E_2$, $A_1B_1C_0D_0E_1$, $A_1B_1C_0D_2E_2$, $A_1B_2C_1D_1E_0$, $A_2B_0C_0D_2E_0$, $A_2B_0C_2D_1E_1$, $A_2B_2C_1D_2E_1$, $A_2B_2C_2D_0E_2$
are all admissible (none contains $A_0E_1$, $A_1B_0$, $A_1C_2$, $A_2B_1$, $B_1C_1$, $B_1D_1$ or $D_0E_0$). Listing the level pairs they carry, factor pair by factor pair: $AB$ gives $A_0B_0$, $A_0B_1$, $A_0B_2$, $A_1B_1$ (twice), $A_1B_2$, $A_2B_0$ (twice), $A_2B_2$ (twice), all $7$ admissible pairs; $AC$ gives $A_0C_0$, $A_0C_1$, $A_0C_2$, $A_1C_0$ (twice), $A_1C_1$, $A_2C_0$, $A_2C_1$, $A_2C_2$ (twice), all $8$; $AD$ gives all nine $A_iD_m$, since the three $A_0$ specimens carry $D_0$, $D_2$, $D_1$, the three $A_1$ specimens $D_0$, $D_2$, $D_1$ and the four $A_2$ specimens $D_2$, $D_1$, $D_2$, $D_0$; $AE$ gives $A_0E_2$, $A_0E_0$, $A_1E_1$, $A_1E_2$, $A_1E_0$, $A_2E_0$, $A_2E_1$, $A_2E_2$, all $8$; $BC$ gives $B_0C_1$, $B_1C_2$, $B_2C_0$, $B_1C_0$, $B_2C_1$, $B_0C_0$, $B_0C_2$, $B_2C_2$, all $8$; $BD$ gives $B_0D_0$, $B_1D_2$, $B_2D_1$, $B_1D_0$, $B_2D_2$, $B_0D_2$, $B_0D_1$, $B_2D_0$, all $8$; $BE$, $CD$ and $CE$ give all $9$ each (for $CD$: $C_1D_0$, $C_2D_2$, $C_0D_1$, $C_0D_0$, $C_0D_2$, $C_1D_1$, $C_2D_1$, $C_1D_2$, $C_2D_0$); $DE$ gives $D_0E_2$, $D_2E_0$, $D_1E_2$, $D_0E_1$, $D_2E_2$, $D_1E_0$, $D_1E_1$, $D_2E_1$, all $8$. All $83$ admissible pairs are covered, so $10$ specimens suffice. This programme is the only one with $10$ specimens: with exactly $10$, every one of the ten pairs of Step 3 sits on its own specimen, which fixes the powder and one more level of each specimen, and the remaining levels are then forced one by one; the verification notes confirm by complete enumeration that no other programme of $10$ exists.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $10$. The bound $9$ of Step 2 is not attainable. Constructions that start from a $3 \times 3$ array for two of the factors, or add specimens one at a time covering as many new pairs as possible, end at $11$ or more, because only one arrangement of $10$ specimens works.

Answer: $10$."""
rubric = [
    dict(id="c1", description=r"Gives $10$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit programme of $10$ admissible specimens covering every admissible level pair (a correct $10$-row test matrix).", points=3, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that $9$ specimens are not enough by a valid argument, for instance a set of $10$ admissible level pairs no two of which fit into one admissible specimen (such as $A_0D_0$, $A_0D_1$, $A_0D_2$, $A_1E_0$, $A_1E_2$, $A_2E_0$, $A_2E_2$, $B_0E_1$, $B_1E_1$, $B_2E_1$), or an equivalent counting argument.", points=1, isFinalAnswer=False),
    dict(id="c4", description=r"States the bound of $9$ specimens from a factor pair with $9$ admissible level pairs and recognises that the unavailable combinations make it unattainable.", points=1, isFinalAnswer=False),
]
wrong = ["9", "11", "12", "13"]
references = r"""Pairwise covering test suites (covering arrays of strength two) with constraints between factor levels, and the practice of building them greedily: D. M. Cohen, S. R. Dalal, M. L. Fredman and G. C. Patton, The AETG system: an approach to testing based on combinatorial design, IEEE Transactions on Software Engineering 23 (1997), 437-444. Covering arrays in general, their lower bounds and the hardness of finding minimum ones: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 105 admissible specimens and the 83 admissible pairs, checks the set of 10 pairwise incompatible pairs against every admissible specimen with the reason for each incompatible couple, checks the 10-specimen programme pair by pair, confirms the minimum by an integer programme and shows by complete enumeration that the 10-specimen programme is unique; the program is embedded with its output."""
necessity = "The factors, their levels and above all the seven unavailable level combinations are given only in the figure; the minimum number of specimens depends on exactly which combinations are unavailable (without them the answer would be 9, and other sets of seven give 10, 11 or 12 with many or few optimal programmes)."
verify_field = "Section 3 of verification_notes.txt gives the lower-bound certificate: ten admissible level pairs (A0D0, A0D1, A0D2, A1E0, A1E2, A2E0, A2E2, B0E1, B1E1, B2E1 in the notation of the solution), checked against all 105 admissible specimens so that no specimen contains two of them, with the reason for every one of the 45 couples. Section 4 gives the 10-specimen programme and checks that it covers all 83 admissible pairs. Section 5 confirms the minimum 10 by an integer programme (scipy HiGHS), shows by enumeration with no-good cuts that this programme is the only one with 10 specimens, and counts 47 different ten-pair certificates of the bound. Section 6 shows that randomised greedy constructions reach only 12 to 15 specimens. Section 7 embeds the program verify_key.py with its output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "engineering", "subdomain": "Materials testing: design of a fatigue test programme (pairwise covering test matrices with constraints)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original table figure of the factors, levels and unavailable combinations)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", verify_field)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "”", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "ALL CHECKS PASSED" in out
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: smallest pairwise-covering fatigue test programme with seven unavailable level combinations

Answer key: 10.

1. The instance (from the figure). Factors A powder (0 TiH2-derived, 1 HDH, 2 gas-atomised), B specimen geometry (0 round
   bar, 1 flat, 2 notched), C space-holder content (0, 1, 2 for 0, 15, 30 vol%), D oxygen (0, 1, 2 for 0.15, 0.30,
   0.45 wt%), E load ratio (0, 1, 2 for -1, 0.1, 0.5). Unavailable combinations A0E1, A1B0, A1C2, A2B1, B1C1, B1D1, D0E0. A
   specimen is admissible if it contains none of them: 105 of the 243 level combinations. Admissible level pairs: 83 of
   90; every admissible pair occurs in some admissible specimen, so the covering requirement can be met.
2. Trivial bound: the factor pairs AD, BE, CD, CE each have 9 admissible level pairs and one specimen covers one level
   pair of a factor pair, so at least 9 specimens.
3. Lower bound 10 (certificate, hand-checkable): the ten pairs A0D0, A0D1, A0D2, A1E0, A1E2, A2E0, A2E2, B0E1, B1E1, B2E1
   are pairwise incompatible (no admissible specimen contains two of them). The program checks this against all 105
   specimens and classifies the 45 couples: 36 disagree on a factor level (16 on A, 14 on E, 3 on D, 3 on B); 9 contain
   the unavailable combination A0E1. In words: three TiH2 specimens (one per oxygen level), two HDH and two gas-atomised
   specimens (load ratios -1 and 0.5), three specimens at load ratio 0.1 (one per geometry) which cannot be TiH2 and are
   not among the four just counted. Hence at least 10 specimens. 47 different ten-pair certificates exist.
4. Upper bound 10: the programme A0B0C1D0E2, A0B1C2D2E0, A0B2C0D1E2, A1B1C0D0E1, A1B1C0D2E2, A1B2C1D1E0, A2B0C0D2E0,
   A2B0C2D1E1, A2B2C1D2E1, A2B2C2D0E2 is admissible and covers all 83 admissible pairs (checked pair by pair).
5. Integer programme (scipy HiGHS, one binary variable per admissible specimen, one covering constraint per admissible
   pair): minimum 10; enumeration with no-good cuts finds exactly one optimal programme, the one in 4. So the bound is
   easy to prove and the construction is the whole difficulty: among the C(105, 10) ten-specimen sets, one works.
6. Wrong routes, computed: the trivial bound 9; randomised greedy constructions (add the admissible specimen covering
   most uncovered pairs, ties broken at random, 200 runs) reach 12 in 24 runs, 13 in 88, 14 in 71, 15 in 17, never 10
   or 11; 11 is what a solver reports who proves the bound 10, fails to find the unique programme and settles for the
   best construction found.

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only, scipy optional
   for section 5; running time about two minutes)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

8. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

{textwrap.indent((HERE / "draw_figure.py").read_text(), "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: smallest pairwise-covering fatigue test programme with unavailable level combinations (version 2, unique optimum)", "",
             "Engineering (materials testing, design of experiments), subdomain: " + task["task"]["subdomain"] + ". Earlier contents of this folder (fractional chromatic number v1 and v2; three crack-growth versions; the first test-matrix version with five unavailable combinations and key 11) are archived in work/v1, work/v2-math, work/eng-v1, work/eng-v2, work/eng-v3, work/tm-v1.", "",
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
