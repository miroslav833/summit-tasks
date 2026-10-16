import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-sixteen-vertices"
question = r"""The figure shows a graph $G$ with $16$ vertices, labelled $1$ to $16$, and $27$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 16\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer."""
final_answer = "5"
variants = [r"$5$", "bandwidth 5"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $13$, $1\,10$, $23$, $29$, $2\,12$, $2\,13$, $3\,10$, $3\,12$, $3\,14$, $3\,15$, $48$, $4\,16$, $56$, $57$, $69$, $6\,14$, $6\,15$, $7\,12$, $7\,16$, $89$, $8\,10$, $8\,13$, $9\,15$, $11\,13$, $11\,14$, $12\,15$ and $13\,16$. The degrees are $6$ (vertex $3$), $4$ (vertices $2$, $6$, $8$, $9$, $12$, $13$ and $15$), $3$ (vertices $7$, $10$, $14$ and $16$) and $2$ (vertices $1$, $4$, $5$ and $11$). The diameter of $G$ is $4$.

Step 2: The easy bounds give $3$ and $4$.
A vertex of degree $6$ forces some incident edge to be stretched by at least $\lceil 6/2 \rceil = 3$. The diameter bound gives $\lceil 15/4 \rceil = 4$. The density bound, $\lceil (k-1)/d \rceil$ for a connected subgraph with $k$ vertices and diameter $d$, never goes above $4$ on this graph, whichever subgraph is taken. So none of the usual bounds settles the answer, and the lower bound needs a different argument.

Step 3: No numbering has width $4$.
Take a numbering of width $b$ and let $P$ be the set of vertices in positions $1$ to $k$. A vertex outside $P$ with a neighbour in $P$ has to sit within $b$ positions of that neighbour, so it sits in one of the positions $k+1$ to $k+b$. So $P$ has at most $b$ neighbours outside $P$, and this holds for every $k$. Now suppose $b = 4$ and build $P$ one vertex at a time, keeping only the sets with at most four outside neighbours. With one vertex, every vertex except $3$ (degree $6$) qualifies. With two vertices $21$ sets survive, with three vertices $15$, with four vertices $5$: $\{1, 4, 8, 10\}$, $\{1, 4, 10, 16\}$, $\{1, 10, 11, 14\}$, $\{4, 5, 7, 16\}$ and $\{4, 11, 13, 16\}$. With five vertices only $\{1, 4, 8, 10, 16\}$ survives, with outside neighbours $3$, $7$, $9$, $13$. Adding a sixth vertex always gives at least five outside neighbours. If the added vertex is one of $3$, $7$, $9$, $13$, the other three stay and the new vertex brings at least two more ($3$ brings $2$, $12$, $14$, $15$, vertex $7$ brings $5$ and $12$, vertex $9$ brings $2$, $6$, $15$, vertex $13$ brings $2$ and $11$). If it is any other vertex, all four stay and the new vertex brings at least one more ($2$ brings $12$, $5$ brings $6$, $6$ brings $5$, $14$, $15$, $11$ brings $14$, $12$ brings $2$ and $15$, $14$ brings $6$ and $11$, $15$ brings $6$ and $12$). So no numbering of width $4$ gets past its sixth vertex, and the bandwidth is at least $5$. The verification notes list all $57$ sets of the chain with their outside neighbours.

Step 4: A numbering of width $5$.
Give the vertices the positions $1 \mapsto 1$, $10 \mapsto 2$, $9 \mapsto 3$, $15 \mapsto 4$, $3 \mapsto 5$, $2 \mapsto 6$, $8 \mapsto 7$, $6 \mapsto 8$, $12 \mapsto 9$, $14 \mapsto 10$, $13 \mapsto 11$, $4 \mapsto 12$, $5 \mapsto 13$, $7 \mapsto 14$, $11 \mapsto 15$, $16 \mapsto 16$. The stretches of the twenty-seven edges are $13{:}\,4$, $1\,10{:}\,1$, $23{:}\,1$, $29{:}\,3$, $2\,12{:}\,3$, $2\,13{:}\,5$, $3\,10{:}\,3$, $3\,12{:}\,4$, $3\,14{:}\,5$, $3\,15{:}\,1$, $48{:}\,5$, $4\,16{:}\,4$, $56{:}\,5$, $57{:}\,1$, $69{:}\,5$, $6\,14{:}\,2$, $6\,15{:}\,4$, $7\,12{:}\,5$, $7\,16{:}\,2$, $89{:}\,4$, $8\,10{:}\,5$, $8\,13{:}\,4$, $9\,15{:}\,1$, $11\,13{:}\,4$, $11\,14{:}\,5$, $12\,15{:}\,5$, $13\,16{:}\,5$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. Breadth-first numberings from any start vertex have width $7$ or more, and the numbering of Step 4 is the only one of width $5$ apart from its reverse, which is why the usual heuristics stop at $6$ or $7$.

Answer: $5$."""
rubric = [
    dict(id="c1", description=r"Gives $5$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits an explicit numbering of the sixteen vertices of width $5$ (every edge stretched by at most $5$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that no numbering of width $4$ exists by a valid argument, for instance the prefix argument (the first $k$ vertices of a numbering of width $4$ have at most four outside neighbours, and no set of six vertices satisfies this) or an exhaustive case analysis.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the degree bound $\lceil 6/2 \rceil = 3$ or the diameter bound $\lceil 15/4 \rceil = 4$ and recognises that neither is tight.", points=1, isFinalAnswer=False),
]
wrong = ["6", "4", "7"]
references = r"""The general theory of the bandwidth problem, including the degree, diameter and density lower bounds: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the written lower-bound proof (the prefix argument: the first $k$ vertices of a numbering of width $4$ have at most four outside neighbours, and the chain of such sets dies at six vertices; all $57$ sets are listed), two independent exact computations of the bandwidth (backtracking over numberings and a dynamic programme over sets of placed vertices), the explicit numbering of width $5$ with the stretch of every edge, the check that no density bound reaches $5$, and the widths of all Cuthill-McKee numberings. The program is embedded with its output."""
necessity = "The graph is given only by the figure. The twenty-seven edges are not listed in the text, and the answer depends on the exact edge set."
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

1. Edges (from the figure): 13, 1-10, 23, 29, 2-12, 2-13, 3-10, 3-12, 3-14, 3-15, 48, 4-16, 56, 57, 69, 6-14,
   6-15, 7-12, 7-16, 89, 8-10, 8-13, 9-15, 11-13, 11-14, 12-15, 13-16. Sixteen vertices, 27 edges; degrees
   2,4,6,2,2,4,3,4,4,3,2,4,4,3,4,3 for vertices 1 to 16; diameter 4.
2. Lower bound, written proof. In a numbering of width b, the set P of the first k vertices has at most b
   neighbours outside P: each such neighbour is within b positions of its earliest neighbour in P, so it
   occupies one of the b positions after P. For b = 4 the program grows P one vertex at a time and keeps the
   sets with at most four outside neighbours: 15 sets of size 1 (every vertex but 3), 21 of size 2, 15 of
   size 3, 5 of size 4, one of size 5 ({{1,4,8,10,16}}, outside neighbours 3,7,9,13), none of size 6. Each
   surviving set is printed with its outside neighbours, so the 57 lines can be checked by hand. So no
   numbering of width 4 exists.
3. Two independent exact computations agree: backtracking over numberings with pruning finds no numbering
   of width 4 and exactly two of width 5; a dynamic programme over (set of placed vertices, last b placed)
   counts 0 numberings of width at most 4 and 2 of width at most 5.
4. Upper bound: the numbering 1,10,9,15,3,2,8,6,12,14,13,4,5,7,11,16 (positions 1 to 16) has width 5; the
   stretch of every edge is listed in the output. It and its reverse are the only numberings of width 5.
5. The easy bounds: degree bound ceil(6/2) = 3, diameter bound ceil(15/4) = 4, and the density bound
   ceil((k-1)/d) over every connected induced subgraph (all 2^16 vertex subsets checked) is at most 4. So
   no bound of that kind reaches 5 and the prefix argument of section 2 is needed.
6. Breadth-first (Cuthill-McKee and reverse Cuthill-McKee) numberings from every start vertex have widths
   7 to 10.

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["# task10: bandwidth of a 16-vertex graph with no short lower bound and a unique optimal numbering", "",
             "Built 2026-10-16 after task05 and its counting version came back from Summit 5/5. Design: an instance where (a) no degree, diameter or density bound reaches the answer, so the lower bound needs the prefix argument (a 57-set chain, short enough to write out), and (b) the optimal numbering is unique up to reversal and heuristics miss it (Cuthill-McKee 7 to 10, simulated annealing 0 of 16 restarts, the width-5 prefix chain has 4455 sets). Found by random search over 16-vertex graphs with 26 to 31 edges (work/gen.py, gen2.py, eval.py). The expected wrong answer is 6, the best width a solver reaches without finding the unique numbering.", "",
             "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer + " (also accepted: " + ", ".join(variants) + ")", "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Section 2 of verification_notes.txt is the written lower-bound proof (the first k vertices of a numbering of width 4 have at most four outside neighbours; the chain of such sets is listed in full and dies at six vertices). Section 3 gives two independent exact computations, section 4 the explicit numbering of width 5 with every edge stretch, section 5 the check that no degree, diameter or density bound reaches 5. Section 7 embeds the program with its output.", "",
              "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
