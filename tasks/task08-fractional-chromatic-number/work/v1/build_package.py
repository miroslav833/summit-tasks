import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "fractional-chromatic-number-twelve-vertices"
question = r"""The figure shows a graph $G$ with $12$ vertices, labelled $1$ to $12$, and $24$ edges. Every vertex has degree $4$. An independent set of $G$ is a set of vertices no two of which are joined by an edge. A fractional colouring of $G$ gives each independent set $I$ a weight $x_I \ge 0$ in such a way that, for every vertex $v$, the weights of the independent sets that contain $v$ add up to at least $1$. The weight of the fractional colouring is $\sum_I x_I$, and the fractional chromatic number $\chi_f(G)$ is the smallest weight of a fractional colouring of $G$.

Find $\chi_f(G)$. Give the exact value as a fraction in lowest terms."""
final_answer = "13/4"
variants = [r"$13/4$", r"$\frac{13}{4}$", "3.25", r"$\chi_f(G) = 13/4$"]
MIS = [[1,2,4],[1,2,6,11],[1,2,6,12],[1,3,4,7],[1,3,11],[1,7,12],[2,4,5,8],[2,5,6,11],[2,8,12],[3,4,7,8],[3,4,7,10],[3,7,8,9],[3,9,11],[3,10,11],[4,5,10],[5,6,9,11],[5,6,10,11],[5,8,9],[6,9,12],[6,10,12],[7,8,9,12],[7,10,12]]
W = {1: "1/2", 9: "1/2", 10: "1/2", 2: "1/4", 3: "1/4", 4: "1/4", 5: "1/4", 8: "1/4", 11: "1/4", 12: "1/4", 6: "0", 7: "0"}
from fractions import Fraction as F
def wt(S): return sum(F(W[v]) for v in S)
mis_tex = ", ".join("$\\{" + ",".join(map(str, S)) + "\\}$" for S in MIS)
mis_w_tex = ", ".join("$\\{" + ",".join(map(str, S)) + "\\}{:}\\," + (str(wt(S)) if wt(S) != 1 else "1") + "$" for S in MIS)
solution = r"""Step 1: Read the graph off the figure.
The edges are $1\,5$, $1\,8$, $1\,9$, $1\,10$, $2\,3$, $2\,7$, $2\,9$, $2\,10$, $3\,5$, $3\,6$, $3\,12$, $4\,6$, $4\,9$, $4\,11$, $4\,12$, $5\,7$, $5\,12$, $6\,7$, $6\,8$, $7\,11$, $8\,10$, $8\,11$, $9\,10$, $11\,12$. The triangles are $1\,8\,10$, $1\,9\,10$, $2\,9\,10$, $3\,5\,12$ and $4\,11\,12$, and there is no $K_4$, so the clique number is $\omega(G) = 3$. The maximal independent sets are the twenty-two sets """ + mis_tex + r""". The largest of them have four vertices, so the independence number is $\alpha(G) = 4$.

Step 2: The bounds that come first, and why they do not settle the question.
A fractional colouring $x$ satisfies $\sum_{I \ni v} x_I \ge 1$ for every vertex $v$. Summing this over the three vertices of a triangle, and using that an independent set contains at most one of them, gives $\sum_I x_I \ge 3 = \omega(G)$. Summing it over all twelve vertices gives $\sum_I |I|\, x_I \ge 12$, and since $|I| \le \alpha(G) = 4$ this is $\sum_I x_I \ge 12/4 = 3 = n/\alpha(G)$. For a vertex-transitive graph the bound $n/\alpha$ is exact, but $G$ is only regular: vertex $10$ lies in three triangles and vertex $6$ in none, so no automorphism carries $6$ to $10$, and the identity $\chi_f(G) = n/\alpha(G)$ is not available. From above, the colour classes $\{1,2,4\}$, $\{3,7,8,9\}$, $\{5,6,10,11\}$, $\{12\}$ form a proper $4$-colouring, which is a fractional colouring of weight $4$. So far $3 \le \chi_f(G) \le 4$.

Step 3: Lower bound $13/4$ from a fractional clique.
Give the vertices $1$, $9$, $10$ the weight $w_v = 1/2$, the vertices $2$, $3$, $4$, $5$, $8$, $11$, $12$ the weight $w_v = 1/4$, and the vertices $6$, $7$ the weight $0$. The total is $3/2 + 7/4 = 13/4$. Every independent set $I$ has weight $w(I) = \sum_{v \in I} w_v \le 1$. To see this, recall that $1$, $9$, $10$ form a triangle, so $I$ contains at most one of them. If $I$ contains none, then $w(I) \le |I|/4 \le \alpha(G)/4 = 1$. If $I$ contains $1$, its other members lie among the vertices of weight $1/4$ that are not adjacent to $1$, namely $2$, $3$, $4$, $11$, $12$; these span the edges $2\,3$, $3\,12$, $4\,11$, $4\,12$, $11\,12$, and one checks that no three of them are pairwise non-adjacent, so $w(I) \le 1/2 + 2/4 = 1$. If $I$ contains $9$, the remaining candidates are $3$, $5$, $8$, $11$, $12$ with the edges $3\,5$, $3\,12$, $5\,12$, $8\,11$, $11\,12$, again with no independent triple; if $I$ contains $10$, they are $3$, $4$, $5$, $11$, $12$ with the edges $3\,5$, $3\,12$, $4\,11$, $4\,12$, $5\,12$, $11\,12$, again with no independent triple. Directly, the weights of the twenty-two maximal independent sets of Step 1 are """ + mis_w_tex + r""", all at most $1$, and a subset of an independent set weighs no more than the set. Now let $x$ be any fractional colouring. Then
$$\sum_I x_I \;\ge\; \sum_I x_I\, w(I) \;=\; \sum_v w_v \sum_{I \ni v} x_I \;\ge\; \sum_v w_v \;=\; \frac{13}{4}.$$
So $\chi_f(G) \ge 13/4$. In particular $\chi_f(G) > 3$, which also shows that $G$ has no proper $3$-colouring, so $\chi(G) = 4$.

Step 4: Upper bound $13/4$ from an explicit fractional colouring.
Take the independent sets $\{1,2,6,12\}$, $\{4,5,10\}$, $\{7,8,9,12\}$, $\{3,10,11\}$ with weight $1/2$ each, and $\{1,2,6,11\}$, $\{1,3,4,7\}$, $\{5,6,9,11\}$, $\{2,4,5,8\}$, $\{3,7,8,9\}$ with weight $1/4$ each. The total weight is $4 \cdot \frac12 + 5 \cdot \frac14 = \frac{13}{4}$. Each vertex is covered with total weight exactly $1$: vertex $1$ by $\{1,2,6,12\}$, $\{1,2,6,11\}$, $\{1,3,4,7\}$ ($\frac12 + \frac14 + \frac14$); vertex $2$ by $\{1,2,6,12\}$, $\{1,2,6,11\}$, $\{2,4,5,8\}$; vertex $3$ by $\{3,10,11\}$, $\{1,3,4,7\}$, $\{3,7,8,9\}$; vertex $4$ by $\{4,5,10\}$, $\{1,3,4,7\}$, $\{2,4,5,8\}$; vertex $5$ by $\{4,5,10\}$, $\{5,6,9,11\}$, $\{2,4,5,8\}$; vertex $6$ by $\{1,2,6,12\}$, $\{1,2,6,11\}$, $\{5,6,9,11\}$; vertex $7$ by $\{7,8,9,12\}$, $\{1,3,4,7\}$, $\{3,7,8,9\}$; vertex $8$ by $\{7,8,9,12\}$, $\{2,4,5,8\}$, $\{3,7,8,9\}$; vertex $9$ by $\{7,8,9,12\}$, $\{5,6,9,11\}$, $\{3,7,8,9\}$; vertex $10$ by $\{4,5,10\}$ and $\{3,10,11\}$ ($\frac12 + \frac12$); vertex $11$ by $\{3,10,11\}$, $\{1,2,6,11\}$, $\{5,6,9,11\}$; vertex $12$ by $\{1,2,6,12\}$ and $\{7,8,9,12\}$. Multiplying the weights by $4$ turns this into a $13$-fold list of independent sets, the four sets of weight $1/2$ taken twice and the five sets of weight $1/4$ once, in which every vertex appears exactly $4$ times: a $13{:}4$-colouring of $G$. Hence $\chi_f(G) \le 13/4$.

Step 5: Conclusion.
Steps 3 and 4 give $\chi_f(G) = 13/4$. The bound $3$ of Step 2 is not attained. The value is also not reached by colourings with fewer than four colours per vertex: the smallest $2$-fold colouring of $G$ uses $7$ colours and the smallest $3$-fold colouring uses $10$, so stopping at a $2$-fold or a $3$-fold colouring gives $7/2$ or $10/3$, and the $4$-fold colouring of Step 4 with $13$ colours is the first one whose ratio equals $\chi_f(G)$.

Answer: $13/4$."""
rubric = [
    dict(id="c1", description=r"Gives $13/4$ (or an exactly equivalent form such as $3.25$).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a fractional colouring of $G$ of total weight $13/4$: a list of independent sets with non-negative weights covering every vertex with total at least $1$ (for instance a $13{:}4$-colouring), with weights summing to $13/4$.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves the lower bound $\chi_f(G) \ge 13/4$ by a valid argument, for instance a vertex weighting of total $13/4$ under which every independent set weighs at most $1$ (such as $1/2$ on vertices $1$, $9$, $10$ and $1/4$ on vertices $2$, $3$, $4$, $5$, $8$, $11$, $12$), or an exact solution of the linear programme and its dual.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Determines the independence number $\alpha(G) = 4$ and the chromatic number $\chi(G) = 4$, so that $3 \le \chi_f(G) \le 4$.", points=1, isFinalAnswer=False),
]
wrong = ["3", "7/2", "10/3", "4"]
references = r"""Fractional colourings, fractional cliques and the linear programming duality between them (every fractional colouring weighs at least as much as every fractional clique, with equality at the optimum): L. Lovasz, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13 (1975), 383-390. The $k$-fold colourings whose ratios $k/d$ attain the fractional chromatic number: S. Stahl, $n$-tuple colorings and associated graphs, Journal of Combinatorial Theory Series B 20 (1976), 185-203. The uploaded file verification_notes.txt lists every independent set of the drawn graph, checks the fractional clique of weight $13/4$ against all of them and the fractional colouring of weight $13/4$ vertex by vertex, solves the linear programme exactly by a rational simplex and numerically by a second solver, and computes the $2$-fold and $3$-fold chromatic numbers ($7$ and $10$); the program is embedded with its output."""
necessity = "The graph is given only by the figure; the twenty-four edges are not listed in the text, and the fractional chromatic number depends on the exact edge set (moving a single edge changes the independent sets and with them both certificates)."
verify_field = "Sections 3 and 4 of verification_notes.txt give the two certificates: the vertex weighting of total 13/4 (1/2 on vertices 1, 9, 10 and 1/4 on vertices 2, 3, 4, 5, 8, 11, 12) with the weight of every maximal independent set listed, and the nine weighted independent sets of total 13/4 that cover every vertex exactly once. Section 5 solves the linear programme exactly by a rational simplex and numerically by HiGHS, both giving 13/4. Section 7 embeds the program verify_key.py with its full output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: fractional graph colouring (fractional chromatic number and linear programming duality)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original straight-line drawing of the graph)",
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
    assert len(question) >= 30 and len(solution) >= 50
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "ALL CHECKS PASSED" in out
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fractional chromatic number of the graph in the figure

Answer key: 13/4.

1. Edges (from the figure): 1-5, 1-8, 1-9, 1-10, 2-3, 2-7, 2-9, 2-10, 3-5, 3-6, 3-12, 4-6, 4-9, 4-11, 4-12, 5-7,
   5-12, 6-7, 6-8, 7-11, 8-10, 8-11, 9-10, 11-12. Twelve vertices, twenty-four edges, every vertex of degree 4.
2. Independent sets: all 4096 vertex subsets were tested; 113 are independent, 22 of them maximal (listed in the
   program output), the largest have 4 vertices. Triangles 1-8-10, 1-9-10, 2-9-10, 3-5-12, 4-11-12; no K4.
   So alpha = 4, omega = 3, n/alpha = 3, and chi = 4 (no proper 3-colouring by backtracking; the 4-colouring
   {{1,2,4}}, {{3,7,8,9}}, {{5,6,10,11}}, {{12}}). The graph is regular but not vertex-transitive (vertex 10 is in
   three triangles, vertex 6 in none), so n/alpha is only a lower bound.
3. Lower bound (fractional clique): weight 1/2 on vertices 1, 9, 10, weight 1/4 on vertices 2, 3, 4, 5, 8, 11, 12,
   weight 0 on 6 and 7; total 13/4. The program checks that every one of the 113 independent sets has weight at
   most 1 and prints the weight of each maximal one. Weak duality: for any fractional colouring x,
   sum_I x_I >= sum_I x_I w(I) = sum_v w_v sum_(I contains v) x_I >= sum_v w_v = 13/4. A hand proof of the
   "at most 1" claim is in Step 3 of the solution (case split on which vertex of the triangle 1, 9, 10 the set
   contains; the remaining weight-1/4 candidates contain no independent triple).
4. Upper bound (fractional colouring): {{1,2,6,12}}, {{4,5,10}}, {{7,8,9,12}}, {{3,10,11}} with weight 1/2 and
   {{1,2,6,11}}, {{1,3,4,7}}, {{5,6,9,11}}, {{2,4,5,8}}, {{3,7,8,9}} with weight 1/4; total 13/4; every vertex covered
   with total weight exactly 1 (printed vertex by vertex). Equivalently a 13:4-colouring (printed).
5. Two further solutions of the linear programme: the dual (maximum weight of a fractional clique) by an exact
   rational tableau simplex written in the program with the standard library, optimum 13/4; the primal over the
   22 maximal independent sets by scipy's HiGHS solver, optimum 3.2500000000.
6. Wrong routes, computed: n/alpha = 3; omega = 3; the best ratio |S|/alpha(G[S]) over all 4095 induced
   subgraphs is 3; chi = 4; no 6:2-colouring but a 7:2-colouring (best 2-fold weight 7/2); no 9:3-colouring but a
   10:3-colouring (best 3-fold weight 10/3).

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; needs only the standard library,
   scipy optional)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08: fractional chromatic number of a 12-vertex 4-regular graph", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
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
