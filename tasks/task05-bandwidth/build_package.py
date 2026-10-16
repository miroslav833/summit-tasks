import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-twelve-vertices"
question = r"""The figure shows a graph $G$ with $12$ vertices, labelled $1$ to $12$, and $20$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 12\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer."""
final_answer = "4"
variants = [r"$4$", "bandwidth 4"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $13$, $14$, $16$, $1\,11$, $26$, $28$, $2\,10$, $34$, $35$, $49$, $4\,10$, $4\,11$, $69$, $58$, $8\,12$, $79$, $9\,12$, $7\,11$ and $10\,11$. The degrees are $5$ (vertices $1$ and $4$), $4$ (vertices $2$, $9$ and $11$), $3$ (vertices $3$, $6$, $8$ and $10$) and $2$ (vertices $5$, $7$ and $12$). The diameter of $G$ is $4$.

Step 2: The easy bounds give only $3$.
In any numbering the two neighbours of a vertex of degree $5$ that are furthest apart differ by at least $5$, so some edge at that vertex is stretched by at least $\lceil 5/2 \rceil = 3$. The diameter bound gives $\lceil (12-1)/4 \rceil = 3$ as well. Both are one short.

Step 3: An induced subgraph of diameter $2$ gives $4$.
If $H$ is a connected subgraph of $G$ with $k$ vertices and diameter $d$, then in any numbering of $G$ the lowest and highest numbered vertices of $H$ differ by at least $k-1$ and are joined inside $H$ by a path of at most $d$ edges, so some edge of that path is stretched by at least $\lceil (k-1)/d \rceil$. Take $H$ to be the subgraph induced on $\{1, 2, 3, 4, 6, 9, 10, 11\}$. Its edges are $12$, $13$, $14$, $16$, $1\,11$, $26$, $2\,10$, $34$, $49$, $4\,10$, $4\,11$, $69$ and $10\,11$. Every two of its eight vertices are adjacent or have a common neighbour inside $H$ (vertex $1$ or vertex $4$ serves for every pair except $\{2, 9\}$, which goes through $6$, and $\{6, 10\}$, which goes through $2$), so $H$ has diameter $2$, and the bound is $\lceil 7/2 \rceil = 4$.

Step 4: A numbering of width $4$.
Give the vertices the positions $5 \mapsto 1$, $8 \mapsto 2$, $12 \mapsto 3$, $6 \mapsto 4$, $3 \mapsto 5$, $2 \mapsto 6$, $9 \mapsto 7$, $1 \mapsto 8$, $4 \mapsto 9$, $10 \mapsto 10$, $7 \mapsto 11$, $11 \mapsto 12$. The stretches of the twenty edges are then $12{:}\,2$, $13{:}\,3$, $14{:}\,1$, $16{:}\,4$, $1\,11{:}\,4$, $26{:}\,2$, $28{:}\,4$, $2\,10{:}\,4$, $34{:}\,4$, $35{:}\,4$, $49{:}\,2$, $4\,10{:}\,1$, $4\,11{:}\,3$, $69{:}\,3$, $58{:}\,1$, $8\,12{:}\,1$, $79{:}\,4$, $9\,12{:}\,4$, $7\,11{:}\,1$, $10\,11{:}\,2$. The largest is $4$.

Step 5: Conclusion.
The bandwidth is at least $4$ by Step 3 and at most $4$ by Step 4, so it equals $4$. (The breadth-first numberings that one writes down first, starting from any vertex, all have width $5$ or more; the numbering of Step 4 interleaves the two dense ends of the graph, placing $1$ and $4$ in the middle with their neighbours spread on both sides.)

Answer: $4$."""
rubric = [
    dict(id="c1", description=r"Gives $4$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit numbering of the twelve vertices of width $4$ (every edge stretched by at most $4$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves the lower bound $4$ by a valid argument, for instance the density bound $\lceil (k-1)/d \rceil$ applied to a connected subgraph with $k = 8$ vertices and diameter $d = 2$ such as the one induced on $\{1, 2, 3, 4, 6, 9, 10, 11\}$, or an exhaustive argument that no numbering of width $3$ exists.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the degree bound $\lceil \Delta/2 \rceil = 3$ or the diameter bound $\lceil 11/4 \rceil = 3$ and recognises that it is not tight.", points=1, isFinalAnswer=False),
]
wrong = ["3", "5", "6"]
references = r"""The density lower bound for the bandwidth (a connected subgraph with $k$ vertices and diameter $d$ forces width at least $\lceil (k-1)/d \rceil$) and the general theory of the bandwidth problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains two independent exact computations of the bandwidth (backtracking over numberings, and a dynamic programme over sets of placed vertices), the diameter computation for the certificate subgraph, the explicit numbering of width $4$ with the stretch of every edge, and the widths of all Cuthill-McKee numberings; the program is embedded with its output."""
necessity = "The graph is given only by the figure; the twenty edges are not listed in the text, and the answer depends on the exact edge set (one edge more or less changes both the certificate subgraph and the optimal numbering)."
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

Answer key: 4.

1. Edges (from the figure): 12, 13, 14, 16, 1-11, 26, 28, 2-10, 34, 35, 49, 4-10, 4-11, 69, 58, 8-12, 79, 9-12, 7-11, 10-11.
2. Lower bound: the induced subgraph on {{1,2,3,4,6,9,10,11}} has 8 vertices and diameter 2, so every
   numbering has width at least ceil(7/2) = 4 (density bound).
3. Upper bound: positions 5->1, 8->2, 12->3, 6->4, 3->5, 2->6, 9->7, 1->8, 4->9, 10->10, 7->11, 11->12
   give width 4 (every edge stretch is listed in the program output).
4. Two independent exact computations (backtracking with pruning; dynamic programme over sets of
   placed vertices) both report: no numbering of width 3, a numbering of width 4.
5. The trivial bounds give 3; all Cuthill-McKee numberings (every start vertex, both directions)
   have width 5 to 7.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["# task05: bandwidth of a 12-vertex graph", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Sections 2 to 4 of verification_notes.txt give the certificate subgraph, the explicit width-4 numbering with every edge stretch, and two independent exact computations; section 6 embeds the program with its output.", "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
