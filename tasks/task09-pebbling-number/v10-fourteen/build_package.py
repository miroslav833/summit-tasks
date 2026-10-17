import json, zipfile, pathlib, textwrap, subprocess, sys, re
HERE = pathlib.Path(__file__).parent
SLUG = "graph-rooted-pebbling-number-fourteen-vertices"
question = r"""The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $20$ edges; the vertex drawn with a double circle is called $r$. A configuration of pebbles on $G$ assigns a non-negative integer number of pebbles to each vertex. A pebbling move removes two pebbles from a vertex and adds one pebble to a neighbour of that vertex; the second pebble is lost. The vertex $r$ is reachable from a configuration if there is a sequence of pebbling moves after which $r$ carries at least one pebble. The pebbling number of $G$ with target $r$, written $\pi(G, r)$, is the least integer $k$ such that every configuration with $k$ pebbles in total reaches $r$.

Find $\pi(G, r)$. Give a single integer."""
final_answer = "27"
variants = [r"$27$", r"$\pi(G, r) = 27$", "pebbling number 27"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $13$, $25$, $28$, $34$, $36$, $3\,10$, $4\,10$, $4\,11$, $58$, $59$, $68$, $6\,10$, $79$, $7\,12$, $8\,13$, $9\,12$, $10\,11$, $12\,14$, $13\,14$. The target is $r = 1$, with the two neighbours $2$ and $3$. The further neighbours of $2$ are $5$ and $8$; the further neighbours of $3$ are $4$, $6$ and $10$. The distances from $1$ are $1$ for $2$ and $3$, $2$ for $4$, $5$, $6$, $8$, $10$, $3$ for $9$, $11$, $13$, and $4$ for $7$, $12$, $14$, so the eccentricity of $1$ is $4$. The graph is planar and $2$-connected. On the right, the vertices $4$, $10$, $11$ form a triangle-shaped pocket with $11$ of degree $2$ at distance $3$; on the left, the part $L = \{7, 9, 12, 13, 14\}$ is joined to the rest of the graph only through the edges $9\,5$ and $13\,8$.

Step 2: The standard lower bounds give $16$ and $14$, and the usual pile constructions give $23$ and $26$.
Fifteen pebbles on the far vertex $7$ and nothing else deliver at most seven pebbles to distance $3$, three to distance $2$ and one to a neighbour of $1$, so $\pi(G, 1) \ge 2^{4} = 16$. One pebble on every vertex other than $1$ allows no move, so $\pi(G, 1) \ge 14$. A pile of fifteen on a far vertex with one pebble on each of a set of other vertices fails with at most $22$ pebbles, which suggests $23$. Two piles do better: fifteen on $7$, seven on $11$ and one pebble each on $12$, $13$ and $14$ is a failing configuration of $25$ pebbles, and no failing configuration with at most two piles has more, which suggests $26$. All of these are short of the answer.

Step 3: A configuration of $26$ pebbles from which $1$ cannot be reached.
Let $C$ be the configuration with fifteen pebbles on $7$, seven pebbles on $11$, three pebbles on $14$, one pebble on $13$ and no pebble elsewhere; it has $26$ pebbles. We claim that $1$ is not reachable from $C$.

Reduction. A move onto $1$ starts at $2$ or at $3$ with two pebbles there. Both start empty, so $1$ is reachable only if two pebbles arrive at $2$ (from $5$ or $8$) or two pebbles arrive at $3$ (from $4$, $6$ or $10$) in the course of the game.

The right pocket. The seven pebbles on $11$ allow three moves out of $11$, onto $4$ or $10$, and one pebble stays behind. Every move into $3$ costs two pebbles on $4$, $6$ or $10$, so these three pebbles bring at most one pebble to $3$, and whatever the pocket does, the pebbles that the pocket sends toward $1$ are worth at most one arrival at $3$. The only way for a second pebble to arrive at $3$ is through $6$, and a pebble reaches $6$ from the left only through $8$.

The left part. The fifteen pebbles on $7$ allow seven moves out of $7$, onto $9$ or $12$. Pebbles leave $L$ only through $9 \to 5$ and $13 \to 8$, each move costing two pebbles on $9$ or on $13$. The three pebbles on $14$ and the one on $13$ add one move: $14$ can send one pebble to $13$, which then makes one move onto $8$, or one pebble to $12$. Counting the moves, at most five pebbles ever enter $\{5, 8\}$ from $L$, and every pebble that goes on from $5$ or $8$ to $2$, or from $8$ through $6$ to $3$, costs two for one at each step. With at most five pebbles entering at distance $2$, split between $5$ and $8$, a second arrival at $2$ would need four pebbles at one of them, which the split prevents, and an arrival at $3$ through $6$ needs four pebbles at $8$ and leaves nothing for $2$. Pebbles sent back into $L$ or across to the pocket are lost at the same rate.

Certificate. The claim is proved by exhaustive enumeration: starting from $C$, every configuration that can be reached by pebbling moves is generated (there are $187\,805$ of them). None has a pebble on $1$, and none has two pebbles on $2$ or on $3$. A dynamic programme over the same configurations shows that over every move sequence at most one pebble ever arrives at $2$ and at most one at $3$. The enumeration and the programme are reproduced in the reference file. Therefore $\pi(G, 1) \ge 27$.

Step 4: Every configuration of $27$ pebbles reaches $1$.
Adding a pebble to a configuration never destroys reachability. For the target $1$ let $U_k$ be the set of configurations of $k$ pebbles with none on $1$ from which $1$ is not reachable; every member of $U_k$ is a member of $U_{k-1}$ with one pebble added, and a candidate belongs to $U_k$ exactly when no move from it lands on $1$ and every move from it leads into $U_{k-1}$. The recursion gives the sizes $1, 13, 89, 424, 1564, 4714, 11984, 26227, 50076, 84113, 124960, 165021, 195106, 208549, 203602, 183222, 153277, 119824, 87410, 58994, 36112, 19351, 8710, 3193, 925, 191, 20, 0$ for $k = 0, 1, \dots, 27$. So $U_{27}$ is empty and $\pi(G, 1) \le 27$. The $20$ members of $U_{26}$ all have seven pebbles on $11$ and nineteen pebbles in the left part $L$, in twelve different shapes: the configuration $C$; thirteen on $7$, five on $14$ and one on $12$; eleven on $7$, five on $14$ and three on $12$; nine on $7$, five on $12$ and five on $14$; seven on $7$, seven on $12$ and five on $14$; fifteen on $14$, three on $7$ and one on $9$; and so on. None of them has fewer than three piles. Two independent implementations of the recursion give the same sizes, a direct search over move sequences confirms that each of the $20$ configurations fails and that every configuration obtained from one of them by adding a pebble reaches $1$, and $60\,000$ random configurations of $25$ to $27$ pebbles give the same verdict by both methods. The reference file embeds the program with its output.

Why the pile constructions stop short. One pile of fifteen on a far vertex is worth a single pebble at a neighbour of $1$, and single pebbles elsewhere never combine with its output, so the one-pile pattern stops at $22$. Seven on $11$ is worth one pebble at $3$ and fifteen on $7$ one pebble at $2$, and with single pebbles on the three remaining vertices of $L$ one gets $25$. The twenty-sixth pebble can be added without creating a useful move only by turning the single pebbles of $L$ into a small second pile whose output is stranded: three on $14$ with one on $13$ produce one pebble on $8$ or $12$ and nothing more. Finding such a configuration is the step the pile patterns miss.

Step 5: Conclusion.
The rooted pebbling number is at least $27$ by Step 3 and at most $27$ by Step 4, so $\pi(G, r) = 27$.

Answer: $27$."""
rubric = [
    dict(id="c1", description=r"Gives $27$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a configuration of $26$ pebbles from which $r$ is not reachable (for instance fifteen pebbles on $7$, seven on $11$, three on $14$ and one on $13$) and gives a valid argument that $r$ is not reachable from it.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Shows by a valid argument (exhaustive, structural, or otherwise) that every configuration of $27$ pebbles reaches $r$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the bounds $\pi(G, r) \ge 2^{4} = 16$ (from the eccentricity of $r$) and $\pi(G, r) \ge n = 14$ and recognises that neither is tight.", points=1, isFinalAnswer=False),
]
wrong = ["26", "23", "16", "25", "28", "14"]
references = r"""Graph pebbling was introduced by F. R. K. Chung, Pebbling in hypercubes, SIAM Journal on Discrete Mathematics 2 (1989), 467-472, and is surveyed in G. Hurlbert, A survey of graph pebbling, Congressus Numerantium 139 (1999), 41-64. The reduction to the first moment a neighbour of the target holds two pebbles, and the fact that wasteful move sequences can be ignored, follow the No-Cycle Lemma of K. Milans and B. Clark, The complexity of graph pebbling, SIAM Journal on Discrete Mathematics 20 (2006), 769-798. For the bounds on graphs of small diameter: T. A. Clarke, R. A. Hochberg and G. H. Hurlbert, Pebbling in diameter two graphs and products of paths, Journal of Graph Theory 25 (1997), 119-128, and B. Bukh, Maximum pebbling number of graphs of diameter three, Journal of Graph Theory 52 (2006), 353-357. The uploaded file verification_notes.txt contains the two independent exact computations of the rooted pebbling number (the layer recursion over unreachable configurations in two implementations, and a direct search over move sequences for all maximal failing configurations, their extensions and 60,000 random configurations), the exhaustive enumeration of the 187,805 configurations reachable from the twenty-six-pebble configuration of Step 3, the move-counting programme, the template bounds, and the program that produces all of it with its output."""
necessity = "The graph and the target vertex are given only by the figure; the twenty edges are not listed in the text, and the answer depends on the exact edge set and on which vertex is the double-circled target (the failing configurations live on the far part at distance 4 from it and on the pocket at distance 3, and the two edges that join the far part to the rest decide how many pebbles are wasted)."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: graph pebbling (rooted pebbling number)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original straight-line drawing of the graph)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Sections 1 to 3 of verification_notes.txt give the graph, the trivial bounds, the twenty-six-pebble configuration (fifteen pebbles on 7, seven on 11, three on 14, one on 13, target 1) with the reduction argument, the exhaustive enumeration of the 187,805 configurations reachable from it, none with a pebble on 1, and the move count showing that at most one pebble ever arrives at 2 and at most one at 3; section 4 gives the two independent exact computations showing that every configuration of 27 pebbles reaches 1 (the layer recursion in two implementations and a direct search over move sequences for all 20 maximal failing configurations, their one-pebble extensions and 60,000 random configurations), and the template bounds; section 5 embeds the program verify_key.py with its full output."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    out = (HERE / "work" / "verify_key_output.txt").read_text()
    assert "ALL CHECKS PASSED: pi(G, 1) = 27." in out
    assert "configurations reachable from C = {7: 15, 11: 7, 14: 3, 13: 1}: 187805" in out
    assert "maximum number of pebbles arriving at 2: 1  at 3: 1" in out
    sizes = re.search(r"ROUTE A: layer sizes.*?: \[(.*?)\]", out).group(1).replace(" ", "")
    assert sizes == "1,13,89,424,1564,4714,11984,26227,50076,84113,124960,165021,195106,208549,203602,183222,153277,119824,87410,58994,36112,19351,8710,3193,925,191,20,0"
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: rooted pebbling number of the graph in the figure (target: the double-circled vertex 1)

Answer key: 27.

1. The graph (from the figure). Vertices 1 to 14, edges 1-2, 1-3, 2-5, 2-8, 3-4, 3-6, 3-10, 4-10, 4-11,
   5-8, 5-9, 6-8, 6-10, 7-9, 7-12, 8-13, 9-12, 10-11, 12-14, 13-14. Target r = 1, neighbours 2 and 3.
   Distances from 1: 1 for 2, 3; 2 for 4, 5, 6, 8, 10; 3 for 9, 11, 13; 4 for 7, 12, 14. Eccentricity of 1
   is 4. The graph is planar and 2-connected. Trivial lower bounds: 2^4 = 16 and n = 14. The left part
   L = {{7, 9, 12, 13, 14}} meets the rest only through the edges 9-5 and 13-8; the pocket {{4, 10, 11}}
   hangs off 3 and 6, with 11 of degree 2 at distance 3.

2. Lower bound 27: the configuration C with fifteen pebbles on 7, seven on 11, three on 14, one on 13
   (twenty-six pebbles) does not reach 1. Reduction (Step 3 of the solution): a pebble reaches 1 only
   from 2 or 3 holding two pebbles, so two pebbles must arrive at 2 (from 5 or 8) or at 3 (from 4, 6 or
   10). Certificate: breadth-first enumeration of every configuration reachable from C (187,805
   configurations, program section 5, certificate (iii)); none has a pebble on 1 and none has two pebbles
   on 2 or on 3. A dynamic programme over the same configurations gives the largest number of moves into
   each vertex over all move sequences: at most one pebble ever arrives at 2 and at most one at 3; at most
   five pebbles leave L, at most four leave 11 (counting re-entries). Structure: the pocket's pile of seven
   is worth one pebble at 3, the pile of fifteen on 7 is worth one pebble at 2, and the three on 14 with
   the one on 13 add a single stranded pebble on 8 or 12.

3. Why this configuration and not the pile patterns. The largest failing configurations with a single
   pile have 22 pebbles (fifteen on 7 or on 12 and single pebbles on seven other vertices), suggesting
   23; the largest with two piles have 25 (fifteen on 7, seven on 11, singles on 12, 13, 14, and four
   relatives), suggesting 26. The 20 failing configurations of 26 pebbles all have seven on 11 and nineteen
   pebbles in L in twelve shapes, every one with at least three piles; they are listed in the Route A
   output.

4. Upper bound 27: Route A (layer recursion over the sets U_k of unreachable configurations of k pebbles,
   integer-encoded, with the shortcut that two pebbles on a neighbour of 1 reach 1) gives the layer sizes
   1, 13, 89, 424, 1564, 4714, 11984, 26227, 50076, 84113, 124960, 165021, 195106, 208549, 203602, 183222,
   153277, 119824, 87410, 58994, 36112, 19351, 8710, 3193, 925, 191, 20, 0; U_27 is empty. Route B (the
   same recursion written independently with tuple-encoded configurations and without the shortcut) gives
   identical sizes. Certificate (i): a memoised depth-first search over move sequences confirms that each
   of the 20 configurations of 26 pebbles fails and that every configuration obtained by adding one pebble
   reaches 1. Certificate (ii): 20,000 random configurations of each size 25, 26, 27 (at most one pebble
   on each neighbour of 1) give the same verdict by direct search and by layer membership. Certificate
   (iv): the template bounds 22 (one pile plus singles), 25 (two piles) and 26 (three piles).

5. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only,
   about four minutes)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09 v10: rooted pebbling number of a 14-vertex graph (revision of SUM-MVBG0GO3)", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
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
