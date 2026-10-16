import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-optimal-numberings-count"
question = r"""The figure shows a graph $G$ with $12$ vertices, labelled $1$ to $12$, and $20$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 12\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

How many numberings of $G$ have width equal to the bandwidth of $G$? A numbering and its reverse (the numbering $v \mapsto 13 - f(v)$) are counted as two different numberings. Give a single integer."""
final_answer = "6"
variants = [r"$6$", "six"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $13$, $14$, $16$, $1\,11$, $26$, $28$, $2\,10$, $34$, $35$, $49$, $4\,10$, $4\,11$, $69$, $58$, $8\,12$, $79$, $9\,12$, $7\,11$ and $10\,11$. The degrees are $5$ (vertices $1$ and $4$), $4$ (vertices $2$, $9$ and $11$), $3$ (vertices $3$, $6$, $8$ and $10$) and $2$ (vertices $5$, $7$ and $12$).

Step 2: The bandwidth is $4$.
Lower bound: if $H$ is a connected subgraph with $k$ vertices and diameter $d$, every numbering stretches some edge of $H$ by at least $\lceil (k-1)/d \rceil$, because the lowest and highest numbered vertices of $H$ differ by at least $k-1$ and are joined inside $H$ by at most $d$ edges. The subgraph induced on $\{1, 2, 3, 4, 6, 9, 10, 11\}$ has eight vertices and diameter $2$ (every two of them are adjacent or have a common neighbour among $1$, $4$, $6$ and $2$), so the width is at least $\lceil 7/2 \rceil = 4$. Upper bound: the numbering $5, 8, 12, 6, 3, 2, 9, 1, 4, 10, 7, 11$ (positions $1$ to $12$) has width $4$.

Step 3: What every numbering of width $4$ must look like.
Write $p(v)$ for the position of $v$. Call $H$ the eight-vertex subgraph of Step 2. Its lowest and highest vertices are at least $7$ apart and joined by a path of at most two edges of stretch at most $4$, so they are exactly $7$ or $8$ apart, and the eight vertices of $H$ fill a window of $8$ or $9$ consecutive positions. The four vertices $5$, $7$, $8$, $12$ outside $H$ therefore occupy the positions outside that window, at most one of them inside it. Vertex $11$ has neighbours $1$, $4$, $7$, $10$; vertex $7$ has neighbours $9$ and $11$; vertex $5$ has neighbours $3$ and $8$; vertex $12$ has neighbours $8$ and $9$; vertex $8$ has neighbours $2$, $5$, $12$. Since $7$, $5$, $12$ and $8$ sit at the ends and each must be within $4$ of its neighbours, $7$ forces $9$ and $11$ to lie within $4$ of an end, which puts $11$ at the end itself on one side (it is in $H$ and its $H$-neighbours $1$, $4$, $10$ must still be reachable), while $5$, $8$, $12$ occupy the other end with $3$ and $9$ just inside. Working through the positions of $1$ and $4$ (adjacent, both of degree $5$, so they sit next to each other in the middle of the window with their ten neighbour slots spread on both sides) leaves exactly three arrangements up to reversal.

Step 4: The complete list.
Reading positions $1$ to $12$:
$$5, 8, 12, 6, 3, 2, 9, 1, 4, 10, 7, 11 \qquad 5, 12, 8, 6, 3, 9, 2, 1, 4, 7, 10, 11 \qquad 8, 5, 12, 6, 2, 3, 9, 1, 10, 4, 7, 11$$
and their three reverses. Each has width $4$ (the eight edges $16$, $1\,11$, $28$, $2\,10$, $34$, $35$, $79$ and $9\,12$ are stretched by exactly $4$ in all six, every other edge by less). That there are no others is the content of Step 3 together with the finite check of the remaining placements; the verification notes carry the full search tree, every dead branch with the reason it dies, and a second, independent count by a dynamic programme over sets of placed vertices. Both give six.

Step 5: Conclusion.
The bandwidth is $4$ and exactly $6$ numberings attain it, $3$ up to reversal. (For comparison, $7\,826$ numberings have width at most $5$.)

Answer: $6$."""
rubric = [
    dict(id="c1", description=r"Gives $6$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Establishes that the bandwidth is $4$: a valid lower-bound argument (for instance the eight-vertex induced subgraph of diameter $2$ on $\{1, 2, 3, 4, 6, 9, 10, 11\}$) and an explicit numbering of width $4$.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Lists the three optimal numberings up to reversal, $5\,8\,12\,6\,3\,2\,9\,1\,4\,10\,7\,11$, $5\,12\,8\,6\,3\,9\,2\,1\,4\,7\,10\,11$ and $8\,5\,12\,6\,2\,3\,9\,1\,10\,4\,7\,11$ (or their reverses), each checked to have width $4$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Shows that no other numbering of width $4$ exists, by a case analysis of the positions of the end vertices and of the adjacent degree-$5$ vertices $1$ and $4$, or by an equivalent exhaustive argument.", points=1, isFinalAnswer=False),
]
wrong = ["3", "2", "12", "4"]
references = r"""The density lower bound for the bandwidth and the general theory of the problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the proof that the bandwidth is $4$, the complete enumeration of the numberings of width $4$ by backtracking (six, listed, with the top of the search tree printed and the reason every dead branch dies), an independent count of six by a dynamic programme over sets of placed vertices, and the structural facts shared by all six numberings; the program is embedded with its output."""
necessity = "The graph is given only by the figure; the twenty edges are not listed in the text, and both the bandwidth and the number of optimal numberings depend on the exact edge set."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: graph layout problems (bandwidth of a graph and its optimal numberings)",
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
    txt = f"""VERIFICATION NOTES: number of optimal numberings of the graph in the figure

Answer key: 6 (bandwidth 4; three numberings up to reversal, six in all).

1. Edges (from the figure): 12, 13, 14, 16, 1-11, 26, 28, 2-10, 34, 35, 49, 4-10, 4-11, 69, 58, 8-12, 79, 9-12, 7-11, 10-11.
2. Bandwidth 4: no numbering of width 3 (exhaustive backtracking); the induced subgraph on
   {{1,2,3,4,6,9,10,11}} has eight vertices and diameter 2, so width >= ceil(7/2) = 4; the numbering
   5,8,12,6,3,2,9,1,4,10,7,11 has width 4.
3. All numberings of width 4, by backtracking with pruning (a vertex can be placed only if all its placed
   neighbours are within 4 positions, and every placed vertex must still have room for its unplaced
   neighbours): exactly six, listed in the output, closed under reversal, three up to reversal. The top
   two levels of the search tree are printed with the reason each dead branch dies, so the start of the
   enumeration can be followed by hand; the live starts are (5,8), (5,12), (8,5), (11,7), (11,10).
4. Independent count: a dynamic programme over (set of placed vertices, last four placed vertices)
   counts the numberings of width at most 4 without listing them: 6.
5. Facts shared by all six: vertex 11 is at an end; the other end is 5 or 8; vertices 1 and 4 are within
   two positions of each other; the same eight edges (16, 1-11, 28, 2-10, 34, 35, 79, 9-12) are stretched
   by exactly 4. For comparison 7826 numberings have width at most 5.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["# task05 v2: number of optimal numberings (bandwidth) of a 12-vertex graph", "",
             "Revision of task05 after Summit returned it (Model A 3/3 fast, short lower-bound arguments). Same figure; the question now asks for the number of numberings attaining the bandwidth.", "",
             "## Question", "", question, "", "## Answer", "", final_answer + " (also accepted: " + ", ".join(variants) + ")", "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 4, the complete list of the six numberings of width 4 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six; section 6 embeds the program with its output.", "",
              "## How to submit", "", "Either revise the returned task05 entry field by field (question text, answer, solution, rubric, common wrong answers, references text, reference file) with the texts above, or import the zip as a new question if the platform allows it.", "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
