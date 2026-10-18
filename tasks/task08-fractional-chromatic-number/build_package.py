import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "hamiltonian-cycles-cubic-graph-28-vertices"
question = r"""Figure shows simple undirected graph on $28$ vertices, which are labelled $A$ to $Z$, $a$ and $b$, and its edges are straight segments drawn between circles. Where two segments cross, crossing point is not vertex, and those two edges do not meet there.

"Hamiltonian cycle" is cycle which passes through each vertex exactly once, and two Hamiltonian cycles are counted as same cycle when they use same set of edges, so starting vertex and direction of travel do not matter.

How many Hamiltonian cycles does this graph have? Give your answer as single integer."""
final_answer = "52"
variants = ["$52$", "52 cycles", "fifty-two"]
solution = r"""Graph in figure has $42$ edges, which are $AG, AJ, AS, BK, BS, BV, CH, CL, CY, DI, DN, DW, EL, EP, EZ, FS, FX, FZ, GT, Gb, HJ, Ha, IM, Ib, JV, KQ, KU, LR, MO, MX, NT, NV, OQ, OZ, PU, PX, QY, RT, Ra, Ub, WY, Wa$, and each vertex has degree $3$, so graph is cubic, as $28 \cdot 3 / 2 = 42$. There are no triangles and no $4$-cycles in it, its girth being $5$, and it is not planar and has no symmetry except identity, so count cannot be shortened by faces or by symmetry and it has to be done as search.

Hamiltonian cycle uses two of three edges at each vertex, so edges which it leaves out form perfect matching, and perfect matching gives Hamiltonian cycle exactly when other $28$ edges close into one cycle and not into several. Search by hand runs on two rules, that when edge is left out the other two edges at both its ends are used, and that when two edges at vertex are used its third edge is left out, and branch is dropped when some vertex keeps fewer than two usable edges or when used edges close cycle shorter than $28$.

I split on edge which is left out at $D$, whose neighbours are $I$, $N$ and $W$, and then inside each case on edge left out at next vertex. When $DI$ is left out, so that $DN$ and $DW$ are used, split at $N$ gives $14$ cycles with $NT$ left out and $8$ with $NV$ left out, $22$ in all. When $DN$ is left out, split at $I$ gives $7$ with $IM$ left out and $7$ with $Ib$ left out, $14$ in all, and when $DW$ is left out, split at $I$ gives $9$ with $IM$ left out and $7$ with $Ib$ left out, $16$ in all. So graph has $22 + 14 + 16 = 52$ Hamiltonian cycles, and one of them, written from $A$, is $A\,G\,T\,N\,D\,I\,b\,U\,K\,B\,V\,J\,H\,C\,L\,R\,a\,W\,Y\,Q\,O\,M\,X\,P\,E\,Z\,F\,S$ and back to $A$, while verification notes list all $52$ of them.

As check, in cubic graph each edge lies on even number of Hamiltonian cycles (Smith's theorem, Thomason 1978), and here cycles through edges at $D$ number $52 - 22 = 30$ for $DI$, $52 - 14 = 38$ for $DN$ and $52 - 16 = 36$ for $DW$, which are all even and add up to $104 = 2 \cdot 52$, because each cycle uses two of three edges at $D$. Count was also done by two separate programs, depth-first search for cycles through $A$ and enumeration of all $98$ perfect matchings, and both of them give $52$.

So answer is $52$."""
rubric = [
    dict(id="c1", description=r"Final answer is $52$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Response reads graph correctly, with $28$ vertices and $42$ edges and each vertex of degree $3$, and gives edge list or adjacency list which agrees with figure.", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Response organises count by edge which is left out at one vertex, or in same way by perfect matchings whose complement is one cycle, and its case totals add up to $52$, as for example $22$, $14$ and $16$ when $DI$, $DN$ and $DW$ are left out at $D$.", points=3, isFinalAnswer=False),
    dict(id="c4", description=r"Response counts each cycle once, and not once for each direction or each starting vertex.", points=1, isFinalAnswer=False),
]
wrong = ["50", "48", "104", "51"]
references = r"""Counting Hamiltonian cycles is #P-complete in general, so no formula is expected here and count is finite search, see L. G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8 (1979), 410-421. Parity check in solution, that each edge of cubic graph lies on even number of Hamiltonian cycles, is Smith's theorem, see A. G. Thomason, Hamiltonian cycles and uniquely edge colourable graphs, Annals of Discrete Mathematics 3 (1978), 259-268. Uploaded file verification_notes.txt gives adjacency list and counts cycles twice, by depth-first search and by perfect matchings, and both give 52, then it gives case split of solution, checks parity at every edge and lists all 52 cycles, while program and its full output come at end."""
necessity = "Graph is given in figure only, since text names no vertex and no edge, and answer is property of that one edge set, so it cannot be found without reading all 42 edges from drawing."
verify_field = "Section 2 of verification_notes.txt counts Hamiltonian cycles by depth-first search from A and finds 52 distinct edge sets, and section 3 counts them second way, as perfect matchings whose complement is one 28-cycle, where 52 of 98 perfect matchings are good. Section 4 gives case split of solution, 22, 14 and 16 when DI, DN and DW are left out, section 5 checks that each edge lies on even number of cycles and section 6 lists all 52 cycles, while program verify_key.py is embedded with its output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: enumeration of Hamiltonian cycles in a cubic graph",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original drawing of a 28-vertex cubic graph)",
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
    txt = f"""VERIFICATION NOTES: number of Hamiltonian cycles of the drawn 28-vertex cubic graph

Answer key: 52.

1. Graph is read from figure and has 28 vertices, A to Z, a and b, and 42 edges, each vertex having degree 3. Its girth
   is 5, its automorphism group is trivial, which was checked separately with networkx, and it is drawn with 14 edge
   crossings, none of them at vertex.
2. First route is depth-first search for Hamiltonian cycles through A, stored as edge sets, and it finds 52.
3. Second route uses that edges left out by Hamiltonian cycle in cubic graph form perfect matching. Graph has 98
   perfect matchings, and for exactly 52 of them other 28 edges form one cycle.
4. Case split of solution is on edge left out at D, so DI gives 22 (14 with NT left out, 8 with NV left out), DN gives
   14 (7 with IM left out, 7 with Ib left out) and DW gives 16 (9 with IM left out, 7 with Ib left out), 52 in all.
5. Each edge lies on even number of Hamiltonian cycles (Smith's theorem), and counts per edge are printed and add up to
   28 x 52 = 1456.
6. All 52 cycles are listed, each written from A.

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only; under a second)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

8. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

{textwrap.indent((HERE / "draw_figure.py").read_text(), "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: number of Hamiltonian cycles of a drawn 28-vertex cubic graph", "",
             "Mathematics, subdomain: " + task["task"]["subdomain"] + ". Earlier contents of this folder (fractional chromatic number, crack growth, test matrices, covering arrays, M/G/1 queue) are archived under work/.", "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", verify_field, "", "## Image necessity", "", necessity, "", "## Screen", "", screen]
    (HERE / "README.md").write_text("\n".join(lines) + "\n"); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    screen = (HERE / "work" / "ham" / "screen.md").read_text()
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(screen); build_zip()
