import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "fatigue-test-matrix-six-factors"
question = r"""A fatigue test programme on metal injection moulded Ti-6Al-7Nb varies the six factors listed in the figure, each at three levels: the powder, the specimen geometry, the space-holder content, the oxygen content, the load ratio and the test environment. Every specimen is made and tested at one level of each factor. The ten level combinations listed in the lower table of the figure are not available; a specimen containing any of them cannot be made or tested.

The programme must cover every admissible pair of levels of two different factors, which is to say that for any two factors and any level of the first with any level of the second, unless that combination is one of the ten unavailable ones, at least one specimen must carry both levels. No other requirement is imposed.

Find the smallest number of specimens with which this can be done. Give a single integer."""
final_answer = "11"
variants = ["$11$", "11 specimens", "eleven"]
solution = r"""Step 1: Set up the counting objects.
Write the factors as $A$ (powder), $B$ (specimen geometry), $C$ (space-holder content), $D$ (oxygen content), $E$ (load ratio), $F$ (environment), with levels $0, 1, 2$ in the order of the figure, so that the unavailable combinations are $A_0B_0$, $A_0C_0$, $A_0D_2$, $A_0F_1$, $A_1B_2$, $B_1E_0$, $C_0D_0$, $C_1E_2$, $D_1F_0$ and $D_2F_1$. A specimen is a choice of one level per factor containing none of them; there are $223$ admissible specimens. The pairs to be covered are the $135 - 10 = 125$ admissible level pairs. Each specimen carries exactly one level pair for each of the fifteen factor pairs.

Step 2: The bounds that come first, and why they are not the answer.
Seven factor pairs ($AE$, $BC$, $BD$, $BF$, $CF$, $DE$, $EF$) keep all $9$ of their level pairs, so at least $9$ specimens are needed. Calling two admissible level pairs incompatible when no admissible specimen contains both, a set of pairwise incompatible pairs also bounds the number of specimens from below, since each needs its own specimen; the largest such sets have $10$ members (for instance $A_1D_0$, $A_2D_0$ together with $C_1D_1$, $C_1D_2$, $C_2D_1$, $C_2D_2$ and $C_0F_0$, $C_0F_1$, $C_0F_2$, $D_0F_1$, or $A_0E_0$, $A_0E_1$, $A_0E_2$ with the pairs $A_1D_0$, $A_2D_0$, $C_1D_1$, $C_1D_2$, $C_2D_1$, $C_2D_2$ and $D_0F_0$), so that route gives $10$. Neither $9$ nor $10$ specimens suffice.

Step 3: Lower bound $11$ from a weighting of level pairs.
Give the following admissible level pairs these weights: $A_1D_0$, $A_2D_0$, $A_0E_0$, $A_0E_1$, $A_0E_2$, $C_1D_1$, $C_2D_1$, $C_1F_1$, $C_2F_1$, $D_0F_0$, $D_0F_2$ weight $\tfrac12$ each, and $C_1D_2$, $C_2D_2$, $C_0F_0$, $C_0F_1$, $C_0F_2$ weight $1$ each; the total is $11 \cdot \tfrac12 + 5 = \tfrac{21}{2}$. No admissible specimen carries total weight more than $1$. To see this, sort the specimens by their level of $C$. A specimen with $C_0$ carries weight $1$ from its $C_0F$ pair and nothing else: $A_0$ and $D_0$ are unavailable with $C_0$, so the $A_0E$, $A_iD_0$ and $D_0F$ pairs cannot occur, and no $C_0D$ pair is weighted. A specimen with $C_1$ or $C_2$ and $D_2$ carries weight $1$ from $C_1D_2$ or $C_2D_2$; it cannot carry $A_0E$ ($A_0D_2$ is unavailable) nor $C_iF_1$ ($D_2F_1$ is unavailable), and the $D_0$ pairs are absent. A specimen with $C_1$ or $C_2$ and $D_1$ carries $\tfrac12$ from $C_iD_1$ and at most one further half: $A_0E$ and $C_iF_1$ cannot both occur, because $A_0F_1$ is unavailable, and the $D_0$ pairs are absent. A specimen with $C_1$ or $C_2$ and $D_0$ carries no $C_iD$ weight; of the halves $A_1D_0$ or $A_2D_0$, $A_0E$, $C_iF_1$ and $D_0F_0$ or $D_0F_2$ at most two can occur: $A_iD_0$ and $A_0E$ exclude each other through $A$, $C_iF_1$ and $D_0F_{0,2}$ through $F$, and $A_0E$ with $C_iF_1$ is excluded by $A_0F_1$. So every specimen has weight at most $1$ while every programme covers all sixteen weighted pairs, whose weights add to $\tfrac{21}{2}$; a programme therefore has at least $\tfrac{21}{2}$, that is at least $11$, specimens.

Step 4: Upper bound $11$, the decisive step.
The eleven specimens
$A_0B_1C_2D_0E_2F_2$, $A_0B_2C_1D_0E_0F_0$, $A_0B_2C_2D_1E_1F_2$, $A_1B_0C_0D_1E_0F_2$, $A_1B_0C_1D_0E_1F_2$, $A_1B_0C_2D_2E_2F_0$, $A_1B_1C_1D_1E_1F_1$, $A_2B_0C_2D_0E_0F_1$, $A_2B_1C_0D_2E_1F_0$, $A_2B_2C_0D_1E_2F_1$, $A_2B_2C_1D_2E_0F_2$
are all admissible. Factor pair by factor pair they carry: $AB$: $A_0B_1$, $A_0B_2$ (twice), $A_1B_0$ (three times), $A_1B_1$, $A_2B_0$, $A_2B_1$, $A_2B_2$ (twice), all $7$ admissible pairs; $AC$: $A_0C_1$, $A_0C_2$ (twice), $A_1C_0$, $A_1C_1$ (twice), $A_1C_2$, $A_2C_0$ (twice), $A_2C_1$, $A_2C_2$, all $8$; $AD$: $A_0D_0$ (twice), $A_0D_1$, $A_1D_0$, $A_1D_1$ (twice), $A_1D_2$, $A_2D_0$, $A_2D_1$, $A_2D_2$ (twice), all $8$; $AE$: $A_0E_0$, $A_0E_1$, $A_0E_2$, $A_1E_0$, $A_1E_1$ (twice), $A_1E_2$, $A_2E_0$ (twice), $A_2E_1$, $A_2E_2$, all $9$; $AF$: $A_0F_0$, $A_0F_2$ (twice), $A_1F_0$, $A_1F_1$, $A_1F_2$ (twice), $A_2F_0$, $A_2F_1$ (twice), $A_2F_2$, all $8$; $BC$, $BD$, $BF$, $CF$, $DE$ and $EF$: all $9$ each (for $CF$: $C_2F_2$, $C_1F_0$, $C_2F_2$, $C_0F_2$, $C_1F_2$, $C_2F_0$, $C_1F_1$, $C_2F_1$, $C_0F_0$, $C_0F_1$, $C_1F_2$, which contains every $C_iF_j$); $BE$: $B_1E_2$, $B_2E_0$, $B_2E_1$, $B_0E_0$, $B_0E_1$, $B_0E_2$, $B_1E_1$, $B_2E_2$, all $8$; $CD$: $C_2D_0$, $C_1D_0$, $C_2D_1$, $C_0D_1$, $C_2D_2$, $C_1D_1$, $C_0D_2$, $C_1D_2$, all $8$; $CE$: $C_2E_2$, $C_1E_0$, $C_2E_1$, $C_0E_0$, $C_1E_1$, $C_2E_0$, $C_0E_1$, $C_0E_2$, all $8$; $DF$: $D_0F_2$, $D_0F_0$, $D_1F_2$, $D_2F_0$, $D_1F_1$, $D_0F_1$, $D_2F_2$, all $7$. All $125$ admissible pairs are covered, so $11$ specimens suffice. Only four programmes of $11$ specimens exist, and they differ only in the environment chosen for one or two of the specimens.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $11$. The bound $9$ of Step 2 is not attainable, and neither is $10$, which is as far as any set of pairwise incompatible pairs reaches; the half weights of Step 3 are what close the gap. Constructions that add specimens one at a time covering as many new pairs as possible end at $13$ or more.

Answer: $11$."""
rubric = [
    dict(id="c1", description=r"Gives $11$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit programme of $11$ admissible specimens covering every admissible level pair (a correct $11$-row test matrix).", points=3, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that $10$ specimens are not enough by a valid argument, for instance a weighting of admissible level pairs with total more than $10$ under which no admissible specimen carries more than $1$ (such as the half-integral weighting of total $21/2$ in the solution), or an exhaustive argument whose case structure is stated.", points=1, isFinalAnswer=False),
    dict(id="c4", description=r"Establishes the lower bound $10$ (for instance from ten pairwise incompatible level pairs) and recognises that it is not attained.", points=1, isFinalAnswer=False),
]
wrong = ["9", "10", "12", "13"]
references = r"""Pairwise covering test suites (covering arrays of strength two) with constraints between factor levels, and the practice of building them greedily: D. M. Cohen, S. R. Dalal, M. L. Fredman and G. C. Patton, The AETG system: an approach to testing based on combinatorial design, IEEE Transactions on Software Engineering 23 (1997), 437-444. Covering arrays in general, their lower bounds and the hardness of finding minimum ones: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 223 admissible specimens and the 125 admissible pairs, checks the weighting of total 21/2 against every admissible specimen, shows that no set of pairwise incompatible pairs has more than 10 members, checks the 11-specimen programme pair by pair, confirms the minimum by an integer programme and enumerates the four optimal programmes; the program is embedded with its output."""
necessity = "The factors, their levels and above all the ten unavailable level combinations are given only in the figure; the minimum number of specimens depends on exactly which combinations are unavailable (without them the answer would be 9, and other sets of ten give 10, 11 or 12 with many or few optimal programmes)."
verify_field = "Section 3 of verification_notes.txt gives the lower-bound certificate: sixteen admissible level pairs with weights 1/2 and 1 adding to 21/2, checked against all 223 admissible specimens so that none carries more than weight 1; Section 2 shows that no set of pairwise incompatible pairs has more than 10 members, so the half weights are needed. Section 4 gives the 11-specimen programme and checks that it covers all 125 admissible pairs. Section 5 confirms the minimum 11 by an integer programme (scipy HiGHS) and lists the four optimal programmes found by enumeration with no-good cuts. Section 6 shows that randomised greedy constructions reach only 13 to 17 specimens. Section 7 embeds the program verify_key.py with its output."
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
    txt = f"""VERIFICATION NOTES: smallest pairwise-covering fatigue test programme with ten unavailable level combinations

Answer key: 11.

1. The instance (from the figure). Factors A powder (0 TiH2-derived, 1 HDH, 2 gas-atomised), B specimen geometry (0 round
   bar, 1 flat, 2 notched), C space-holder content (0, 1, 2 for 0, 15, 30 vol%), D oxygen (0, 1, 2 for 0.15, 0.30,
   0.45 wt%), E load ratio (0, 1, 2 for -1, 0.1, 0.5), F environment (0 laboratory air, 1 Ringer's solution, 2 Ringer's
   with hydrogen charging). Unavailable combinations A0B0, A0C0, A0D2, A0F1, A1B2, B1E0, C0D0, C1E2, D1F0, D2F1. A
   specimen is admissible if it contains none of them: 223 of the 729 level combinations. Admissible level pairs: 125 of
   135; every admissible pair occurs in some admissible specimen, so the covering requirement can be met.
2. Trivial bound: seven factor pairs keep all 9 level pairs, so at least 9 specimens. Sets of pairwise incompatible
   pairs (no admissible specimen contains two of them) have at most 10 members (maximum found by exhaustive clique
   search in the program), so that route proves only 10.
3. Lower bound 11 (certificate, hand-checkable): weights 1/2 on A1D0, A2D0, A0E0, A0E1, A0E2, C1D1, C2D1, C1F1, C2F1, D0F0,
   D0F2 and 1 on C1D2, C2D2, C0F0, C0F1, C0F2, total 21/2. The program checks that every one of the 223 admissible
   specimens carries total weight at most 1 (202 of them exactly 1) and prints the weight of each; Step 3 of the
   solution gives the case split by the level of C. Every programme covers each weighted pair, so it has at least
   21/2 specimens, hence 11.
4. Upper bound 11: the programme A0B1C2D0E2F2, A0B2C1D0E0F0, A0B2C2D1E1F2, A1B0C0D1E0F2, A1B0C1D0E1F2, A1B0C2D2E2F0,
   A1B1C1D1E1F1, A2B0C2D0E0F1, A2B1C0D2E1F0, A2B2C0D1E2F1, A2B2C1D2E0F2 is admissible and covers all 125 admissible pairs
   (checked pair by pair).
5. Integer programme (scipy HiGHS, one binary variable per admissible specimen, one covering constraint per admissible
   pair): minimum 11; enumeration with no-good cuts finds four optimal programmes, which differ only in the environment
   of one or two specimens. So the bound needs half weights and the construction has very few solutions.
6. Wrong routes, computed: the trivial bound 9; the incompatible-pair bound 10 (what a solver reports who proves 10 and
   believes a 10-specimen programme exists); randomised greedy constructions (add the admissible specimen covering most
   uncovered pairs, ties at random, 200 runs) reach 13 in 24 runs, 14 in 106, 15 in 55, 16 in 14, 17 in 1, never 11
   or 12; 12 is what a solver reports who proves 11 and settles for the best construction found.

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
    lines = ["# task08: smallest pairwise-covering fatigue test programme with unavailable level combinations (version 3, six factors)", "",
             "Engineering (materials testing, design of experiments), subdomain: " + task["task"]["subdomain"] + ". Earlier contents of this folder (fractional chromatic number v1 and v2; three crack-growth versions; the five-factor test-matrix versions with keys 11 and 10) are archived in work/v1, work/v2-math, work/eng-v1, work/eng-v2, work/eng-v3, work/tm-v1, work/tm-v2.", "",
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
