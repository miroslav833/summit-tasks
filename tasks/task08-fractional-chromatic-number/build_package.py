import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "covering-array-forbidden-pairs-six-columns"
question = r"""An array has $N$ rows and $6$ columns. The entries $x_1, \dots, x_5$ of a row are symbols from $\{0, 1, 2\}$ and the entry $x_6$ is a symbol from $\{0, 1\}$. The figure marks ten forbidden pairs: a cell marked F in the row labelled $x_i = a$ and the column labelled $x_j = b$ means that no row of the array may have $x_i = a$ and $x_j = b$ at the same time. Every row of the array must avoid all ten forbidden pairs.

The array is called covering if, for every two distinct columns $i$ and $j$ and every pair of symbols $(a, b)$ allowed in those columns that is not forbidden, some row of the array has $x_i = a$ and $x_j = b$. Nothing else is required.

Find the smallest $N$ for which a covering array exists. Give a single integer."""
final_answer = "10"
variants = ["$10$", "10 rows", "ten", "N = 10"]
solution = r"""Step 1: Set up the counting objects.
Write $A, \dots, F$ for the columns $x_1, \dots, x_6$ and $A_a$ for the entry $x_1 = a$. The forbidden pairs read from the figure are $A_1B_1$, $A_1C_2$, $A_1E_1$, $A_2C_0$, $A_2D_0$, $C_0E_0$, $C_1F_0$, $C_2E_1$, $D_0E_1$ and $D_2F_0$. An admissible row avoids all of them; there are $136$ admissible rows out of $3^5 \cdot 2 = 486$. The pairs to be covered are the $120 - 10 = 110$ admissible symbol pairs, and each row carries exactly one symbol pair for each of the fifteen column pairs.

Step 2: The bounds that come first.
The column pairs $BC$, $BD$, $BE$ and $CD$ keep all $9$ of their symbol pairs, so $N \ge 9$. Without forbidden pairs the smallest covering array with five ternary and one binary column has $11$ rows; the forbidden pairs remove requirements as well as rows, and the answer is smaller.

Step 3: Lower bound $10$.
Call two admissible symbol pairs incompatible if no admissible row contains both. The ten pairs
$$B_0E_1,\ B_1E_1,\ B_2E_1,\ C_0D_0,\ C_1D_0,\ C_2D_0,\ D_1E_0,\ D_1E_2,\ D_2E_0,\ D_2E_2$$
are pairwise incompatible. Pairs that need one column with two different symbols account for most couples: the three $B_jE_1$ differ in $B$, the three $C_iD_0$ differ in $C$, the four $D_mE_n$ differ in $D$ or $E$ among themselves, every $B_jE_1$ differs in $E$ from every $D_mE_n$ (where $n \in \{0, 2\}$), and every $C_iD_0$ differs in $D$ from every $D_mE_n$ (where $m \in \{1, 2\}$). The remaining nine couples, $B_jE_1$ with $C_iD_0$, put $x_4 = 0$ and $x_5 = 1$ into one row, which is the forbidden pair $D_0E_1$. In words: the symbol $1$ in column $E$ must meet all three symbols of column $B$, the symbol $0$ in column $D$ must meet all three symbols of column $C$ on rows that cannot have $x_5 = 1$, and the four pairs $(x_4, x_5) \in \{1, 2\} \times \{0, 2\}$ need four more rows. Hence $N \ge 3 + 3 + 4 = 10$.

Step 4: Upper bound $10$, the decisive step.
The ten rows (written $x_1 x_2 x_3 x_4 x_5 x_6$)
$$001211,\ 010110,\ 011021,\ 022000,\ 100020,\ 101101,\ 120221,\ 202120,\ 212201,\ 221111$$
contain no forbidden pair. Column pair by column pair they carry every admissible symbol pair: $AB$ all $8$ (everything except $A_1B_1$), $AC$ all $7$, $AD$ all $8$, $AE$ all $8$, $AF$ all $6$; $BC$, $BD$, $BE$ all $9$ each; $BF$ all $6$; $CD$ all $9$; $CE$ all $7$ (missing only $C_0E_0$ and $C_2E_1$); $CF$ all $5$ (missing only $C_1F_0$); $DE$ all $8$ (missing only $D_0E_1$); $DF$ all $5$ (missing only $D_2F_0$); $EF$ all $6$. For instance $CD$ is read off as $C_1D_2$, $C_0D_1$, $C_1D_0$, $C_2D_0$, $C_0D_0$, $C_1D_1$, $C_0D_2$, $C_2D_1$, $C_2D_2$, $C_1D_1$, and $DE$ as $D_2E_1$, $D_1E_0$, $D_0E_2$, $D_0E_0$, $D_0E_2$, $D_1E_1$, $D_2E_2$, $D_1E_2$, $D_2E_0$, $D_1E_1$. All $110$ admissible pairs are covered, so $N = 10$ is attained. A $10$-row array must use each of the ten pairs of Step 3 on its own row, which leaves very little freedom: exactly two covering arrays with $10$ rows exist (the verification notes enumerate them), so the construction cannot be found by local improvements of a greedy array.

Step 5: Conclusion.
Steps 3 and 4 give the minimum $N = 10$. The bound $9$ is not attainable, and the unconstrained value $11$ is one too many; constructions that add rows greedily end at $11$ to $16$.

Answer: $10$."""
rubric = [
    dict(id="c1", description=r"Gives $10$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit covering array of $10$ admissible rows (every admissible symbol pair present, no forbidden pair in any row).", points=3, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that $9$ rows are not enough by a valid argument, for instance ten admissible symbol pairs no two of which fit into one admissible row (such as $(x_2,x_5) = (0,1), (1,1), (2,1)$, $(x_3,x_4) = (0,0), (1,0), (2,0)$ and $(x_4,x_5) = (1,0), (1,2), (2,0), (2,2)$), or an equivalent counting argument.", points=1, isFinalAnswer=False),
    dict(id="c4", description=r"States the bound of $9$ rows from a column pair with $9$ admissible symbol pairs and recognises that it is not attained.", points=1, isFinalAnswer=False),
]
wrong = ["9", "11", "12", "13"]
references = r"""Covering arrays avoiding forbidden edges, which is exactly the object of the question, and the hardness of their minimum size: P. Danziger, E. Mendelsohn, L. Moura and B. Stevens, Covering arrays avoiding forbidden edges, Theoretical Computer Science 410 (2009), 5403-5414. Covering arrays in general and their known small values: C. J. Colbourn, Combinatorial aspects of covering arrays, Le Matematiche 59 (2004), 125-172. The uploaded file verification_notes.txt lists the 136 admissible rows and 110 admissible pairs, checks the set of ten pairwise incompatible pairs against every admissible row with the reason for each couple, checks the 10-row array column pair by column pair, confirms the minimum by an integer programme and enumerates the two optimal arrays; the program is embedded with its output."""
necessity = "The ten forbidden pairs are given only in the figure; the minimum number of rows depends on exactly which pairs are forbidden (with none forbidden the answer would be 11, and other sets of ten give 10, 11 or 12)."
verify_field = "Section 3 of verification_notes.txt gives the lower-bound certificate: ten admissible symbol pairs (B0E1, B1E1, B2E1, C0D0, C1D0, C2D0, D1E0, D1E2, D2E0, D2E2, where A to F stand for the columns x1 to x6), checked against all 136 admissible rows so that no row contains two of them, with the reason for every one of the 45 couples. Section 4 gives the 10-row array and checks every column pair. Section 5 confirms the minimum 10 by an integer programme (scipy HiGHS) and enumerates the two optimal arrays. Section 7 embeds the program verify_key.py with its output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Combinatorial design theory: covering arrays avoiding forbidden pairs",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original chart of the forbidden symbol pairs)",
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
    txt = f"""VERIFICATION NOTES: smallest covering array with six columns (five ternary, one binary) avoiding ten forbidden pairs

Answer key: 10.

1. The instance (from the figure). Columns x1 to x6, written A to F; x1..x5 over 0, 1, 2 and x6 over 0, 1. Forbidden pairs
   A1B1, A1C2, A1E1, A2C0, A2D0, C0E0, C1F0, C2E1, D0E1, D2F0. Admissible rows: 136 of 486. Admissible symbol pairs: 110 of
   120, each realised by some admissible row.
2. Trivial bound: BC, BD, BE, CD keep 9 symbol pairs each, so at least 9 rows. Without forbidden pairs the minimum would be
   11 (the covering array number for five ternary columns and one binary column).
3. Lower bound 10: the pairs B0E1, B1E1, B2E1, C0D0, C1D0, C2D0, D1E0, D1E2, D2E0, D2E2 are pairwise incompatible; 36 couples
   need one column with two different symbols, 9 couples (BjE1 with CiD0) contain the forbidden pair D0E1. Checked against
   all 136 admissible rows by the program; 42 different ten-pair certificates exist.
4. Upper bound 10: 001211, 010110, 011021, 022000, 100020, 101101, 120221, 202120, 212201, 221111 (rows written x1..x6),
   checked column pair by column pair.
5. Integer programme (scipy HiGHS): minimum 10; enumeration with no-good cuts gives exactly two optimal arrays.
6. Wrong routes: 9 (trivial bound), 11 (unconstrained value, or the best construction found), greedy constructions 11 to 16.

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only, scipy optional
   for section 5; running time about a minute)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

8. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

{textwrap.indent((HERE / "draw_figure.py").read_text(), "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: smallest covering array with six columns avoiding ten forbidden pairs", "",
             "Mathematics, subdomain: " + task["task"]["subdomain"] + ". The five-column version (key 10, solved by Opus 3/3 locally) is archived in work/ca-v1. Earlier contents of this folder (fractional chromatic number; three crack-growth versions; four test-matrix versions) are archived under work/.", "",
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
