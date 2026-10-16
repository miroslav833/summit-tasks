import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-bandwidth-fourteen-optimal-numberings-count"
question = r"""The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $29$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 14\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

How many numberings of $G$ have width equal to the bandwidth of $G$? A numbering and its reverse (the numbering $v \mapsto 15 - f(v)$) are counted as two different numberings. Give a single integer."""
final_answer = "6"
variants = [r"$6$", "six"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $14$, $16$, $18$, $1\,11$, $1\,14$, $28$, $37$, $38$, $3\,10$, $3\,12$, $3\,13$, $4\,10$, $4\,11$, $4\,13$, $4\,14$, $59$, $5\,12$, $67$, $69$, $6\,10$, $6\,11$, $78$, $7\,11$, $9\,13$, $9\,14$, $11\,13$, $11\,14$ and $12\,14$. The degrees are $6$ (vertices $1$ and $11$), $5$ (vertices $3$, $4$, $6$ and $14$), $4$ (vertices $7$, $8$, $9$ and $13$), $3$ (vertices $10$ and $12$) and $2$ (vertices $2$ and $5$). The diameter of $G$ is $4$.

Step 2: The bandwidth is $5$.
Lower bound. Take a connected subgraph $H$ with $k$ vertices and diameter $d$. In any numbering the lowest and the highest vertex of $H$ are at least $k-1$ apart, and a path of at most $d$ edges inside $H$ joins them, so one of those edges is stretched by at least $\lceil (k-1)/d \rceil$. The subgraph induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$ has ten vertices and diameter $2$. Any two of them are adjacent or share a neighbour inside the subgraph ($1$ and $3$ share $8$, $3$ and $4$ share $10$, $7$ and $14$ share $11$, $12$ and $13$ share $3$, and so on for the other pairs). This gives width at least $\lceil 9/2 \rceil = 5$. The degree bound $\lceil 6/2 \rceil = 3$ and the diameter bound $\lceil 13/4 \rceil = 4$ are weaker. Upper bound. The numbering $2, 8, 7, 1, 11, 4, 3, 6, 14, 13, 10, 12, 9, 5$ (positions $1$ to $14$) has width $5$. So the bandwidth is $5$.

Step 3: What a numbering of width $5$ must look like.
Write $p(v)$ for the position of $v$. Suppose $v$ is in position $1$. Each neighbour of $v$ is then in a position at most $6$, and each vertex at distance $2$ from $v$ in a position at most $11$, so the whole ball of radius $2$ around $v$ has to fit into eleven positions. Count these balls. Around $2$ the ball has $9$ vertices and around $5$ it has $7$. Around every other vertex it has at least $12$ ($12$ around $8$, $9$, $10$ and $12$, $13$ around $1$, $4$, $6$, $7$, $11$ and $13$, $14$ around $3$ and $14$). So the ends of the numbering are $2$ and $5$, and after a reversal we can take $p(2) = 1$ and $p(5) = 14$. The neighbours of $2$ are $1$ and $8$. Put $1$ in position $2$ and its other five neighbours fill positions $3$ to $7$; their further neighbours $3$, $7$, $9$, $10$, $12$, $13$ then have to sit in position $12$ or lower, and that is thirteen vertices in twelve positions. So $p(8) = 2$, and $1$ is somewhere in positions $3$ to $6$. Now the other end. The vertex in position $13$ has its radius-$2$ ball inside positions $3$ to $14$, twelve positions, and $5$ is in there as well. This rules out every vertex except $9$. The balls around $8$ and $10$ have $12$ vertices and do not contain $5$, and for $12$ the vertex $6$ joins the count, because $6$ is adjacent to $9$ and $9$ is within five positions of $5$. So $p(9) = 13$, and $12$ is in one of positions $9$ to $12$. The two vertices of degree $6$, $1$ and $11$, need room on both sides, so they sit in the middle. The same holds for $3$ and $6$, which have neighbours near both ends ($3$ is adjacent to $8$ and $12$, $6$ to $7$ and $9$). Checking the placements that keep every edge within $5$ gives $p(1) \in \{4, 5\}$, $p(12) = 12$, $p(3) = 7$, $p(6) = 8$, and three arrangements in all.

Step 4: The complete list.
Reading positions $1$ to $14$:
$$2, 8, 7, 1, 11, 4, 3, 6, 14, 13, 10, 12, 9, 5 \qquad 2, 8, 7, 10, 1, 11, 3, 6, 4, 14, 13, 12, 9, 5 \qquad 2, 8, 10, 7, 1, 4, 3, 6, 11, 14, 13, 12, 9, 5$$
and their three reverses. Each has width $5$. In the first two the edges $1\,14$, $38$, $3\,12$, $4\,10$, $67$, $69$ and $11\,13$ are stretched by exactly $5$, in the third the edges $1\,14$, $38$, $3\,12$, $4\,13$, $69$, $6\,10$ and $7\,11$. No other numbering works, by Step 3 and the finite check of what is left. The verification notes carry the search tree with the reason each dead branch dies, and a second count by a dynamic programme over sets of placed vertices. Both give six.

Step 5: Conclusion.
The bandwidth is $5$ and exactly $6$ numberings attain it, $3$ up to reversal. For comparison, $23\,662$ numberings have width at most $6$.

Answer: $6$."""
rubric = [
    dict(id="c1", description=r"Gives $6$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Establishes that the bandwidth is $5$: a valid lower-bound argument (for instance the ten-vertex induced subgraph of diameter $2$ on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$) and an explicit numbering of width $5$.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Lists the three optimal numberings up to reversal, $2\,8\,7\,1\,11\,4\,3\,6\,14\,13\,10\,12\,9\,5$, $2\,8\,7\,10\,1\,11\,3\,6\,4\,14\,13\,12\,9\,5$ and $2\,8\,10\,7\,1\,4\,3\,6\,11\,14\,13\,12\,9\,5$ (or their reverses), each checked to have width $5$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Shows that no other numbering of width $5$ exists, by a case analysis of the end vertices (they must be $2$ and $5$) and of the positions of the degree-$6$ vertices $1$ and $11$, or by an exhaustive argument.", points=1, isFinalAnswer=False),
]
wrong = ["2", "4", "8", "3", "12"]
references = r"""The density lower bound for the bandwidth and the general theory of the problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the proof that the bandwidth is $5$, the complete enumeration of the numberings of width $5$ by backtracking (six, listed, with the top of the search tree printed and the reason every dead branch dies), an independent count of six by a dynamic programme over sets of placed vertices, and the structural facts shared by all six numberings. The program is embedded with its output."""
necessity = "The graph is given only by the figure. The twenty-nine edges are not listed in the text, and both the bandwidth and the number of optimal numberings depend on the exact edge set. Removing either of the edges 67 or 6-10 raises the count from six to twenty or more."
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

Answer key: 6 (bandwidth 5; three numberings up to reversal, six in all).

1. Edges (from the figure): 12, 14, 16, 18, 1-11, 1-14, 28, 37, 38, 3-10, 3-12, 3-13, 4-10, 4-11, 4-13, 4-14,
   59, 5-12, 67, 69, 6-10, 6-11, 78, 7-11, 9-13, 9-14, 11-13, 11-14, 12-14. Fourteen vertices, 29 edges,
   degrees 6,2,5,5,2,5,4,4,4,3,6,3,4,5 for vertices 1 to 14, diameter 4.
2. Bandwidth 5: no numbering of width 4 (exhaustive backtracking); the induced subgraph on
   {{1,3,4,7,8,10,11,12,13,14}} has ten vertices and diameter 2 (a common neighbour inside the subgraph is
   printed for every non-adjacent pair), so width >= ceil(9/2) = 5; the numbering
   2,8,7,1,11,4,3,6,14,13,10,12,9,5 has width 5. The degree bound gives 3 and the diameter bound 4.
3. All numberings of width 5, by backtracking with pruning (a vertex can be placed only if all its placed
   neighbours are within 5 positions, and every placed vertex must still have room for its unplaced
   neighbours): exactly six, listed in the output, closed under reversal, three up to reversal. The top
   two levels of the search tree are printed with the reason each dead branch dies, so the start of the
   enumeration can be followed by hand; the only live starts are (2,8) and (5,9).
4. Independent count: a dynamic programme over (set of placed vertices, last five placed vertices)
   counts the numberings of width at most 5 without listing them: 6.
5. Facts shared by all six, with the hand-checkable reasons the program prints: the ends are 2 and 5 (a
   vertex in position 1 has its whole distance-2 ball in positions 1 to 11; only 2 and 5 have a ball of
   at most 11 vertices, sizes 9 and 7, every other ball has 12 to 14 vertices); with 2 in position 1,
   8 is in position 2 (1 in position 2 would force thirteen vertices into positions 1 to 12) and 9 is in
   position 13 (the vertex there has its distance-2 ball plus vertex 5 inside positions 3 to 14; for
   every candidate but 9 that is thirteen vertices in twelve positions); the search then gives 1 in
   position 4 or 5, 3 in position 7, 6 in position 8, 12 in position 12; seven edges are stretched by
   exactly 5 in each numbering (listed in the output). For comparison 23662 numberings have width at
   most 6, and every breadth-first (Cuthill-McKee) numbering has width 7 to 9.

6. Program verify_key.py (run with {pyver}; command: python3 verify_key.py)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme():
    lines = ["# task06 v2: number of optimal numberings (bandwidth) of a 14-vertex graph", "",
             "Counting version of task06. Summit returned task05 and suggested asking for the number of optimal numberings instead. The task06 graph has 248 of them, far too many for any hand route, so two edges were added (67 and 6-10, 29 edges in all). The bandwidth stays 5, the easy bounds stay 3 and 4, the diameter stays 4, and exactly six numberings (three up to reversal) attain width 5. New figure, same drawing style.", "",
             "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer + " (also accepted: " + ", ".join(variants) + ")", "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", "Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 5, the complete list of the six numberings of width 5 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six; section 6 embeds the program with its output.", "",
              "## How to submit", "", "Import the zip as a new question (the figure is new, so this is not a field-by-field revision of task06).", "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
