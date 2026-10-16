import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-rooted-pebbling-number-thirteen-vertices"
question = r"""The figure shows a graph $G$ with $13$ vertices, labelled $1$ to $13$, and $19$ edges; the vertex drawn with a double circle is called $r$. A configuration of pebbles on $G$ assigns a non-negative integer number of pebbles to each vertex. A pebbling move removes two pebbles from a vertex and adds one pebble to a neighbour of that vertex; the second pebble is lost. The vertex $r$ is reachable from a configuration if there is a sequence of pebbling moves after which $r$ carries at least one pebble. The pebbling number of $G$ with target $r$, written $\pi(G, r)$, is the least integer $k$ such that every configuration with $k$ pebbles in total reaches $r$.

Find $\pi(G, r)$. Give a single integer."""
final_answer = "25"
variants = [r"$25$", r"$\pi(G, r) = 25$", "pebbling number 25"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $13$, $24$, $35$, $45$, $47$, $48$, $56$, $58$, $69$, $78$, $7\,10$, $7\,12$, $8\,11$, $8\,12$, $9\,11$, $10\,12$, $10\,13$, $12\,13$. The target is $r = 9$, with the two neighbours $6$ and $11$. Vertex $6$ has the single further neighbour $5$, vertex $11$ the single further neighbour $8$. The distances from $9$ are $1$ for $6$ and $11$, $2$ for $5$ and $8$, $3$ for $3$, $4$, $7$, $12$, and $4$ for $1$, $2$, $10$, $13$, so the eccentricity of $9$ is $4$. The graph is planar and $2$-connected. Two parts hang off the middle $M = \{4, 5, 7, 8\}$: the path $2\,1\,3$ (vertex $1$ far, joined to $M$ through $2\,4$ and $3\,5$) and the triangle $10\,12\,13$ with the edge $10\,12$ (vertex $13$ far, joined to $M$ through $10\,7$, $12\,7$ and $12\,8$).

Step 2: The standard lower bounds give $16$ and $13$.
Fifteen pebbles on the far vertex $1$ and nothing else deliver at most $7$ pebbles to the next vertex, $3$ to the next and $1$ to a neighbour of $9$, so $\pi(G, 9) \ge 2^{4} = 16$. One pebble on every vertex other than $9$ allows no move, so $\pi(G, 9) \ge 13$. Both are far from the answer. The configurations built from one pile of $15$ and single pebbles stop at $21$ pebbles (Step 4), so the answer $22$ that this pattern suggests is also short.

Step 3: A configuration of $24$ pebbles from which $9$ cannot be reached.
Let $C$ be the configuration with eleven pebbles on $1$, eleven pebbles on $13$, one pebble on $2$, one pebble on $10$ and no pebble elsewhere; it has $24$ pebbles. We claim that $9$ is not reachable from $C$.

Reduction. A move onto $9$ starts at $6$ or $11$ with two pebbles there. Both start empty, and the only neighbour of $6$ other than $9$ is $5$, the only neighbour of $11$ other than $9$ is $8$. So if $9$ is reachable, then at the first moment at which $6$ or $11$ holds two pebbles, both of its pebbles were delivered by moves from $5$, respectively from $8$, and up to that moment no move has started at $6$, $9$ or $11$. Hence $9$ is reachable from $C$ only if, in the game played on the other ten vertices, vertex $5$ can make two moves to $6$ or vertex $8$ can make two moves to $11$; since $5$ and $8$ start empty, this needs four pebbles to arrive at $5$ or four pebbles to arrive at $8$ over the course of the game, counting only pebbles that are then spent on the moves toward $9$.

Why this fails for $C$. Every pebble starts in one of the two far parts. The eleven pebbles on $1$ can leave $1$ only by moves to $2$ or $3$, at most five of them in total, and the one pebble on $2$ can only be used as a partner for a pebble arriving from $1$. A pebble that reaches the middle from this part through $2 \to 4$ or $3 \to 5$ costs two pebbles on $2$ or $3$, that is four pebbles on $1$ (three for the first move through $2$, where the single pebble helps). So the part $\{1, 2, 3\}$ sends at most three pebbles into the middle, and the same holds for the part $\{10, 12, 13\}$ with its eleven pebbles on $13$ and single pebble on $10$. A pebble that reaches $5$ or $8$ from $4$ or $7$ costs two pebbles there, and each of the two parts can bring at most one of its three pebbles directly to $5$ (through $3$) or to $8$ (through $12$) while still sending two to $4$ or $7$. Pebbles that cross the middle to the other side, or that are sent back into a far part, are lost at the rate of two for one. Adding up, neither $5$ nor $8$ can receive the four pebbles that two moves toward $9$ would consume: the two piles are odd, each loses one pebble at every level, and the leftovers of the two parts cannot be combined, because the parts are joined only through the middle.

Certificate. The claim is proved by exhaustive enumeration: starting from $C$, every configuration that can be reached by pebbling moves is generated (there are $61\,608$ of them). None has a pebble on $9$, and none has two pebbles on $6$ or on $11$; the largest numbers of pebbles ever present on $5$ and on $8$ are $3$ and $3$. The enumeration is reproduced by the program in the reference file. Therefore $\pi(G, 9) \ge 25$.

Step 4: Every configuration of $25$ pebbles reaches $9$.
Adding a pebble to a configuration never destroys reachability. For the target $9$ let $U_k$ be the set of configurations of $k$ pebbles with none on $9$ from which $9$ is not reachable; every member of $U_k$ is a member of $U_{k-1}$ with one pebble added, and a candidate belongs to $U_k$ exactly when no move from it lands on $9$ and every move from it leads into $U_{k-1}$. The recursion gives the sizes $1, 12, 76, 338, 1179, 3401, 8337, 17621, 32394, 52170, 74189, 94079, 107523, 111542, 105278, 90499, 70662, 49653, 30973, 16824, 7746, 2930, 893, 210, 28, 0$ for $k = 0, 1, \dots, 25$. So $U_{25}$ is empty and $\pi(G, 9) \le 25$. The $28$ members of $U_{24}$ all have eleven, ten or nine pebbles on $1$ and the rest spread over $2$, $4$, $10$, $13$ and $7$; the configuration $C$ is one of them, and so are, for instance, nine on $1$, three on $2$, nine on $13$ and three on $10$, or eleven on $1$, one on $2$, five on $10$ and seven on $13$. Two independent implementations of the recursion give the same sizes, a direct search over move sequences confirms that each of the $28$ configurations fails and that every configuration obtained from one of them by adding a pebble reaches $9$, and $60\,000$ random configurations of $23$ to $25$ pebbles give the same verdict by both methods. The reference file embeds the program with its output.

The largest failing configurations with only one pile have $21$ pebbles, for example fifteen on $1$ and one each on $2$, $7$, $8$, $10$, $12$, $13$. Two odd piles, one in each far part, waste three more pebbles than one pile, because each pile loses its odd pebble at every level and the single pebbles on $2$ and $10$ are stranded.

Step 5: Conclusion.
The rooted pebbling number is at least $25$ by Step 3 and at most $25$ by Step 4, so $\pi(G, r) = 25$.

Answer: $25$."""
rubric = [
    dict(id="c1", description=r"Gives $25$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a configuration of $24$ pebbles from which $r$ is not reachable (for instance eleven pebbles on $1$, eleven on $13$, one on $2$ and one on $10$) and gives a valid argument that $r$ is not reachable from it.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Shows by a valid argument (exhaustive, structural, or otherwise) that every configuration of $25$ pebbles reaches $r$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the bounds $\pi(G, r) \ge 2^{4} = 16$ (from the eccentricity of $r$) and $\pi(G, r) \ge n = 13$ and recognises that neither is tight.", points=1, isFinalAnswer=False),
]
wrong = ["22", "16", "21", "24", "23", "13"]
references = r"""Graph pebbling was introduced by F. R. K. Chung, Pebbling in hypercubes, SIAM Journal on Discrete Mathematics 2 (1989), 467-472, and is surveyed in G. Hurlbert, A survey of graph pebbling, Congressus Numerantium 139 (1999), 41-64. The reduction to the first moment a neighbour of the target holds two pebbles, and the fact that wasteful move sequences can be ignored, follow the No-Cycle Lemma of K. Milans and B. Clark, The complexity of graph pebbling, SIAM Journal on Discrete Mathematics 20 (2006), 769-798. For the bounds on graphs of small diameter: T. A. Clarke, R. A. Hochberg and G. H. Hurlbert, Pebbling in diameter two graphs and products of paths, Journal of Graph Theory 25 (1997), 119-128, and B. Bukh, Maximum pebbling number of graphs of diameter three, Journal of Graph Theory 52 (2006), 353-357. The uploaded file verification_notes.txt contains the two independent exact computations of the rooted pebbling number (the layer recursion over unreachable configurations in two implementations, and a direct search over move sequences for all maximal failing configurations, their extensions and 60,000 random configurations), the exhaustive enumeration of the 61,608 configurations reachable from the twenty-four-pebble configuration of Step 3, the template bounds, and the program that produces all of it with its output."""
necessity = "The graph and the target vertex are given only by the figure; the nineteen edges are not listed in the text, and the answer depends on the exact edge set and on which vertex is the double-circled target (the failing configurations live on the two far parts at distance 4 from it, and the two routes into the middle decide how many pebbles are wasted)."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: graph pebbling (rooted pebbling number)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original straight-line drawing of the graph)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Sections 1 to 3 of verification_notes.txt give the graph, the trivial bounds, the twenty-four-pebble configuration (eleven pebbles on 1, eleven on 13, one on 2, one on 10, target 9) with the reduction argument and the exhaustive enumeration of the 61,608 configurations reachable from it, none with a pebble on 9; section 4 gives the two independent exact computations showing that every configuration of 25 pebbles reaches 9 (the layer recursion in two implementations and a direct search over move sequences for all 28 maximal failing configurations, their 311 one-pebble extensions and 60,000 random configurations), and the template bounds; section 5 embeds the program verify_key.py with its full output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: rooted pebbling number of the graph in the figure (target: the double-circled vertex 9)

Answer key: 25.

1. The graph (from the figure). Vertices 1 to 13, edges 1-2, 1-3, 2-4, 3-5, 4-5, 4-7, 4-8, 5-6, 5-8, 6-9,
   7-8, 7-10, 7-12, 8-11, 8-12, 9-11, 10-12, 10-13, 12-13. Target r = 9, neighbours 6 and 11. Distances
   from 9: 1 for 6, 11; 2 for 5, 8; 3 for 3, 4, 7, 12; 4 for 1, 2, 10, 13. Eccentricity of 9 is 4. The graph
   is planar and 2-connected. Trivial lower bounds: 2^4 = 16 and n = 13.

2. Lower bound 25: the configuration C with eleven pebbles on 1, eleven on 13, one on 2, one on 10
   (twenty-four pebbles) does not reach 9. Reduction (Step 3 of the solution): a pebble reaches 9 only
   from 6 or 11 holding two pebbles, which must both come from 5 (for 6) or from 8 (for 11), so 9 is
   reachable only if 5 makes two moves to 6 or 8 makes two moves to 11. Certificate: breadth-first
   enumeration of every configuration reachable from C (61,608 configurations, program section 5,
   certificate (iii)); none has a pebble on 9, none has two pebbles on 6 or 11, and the largest numbers of
   pebbles ever present on 5 and 8 are 3 and 3. Structure: each odd pile of eleven loses one pebble at
   every level, the single pebbles on 2 and 10 are stranded, and the two far parts {{1,2,3}} and
   {{10,12,13}} are joined only through the middle {{4,5,7,8}}, so their leftovers cannot be combined.

3. Why this configuration and not the textbook one. The largest failing configurations with a single
   pile have 21 pebbles (fifteen on 1 and single pebbles on 2, 7, 8, 10, 12, 13, for instance), so the
   usual pattern suggests 22. The 28 failing configurations of 24 pebbles all use two odd piles, one in
   each far part (eleven and eleven, nine and nine with three and three, eleven with five and seven, and
   so on); they are listed in the Route A output.

4. Upper bound 25: Route A (layer recursion over the sets U_k of unreachable configurations of k pebbles,
   integer-encoded, with the shortcut that two pebbles on a neighbour of 9 reach 9) gives the layer sizes
   1, 12, 76, 338, 1179, 3401, 8337, 17621, 32394, 52170, 74189, 94079, 107523, 111542, 105278, 90499,
   70662, 49653, 30973, 16824, 7746, 2930, 893, 210, 28, 0; U_25 is empty. Route B (the same recursion
   written independently with tuple-encoded configurations and without the shortcut) gives identical
   sizes. Certificate (i): a memoised depth-first search over move sequences confirms that each of the 28
   configurations of 24 pebbles fails and that all 311 configurations obtained by adding one pebble reach
   9. Certificate (ii): 20,000 random configurations of each size 23, 24, 25 (at most one pebble on each
   neighbour of 9) give the same verdict by direct search and by layer membership. Certificate (iv): the
   template bounds 21 (one pile plus singles) and 24 (two piles).

5. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only,
   about five minutes)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v2: rooted pebbling number of a 13-vertex graph (revision of SUM-MVBG0GO3)", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
             "## Question", "", question, "", "## Answer", "", final_answer, "", "Also accepted: " + ", ".join(variants), "", "## Image necessity", "", necessity, "", "## Solution", "", solution, "", "## Rubric", ""]
    for c in rubric: lines.append(f"- {c['id']} ({c['points']} pts{', final answer' if c['isFinalAnswer'] else ''}): {c['description']}")
    lines += ["", "Common wrong answers: " + ", ".join(wrong), "", "## References box", "", references, "",
              "## Verify field", "", VERIFY_FIELD, "", "## Screen", "", "(filled in after the screen)"]
    (HERE / "README.md").write_text("\n".join(lines)); print("README.md written")
def build_zip():
    with zipfile.ZipFile(HERE / f"{SLUG}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("task.json", "image.png", "reference.txt"): z.write(HERE / f, f)
    print("zip written")
if __name__ == "__main__":
    check(); (HERE / "task.json").write_text(json.dumps(task, indent=2, ensure_ascii=False)); build_reference(); build_readme(); build_zip()
