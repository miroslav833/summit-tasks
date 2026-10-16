import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-crossing-number-ten-vertices"
question = r"""The figure shows a graph $G$ with $10$ vertices, labelled $1$ to $10$, and $21$ edges. The vertices have been placed on a circle and every edge is drawn as a straight chord. This is just one way of drawing $G$ and the figure is not claimed to be a good one.

A drawing of $G$ in the plane places the vertices at distinct points and represents each edge by a simple curve between its two endpoints that passes through no other vertex. A crossing is a point that lies in the interior of two edges. Only drawings in which no three edges pass through one point are considered, so every crossing is a crossing of exactly two edges. The crossing number $\mathrm{cr}(G)$ is the smallest number of crossings over all drawings of $G$.

What is $\mathrm{cr}(G)$? Give a single integer."""
final_answer = "3"
variants = [r"$3$", r"$\mathrm{cr}(G) = 3$", "crossing number 3"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $15$, $19$, $1\,10$, $23$, $24$, $26$, $35$, $36$, $38$, $39$, $45$, $46$, $48$, $4\,10$, $56$, $67$, $78$, $79$, $7\,10$, $8\,10$. The degrees are $5$ (vertices $3$, $4$ and $6$), $4$ (vertices $1$, $2$, $5$, $7$, $8$ and $10$) and $3$ (vertex $9$). $G$ is $3$-connected. The bound from Euler's formula gives nothing: $21 \le 3 \cdot 10 - 6 = 24$, so $m - 3n + 6 = -3$. The graph is not planar: it contains a subdivision of $K_{3,3}$ with the vertices $3$, $4$, $7$ on one side and $6$, $8$, $9$ on the other, the nine connections being the edges $36$, $38$, $39$, $46$, $48$, $67$, $78$, $79$ and the path $4\,5\,1\,9$.

Step 2: No drawing has one crossing, and only two pairs of edges can be deleted to leave a planar graph.
If a drawing had a single crossing, say between the edges $a$ and $b$, then deleting $a$ would leave a crossing-free drawing of $G - a$, so $G - a$ would be planar. Deleting any one of the $21$ edges leaves a non-planar graph (all $21$ subgraphs are checked in the notes; for the edges outside the subdivision of Step 1 this is immediate, and for each of the other nine edges another Kuratowski subgraph avoiding it exists), so $\mathrm{cr}(G) \ge 2$. Among the $\binom{21}{2} = 210$ pairs of edges, exactly two can be deleted to leave a planar graph: $\{12, 67\}$ and $\{15, 67\}$. Every other pair leaves a non-planar graph. (The two planar subgraphs with $19$ edges are both $3$-connected; their faces are listed in the notes.)

Step 3: No drawing has two crossings.
Suppose a drawing of $G$ has exactly two crossings, one between the edges $a$ and $b$ and one between the edges $c$ and $d$. If an edge took part in both crossings, say $a = c$, deleting $a$ would leave a crossing-free drawing of $G - a$, which is impossible by Step 2. So $a$, $b$, $c$, $d$ are four distinct edges. Deleting $a$ and $c$ removes both crossings, so $G - \{a, c\}$ is planar; in the same way $G - \{a, d\}$, $G - \{b, c\}$ and $G - \{b, d\}$ are planar. These are four distinct pairs of edges whose deletion leaves a planar graph, but by Step 2 only two such pairs exist. Hence $\mathrm{cr}(G) \ge 3$.

The same conclusion comes from the two planar subgraphs directly. In the unique embedding of $G - \{12, 67\}$ the faces are $2\,3\,6$, $3\,5\,6$, $8\,4\,10$, $6\,5\,4$, $1\,10\,4\,5$, $5\,3\,9\,1$, $7\,8\,10$, $4\,8\,3\,2$, $6\,4\,2$, $9\,3\,8\,7$ and $10\,1\,9\,7$; no face containing vertex $1$ shares an edge with a face containing vertex $2$, so the edge $12$ cannot be added with a single crossing, and the same holds for $67$. In the unique embedding of $G - \{15, 67\}$ the faces are $2\,3\,9\,1$, $8\,10\,7$, $8\,7\,9\,3$, $5\,3\,6$, $10\,8\,4$, $1\,9\,7\,10$, $10\,4\,2\,1$, $3\,2\,6$, $6\,2\,4$, $4\,8\,3\,5$ and $6\,4\,5$, and again neither missing edge can be added with one crossing. Starting from a planar subgraph with $19$ edges, the two missing edges need two crossings each, so that route gives a drawing with four crossings, not three.

Step 4: A drawing with three crossings.
Place the vertices at the points $1 \mapsto (0, 4)$, $2 \mapsto (6, 6)$, $3 \mapsto (5, 7)$, $4 \mapsto (8, 6)$, $5 \mapsto (2, 5)$, $6 \mapsto (7, 7)$, $7 \mapsto (12, 10)$, $8 \mapsto (9, 8)$, $9 \mapsto (5, 12)$, $10 \mapsto (10, 3)$ and draw every edge as a straight segment. No vertex lies on a segment that is not incident to it, and the only pairs of segments that cross are $12$ with $45$, $23$ with $56$, and $38$ with $67$. (Equivalently: the subgraph $G - \{12, 23, 38\}$ with $18$ edges is planar, and in its embedding with the ten faces $8\,4\,10$, $3\,5\,6$, $5\,3\,9\,1$, $5\,1\,10\,4$, $4\,6\,2$, $6\,4\,8\,7$, $7\,8\,10$, $9\,3\,6\,7$, $10\,1\,9\,7$ and $6\,5\,4\,2$, each deleted edge joins two faces that share one edge: $12$ goes from the face $5\,1\,10\,4$ across $45$ into $6\,5\,4\,2$, $23$ from $3\,5\,6$ across $56$ into $6\,5\,4\,2$, and $38$ from $9\,3\,6\,7$ across $67$ into $6\,4\,8\,7$. The three new curves can be drawn without meeting each other, as the coordinates above show.) So $\mathrm{cr}(G) \le 3$.

Step 5: Conclusion.
$\mathrm{cr}(G) \ge 3$ by Step 3 and $\mathrm{cr}(G) \le 3$ by Step 4, so $\mathrm{cr}(G) = 3$. Deleting two edges is enough to make $G$ planar, yet no drawing with two crossings exists, so the number of edges that must be deleted for planarity is one less than the crossing number here. In each of the four optimal crossing patterns the edge $38$ crosses $67$.

Answer: $3$."""
rubric = [
    dict(id="c1", description=r"Gives $3$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a drawing of $G$ with exactly three crossings (for instance explicit coordinates, or a planar subgraph with $18$ edges together with the three missing edges each added with one crossing, such as $12$ crossing $45$, $23$ crossing $56$ and $38$ crossing $67$).", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves that no drawing with two crossings exists by a valid argument, for instance: no single edge deletion leaves a planar graph, only the pairs $\{12, 67\}$ and $\{15, 67\}$ can be deleted to leave a planar graph, and a drawing with two crossings would give four such pairs; or an exhaustive check that neither $19$-edge planar subgraph admits both missing edges with one crossing each.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Shows that $G$ is non-planar and that deleting the two edges $12$ and $67$ (or $15$ and $67$) leaves a planar graph.", points=1, isFinalAnswer=False),
]
wrong = ["2", "4", "1"]
references = r"""The crossing number and its basic properties, including the fact that in a drawing with the fewest crossings adjacent edges do not cross and two edges cross at most once: M. Schaefer, The graph crossing number and its variants: a survey, Electronic Journal of Combinatorics, Dynamic Survey DS21 (2013, updated). NP-completeness of the crossing number, which is why the value needs a certificate on each side: M. R. Garey and D. S. Johnson, Crossing number is NP-complete, SIAM Journal on Algebraic and Discrete Methods 4 (1983), 312-316. The planarity algorithm used for the independent check: G. Demoucron, Y. Malgrange and R. Pertuiset, Graphes planaires: reconnaissance et construction de representations planaires topologiques, Revue Francaise de Recherche Operationnelle 8 (1964), 33-47. The uploaded file verification_notes.txt contains two independent computations: an exhaustive enumeration of all crossing sets with up to three crossings (planarity of every planarization), and a library-free route with its own planarity test that lists the only two edge pairs whose deletion leaves a planar graph, the faces of those two planar subgraphs, and a straight-line drawing with exactly three crossings checked by exact integer arithmetic; the program is embedded with its output."""
necessity = "The graph is given only by the figure; the twenty-one edges are not listed in the text, and the answer depends on the exact edge set (adding or removing one edge changes which edge pairs can be deleted to leave a planar graph and changes the optimal drawing)."
verify_field = "Section 2 of verification_notes.txt gives the two edge pairs whose deletion leaves a planar graph and the four-pairs argument that rules out two crossings; section 3 gives the straight-line drawing with its coordinates and its three crossing pairs; section 4 is the exhaustive enumeration of crossing sets (none with one or two crossings, four with three); section 6 embeds the program verify_key.py with its full output, including an independent planarity test that does not use a graph library."
SCREEN = "(filled in after the screen)"
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: topological graph theory (crossing number of a graph)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original drawing of the graph with the vertices on a circle)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}


def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", verify_field)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"):
            assert ch not in text, name
    print("package checks passed")


def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "Both routes agree" in out, "verify_key_output.txt is not a complete run"
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: crossing number of the graph in the figure

Answer key: 3.

1. Edges (from the figure): 1-2, 1-5, 1-9, 1-10, 2-3, 2-4, 2-6, 3-5, 3-6, 3-8, 3-9, 4-5, 4-6, 4-8, 4-10,
   5-6, 6-7, 7-8, 7-9, 7-10, 8-10.  Ten vertices, twenty-one edges, 3-connected, not planar.
   Euler's bound m - 3n + 6 = -3 gives nothing.

2. Lower bound.  No single edge can be deleted to leave a planar graph (all 21 subgraphs checked).
   Exactly two pairs of edges can be deleted to leave a planar graph: {{1-2, 6-7}} and {{1-5, 6-7}}
   (all 210 pairs checked, by two different planarity tests).  A drawing with one crossing between
   edges a and b would make G - a planar, so there is none.  In a drawing with two crossings, between
   a, b and between c, d, the four edges are distinct (an edge in both crossings could be deleted to
   leave a planar graph), and each of G - {{a,c}}, G - {{a,d}}, G - {{b,c}}, G - {{b,d}} is planar; that
   is four distinct planar pairs, but only two exist.  So cr(G) >= 3.
   Second form of the same bound: both 19-edge planar subgraphs are 3-connected, so each has one
   embedding; the faces are printed in the program output, and in each embedding neither missing edge
   has its endpoints on two faces that share an edge, so neither can be added with one crossing.
   Starting from a 19-edge planar subgraph the missing edges cost two crossings each (four in total).

3. Upper bound.  Straight-line drawing with the vertices at
   1 (0,4), 2 (6,6), 3 (5,7), 4 (8,6), 5 (2,5), 6 (7,7), 7 (12,10), 8 (9,8), 9 (5,12), 10 (10,3).
   Exact integer orientation tests: no vertex on a non-incident segment, no touching or overlapping
   segments, no three segments through one point, and exactly three crossing pairs:
   1-2 with 4-5, 2-3 with 5-6, 3-8 with 6-7.  So cr(G) <= 3.

4. Exhaustive enumeration (route A).  A drawing with k crossings in which adjacent edges do not cross
   and two edges cross at most once is the same as a planar embedding of its planarization (each
   crossing a new degree-4 vertex, each edge split in the order of its crossings).  Optimal drawings
   have both properties.  Over all sets of k independent edge pairs and all orders along the edges:
   k = 1: no planar planarization; k = 2: none; k = 3: four crossing sets, namely
   {{1-2 x 3-5, 2-4 x 5-6, 3-8 x 6-7}}, {{1-2 x 4-5, 2-3 x 5-6, 3-8 x 6-7}}, {{1-5 x 2-3, 2-6 x 4-5, 3-8 x 6-7}},
   {{1-5 x 2-4, 2-6 x 3-5, 3-8 x 6-7}}.  Every optimal drawing has 3-8 crossing 6-7.

5. Independence of the two routes.  Route A uses the networkx left-right planarity test on every
   planarization.  Route B uses a planarity test and embedding written from the Demoucron-Malgrange-
   Pertuiset description with no graph library, lists the planar pairs again, prints the faces of the
   two 19-edge planar subgraphs and of the 18-edge planar subgraph behind the drawing of section 3,
   and checks the straight-line drawing by integer arithmetic.  Both give cr(G) = 3.

6. Program verify_key.py (run with {pyver} and networkx 3.7; command: python3 verify_key.py;
   running time about seven minutes, almost all of it in the k = 3 enumeration of route A)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")


def build_readme():
    lines = ["# task07: crossing number of a 10-vertex graph", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", verify_field, "", "## Screen", "", SCREEN]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")


def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")


if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
