import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "fatigue-test-matrix-minimum-specimens"
question = r"""A fatigue test programme on metal injection moulded Ti-6Al-7Nb varies the five factors listed in the figure, each at three levels: the powder, the specimen geometry, the space-holder content, the oxygen content and the load ratio. Every specimen is made and tested at one level of each factor. The five level combinations listed in the lower table of the figure cannot be produced or tested; a specimen containing any of them is not available.

The programme must cover every admissible pair of levels of two different factors, which is to say that for any two factors and any level of the first with any level of the second, unless that combination is one of the five unavailable ones, at least one specimen must carry both levels. No other requirement is imposed.

Find the smallest number of specimens with which this can be done. Give a single integer."""
final_answer = "11"
variants = ["$11$", "11 specimens", "eleven"]
solution = r"""Step 1: Set up the counting objects.
Write the factors as $A$ (powder), $B$ (specimen geometry), $C$ (space-holder content), $D$ (oxygen content), $E$ (load ratio), with levels $0, 1, 2$ in the order of the figure, so that the unavailable combinations are $A_0C_1$, $A_0C_2$ (TiH$_2$-derived powder with $15$ and $30$ vol% space holder), $A_1D_0$ (HDH powder with $0.15$ wt% oxygen), $A_2B_1$ (gas-atomised powder with the flat geometry) and $B_0D_1$ (round bar with $0.30$ wt% oxygen). A specimen is a choice of one level per factor containing none of these five; there are $243 - 129 = 114$ admissible specimens. The pairs to be covered are the $90 - 5 = 85$ admissible level pairs. Each specimen carries exactly one level pair for each of the ten factor pairs.

Step 2: The bound that comes first, and why it is not the answer.
Two factors with $9$ admissible level pairs between them ($A$ and $E$, for instance, or $C$ and $D$) force at least $9$ specimens, since one specimen covers one level pair of a given factor pair. No specimen covers two different level pairs of the same two factors, so this bound cannot be improved by looking at one factor pair at a time. The unavailable combinations, however, also make pairs from different factor pairs incompatible, and that is what pushes the minimum up.

Step 3: Lower bound $11$ from eleven pairwise incompatible level pairs.
Call two admissible level pairs incompatible if no admissible specimen contains both. Two pairs are incompatible when they need the same factor at different levels, when their union contains an unavailable combination, or when every completion of their union to a full specimen contains one. Consider the eleven level pairs
$$A_0B_0,\ A_0B_2,\ A_1B_0,\ A_1B_2,\ A_2D_1,\ A_2D_2,\ B_1E_0,\ B_1E_1,\ B_1E_2,\ C_1D_0,\ C_2D_0 .$$
They are pairwise incompatible. The four pairs $A_iB_j$ with $i \in \{0,1\}$, $j \in \{0,2\}$ and the two pairs $A_2D_m$ disagree on $A$ with one another whenever their $A$ levels differ, and $A_2D_1$, $A_2D_2$ disagree on $D$; the three pairs $B_1E_n$ disagree on $E$ with one another and on $B$ with the four $A_iB_j$; $C_1D_0$ and $C_2D_0$ disagree on $C$ with each other and on $D$ with $A_2D_1$, $A_2D_2$. The remaining couples contain an unavailable combination or force one: $A_0B_j$ with $C_1D_0$ or $C_2D_0$ contains $A_0C_1$ or $A_0C_2$; $A_1B_j$ with $C_1D_0$ or $C_2D_0$ contains $A_1D_0$; $A_2D_m$ with $B_1E_n$ contains $A_2B_1$; and $B_1E_n$ with $C_1D_0$ or $C_2D_0$ fixes $B_1$, $C_1$ or $C_2$, $D_0$ and $E_n$, after which no level of $A$ is admissible, because $A_0$ is unavailable with $C_1$ and $C_2$, $A_1$ with $D_0$, and $A_2$ with $B_1$. Since each of the eleven pairs must be covered and no specimen covers two of them, every programme that covers all admissible pairs has at least $11$ specimens.

Step 4: Upper bound $11$ from an explicit programme.
The eleven specimens
$A_0B_0C_0D_2E_1$, $A_0B_1C_0D_0E_2$, $A_0B_2C_0D_1E_0$, $A_1B_0C_1D_2E_2$, $A_1B_1C_1D_1E_1$, $A_1B_1C_2D_2E_0$, $A_1B_2C_0D_2E_1$, $A_2B_0C_0D_2E_0$, $A_2B_0C_2D_0E_1$, $A_2B_2C_1D_0E_0$, $A_2B_2C_2D_1E_2$
are all admissible (none contains $A_0C_1$, $A_0C_2$, $A_1D_0$, $A_2B_1$ or $B_0D_1$). Listing the level pairs they carry, factor pair by factor pair, gives all $8$ admissible $AB$ pairs, all $7$ $AC$ pairs, all $8$ $AD$ pairs, all $9$ $AE$ pairs, all $9$ $BC$ pairs, all $8$ $BD$ pairs, all $9$ $BE$ pairs, all $9$ $CD$ pairs, all $9$ $CE$ pairs and all $9$ $DE$ pairs: for instance the $AB$ pairs are $A_0B_0$, $A_0B_1$, $A_0B_2$, $A_1B_0$, $A_1B_1$ (twice), $A_1B_2$, $A_2B_0$ (twice), $A_2B_2$ (twice), and the $CD$ pairs are $C_0D_2$ (three times), $C_0D_0$, $C_0D_1$, $C_1D_2$, $C_1D_1$, $C_2D_2$, $C_2D_0$, $C_1D_0$, $C_2D_1$. All $85$ admissible pairs are covered, so $11$ specimens suffice.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $11$. The bound $9$ of Step 2 is not attainable, and neither is $10$. Constructions that extend a $3 \times 3$ array for two of the factors, or that add specimens one at a time covering as many new pairs as possible, end at $12$ or more; there are only $24$ programmes with $11$ specimens, which are $4$ programmes up to renaming the three load ratios, which no unavailable combination distinguishes.

Answer: $11$."""
rubric = [
    dict(id="c1", description=r"Gives $11$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit programme of $11$ admissible specimens covering every admissible level pair (equivalently, a correct $11$-row test matrix).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that $10$ specimens are not enough by a valid argument, for instance a set of $11$ admissible level pairs no two of which fit into one admissible specimen (such as $A_0B_0$, $A_0B_2$, $A_1B_0$, $A_1B_2$, $A_2D_1$, $A_2D_2$, $B_1E_0$, $B_1E_1$, $B_1E_2$, $C_1D_0$, $C_2D_0$), or an exhaustive search whose state space is described.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the bound of $9$ specimens from a factor pair with $9$ admissible level pairs and recognises that the unavailable combinations make it unattainable.", points=1, isFinalAnswer=False),
]
wrong = ["9", "10", "12", "13"]
references = r"""Pairwise covering test suites (covering arrays of strength two) with constraints between factor levels, and the practice of building them greedily: D. M. Cohen, S. R. Dalal, M. L. Fredman and G. C. Patton, The AETG system: an approach to testing based on combinatorial design, IEEE Transactions on Software Engineering 23 (1997), 437-444. Covering arrays in general, their lower bounds and the hardness of finding minimum ones: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 114 admissible specimens and the 85 admissible pairs, checks the set of 11 pairwise incompatible pairs against every admissible specimen with the reason for each incompatible couple, checks the 11-specimen programme pair by pair, confirms the minimum by an integer programme and enumerates all 24 optimal programmes; the program is embedded with its output."""
necessity = "The factors, their levels and above all the five unavailable level combinations are given only in the figure; the minimum number of specimens depends on exactly which combinations are unavailable (without them the answer would be 9, and other sets of five give 10 or 12)."
verify_field = "Section 3 of verification_notes.txt gives the lower-bound certificate: eleven admissible level pairs (A0B0, A0B2, A1B0, A1B2, A2D1, A2D2, B1E0, B1E1, B1E2, C1D0, C2D0 in the notation of the solution), checked against all 114 admissible specimens so that no specimen contains two of them, with the reason for every one of the 55 couples. Section 4 gives the 11-specimen programme and checks that it covers all 85 admissible pairs. Section 5 confirms the minimum 11 by an integer programme (scipy HiGHS) and lists all 24 optimal programmes (4 up to renaming the load ratios). Section 6 shows that randomised greedy constructions reach only 12 to 16 specimens. Section 7 embeds the program verify_key.py with its output."
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
    txt = f"""VERIFICATION NOTES: smallest pairwise-covering fatigue test programme with five unavailable level combinations

Answer key: 11.

1. The instance (from the figure). Factors A powder (0 TiH2-derived, 1 HDH, 2 gas-atomised), B specimen geometry (0 round
   bar, 1 flat, 2 notched), C space-holder content (0, 1, 2 for 0, 15, 30 vol%), D oxygen (0, 1, 2 for 0.15, 0.30,
   0.45 wt%), E load ratio (0, 1, 2 for -1, 0.1, 0.5). Unavailable combinations A0C1, A0C2, A1D0, A2B1, B0D1. A specimen is
   admissible if it contains none of them: 114 of the 243 level combinations. Admissible level pairs: 85 of 90; every
   admissible pair occurs in some admissible specimen, so the covering requirement can be met.
2. Trivial bound: the factor pairs AE, BC, BE, CD, CE, DE each have 9 admissible level pairs and one specimen covers one
   level pair of a factor pair, so at least 9 specimens. (AB and AD and BD have 8, AC has 7.)
3. Lower bound 11 (certificate, hand-checkable): the eleven pairs A0B0, A0B2, A1B0, A1B2, A2D1, A2D2, B1E0, B1E1, B1E2,
   C1D0, C2D0 are pairwise incompatible (no admissible specimen contains two of them). The program checks this against
   all 114 specimens and classifies the 55 couples: 35 disagree on a factor level (14 on B, 12 on A, 5 on D, 3 on E, 1 on
   C); 14 contain an unavailable combination (A0C1, A0C2, A1D0 or A2B1); 6 (B1En with C1D0 or C2D0) leave no admissible
   level of A, since A0 is unavailable with C1 and C2, A1 with D0, and A2 with B1. Hence at least 11 specimens.
4. Upper bound 11: the programme A0B0C0D2E1, A0B1C0D0E2, A0B2C0D1E0, A1B0C1D2E2, A1B1C1D1E1, A1B1C2D2E0, A1B2C0D2E1,
   A2B0C0D2E0, A2B0C2D0E1, A2B2C1D0E0, A2B2C2D1E2 is admissible and covers all 85 admissible pairs (checked pair by
   pair by the program).
5. Integer programme (scipy HiGHS, one binary variable per admissible specimen, one covering constraint per admissible
   pair): minimum 11; with no-good cuts all optimal programmes are enumerated: 24, which are 4 up to the renaming of
   the three load ratios (factor E appears in no unavailable combination). So there is no programme with 10 specimens,
   independently of the certificate in 3.
6. Wrong routes, computed: the trivial bound 9; 10 (the bound plus one, without proof); randomised greedy constructions
   (add the admissible specimen covering most uncovered pairs, ties broken at random, 200 runs) reach 12 in 9 runs,
   13 in 41, 14 in 91, 15 in 46, 16 in 13, never 11.

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
    lines = ["# task08: smallest pairwise-covering fatigue test programme with unavailable level combinations", "",
             "Engineering (materials testing, design of experiments), subdomain: " + task["task"]["subdomain"] + ". Earlier contents of this folder (fractional chromatic number v1 and v2; three crack-growth versions) are archived in work/v1, work/v2-math, work/eng-v1, work/eng-v2, work/eng-v3.", "",
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
