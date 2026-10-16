import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-fourteen-vertices"
question = r"""The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $27$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 14\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer."""
final_answer = "5"
variants = [r"$5$", "bandwidth 5"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $14$, $16$, $18$, $1\,11$, $1\,14$, $28$, $37$, $38$, $3\,10$, $3\,12$, $3\,13$, $4\,10$, $4\,11$, $4\,13$, $4\,14$, $59$, $5\,12$, $69$, $6\,11$, $78$, $7\,11$, $9\,13$, $9\,14$, $11\,13$, $11\,14$, $12\,14$. The degrees are $6$ (vertices $1$ and $11$), $5$ (vertices $3$, $4$ and $14$), $4$ (vertices $8$, $9$ and $13$), $3$ (vertices $6$, $7$ and $12$) and $2$ (vertices $2$, $5$ and $10$). The diameter of $G$ is $4$.

Step 2: The easy bounds give $3$ and $4$.
A vertex of degree $6$ forces some incident edge to be stretched by at least $\lceil 6/2 \rceil = 3$, and the diameter bound gives $\lceil (14-1)/4 \rceil = 4$. Both are short of the answer.

Step 3: An induced subgraph of diameter $2$ gives $5$.
If $H$ is a connected subgraph with $k$ vertices and diameter $d$, then in any numbering the lowest and highest numbered vertices of $H$ differ by at least $k-1$ and are joined inside $H$ by a path of at most $d$ edges, so some edge of that path is stretched by at least $\lceil (k-1)/d \rceil$. Take $H$ to be the subgraph induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$. Every two of its ten vertices are adjacent or have a common neighbour inside $H$: the non-adjacent pairs and a common neighbour are $\{1,3\}{:}\,8$, $\{1,7\}{:}\,8$, $\{1,10\}{:}\,4$, $\{1,12\}{:}\,14$, $\{1,13\}{:}\,4$, $\{3,4\}{:}\,10$, $\{3,11\}{:}\,7$, $\{3,14\}{:}\,12$, $\{4,7\}{:}\,11$, $\{4,8\}{:}\,1$, $\{4,12\}{:}\,14$, $\{7,10\}{:}\,3$, $\{7,12\}{:}\,3$, $\{7,13\}{:}\,3$, $\{7,14\}{:}\,11$, $\{8,10\}{:}\,3$, $\{8,11\}{:}\,1$, $\{8,12\}{:}\,3$, $\{8,13\}{:}\,3$, $\{8,14\}{:}\,1$, $\{10,11\}{:}\,4$, $\{10,12\}{:}\,3$, $\{10,13\}{:}\,3$, $\{10,14\}{:}\,4$, $\{11,12\}{:}\,14$, $\{12,13\}{:}\,3$, $\{13,14\}{:}\,4$. So $H$ has diameter $2$ and the bound is $\lceil 9/2 \rceil = 5$.

Step 4: A numbering of width $5$.
Give the vertices the positions $2 \mapsto 1$, $7 \mapsto 2$, $8 \mapsto 3$, $1 \mapsto 4$, $11 \mapsto 5$, $4 \mapsto 6$, $3 \mapsto 7$, $6 \mapsto 8$, $14 \mapsto 9$, $13 \mapsto 10$, $10 \mapsto 11$, $12 \mapsto 12$, $9 \mapsto 13$, $5 \mapsto 14$. The stretches of the twenty-seven edges are $12{:}\,3$, $14{:}\,2$, $16{:}\,4$, $18{:}\,1$, $1\,11{:}\,1$, $1\,14{:}\,5$, $28{:}\,2$, $37{:}\,5$, $38{:}\,4$, $3\,10{:}\,4$, $3\,12{:}\,5$, $3\,13{:}\,3$, $4\,10{:}\,5$, $4\,11{:}\,1$, $4\,13{:}\,4$, $4\,14{:}\,3$, $59{:}\,1$, $5\,12{:}\,2$, $69{:}\,5$, $6\,11{:}\,3$, $78{:}\,1$, $7\,11{:}\,3$, $9\,13{:}\,3$, $9\,14{:}\,4$, $11\,13{:}\,5$, $11\,14{:}\,4$, $12\,14{:}\,3$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. (Breadth-first numberings from any start vertex have width $6$ or more; the numbering of Step 4 places the two vertices of degree $6$ at positions $4$ and $5$ and spreads their neighbours on both sides.)

Answer: $5$."""
rubric = [
    dict(id="c1", description=r"Gives $5$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit numbering of the fourteen vertices of width $5$ (every edge stretched by at most $5$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves the lower bound $5$ by a valid argument, for instance the density bound $\lceil (k-1)/d \rceil$ applied to a connected subgraph with $k = 10$ vertices and diameter $d = 2$ such as the one induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$, or an exhaustive argument that no numbering of width $4$ exists.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the degree bound $\lceil \Delta/2 \rceil = 3$ or the diameter bound $\lceil 13/4 \rceil = 4$ and recognises that it is not tight.", points=1, isFinalAnswer=False),
]
wrong = ["4", "6", "7"]
references = r"""The density lower bound for the bandwidth (a connected subgraph with $k$ vertices and diameter $d$ forces width at least $\lceil (k-1)/d \rceil$) and the general theory of the bandwidth problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains two independent exact computations of the bandwidth (backtracking over numberings, and a dynamic programme over sets of placed vertices), the diameter computation for the certificate subgraph, the explicit numbering of width $5$ with the stretch of every edge, and the widths of all Cuthill-McKee numberings; the program is embedded with its output."""
necessity = "The graph is given only by the figure; the twenty-seven edges are not listed in the text, and the answer depends on the exact edge set (one edge more or less changes both the certificate subgraph and the optimal numbering)."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: graph layout problems (bandwidth of a graph)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original drawing of the graph from a force-directed layout)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: bandwidth of the graph in the figure

Answer key: 5.

1. Edges (from the figure): 1-2, 1-4, 1-6, 1-8, 1-11, 1-14, 2-8, 3-7, 3-8, 3-10, 3-12, 3-13, 4-10, 4-11, 4-13, 4-14, 5-9, 5-12, 6-9, 6-11, 7-8, 7-11, 9-13, 9-14, 11-13, 11-14, 12-14.
2. Lower bound: the induced subgraph on {{1,3,4,7,8,10,11,12,13,14}} has 10 vertices and diameter 2
   (a common neighbour inside the subgraph is listed for every non-adjacent pair in the program
   output), so every numbering has width at least ceil(9/2) = 5 (density bound).
3. Upper bound: positions 2->1, 7->2, 8->3, 1->4, 11->5, 4->6, 3->7, 6->8, 14->9, 13->10, 10->11, 12->12, 9->13, 5->14
   give width 5 (every edge stretch is listed in the program output).
4. Two independent exact computations (backtracking with pruning; dynamic programme over sets of
   placed vertices) both report: no numbering of width 4, a numbering of width 5.
5. The trivial bounds give 3 and 4; all Cuthill-McKee numberings (every start vertex, both
   directions) have width 6 to 9.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["# task06: bandwidth of a 14-vertex graph", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Sections 2 to 4 of verification_notes.txt give the certificate subgraph (ten vertices, diameter 2, with a common neighbour listed for every non-adjacent pair), the explicit width-5 numbering with every edge stretch, and two independent exact computations showing no numbering of width 4 exists; section 6 embeds the program with its output.", "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
