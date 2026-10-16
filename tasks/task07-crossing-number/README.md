# task07: crossing number of a 10-vertex graph

Domain: Mathematics. Subdomain: Graph theory: topological graph theory (crossing number of a graph)

## Question

The figure shows a graph $G$ with $10$ vertices, labelled $1$ to $10$, and $21$ edges, drawn with straight edges. The drawing in the figure has four crossings, and it is only one of many drawings of $G$.

A drawing of $G$ in the plane places the vertices at distinct points and represents each edge by a simple curve between its two endpoints that passes through no other vertex. A crossing is a point that lies in the interior of two edges. Only drawings in which no three edges pass through one point are considered, so every crossing is a crossing of exactly two edges. The crossing number $\mathrm{cr}(G)$ is the smallest number of crossings over all drawings of $G$.

Two facts about $G$ may be used without proof. Deleting any single edge of $G$ leaves a non-planar graph. Deleting the two edges $\{1, 2\}$ and $\{6, 7\}$ leaves a planar graph, deleting the two edges $\{1, 5\}$ and $\{6, 7\}$ leaves a planar graph, and no other pair of edges has this property.

What is $\mathrm{cr}(G)$? Give a single integer.

## Answer

3

## Solution

Step 1: Read the graph off the figure.
Write $uv$ for the edge joining the vertices $u$ and $v$. The edges are $12$, $15$, $19$, $1\,10$, $23$, $24$, $26$, $35$, $36$, $38$, $39$, $45$, $46$, $48$, $4\,10$, $56$, $67$, $78$, $79$, $7\,10$, $8\,10$. The degrees are $5$ (vertices $3$, $4$ and $6$), $4$ (vertices $1$, $2$, $5$, $7$, $8$ and $10$) and $3$ (vertex $9$). The bound from Euler's formula gives nothing, since $21 \le 3 \cdot 10 - 6 = 24$. The graph is not planar: it contains a subdivision of $K_{3,3}$ with the vertices $3$, $4$, $7$ on one side and $6$, $8$, $9$ on the other, the nine connections being the edges $36$, $38$, $39$, $46$, $48$, $67$, $78$, $79$ and the path $4\,5\,1\,9$. The drawing in the figure shows that $\mathrm{cr}(G) \le 4$.

Step 2: No drawing has one crossing.
If a drawing had a single crossing, between the edges $a$ and $b$, then deleting $a$ would leave a crossing-free drawing of $G - a$, so $G - a$ would be planar. By the first given fact no single edge deletion is planar, so $\mathrm{cr}(G) \ge 2$.

Step 3: No drawing has two crossings.
Suppose a drawing of $G$ has exactly two crossings, one between the edges $a$ and $b$ and one between the edges $c$ and $d$. If an edge took part in both crossings, say $a = c$, deleting $a$ would leave a crossing-free drawing of $G - a$, which is impossible by Step 2. So $a$, $b$, $c$, $d$ are four distinct edges. Deleting $a$ and $c$ removes both crossings, so $G - \{a, c\}$ is planar; in the same way $G - \{a, d\}$, $G - \{b, c\}$ and $G - \{b, d\}$ are planar. These are four distinct pairs of edges whose deletion leaves a planar graph, but by the second given fact only two such pairs exist, $\{12, 67\}$ and $\{15, 67\}$. Hence $\mathrm{cr}(G) \ge 3$. In particular the two edges $12$ and $67$ cannot be put back into a planar drawing of $G - \{12, 67\}$ with one crossing each, although two deleted edges are enough to make $G$ planar.

The same conclusion can be read off the planar subgraphs directly. $G - \{12, 67\}$ is $3$-connected, so it has a single embedding in the sphere, with faces $2\,3\,6$, $3\,5\,6$, $8\,4\,10$, $6\,5\,4$, $1\,10\,4\,5$, $5\,3\,9\,1$, $7\,8\,10$, $4\,8\,3\,2$, $6\,4\,2$, $9\,3\,8\,7$ and $10\,1\,9\,7$. No face containing vertex $1$ shares an edge with a face containing vertex $2$, so the edge $12$ needs at least two crossings in this embedding, and the same holds for $67$. For $G - \{15, 67\}$ the faces are $2\,3\,9\,1$, $8\,10\,7$, $8\,7\,9\,3$, $5\,3\,6$, $10\,8\,4$, $1\,9\,7\,10$, $10\,4\,2\,1$, $3\,2\,6$, $6\,2\,4$, $4\,8\,3\,5$ and $6\,4\,5$, and again neither missing edge can be added with one crossing. Starting from a planar subgraph with $19$ edges therefore costs two crossings per missing edge, four in all.

Step 4: A drawing with three crossings.
In the figure the edges $38$ and $48$ both cross edges at vertex $7$, namely $79$ and $7\,10$. Keep every vertex where it is and move vertex $7$ down and to the right, below the edge $8\,10$ and to the right of vertex $8$, so that its three edges $78$, $79$ and $7\,10$ no longer meet $38$ and $48$; the edge $67$ then crosses $38$ once. With integer coordinates: $1 \mapsto (0, 1)$, $2 \mapsto (0, 20)$, $3 \mapsto (17, 17)$, $4 \mapsto (6, 7)$, $5 \mapsto (6, 13)$, $6 \mapsto (12, 12)$, $7 \mapsto (13, 1)$, $8 \mapsto (12, 3)$, $9 \mapsto (19, 0)$, $10 \mapsto (4, 3)$, every edge a straight segment. No vertex lies on a segment that is not incident to it, and the only pairs of segments that cross are $15$ with $24$, $26$ with $35$, and $38$ with $67$. Equivalently, the subgraph $G - \{15, 26, 38\}$ with $18$ edges is planar, with the ten faces $4\,6\,5$, $8\,10\,7$, $8\,7\,6\,4$, $10\,8\,4$, $4\,5\,3\,2$, $3\,5\,6$, $2\,3\,9\,1$, $7\,10\,1\,9$, $10\,4\,2\,1$ and $9\,3\,6\,7$, and each deleted edge joins two faces that share one edge: $15$ goes from the face $10\,4\,2\,1$ across $24$ into $4\,5\,3\,2$, $26$ from $4\,5\,3\,2$ across $35$ into $3\,5\,6$, and $38$ from $9\,3\,6\,7$ across $67$ into $8\,7\,6\,4$; the coordinates show that the three new edges can be drawn without meeting each other. So $\mathrm{cr}(G) \le 3$. The three crossed edges $15$, $26$, $38$ are not one of the two pairs that make $G$ planar when deleted: the better drawing does not come from a planar subgraph with $19$ edges, and it crosses $67$ instead of deleting it.

Step 5: Conclusion.
$\mathrm{cr}(G) \ge 3$ by Step 3 and $\mathrm{cr}(G) \le 3$ by Step 4, so $\mathrm{cr}(G) = 3$. Two deleted edges make $G$ planar, yet no drawing has two crossings: the number of edges that must be deleted for planarity is one less than the crossing number of this graph.

Answer: $3$.

## Rubric

- c1 (5 pts, final answer): Gives $3$.
- c2 (2 pts): Exhibits a drawing of $G$ with exactly three crossings (explicit coordinates, or a planar subgraph with $18$ edges together with the three missing edges each added with one crossing, such as $15$ crossing $24$, $26$ crossing $35$ and $38$ crossing $67$, which is the figure with vertex $7$ moved).
- c3 (2 pts): Proves that no drawing with two crossings exists by a valid argument, for instance: the two crossings would involve four distinct edges and deleting one edge from each crossing in all four ways would give four distinct pairs whose deletion leaves a planar graph, against the two that exist; or shows that in the unique embedding of $G - \{12, 67\}$ (and of $G - \{15, 67\}$) neither missing edge can be added with one crossing.
- c4 (1 pts): States and justifies $\mathrm{cr}(G) \ge 2$ from the fact that no single edge deletion leaves a planar graph.

Common wrong answers: 2, 4, 1

## References box

The crossing number and its basic properties, including the fact that in a drawing with the fewest crossings adjacent edges do not cross and two edges cross at most once: M. Schaefer, The graph crossing number and its variants: a survey, Electronic Journal of Combinatorics, Dynamic Survey DS21 (2013, updated). NP-completeness of the crossing number, which is why the value needs a certificate on each side: M. R. Garey and D. S. Johnson, Crossing number is NP-complete, SIAM Journal on Algebraic and Discrete Methods 4 (1983), 312-316. The planarity algorithm used for the independent check: G. Demoucron, Y. Malgrange and R. Pertuiset, Graphes planaires: reconnaissance et construction de representations planaires topologiques, Revue Francaise de Recherche Operationnelle 8 (1964), 33-47. The uploaded file verification_notes.txt verifies the two facts stated in the question (no single edge deletion and exactly two pair deletions leave a planar graph, by two different planarity tests) and the answer key by two independent routes: an exhaustive enumeration of all crossing sets with up to three crossings (planarity of every planarization), and a library-free route with its own planarity test that gives the faces of the two planar subgraphs, the drawing of the figure with its four crossings, and a straight-line drawing with exactly three crossings (the figure with one vertex moved) checked by exact integer arithmetic; the program is embedded with its output.

## Verify field

Section 2 of verification_notes.txt checks the two facts given in the question (no single edge deletion and only the pairs 1-2 with 6-7 and 1-5 with 6-7 leave a planar graph) and gives the four-pairs argument that rules out two crossings; section 3 gives the figure's drawing with its four crossings and the straight-line drawing with three crossings, both with integer coordinates and the list of crossing pairs; section 4 is the exhaustive enumeration of crossing sets (none with one or two crossings, four with three); section 6 embeds the program verify_key.py with its full output, including an independent planarity test that does not use a graph library.

## Screen

Screen v1 (first version: circular figure with 32 crossings, no facts in the stem, same graph): Opus 0/1, cut off at the 64k output ceiling with no answer, in two runs (2 and 8 reads of the figure, every token spent on reading chords and trying embeddings); Sonnet 0/1, answered 2 after misreading three edges (26 min, 134k tokens). Verdict: the difficulty was length, not reasoning. Reworked into v2.

Screen v2 (this package: clean straight-line figure with four crossings, the two planarity facts stated in the stem): Opus 1/1 correct, 3 in 28 min and 119k tokens (read all 21 edges, settled the one ambiguous segment 7-9 from the given facts, the four-pairs argument for the lower bound, then an explicit three-crossing drawing on the hexagon 3-6-4-10-1-9 with 6-7 crossing 3-8, 1-5 crossing 2-3, 4-5 crossing 2-6). Sonnet 1/1 correct by the final answer, 3 in 31 min and 98k tokens (read 4-10 as 5-10, lower bound by the four-pairs argument, upper bound by a false claim that G minus 6-7 has a one-crossing drawing). Tally: Opus 1/1, Sonnet 1/1. Both screens solved; held back, the owner decides.