import json, zipfile, pathlib, textwrap, subprocess, sys
from fractions import Fraction as F
HERE = pathlib.Path(__file__).parent
SLUG = "fractional-chromatic-number-twenty-vertices"
question = r"""The figure shows a planar graph $G$ with $20$ vertices, labelled $1$ to $20$, and $40$ edges. Every vertex has degree $4$. An independent set of $G$ is a set of vertices no two of which are joined by an edge. A fractional colouring of $G$ gives each independent set $I$ a weight $x_I \ge 0$ in such a way that, for every vertex $v$, the weights of the independent sets that contain $v$ add up to at least $1$. The weight of the fractional colouring is $\sum_I x_I$, and the fractional chromatic number $\chi_f(G)$ is the smallest weight of a fractional colouring of $G$.

Find $\chi_f(G)$. Give the exact value as a fraction in lowest terms."""
final_answer = "35/11"
variants = [r"$35/11$", r"$\frac{35}{11}$", r"$\chi_f(G) = 35/11$", "3.1818"]
EDGES = [(1, 2), (1, 3), (1, 5), (1, 6), (2, 4), (2, 6), (2, 9), (3, 4), (3, 11), (3, 15), (4, 17), (4, 20), (5, 6), (5, 7), (5, 8), (6, 10), (7, 8), (7, 11), (7, 12), (8, 12), (8, 18), (9, 10), (9, 16), (9, 17), (10, 16), (10, 18), (11, 12), (11, 13), (12, 13), (13, 14), (13, 18), (14, 15), (14, 18), (14, 19), (15, 19), (15, 20), (16, 17), (16, 19), (17, 20), (19, 20)]
SEVEN = [[2, 3, 5, 10, 12, 14, 17], [2, 3, 5, 10, 12, 14, 20], [2, 3, 5, 10, 12, 17, 19], [2, 3, 5, 10, 13, 17, 19], [2, 3, 5, 12, 14, 16, 20], [2, 3, 5, 12, 16, 18, 20], [2, 3, 5, 12, 17, 18, 19], [2, 3, 7, 10, 13, 17, 19], [2, 3, 8, 10, 13, 17, 19]]
COLOURING = [([1, 7, 10, 13, 15, 17], F(5, 11)), ([1, 8, 10, 13, 17, 19], F(2, 11)), ([1, 8, 10, 11, 14, 20], F(2, 11)), ([1, 4, 9, 11, 15, 18], F(2, 11)), ([2, 3, 5, 12, 17, 18, 19], F(2, 11)), ([2, 3, 5, 12, 16, 18, 20], F(2, 11)), ([2, 3, 5, 12, 14, 16, 20], F(4, 11)), ([2, 3, 7, 10, 13, 17, 19], F(2, 11)), ([2, 5, 12, 15, 16, 18], F(1, 11)), ([3, 6, 7, 9, 18, 19], F(1, 11)), ([4, 5, 9, 12, 18, 19], F(2, 11)), ([6, 8, 9, 11, 14, 20], F(2, 11)), ([6, 8, 11, 14, 16, 20], F(1, 11)), ([4, 6, 8, 9, 11, 19], F(2, 11)), ([4, 6, 8, 9, 11, 14], F(2, 11)), ([4, 6, 7, 15, 16, 18], F(1, 11)), ([4, 6, 7, 13, 15, 16], F(2, 11))]
LETTERS = "ABCDEFGHIJKLMNOPQ"
def tex_set(S): return "$\\{" + ",".join(map(str, S)) + "\\}$"
def tex_frac(x): return f"$\\tfrac{{{x.numerator}}}{{{x.denominator}}}$" if x.denominator != 1 else f"${x.numerator}$"
edges_tex = ", ".join(f"${u}\\,{v}$" for u, v in EDGES)
seven_tex = ", ".join(tex_set(S) for S in SEVEN)
colouring_tex = "; ".join(f"${L}$ = {tex_set(S)} with weight {tex_frac(x)}" for L, (S, x) in zip(LETTERS, COLOURING))
cover_parts = []
for v in range(1, 21):
    idx = [L for L, (S, x) in zip(LETTERS, COLOURING) if v in S]
    tot = sum(x for S, x in COLOURING if v in S); assert tot == 1
    cover_parts.append(f"${v}$: ${', '.join(idx)}$")
cover_tex = "; ".join(cover_parts)
solution = r"""Step 1: Read the graph off the figure.
The edges are """ + edges_tex + r""". Every vertex has degree $4$. The triangles are $1\,2\,6$, $1\,5\,6$, $4\,17\,20$, $5\,7\,8$, $7\,8\,12$, $7\,11\,12$, $9\,10\,16$, $9\,16\,17$, $11\,12\,13$, $13\,14\,18$, $14\,15\,19$ and $15\,19\,20$, and there is no $K_4$, so the clique number is $\omega(G) = 3$. The graph has $2455$ non-empty independent sets, $212$ of them maximal (they are listed in the verification notes). The largest have seven vertices, so the independence number is $\alpha(G) = 7$, and the nine independent sets of size $7$ are """ + seven_tex + r""". Each of them contains the vertices $2$ and $3$ and exactly one of $17$ and $20$.

Step 2: The bounds that come first, and why they do not settle the question.
A fractional colouring $x$ satisfies $\sum_{I \ni v} x_I \ge 1$ for every vertex $v$. Summing over the three vertices of a triangle, and using that an independent set contains at most one of them, gives $\sum_I x_I \ge 3 = \omega(G)$. Summing over all twenty vertices gives $\sum_I |I|\, x_I \ge 20$, and since $|I| \le 7$ this is $\sum_I x_I \ge 20/7 = n/\alpha(G)$. For a vertex-transitive graph the bound $n/\alpha$ is exact, but $G$ is only regular: its automorphism group is trivial (vertex $3$ lies in no triangle and vertex $7$ in three, for instance), so the identity $\chi_f(G) = n/\alpha(G)$ is not available. The same summation over the nineteen vertices other than $2$ gives more, because every independent set of $G - 2$ has at most six vertices (the nine sets of size $7$ all contain $2$): $\chi_f(G) \ge \chi_f(G - 2) \ge 19/6$, and the same holds for $G - 3$. From above, the colour classes $\{1,4,7,9,13,15\}$, $\{2,3,5,10,12,14,17\}$, $\{6,8,11,16,20\}$, $\{18,19\}$ form a proper $4$-colouring, which is a fractional colouring of weight $4$. So far $19/6 \le \chi_f(G) \le 4$.

Step 3: Lower bound $35/11$ from a fractional clique.
Let $L = \{2, 3, 4, 17, 20\}$. Give each vertex of $L$ the weight $w_v = 1/11$ and each of the other fifteen vertices the weight $w_v = 2/11$. The total is $5/11 + 30/11 = 35/11$. For an independent set $I$ the weight is $w(I) = \sum_{v \in I} w_v = (2|I| - |I \cap L|)/11$, and the claim is that $w(I) \le 1$ for every independent set. If $|I| \le 5$ then $w(I) \le 10/11$. If $|I| = 6$ then $w(I) \le 1$ exactly when $I$ meets $L$, and every independent set of six vertices does meet $L$: the fifteen vertices outside $L$ induce a subgraph with independence number $5$ (the enumeration in the verification notes lists all $179$ independent sets of size $6$, each containing a vertex of $L$; $72$ of them contain exactly one and have weight exactly $1$). If $|I| = 7$ then $I$ is one of the nine sets of Step 1, each of which contains $2$, $3$ and one of $17$, $20$, so $|I \cap L| = 3$ and $w(I) = (14 - 3)/11 = 1$. Now let $x$ be any fractional colouring. Then
$$\sum_I x_I \;\ge\; \sum_I x_I\, w(I) \;=\; \sum_v w_v \sum_{I \ni v} x_I \;\ge\; \sum_v w_v \;=\; \frac{35}{11}.$$
So $\chi_f(G) \ge 35/11$, which is strictly more than the bound $19/6$ of Step 2.

Step 4: Upper bound $35/11$ from an explicit fractional colouring.
Take the seventeen independent sets """ + colouring_tex + r""". Each set is independent (no two of its vertices appear together in the edge list of Step 1), and the weights add up to $(5 + 2 + 2 + 2 + 2 + 2 + 4 + 2 + 1 + 1 + 2 + 2 + 1 + 2 + 2 + 1 + 2)/11 = 35/11$. Every vertex is covered with total weight exactly $1$; the sets containing each vertex are """ + cover_tex + r""", and in each case the listed weights sum to $11/11$. Multiplying all weights by $11$ turns the list into $35$ independent sets (set $A$ five times, set $G$ four times, the sets with weight $2/11$ twice, the sets with weight $1/11$ once) in which every vertex appears exactly $11$ times: a $35{:}11$-colouring of $G$. Hence $\chi_f(G) \le 35/11$.

Step 5: Conclusion.
Steps 3 and 4 give $\chi_f(G) = 35/11$. None of the bounds of Step 2 is attained: $20/7$, $3$ and $19/6$ are all smaller, and $4$ is larger. A $2$-fold colouring needs $7$ colours (there is no $6{:}2$-colouring, by the search in the verification notes), so stopping at a $2$-fold colouring gives $7/2$; the first $k$-fold colouring whose ratio equals $\chi_f(G)$ is the $35{:}11$-colouring of Step 4.

Answer: $35/11$."""
rubric = [
    dict(id="c1", description=r"Gives $35/11$ (or an exactly equivalent form).", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a fractional colouring of $G$ of total weight $35/11$: a list of independent sets with non-negative weights covering every vertex with total at least $1$ (for instance a $35{:}11$-colouring), with weights summing to $35/11$.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Proves the lower bound $\chi_f(G) \ge 35/11$ by a valid argument, for instance a vertex weighting of total $35/11$ under which every independent set weighs at most $1$ (such as $1/11$ on vertices $2$, $3$, $4$, $17$, $20$ and $2/11$ on the other fifteen vertices), or an exact solution of the linear programme and its dual.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"Determines the independence number $\alpha(G) = 7$ and the chromatic number $\chi(G) = 4$, so that $20/7 \le \chi_f(G) \le 4$.", points=1, isFinalAnswer=False),
]
wrong = ["20/7", "3", "19/6", "4", "7/2"]
references = r"""Fractional colourings, fractional cliques and the linear programming duality between them (every fractional colouring weighs at least as much as every fractional clique, with equality at the optimum): L. Lovasz, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13 (1975), 383-390. The $k$-fold colourings whose ratios $k/d$ attain the fractional chromatic number: S. Stahl, $n$-tuple colorings and associated graphs, Journal of Combinatorial Theory Series B 20 (1976), 185-203. The uploaded file verification_notes.txt enumerates every independent set of the drawn graph (2455 non-empty, 212 maximal, nine of size 7), checks the fractional clique of weight $35/11$ against all of them and the fractional colouring of weight $35/11$ vertex by vertex, solves the linear programme exactly by a rational simplex and numerically by a second solver, computes the best induced-subgraph ratio ($19/6$) over all induced subgraphs, and shows that no $6{:}2$-colouring exists; the program is embedded with its output."""
necessity = "The graph is given only by the figure; the forty edges are not listed in the text, and the fractional chromatic number depends on the exact edge set (moving a single edge changes the independent sets and with them both certificates)."
verify_field = "Sections 3 and 4 of verification_notes.txt give the two certificates: the vertex weighting of total 35/11 (1/11 on vertices 2, 3, 4, 17, 20 and 2/11 on the other fifteen vertices) with the weight of every maximal independent set listed and the two facts behind it (every independent set of six vertices meets {2, 3, 4, 17, 20}; each of the nine independent sets of seven vertices contains three of them), and the seventeen weighted independent sets of total 35/11 that cover every vertex exactly once. Section 5 solves the linear programme exactly by a rational simplex and numerically by HiGHS, both giving 35/11. Section 6 computes the best induced-subgraph ratio 19/6 over all induced subgraphs. Section 7 embeds the program verify_key.py with its full output."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: fractional graph colouring (fractional chromatic number and linear programming duality)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original planar straight-line drawing of the graph from a Tutte embedding)",
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
    assert len(question) >= 30 and len(solution) >= 50 and len(solution) <= 30000
    # every set in Step 4 independent, total 35/11
    adj = {}
    for u, v in EDGES: adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    for S, x in COLOURING: assert all(b not in adj[a] for a in S for b in S), S
    assert sum(x for S, x in COLOURING) == F(35, 11)
    for S in SEVEN: assert all(b not in adj[a] for a in S for b in S) and len(S) == 7
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "ALL CHECKS PASSED" in out
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: fractional chromatic number of the graph in the figure

Answer key: 35/11.

1. Edges (from the figure): {", ".join(f"{u}-{v}" for u, v in EDGES)}.
   Twenty vertices, forty edges, every vertex of degree 4, planar (the figure is a planar straight-line drawing).
2. Independent sets: enumerated by backtracking; 2455 non-empty independent sets (20 of size 1, 150 of size 2, 528 of
   size 3, 895 of size 4, 674 of size 5, 179 of size 6, 9 of size 7), 212 of them maximal (listed in the program output).
   Twelve triangles, no K4. So alpha = 7, omega = 3, n/alpha = 20/7, and chi = 4 (no proper 3-colouring by
   backtracking; the 4-colouring {{1,4,7,9,13,15}}, {{2,3,5,10,12,14,17}}, {{6,8,11,16,20}}, {{18,19}}). The graph is
   regular but not vertex-transitive (trivial automorphism group; vertex 3 is in no triangle, vertex 7 in three), so
   n/alpha is only a lower bound.
3. Lower bound (fractional clique): weight 1/11 on L = {{2, 3, 4, 17, 20}}, weight 2/11 on the other fifteen vertices;
   total 35/11. The weight of an independent set I is (2|I| - |I meets L|)/11, so the claim "every independent set
   has weight at most 1" reduces to: every independent 6-set meets L (true: the fifteen vertices outside L have
   independence number 5; all 179 independent 6-sets were checked), and every independent 7-set contains at least
   three vertices of L (true: each of the nine contains 2, 3 and one of 17, 20). The program checks the weight of
   every one of the 2455 independent sets directly and prints the weight of each maximal one. Weak duality: for any
   fractional colouring x, sum_I x_I >= sum_I x_I w(I) = sum_v w_v sum_(I contains v) x_I >= sum_v w_v = 35/11.
4. Upper bound (fractional colouring): seventeen independent sets with weights k/11 (listed in Step 4 of the solution
   and in the program); total 35/11; every vertex covered with total weight exactly 1 (printed vertex by vertex).
   Equivalently a 35:11-colouring (printed).
5. Two further solutions of the linear programme: the dual (maximum weight of a fractional clique) by an exact
   rational tableau simplex written in the program with the standard library, optimum 35/11; the primal over the
   212 maximal independent sets by scipy's HiGHS solver, optimum 3.1818181818.
6. Wrong routes, computed: n/alpha = 20/7; omega = 3; the best ratio |S|/alpha(G[S]) over all 2^20 - 1 induced
   subgraphs is 19/6 (delete vertex 2 or vertex 3); chi = 4; no 6:2-colouring but a 7:2-colouring, so the best
   2-fold colouring has weight 7/2.

7. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; needs only the standard library,
   numpy and scipy optional; running time about one minute)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written")
def build_readme(screen):
    lines = ["# task08 (revision): fractional chromatic number of a 20-vertex planar 4-regular graph", "",
             "Revision of Summit item SUM-MVBCQZWW (the 12-vertex version came back too easy: the weaker model solved it twice out of three). The 12-vertex package is kept in work/v1/.", "",
             "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", verify_field, "", "## Screen", "", screen]
    (HERE / "README.md").write_text("\n".join(lines) + "\n"); print("README.md written")
def build_paste():
    lines = ["# Paste sheet for revising SUM-MVBCQZWW on the platform (edit field by field, no zip re-import)", "",
             "Replace every field below with the text given. Upload image.png as the new image and reference.txt as the new References file (display name verification_notes.txt). Subdomain, modality, task type and answer type stay as they are.", "",
             "## Image source", "", task["task"]["imageCreationTool"], "", "## Why the image is necessary", "", necessity, "",
             "## Question text", "", question, "", "## Correct answer", "", final_answer, "", "## Also accepted", ""]
    lines += [f"- {v}" for v in variants]
    lines += ["", "## Answer precision", "", "Not set / no precision stated (exact fraction).", "", "## Solution", "", solution, "", "## Rubric (10 points, c1 is the final-answer criterion)", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "## Common wrong answers", ""] + [f"- {w}" for w in wrong]
    lines += ["", "## References text", "", references, "", "## Verify box (where to find or verify the answer)", "", verify_field, ""]
    (HERE / "paste-for-edit.md").write_text("\n".join(lines)); print("paste-for-edit.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    screen = (HERE / "work" / "screen.md").read_text() if (HERE / "work" / "screen.md").exists() else "(filled in after the screen)"
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(screen); build_paste(); build_zip()
