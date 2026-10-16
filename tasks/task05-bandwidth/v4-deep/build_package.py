import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-fourteen-vertices-v4"
question = r"""The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $25$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 14\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer."""
final_answer = "5"
variants = [r"$5$", "bandwidth 5"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $17$, $1\,14$, $27$, $2\,10$, $2\,14$, $36$, $3\,11$, $3\,13$, $45$, $46$, $48$, $49$, $58$, $6\,11$, $6\,12$, $6\,13$, $7\,11$, $7\,12$, $7\,13$, $8\,10$, $9\,10$, $10\,12$, $10\,14$, $12\,14$, $13\,14$. The degrees are $5$ for the vertices $6, 7, 10, 14$, $4$ for $4, 12, 13$, $3$ for $2, 3, 8, 11$ and $2$ for $1, 5, 9$; the maximum degree is $5$ and the diameter is $4$.

Step 2: The cheap bounds all stop at $4$.
A vertex of degree $5$ forces a stretch of at least $\lceil 5/2 \rceil = 3$; the diameter bound gives $\lceil 13/4 \rceil = 4$; and the density bound, $\lceil (k-1)/d \rceil$ for a connected subgraph with $k$ vertices and diameter $d$, never exceeds $4$: the eleven vertices $2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13$ induce a subgraph of diameter $3$, which gives $\lceil 10/3 \rceil = 4$, and no connected induced subgraph does better (all of them are checked in the verification notes). The two standard end-vertex arguments are also inconclusive: six vertices ($1, 3, 5, 8, 9, 11$) have at most $9$ vertices within distance $2$ and so could sit at an end of a width-$4$ numbering, and eighteen pairs of vertices have at most four outside neighbours and so could start one. So these arguments prove only that the bandwidth is at least $4$.

Step 3: There is no numbering of width $4$.
Build a numbering position by position. A vertex may be placed at position $i$ only if all its already placed neighbours sit at positions $i-4$ or later, and after each placement every placed vertex $u$ at position $p$ must still have at least as many free positions in $(i, p+4]$ as it has unplaced neighbours. These two rules are exact: a numbering of width $4$ exists if and only if the construction reaches position $14$. Carried out for every choice at every step, the construction dies in every branch, some only at position $11$; the complete tree has $2\,471$ nodes, and the verification notes print every branch down to depth $3$ with the rule that kills it, together with the full program. An independent check with a different formulation (a dynamic programme over the set of placed vertices and the last four placed) also finds no numbering of width $4$. Hence the bandwidth is at least $5$.

Step 4: A numbering of width $5$.
Give the vertices the positions $1 \mapsto 1$, $2 \mapsto 2$, $5 \mapsto 3$, $8 \mapsto 4$, $14 \mapsto 5$, $7 \mapsto 6$, $10 \mapsto 7$, $4 \mapsto 8$, $12 \mapsto 9$, $13 \mapsto 10$, $11 \mapsto 11$, $9 \mapsto 12$, $6 \mapsto 13$, $3 \mapsto 14$. The stretches of the twenty-five edges are $17{:}\,5$, $1\,14{:}\,4$, $27{:}\,4$, $2\,10{:}\,5$, $2\,14{:}\,3$, $36{:}\,1$, $3\,11{:}\,3$, $3\,13{:}\,4$, $45{:}\,5$, $46{:}\,5$, $48{:}\,4$, $49{:}\,4$, $58{:}\,1$, $6\,11{:}\,2$, $6\,12{:}\,4$, $6\,13{:}\,3$, $7\,11{:}\,5$, $7\,12{:}\,3$, $7\,13{:}\,4$, $8\,10{:}\,3$, $9\,10{:}\,5$, $10\,12{:}\,2$, $10\,14{:}\,2$, $12\,14{:}\,4$, $13\,14{:}\,5$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. There are $23\,616$ numberings of width $5$.

Answer: $5$."""
rubric = [
    dict(id="c1", description=r"Gives $5$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit numbering of the fourteen vertices of width $5$ (every edge stretched by at most $5$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that no numbering of width $4$ exists by a complete argument (an exhaustive placement search with correct pruning rules, or an equivalent case analysis that covers every possibility).", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States a valid lower bound of $4$ (the diameter bound $\lceil 13/4 \rceil = 4$ or a density bound on a connected subgraph) and recognises that it is not tight.", points=1, isFinalAnswer=False),
]
wrong = ["4", "6", "3"]
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

Answer key: 5.

1. Edges (from the figure): 1-7, 1-14, 2-7, 2-10, 2-14, 3-6, 3-11, 3-13, 4-5, 4-6, 4-8, 4-9, 5-8, 6-11, 6-12, 6-13, 7-11, 7-12, 7-13, 8-10, 9-10, 10-12, 10-14, 12-14, 13-14.
2. Lower bound: no numbering of width 4 exists. Two independent exact methods (backtracking over
   positions with the two pruning rules stated in the solution, 2471 nodes, every branch to depth 3
   printed with the rule that kills it; and a dynamic programme over (set of placed vertices, last four
   placed)) both report none. Every cheap bound stops at 4: degree bound 2, diameter bound 4, and the
   density bound ceil((|S|-1)/diam(S)) is at most 4 over all connected induced subgraphs S (all 8191
   subsets checked).
3. Upper bound: positions 1->1, 2->2, 5->3, 8->4, 14->5, 7->6, 10->7, 4->8, 12->9, 13->10, 11->11, 9->12, 6->13, 3->14
   give width 5 (every edge stretch is listed in the program output).
4. There are 23616 numberings of width 5; Cuthill-McKee numberings have widths 5 to 9 depending on
   the start vertex.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["task05 v4", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Section 2 of verification_notes.txt gives the two independent exact computations showing no numbering of width 4 exists (the pruned placement search with its tree printed to depth 3, and a dynamic programme) and the check that every cheap lower bound stops at 4; section 3 gives the explicit width-5 numbering with every edge stretch; section 6 embeds the program verify_key.py with its full output.", "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
