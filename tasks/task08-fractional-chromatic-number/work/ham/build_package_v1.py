import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "hamiltonian-cycles-cubic-graph-28-vertices"
question = r"""The figure shows a simple undirected graph on $28$ vertices, labelled $A$ to $Z$, $a$ and $b$. The edges are the straight segments drawn between the circles. Where two segments cross, the crossing point is not a vertex and the two edges do not meet.

A Hamiltonian cycle is a cycle that passes through every vertex exactly once. Two Hamiltonian cycles count as the same if they use the same set of edges, so the starting vertex and the direction of travel do not matter.

How many Hamiltonian cycles does the graph have? Give a single integer."""
final_answer = "52"
variants = ["$52$", "52 cycles", "fifty-two"]
solution = r"""Step 1: Read the graph.
The figure has $42$ edges: $AG, AJ, AS, BK, BS, BV, CH, CL, CY, DI, DN, DW, EL, EP, EZ, FS, FX, FZ, GT, Gb, HJ, Ha, IM, Ib, JV, KQ, KU, LR, MO, MX, NT, NV, OQ, OZ, PU, PX, QY, RT, Ra, Ub, WY, Wa$. Every vertex has degree $3$, so the graph is cubic ($28 \cdot 3 / 2 = 42$). It has no triangles and no $4$-cycles (girth $5$), it is not planar and it has no symmetry other than the identity, so the count has to be done by a search.

Step 2: Reduce to one choice per vertex.
A Hamiltonian cycle uses exactly two of the three edges at every vertex, so the unused edges form a perfect matching, and a perfect matching gives a Hamiltonian cycle exactly when the remaining $28$ edges form one cycle rather than several. Two propagation rules drive a hand search: if an edge is left out, the other two edges at both of its ends are used; if two edges at a vertex are used, the third is left out. A branch dies when a vertex keeps fewer than two usable edges or when the used edges close a cycle shorter than $28$.

Step 3: The case split.
Split on the edge left out at $D$ (its neighbours are $I$, $N$, $W$), and inside each case on the edge left out at the next vertex.
- $DI$ left out ($DN$, $DW$ used): split at $N$. Leaving out $NT$ gives $14$ cycles, leaving out $NV$ gives $8$; total $22$.
- $DN$ left out ($DI$, $DW$ used): split at $I$. Leaving out $IM$ gives $7$, leaving out $Ib$ gives $7$; total $14$.
- $DW$ left out ($DI$, $DN$ used): split at $I$. Leaving out $IM$ gives $9$, leaving out $Ib$ gives $7$; total $16$.
Hence the graph has $22 + 14 + 16 = 52$ Hamiltonian cycles. For example $A\,G\,T\,N\,D\,I\,b\,U\,K\,B\,V\,J\,H\,C\,L\,R\,a\,W\,Y\,Q\,O\,M\,X\,P\,E\,Z\,F\,S$ (back to $A$) is one of them; the verification notes list all $52$.

Step 4: Checks.
(i) In a cubic graph every edge lies on an even number of Hamiltonian cycles (Smith's theorem, Thomason 1978). The counts through the edges at $D$ are $52 - 22 = 30$ for $DI$, $52 - 14 = 38$ for $DN$ and $52 - 16 = 36$ for $DW$, all even, and they add up to $104 = 2 \cdot 52$ because each cycle uses two of the three edges. (ii) The count was confirmed by two independent programs: a depth-first search for cycles through $A$, and an enumeration of all $98$ perfect matchings of which exactly $52$ leave a single $28$-cycle.

Step 5: The traps.
Counting each cycle once per direction gives $104$. The hand search is long, and losing cycles in a branch gives $48$, $50$ or $51$; losing two cycles can leave every parity even, so the parity check does not catch it.

Answer: $52$."""
rubric = [
    dict(id="c1", description=r"Gives $52$ as the final answer.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Reads the graph correctly: $28$ vertices, $42$ edges, every vertex of degree $3$ (an edge list or adjacency list matching the figure).", points=1, isFinalAnswer=False),
    dict(id="c3", description=r"Organises the count by which edge is left out at a vertex (equivalently, by perfect matchings whose complement is a single cycle) and reports case totals that add up to $52$, for instance $22$, $14$ and $16$ for the edges $DI$, $DN$, $DW$ left out at $D$.", points=3, isFinalAnswer=False),
    dict(id="c4", description=r"Counts each cycle once, not once per direction or starting vertex.", points=1, isFinalAnswer=False),
]
wrong = ["50", "48", "104", "51"]
references = r"""Counting Hamiltonian cycles is #P-complete in general, so no formula is expected and the count is a finite search: L. G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8 (1979), 410-421. The parity check used in the solution (every edge of a cubic graph lies on an even number of Hamiltonian cycles, Smith's theorem): A. G. Thomason, Hamiltonian cycles and uniquely edge colourable graphs, Annals of Discrete Mathematics 3 (1978), 259-268. The uploaded file verification_notes.txt gives the adjacency list, counts the cycles by a depth-first search and by perfect matchings (both 52), gives the case split of the solution, checks the parity of every edge and lists all 52 cycles; the program is embedded with its output."""
necessity = "The graph exists only in the figure: the question gives no vertex or edge, and the answer is a property of that particular edge set, so it cannot be found without reading all 42 edges from the drawing."
verify_field = "Section 2 of verification_notes.txt counts the Hamiltonian cycles by a depth-first search from A (52 distinct edge sets). Section 3 counts them a second way, as the perfect matchings whose complement is one 28-cycle (98 perfect matchings, 52 good). Section 4 gives the case split of the solution (DI, DN, DW left out: 22, 14, 16). Section 5 checks that every edge lies on an even number of the cycles. Section 6 lists all 52 cycles. The program verify_key.py is embedded with its output."
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

1. The graph (from the figure). 28 vertices A to Z, a, b; 42 edges; every vertex of degree 3; girth 5; trivial
   automorphism group (checked separately with networkx); drawn with 14 edge crossings, none at a vertex.
2. Route 1: depth-first search for Hamiltonian cycles through A, stored as edge sets: 52.
3. Route 2: the unused edges of a Hamiltonian cycle in a cubic graph form a perfect matching. The graph has 98 perfect
   matchings; for exactly 52 of them the other 28 edges form one cycle.
4. Case split of the solution: edge left out at D. DI: 22 (NT left out 14, NV left out 8). DN: 14 (IM left out 7,
   Ib left out 7). DW: 16 (IM left out 9, Ib left out 7). Total 52.
5. Parity: every edge lies on an even number of Hamiltonian cycles (Smith's theorem); the counts per edge are printed
   and add up to 28 x 52 = 1456.
6. All 52 cycles, each written from A.
7. Wrong routes: 104 (each cycle counted in both directions), 48, 50, 51 (cycles lost in the case split).

8. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only; under a second)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}

9. Figure script draw_figure.py (same Python; command: python3 draw_figure.py; needs matplotlib)

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
