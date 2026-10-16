import json, zipfile, pathlib, textwrap, subprocess, sys
HERE = pathlib.Path(__file__).parent
SLUG = "graph-rooted-pebbling-number-ten-vertices"
question = r"""The figure shows a graph $G$ with $10$ vertices, labelled $1$ to $10$, and $14$ edges; the vertex drawn with a double circle is called $r$. A configuration of pebbles on $G$ assigns a non-negative integer number of pebbles to each vertex. A pebbling move removes two pebbles from a vertex and adds one pebble to a neighbour of that vertex; the second pebble is lost. The vertex $r$ is reachable from a configuration if there is a sequence of pebbling moves after which $r$ carries at least one pebble. The pebbling number of $G$ with target $r$, written $\pi(G, r)$, is the least integer $k$ such that every configuration with $k$ pebbles in total reaches $r$.

Find $\pi(G, r)$. Give a single integer."""
final_answer = "13"
variants = [r"$13$", r"$\pi(G, r) = 13$", "pebbling number 13"]
solution = r"""Step 1: Read the graph off the figure.
The edges are $12$, $13$, $16$, $23$, $28$, $35$, $46$, $47$, $57$, $67$, $69$, $78$, $8\,10$, $9\,10$. Vertices $6$ and $7$ have degree $4$, vertices $1$, $2$, $3$, $8$ have degree $3$, vertices $4$, $5$, $9$, $10$ have degree $2$. The graph is $2$-connected and has diameter $3$; the vertices $6$, $7$, $8$ have eccentricity $2$ and all others have eccentricity $3$. Vertices $9$ and $10$ are adjacent vertices of degree $2$, with the other neighbours $6$ and $8$ respectively. The target $r$ is the vertex $3$, with neighbours $1$, $2$, $5$; the vertices $6$, $7$, $8$ are at distance $2$ from it and $4$, $9$, $10$ at distance $3$.

Step 2: The two standard lower bounds give $10$ and $8$.
One pebble on every vertex except $3$ leaves no move at all, so $\pi(G, 3) \ge n = 10$. Seven pebbles on a vertex at distance $3$ from $3$ and no other pebble deliver at most one pebble to a neighbour of $3$, so $\pi(G, 3) \ge 2^{3} = 8$. Both bounds are short of the answer, and so are the configurations of $11$ pebbles built from one pile of seven and single pebbles (Step 4).

Step 3: A configuration of $12$ pebbles from which vertex $3$ cannot be reached.
Let $C$ be the configuration with five pebbles on $9$, five pebbles on $10$, one pebble on $4$, one pebble on $7$ and no pebble elsewhere; it has $12$ pebbles. The neighbours of $3$ are $1$, $2$ and $5$. Outside the set $\{1,2,3,5\}$, vertex $1$ has the single neighbour $6$, vertex $2$ has the single neighbour $8$, and vertex $5$ has the single neighbour $7$.

Suppose that $3$ is reachable from $C$. By the No-Cycle Lemma (Milans and Clark, 2006) there is a sequence of moves from $C$ that reaches $3$ and whose move digraph $D$, with an arc $a \to b$ whenever some move from $a$ to $b$ occurs, has no directed cycle. The last move puts a pebble on $3$ from a neighbour that holds two pebbles, so some vertex of $\{1,2,5\}$ holds two pebbles at some moment; let $u$ be the first such vertex and let $P$ be the part of the sequence up to that moment. During $P$ no vertex of $\{1,2,3,5\}$ holds two pebbles, so no move of $P$ starts there, and both pebbles on $u$ were moved onto $u$ from the vertex $x$ with $x = 6$ for $u = 1$, $x = 8$ for $u = 2$, $x = 7$ for $u = 5$. Every move of $P$ starts in $R = \{4,6,7,8,9,10\}$. Write $m(a,b)$ for the number of moves from $a$ to $b$ in $P$, and $a(v)$ for the number of pebbles that arrive at $v$ during $P$. A vertex that starts with $c(v)$ pebbles and receives $a(v)$ pebbles makes at most $\lfloor (c(v) + a(v))/2 \rfloor$ moves. Hence $m(6,1) \ge 2$ needs $a(6) \ge 4$, $m(8,2) \ge 2$ needs $a(8) \ge 4$, and $m(7,5) \ge 2$ needs $a(7) \ge 3$, because $6$ and $8$ start empty and $7$ starts with one pebble. We show that $a(6) \le 3$, $a(8) \le 3$ and $a(7) \le 2$.

(a) No pebble enters the pair $\{9,10\}$ during $P$. Suppose $m(6,9) \ge 1$. Then $m(9,6) = 0$, since $6 \to 9 \to 6$ would be a cycle of $D$, so every pebble that reaches $6$ comes from $4$ or $7$. The set $T = \{4,6,7\}$ starts with one pebble on $4$ and one on $7$, so no vertex of $T$ can move before a pebble enters $T$ from outside; the only entries are $9 \to 6$, which is excluded, and $8 \to 7$. Hence $m(8,7) \ge 1$, so $m(7,8) = 0$, and $8$ receives pebbles from $10$ only. The arcs $10 \to 8 \to 7$, then $7 \to 6$ or $7 \to 4 \to 6$, then $6 \to 9$ form a directed path of $D$, so the arc $9 \to 10$ would close a cycle: $m(9,10) = 0$. Also $m(8,10) = 0$ because of the two-cycle with $10 \to 8$. So $10$ receives nothing and makes at most two moves, $8$ receives at most two pebbles and makes at most one move, $7$ holds at most two pebbles and makes at most one move, and $6$ receives at most one pebble, directly from $7$ or from $4$ after the move $7 \to 4$. So $6$ never holds two pebbles and $m(6,9) = 0$, a contradiction. In the same way $m(8,10) \ge 1$ is impossible: it forces $m(10,8) = 0$, so $8$ is fed by $7$ only and $7$ by $4$ or $6$ only, the pebbles of $\{4,6,7\}$ can only be supplemented through $9 \to 6$, the path $9 \to 6 \to 7 \to 8 \to 10$ (or through $4$) excludes $10 \to 9$, so $9$ makes at most two moves, $6$ receives at most two pebbles and makes at most one move, $7$ holds at most two pebbles and makes at most one move, and $8$ receives at most one pebble and never moves.

(b) Pebbles leaving the pair. By (a), vertices $9$ and $10$ hold ten pebbles between them and receive nothing from outside the pair, and at most one of the arcs $9 \to 10$, $10 \to 9$ is in $D$. If neither is, each of $9$ and $10$ makes at most $\lfloor 5/2 \rfloor = 2$ moves, so $m(9,6) \le 2$ and $m(10,8) \le 2$. If $10 \to 9$ occurs $k \ge 1$ times, then $2k + 2\,m(10,8) \le 5$ and $2\,m(9,6) \le 5 + k$, so either $k = 1$, $m(10,8) \le 1$, $m(9,6) \le 3$, or $k = 2$, $m(10,8) = 0$, $m(9,6) \le 3$; the case of $9 \to 10$ is symmetric. In every case $m(9,6) \le 3$, $m(10,8) \le 3$, $m(9,6) + m(10,8) \le 4$, and $m(9,6) = 3$ forces $m(10,8) \le 1$ while $m(10,8) = 3$ forces $m(9,6) \le 1$.

(c) Arrivals at $6$, $8$ and $7$. Put $a = m(9,6)$ and $b = m(10,8)$. The set $B = \{4,6,7,8\}$ starts with one pebble on $4$ and one on $7$, receives $a$ pebbles at $6$ and $b$ pebbles at $8$, and nothing else, since $1$, $2$, $5$ never move during $P$ and nothing comes back from the pair.
Arrivals at $6$. Apart from the $a$ pebbles from $9$, a pebble reaches $6$ from $4$ or $7$, and it cannot have passed through $6$ before, because $6 \to 4 \to 6$, $6 \to 7 \to 6$, $6 \to 4 \to 7 \to 6$ and $6 \to 7 \to 4 \to 6$ are cycles. So it comes from the pebbles that $\{4,7,8\}$ holds on its own: one on $4$, one on $7$, $b$ on $8$. As $b \le 3$ and $7 \to 8$ together with $8 \to 7$ is a two-cycle, vertex $8$ makes at most one move toward $7$; then $7$ holds at most two pebbles and makes at most one move, which is $7 \to 6$ or $7 \to 4$ followed by $4 \to 6$. So at most one pebble reaches $6$ from $\{4,7,8\}$, and only when $b \ge 2$, which forces $a \le 2$. Hence $a(6) \le 3$.
Arrivals at $8$. Apart from the $b$ pebbles from $10$, a pebble reaches $8$ only from $7$, and it comes from the pebbles that $\{4,6,7\}$ holds on its own, one on $4$, $a$ on $6$, one on $7$, because $8 \to 7 \to 8$ is a cycle. As $a \le 3$, vertex $6$ makes at most one move; after it $7$ holds at most two pebbles, directly or after $6 \to 4 \to 7$, and makes at most one move. So at most one pebble reaches $8$ from $\{4,6,7\}$, and only when $a \ge 2$, which forces $b \le 2$. Hence $a(8) \le 3$.
Arrivals at $7$. A pebble reaches $7$ from $4$, $6$ or $8$. Vertex $8$ holds the $b \le 3$ pebbles from $10$ and nothing else that could return to $7$, so it sends at most one pebble to $7$. Vertex $4$ holds one pebble and can be fed only by $6$ or by $7$; a pebble fed by $7$ cannot come back to $7$ ($7 \to 4 \to 7$ and $7 \to 4 \to 6 \to 7$ are cycles), so the pebbles that reach $7$ from $4$ or $6$ come from the $a \le 3$ pebbles on $6$, which make at most one move, directly to $7$ or to $4$ followed by $4 \to 7$: at most one arrival. Hence $a(7) \le 2$.

So $a(6) \le 3 < 4$, $a(8) \le 3 < 4$ and $a(7) \le 2 < 3$, no vertex of $\{1,2,5\}$ ever holds two pebbles, and $3$ is not reachable from $C$. Therefore $\pi(G, 3) \ge 13$.

Step 4: Every configuration of $13$ pebbles reaches $3$.
Adding a pebble to a configuration never destroys reachability. For a target $r$ let $U_k$ be the set of configurations of $k$ pebbles with none on $r$ from which $r$ is not reachable; then every member of $U_k$ is a member of $U_{k-1}$ with one pebble added, and a candidate belongs to $U_k$ exactly when no move from it lands on $r$ and every move from it leads into $U_{k-1}$. Running this recursion for the target $3$ gives sets of sizes $1, 9, 42, 135, 328, 615, 876, 905, 658, 345, 124, 21, 1, 0$ for $k = 0, 1, \dots, 13$; the single member of $U_{12}$ is the configuration $C$ of Step 3, and $U_{13}$ is empty. An independent depth-first search over move sequences confirms that each of the $203\,490$ configurations of $13$ pebbles with none on $3$ reaches $3$, and that exactly one of the $125\,970$ configurations of $12$ pebbles does not. The reference file embeds both programs with their output.

The configuration $C$ is the only one of $12$ pebbles that fails. The same twelve pebbles split as seven on $10$ and three on $9$ do reach $3$: three moves $10 \to 8$, then $8 \to 2$, $9 \to 10$, $10 \to 8$, $8 \to 2$ and $2 \to 3$. In $C$ each of the odd piles on $9$ and $10$ delivers one pebble to a different neighbour of $3$ and keeps one pebble that cannot move, and the single pebbles on $4$ and $7$ cannot be combined with anything.

Step 5: Conclusion.
The rooted pebbling number is at least $13$ by Step 3 and at most $13$ by Step 4, so $\pi(G, r) = 13$. The same recursion for the other targets gives $12$ for $1$, $2$, $4$, $5$, $9$, $10$ and $10$ for $6$, $7$, $8$, so $3$ is also the target that realises the pebbling number $\pi(G) = 13$ of the graph.

Answer: $13$."""
rubric = [
    dict(id="c1", description=r"Gives $13$.", points=5, isFinalAnswer=True),
    dict(id="c2", description=r"Exhibits a configuration of $12$ pebbles from which $r$ is not reachable (five pebbles on $9$, five on $10$, one on $4$ and one on $7$) and gives a valid argument that $r$ is not reachable from it.", points=2, isFinalAnswer=False),
    dict(id="c3", description=r"Shows by a valid argument (exhaustive, structural, or otherwise) that every configuration of $13$ pebbles reaches $r$.", points=2, isFinalAnswer=False),
    dict(id="c4", description=r"States the bounds $\pi(G, r) \ge n = 10$ and $\pi(G, r) \ge 2^{3} = 8$ (from the eccentricity of $r$) and recognises that neither is tight.", points=1, isFinalAnswer=False),
]
wrong = ["12", "10", "11", "14", "8"]
references = r"""Graph pebbling was introduced by F. R. K. Chung, Pebbling in hypercubes, SIAM Journal on Discrete Mathematics 2 (1989), 467-472, and is surveyed in G. Hurlbert, A survey of graph pebbling, Congressus Numerantium 139 (1999), 41-64. The No-Cycle Lemma used in Step 3 is Lemma 2 of K. Milans and B. Clark, The complexity of graph pebbling, SIAM Journal on Discrete Mathematics 20 (2006), 769-798. For the bounds on graphs of small diameter: T. A. Clarke, R. A. Hochberg and G. H. Hurlbert, Pebbling in diameter two graphs and products of paths, Journal of Graph Theory 25 (1997), 119-128, and B. Bukh, Maximum pebbling number of graphs of diameter three, Journal of Graph Theory 52 (2006), 353-357. The uploaded file verification_notes.txt contains the two independent exact computations of the rooted pebbling number (the layer recursion over unreachable configurations and a direct search over move sequences for every target), the list of all configurations reachable from the twelve-pebble configuration of Step 3, the acyclic-sequence bounds used in the written proof, the rooted values for every target, and the program that produces all of it with its output."""
necessity = "The graph and the target vertex are given only by the figure; the fourteen edges are not listed in the text, and the answer depends on the exact edge set and on which vertex is the double-circled target (the failing configuration lives on the two adjacent degree-2 vertices at distance 3 from it)."
task = {"schema_version": "summit-task-package-v1", "task": {
    "domain": "mathematics", "subdomain": "Graph theory: graph pebbling (rooted pebbling number)",
    "modality": "image_reference", "taskType": "image_multistep_discrete_reasoning",
    "imageCreationTool": "matplotlib (original straight-line drawing of the graph)",
    "imageNecessityExplanation": necessity, "questionText": question, "answerType": "exact_match",
    "finalAnswer": [final_answer], "acceptableAnswerVariants": variants, "multipleChoiceOptions": [],
    "answerPrecision": {"kind": "none"}, "solution": solution, "references": references,
    "rubric": {"criteria": rubric, "commonWrongAnswers": wrong}, "image": {"entry": "image.png"},
    "referenceFile": {"entry": "reference.txt", "fileName": "verification_notes.txt"}}}
VERIFY_FIELD = "Sections 1 to 3 of verification_notes.txt give the graph, the trivial bounds, the twelve-pebble configuration (five pebbles on 9, five on 10, one on 4, one on 7, target 3) with the written proof that it fails and the list of all 590 configurations reachable from it, none with a pebble on 3; section 4 gives the two independent exact computations showing that every configuration of 13 pebbles reaches the target 3 (layer recursion and direct search, both embedded in the program verify_key.py with its full output in section 5), and the rooted pebbling numbers of all ten targets."
def check():
    assert sum(c["points"] for c in rubric) == 10 and sum(c["isFinalAnswer"] for c in rubric) == 1
    assert final_answer in rubric[0]["description"] and final_answer not in wrong
    for name, text in [("question", question), ("solution", solution), ("references", references), ("necessity", necessity), ("verify", VERIFY_FIELD)] + [(c["id"], c["description"]) for c in rubric]:
        for ch in ("—", "–", "’", "“", "​"): assert ch not in text, name
    print("package checks passed")
def build_reference():
    src = (HERE / "verify_key.py").read_text(); out = (HERE / "work" / "verify_key_output.txt").read_text()
    pyver = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    txt = f"""VERIFICATION NOTES: rooted pebbling number of the graph in the figure (target: the double-circled vertex 3)

Answer key: 13.

1. The graph (from the figure). Vertices 1 to 10, edges 1-2, 1-3, 1-6, 2-3, 2-8, 3-5, 4-6, 4-7, 5-7, 6-7,
   6-9, 7-8, 8-10, 9-10. Degrees: 6 and 7 have degree 4; 1, 2, 3, 8 have degree 3; 4, 5, 9, 10 have
   degree 2. Diameter 3 (vertices 6, 7, 8 have eccentricity 2, the others 3). 2-connected, not chordal.
   Trivial lower bounds: n = 10 and 2^diam = 8.

2. Lower bound 13: the configuration C with five pebbles on 9, five on 10, one on 4, one on 7 (twelve
   pebbles) does not reach vertex 3. Written proof (same as Step 3 of the solution): if 3 were reachable,
   the No-Cycle Lemma (Milans and Clark 2006, Lemma 2) gives a reaching sequence with an acyclic move
   digraph; take the first moment a neighbour u of 3 holds two pebbles; both pebbles came from the unique
   neighbour x of u outside {{1,2,3,5}} (x = 6, 8, 7 for u = 1, 2, 5), so x received at least 4 pebbles
   (6 or 8) or at least 3 pebbles (7) while all moves started in {{4,6,7,8,9,10}}. Part (a): no pebble
   enters the pair {{9,10}} in an acyclic sequence. Part (b): at most 3 pebbles move 9->6, at most 3 move
   10->8, at most 4 in total, and 3 on one side forces at most 1 on the other. Part (c): at most one
   further pebble reaches 6 (from {{4,7,8}}), at most one further pebble reaches 8 (from {{4,6,7}}), and at
   most two pebbles reach 7 in total. So 6 and 8 receive at most 3 pebbles and 7 at most 2, no neighbour
   of 3 ever holds two pebbles, contradiction.
   Machine certificate: all 590 configurations reachable from C are listed in section 5 (certificate (i));
   none has a pebble on 3 and none has two pebbles on 1, 2 or 5. Certificate (ii) enumerates every move
   sequence with an acyclic move digraph (206 pairs of configuration and arc set) and confirms the
   bounds used in parts (a) to (c): maximal arrivals 3 at 6, 3 at 8, 2 at 7; no move 6->9 or 8->10;
   at most 4 pebbles leave the pair.

3. Why this configuration and not the textbook one. Seven pebbles on 10 and three on 9, with the same
   single pebbles on 4 and 7, does reach 3: 10->8 three times, 8->2, 9->10, 10->8, 8->2, 2->3. In C each
   odd pile of five delivers one pebble to a different neighbour of 3 and keeps one immobile pebble.

4. Upper bound 13 (and the other targets, for comparison): two independent exact computations (section 5). Route A (layer recursion over the
   sets U_k of unreachable configurations of k pebbles) gives the rooted values pi(G,r): 13 for r = 3,
   12 for r = 1, 2, 4, 5, 9, 10, 10 for r = 6, 7, 8; for the target 3 the layer sizes are 1, 9, 42, 135,
   328, 615, 876, 905, 658, 345, 124, 21, 1, 0, and the single unreachable configuration of 12 pebbles
   is C. Route B (memoised depth-first search over move sequences) checks all 203,490 configurations of
   13 pebbles for every target (all reach the target) and all 125,970 configurations of 12 pebbles for
   the target 3 (exactly one fails, namely C).

5. Program verify_key.py (run with {pyver}; command: python3 verify_key.py; standard library only,
   about 15 seconds)

{textwrap.indent(src, "   ")}

   Output:

{textwrap.indent(out, "   ")}
"""
    (HERE / "reference.txt").write_text(txt); print("reference.txt written", len(txt), "bytes")
def build_readme():
    lines = ["# task09: rooted pebbling number of a 10-vertex graph", "", "Domain: Mathematics. Subdomain: " + task["task"]["subdomain"], "",
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
