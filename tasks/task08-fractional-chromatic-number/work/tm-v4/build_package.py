import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "fatigue-test-matrix-eight-unavailable"
question = r"""A fatigue test programme on metal injection moulded Ti-6Al-7Nb varies the five factors listed in the figure, each at three levels: the powder, the specimen geometry, the space-holder content, the oxygen content and the load ratio. Every specimen is made and tested at one level of each factor. The eight level combinations listed in the lower table of the figure are not available; a specimen containing any of them cannot be made or tested.

The programme must cover every admissible pair of levels of two different factors, which is to say that for any two factors and any level of the first with any level of the second, unless that combination is one of the eight unavailable ones, at least one specimen must carry both levels. No other requirement is imposed.

Find the smallest number of specimens with which this can be done. Give a single integer."""
final_answer = "11"
variants = ["$11$", "11 specimens", "eleven"]
solution = r"""Step 1: Set up the counting objects.
Write the factors as $A$ (powder), $B$ (specimen geometry), $C$ (space-holder content), $D$ (oxygen content), $E$ (load ratio), with levels $0, 1, 2$ in the order of the figure, so that the unavailable combinations are $A_0C_2$, $A_0D_1$, $A_1C_1$, $A_1E_0$, $A_2B_2$, $B_0C_2$, $B_1D_2$ and $B_2E_1$. A specimen is a choice of one level per factor containing none of them; there are $82$ admissible specimens. The pairs to be covered are the $90 - 8 = 82$ admissible level pairs. Each specimen carries exactly one level pair for each of the ten factor pairs.

Step 2: The bounds that come first, and why they are not the answer.
The factor pairs $CD$, $CE$ and $DE$ keep all $9$ of their level pairs, and one specimen covers one level pair of a given factor pair, so at least $9$ specimens are needed. Counting specimens level by level gives no more: every level of every factor needs at least three specimens, and no level is forced into a single level of another factor. Neither $9$ nor $10$ specimens suffice, as the next step shows.

Step 3: Lower bound $11$.
Call two admissible level pairs incompatible if no admissible specimen contains both. Consider the eleven pairs
$$A_1B_0,\ A_1B_1,\ A_0E_1,\ A_0E_2,\ A_2E_1,\ A_2E_2,\ B_2D_1,\ C_2D_2,\ D_0E_0,\ D_1E_0,\ D_2E_0 .$$
They are pairwise incompatible, for the following reasons. Couples that need one factor at two different levels: $A_1B_j$ against $A_0E_n$ and $A_2E_n$ (factor $A$), $A_0E_n$ against $A_2E_n$ (factor $A$), $A_1B_0$ against $A_1B_1$ and both against $B_2D_1$ (factor $B$), every $A_iE_n$ with $n \in \{1, 2\}$ against the three $D_mE_0$ and against one another when $n$ differs (factor $E$), and $B_2D_1$, $C_2D_2$, $D_0E_0$, $D_1E_0$, $D_2E_0$ against one another whenever their $D$ levels differ (factor $D$). Couples whose union contains an unavailable combination: $A_1B_j$ with any $D_mE_0$ contains $A_1E_0$; $A_1B_0$ with $C_2D_2$ contains $B_0C_2$; $A_1B_1$ with $C_2D_2$ contains $B_1D_2$; $A_0E_n$ with $B_2D_1$ contains $A_0D_1$; $A_0E_n$ with $C_2D_2$ contains $A_0C_2$; $A_2E_n$ with $B_2D_1$ contains $A_2B_2$. Finally four couples whose union is admissible but cannot be completed to a specimen: $A_2E_n$ with $C_2D_2$ fixes $A_2$, $C_2$, $D_2$, and then $B_0$ is unavailable with $C_2$, $B_1$ with $D_2$ and $B_2$ with $A_2$, so no geometry remains; $B_2D_1$ with $D_1E_0$ fixes $B_2$, $D_1$, $E_0$, and then $A_0$ is unavailable with $D_1$, $A_1$ with $E_0$ and $A_2$ with $B_2$, so no powder remains; $C_2D_2$ with $D_2E_0$ fixes $C_2$, $D_2$, $E_0$, and then $A_0$ is unavailable with $C_2$, $A_1$ with $E_0$, and $A_2$ would leave no geometry, as just shown. Since each of the eleven pairs must be covered and no specimen covers two of them, every programme has at least $11$ specimens.

Step 4: Upper bound $11$, the decisive step.
The eleven specimens
$A_0B_0C_1D_2E_1$, $A_0B_1C_0D_0E_2$, $A_0B_2C_1D_0E_0$, $A_1B_0C_0D_1E_1$, $A_1B_1C_2D_0E_1$, $A_1B_2C_0D_1E_2$, $A_1B_2C_2D_2E_2$, $A_2B_0C_0D_2E_0$, $A_2B_0C_1D_0E_2$, $A_2B_1C_1D_1E_1$, $A_2B_1C_2D_1E_0$
are all admissible. Factor pair by factor pair they carry: $AB$: $A_0B_0$, $A_0B_1$, $A_0B_2$, $A_1B_0$, $A_1B_1$, $A_1B_2$ (twice), $A_2B_0$ (twice), $A_2B_1$ (twice), all $8$ admissible pairs; $AC$: $A_0C_1$ (twice), $A_0C_0$, $A_1C_0$ (twice), $A_1C_2$ (twice), $A_2C_0$, $A_2C_1$ (twice), $A_2C_2$, all $7$; $AD$: $A_0D_2$, $A_0D_0$ (twice), $A_1D_1$ (twice), $A_1D_0$, $A_1D_2$, $A_2D_2$, $A_2D_0$, $A_2D_1$ (twice), all $8$; $AE$: $A_0E_1$, $A_0E_2$, $A_0E_0$, $A_1E_1$ (twice), $A_1E_2$ (twice), $A_2E_0$ (twice), $A_2E_2$, $A_2E_1$, all $8$; $BC$: $B_0C_1$ (twice), $B_1C_0$, $B_2C_1$, $B_0C_0$ (twice), $B_1C_2$ (twice), $B_2C_0$, $B_2C_2$, $B_1C_1$, all $8$; $BD$: $B_0D_2$ (twice), $B_1D_0$ (twice), $B_2D_0$, $B_0D_1$, $B_2D_1$, $B_2D_2$, $B_0D_0$, $B_1D_1$ (twice), all $8$; $BE$: $B_0E_1$ (twice), $B_1E_2$, $B_2E_0$, $B_1E_1$ (twice), $B_2E_2$ (twice), $B_0E_0$, $B_0E_2$, $B_1E_0$, all $8$; $CD$: $C_1D_2$, $C_0D_0$, $C_1D_0$ (twice), $C_0D_1$ (twice), $C_2D_0$, $C_2D_2$, $C_0D_2$, $C_1D_1$, $C_2D_1$, all $9$; $CE$: $C_1E_1$ (twice), $C_0E_2$ (twice), $C_1E_0$, $C_0E_1$, $C_2E_1$, $C_2E_2$, $C_0E_0$, $C_1E_2$, $C_2E_0$, all $9$; $DE$: $D_2E_1$, $D_0E_2$ (twice), $D_0E_0$, $D_1E_1$ (twice), $D_0E_1$, $D_1E_2$, $D_2E_2$, $D_2E_0$, $D_1E_0$, all $9$. All $82$ admissible pairs are covered, so $11$ specimens suffice. This programme is the only one with $11$ specimens, as the complete enumeration in the verification notes shows.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $11$. The bound $9$ of Step 2 is not attainable and neither is $10$; sets of ten pairwise incompatible pairs that use only level clashes and unavailable combinations are easy to find, but closing the gap to $11$ needs the couples that are incompatible only because no completion to a specimen exists. Constructions that add specimens one at a time covering as many new pairs as possible end at $12$ or more almost always, because a single arrangement of $11$ specimens works.

Answer: $11$."""
rubric = [
    dict(id="c1", description=r"Gives $11$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit programme of $11$ admissible specimens covering every admissible level pair (a correct $11$-row test matrix).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that $10$ specimens are not enough by a valid argument, for instance a set of $11$ admissible level pairs no two of which fit into one admissible specimen (such as $A_1B_0$, $A_1B_1$, $A_0E_1$, $A_0E_2$, $A_2E_1$, $A_2E_2$, $B_2D_1$, $C_2D_2$, $D_0E_0$, $D_1E_0$, $D_2E_0$, including the couples that are incompatible only because they cannot be completed), or an exhaustive argument whose case structure is stated.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Establishes the lower bound $10$ (for instance from ten pairwise incompatible level pairs) and recognises that it is not attained.", points=1, isFinalAnswer=False),
]
wrong = ["9", "10", "12", "13"]
references = r"""Pairwise covering test suites (covering arrays of strength two) with constraints between factor levels, and the practice of building them greedily: D. M. Cohen, S. R. Dalal, M. L. Fredman and G. C. Patton, The AETG system: an approach to testing based on combinatorial design, IEEE Transactions on Software Engineering 23 (1997), 437-444. Covering arrays in general, their lower bounds and the hardness of finding minimum ones: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 82 admissible specimens and the 82 admissible pairs, checks the set of 11 pairwise incompatible pairs against every admissible specimen with the reason for each incompatible couple, checks the 11-specimen programme pair by pair, confirms the minimum by an integer programme and shows by complete enumeration that the 11-specimen programme is unique; the program is embedded with its output."""
necessity = "The factors, their levels and above all the eight unavailable level combinations are given only in the figure; the minimum number of specimens depends on exactly which combinations are unavailable (without them the answer would be 9, and other sets of eight give 10, 11 or 12 with many or few optimal programmes)."
verify_field = "Section 3 of verification_notes.txt gives the lower-bound certificate: eleven admissible level pairs (A1B0, A1B1, A0E1, A0E2, A2E1, A2E2, B2D1, C2D2, D0E0, D1E0, D2E0 in the notation of the solution), checked against all 82 admissible specimens so that no specimen contains two of them, with the reason for every one of the 55 couples, four of which are incompatible only because no completion to a specimen exists. Section 4 gives the 11-specimen programme and checks that it covers all 82 admissible pairs. Section 5 confirms the minimum 11 by an integer programme (scipy HiGHS), shows by enumeration with no-good cuts that this programme is the only one with 11 specimens, and counts the eleven-pair certificates of the bound. Section 6 shows what randomised greedy constructions reach. Section 7 embeds the program verify_key.py with its output."
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
    txt = f"""VERIFICATION NOTES: smallest pairwise-covering fatigue test programme with eight unavailable level combinations

Answer key: 11.

1. The instance (from the figure). Factors A powder (0 TiH2-derived, 1 HDH, 2 gas-atomised), B specimen geometry (0 round
   bar, 1 flat, 2 notched), C space-holder content (0, 1, 2 for 0, 15, 30 vol%), D oxygen (0, 1, 2 for 0.15, 0.30,
   0.45 wt%), E load ratio (0, 1, 2 for -1, 0.1, 0.5). Unavailable combinations A0C2, A0D1, A1C1, A1E0, A2B2, B0C2, B1D2,
   B2E1. A specimen is admissible if it contains none of them: 82 of the 243 level combinations. Admissible level
   pairs: 82 of 90; every admissible pair occurs in some admissible specimen, so the covering requirement can be met.
2. Trivial bound: the factor pairs CD, CE, DE each have 9 admissible level pairs and one specimen covers one level pair
   of a factor pair, so at least 9 specimens. Level counting with forced levels gives no more (no level is forced).
3. Lower bound 11 (certificate, hand-checkable): the eleven pairs A1B0, A1B1, A0E1, A0E2, A2E1, A2E2, B2D1, C2D2, D0E0,
   D1E0, D2E0 are pairwise incompatible (no admissible specimen contains two of them). The program checks this against
   all 82 specimens and classifies the 55 couples: 37 disagree on a factor level (12 on A, 3 on B, 8 on D, 14 on E);
   14 contain an unavailable combination (A1E0 six times, A0D1, A0C2, A2B2 twice each, B0C2, B1D2 once each); 4 are
   admissible as four fixed levels but have no completion: A2En with C2D2 leaves no geometry (B0 blocked by C2, B1 by
   D2, B2 by A2), B2D1 with D1E0 leaves no powder (A0 blocked by D1, A1 by E0, A2 by B2), C2D2 with D2E0 leaves no
   powder (A0 blocked by C2, A1 by E0, A2 then leaves no geometry). Hence at least 11 specimens. Nine different
   eleven-pair certificates exist; each needs completion-blocked couples.
4. Upper bound 11: the programme A0B0C1D2E1, A0B1C0D0E2, A0B2C1D0E0, A1B0C0D1E1, A1B1C2D0E1, A1B2C0D1E2, A1B2C2D2E2,
   A2B0C0D2E0, A2B0C1D0E2, A2B1C1D1E1, A2B1C2D1E0 is admissible and covers all 82 admissible pairs (checked pair by
   pair).
5. Integer programme (scipy HiGHS, one binary variable per admissible specimen, one covering constraint per admissible
   pair): minimum 11; enumeration with no-good cuts finds exactly one optimal programme, the one in 4.
6. Wrong routes, computed: the trivial bound 9; 10 (what a solver reports who finds ten pairwise incompatible pairs and
   believes a 10-specimen programme exists); randomised greedy constructions (add the admissible specimen covering
   most uncovered pairs, ties broken at random, 200 runs) reach 11 once, 12 three times, 13 in 28 runs, 14 in 78,
   15 in 69, 16 in 17, 17 in 4; 12 is what a solver reports who proves 11 and settles for the best construction found.

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
    lines = ["# task08: smallest pairwise-covering fatigue test programme with unavailable level combinations (version 4: eight unavailable, gap two, unique optimum)", "",
             "Engineering (materials testing, design of experiments), subdomain: " + task["task"]["subdomain"] + ". Earlier contents of this folder (fractional chromatic number v1 and v2; three crack-growth versions; the earlier test-matrix versions: five unavailable with key 11, seven unavailable with unique key 10, six factors with key 11) are archived in work/v1, work/v2-math, work/eng-v1, work/eng-v2, work/eng-v3, work/tm-v1, work/tm-v2, work/tm-v3.", "",
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
