# task06 v3: bandwidth of a 16-vertex graph with no short lower bound and a unique optimal numbering

Revision of task06 (the 14-vertex instance was solved by Opus on one run, and task05 with its counting version came back from Summit 5/5). It replaces the task06 entry on Summit field by field: new figure, the same question text with 16 vertices and 27 edges, the same answer 5, new solution, rubric, references text and reference file. Design: an instance where (a) no degree, diameter or density bound reaches the answer, so the lower bound needs the prefix argument (a 57-set chain, short enough to write out), and (b) the optimal numbering is unique up to reversal and heuristics miss it (Cuthill-McKee 7 to 10, simulated annealing 0 of 16 restarts, the width-5 prefix chain has 4455 sets). Found by random search over 16-vertex graphs with 26 to 31 edges (work/gen.py, gen2.py, eval.py). The expected wrong answer is 6, the best width a solver reaches without finding the unique numbering.

Domain: Mathematics. Subdomain: Graph theory: graph layout problems (bandwidth of a graph)

## Question

The figure shows a graph $G$ with $16$ vertices, labelled $1$ to $16$, and $27$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 16\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer.

## Answer

5 (also accepted: $5$, bandwidth 5)

## Solution

Step 1: Read the graph off the figure.
The edges are $13$, $1\,10$, $23$, $29$, $2\,12$, $2\,13$, $3\,10$, $3\,12$, $3\,14$, $3\,15$, $48$, $4\,16$, $56$, $57$, $69$, $6\,14$, $6\,15$, $7\,12$, $7\,16$, $89$, $8\,10$, $8\,13$, $9\,15$, $11\,13$, $11\,14$, $12\,15$ and $13\,16$. The degrees are $6$ (vertex $3$), $4$ (vertices $2$, $6$, $8$, $9$, $12$, $13$ and $15$), $3$ (vertices $7$, $10$, $14$ and $16$) and $2$ (vertices $1$, $4$, $5$ and $11$). The diameter of $G$ is $4$.

Step 2: The easy bounds give $3$ and $4$.
A vertex of degree $6$ forces some incident edge to be stretched by at least $\lceil 6/2 \rceil = 3$. The diameter bound gives $\lceil 15/4 \rceil = 4$. The density bound, $\lceil (k-1)/d \rceil$ for a connected subgraph with $k$ vertices and diameter $d$, never goes above $4$ on this graph, whichever subgraph is taken. So none of the usual bounds settles the answer, and the lower bound needs a different argument.

Step 3: No numbering has width $4$.
Take a numbering of width $b$ and let $P$ be the set of vertices in positions $1$ to $k$. A vertex outside $P$ with a neighbour in $P$ has to sit within $b$ positions of that neighbour, so it sits in one of the positions $k+1$ to $k+b$. So $P$ has at most $b$ neighbours outside $P$, and this holds for every $k$. Now suppose $b = 4$ and build $P$ one vertex at a time, keeping only the sets with at most four outside neighbours. With one vertex, every vertex except $3$ (degree $6$) qualifies. With two vertices $21$ sets survive, with three vertices $15$, with four vertices $5$: $\{1, 4, 8, 10\}$, $\{1, 4, 10, 16\}$, $\{1, 10, 11, 14\}$, $\{4, 5, 7, 16\}$ and $\{4, 11, 13, 16\}$. With five vertices only $\{1, 4, 8, 10, 16\}$ survives, with outside neighbours $3$, $7$, $9$, $13$. Adding a sixth vertex always gives at least five outside neighbours. If the added vertex is one of $3$, $7$, $9$, $13$, the other three stay and the new vertex brings at least two more ($3$ brings $2$, $12$, $14$, $15$, vertex $7$ brings $5$ and $12$, vertex $9$ brings $2$, $6$, $15$, vertex $13$ brings $2$ and $11$). If it is any other vertex, all four stay and the new vertex brings at least one more ($2$ brings $12$, $5$ brings $6$, $6$ brings $5$, $14$, $15$, $11$ brings $14$, $12$ brings $2$ and $15$, $14$ brings $6$ and $11$, $15$ brings $6$ and $12$). So no numbering of width $4$ gets past its sixth vertex, and the bandwidth is at least $5$. The verification notes list all $57$ sets of the chain with their outside neighbours.

Step 4: A numbering of width $5$.
Give the vertices the positions $1 \mapsto 1$, $10 \mapsto 2$, $9 \mapsto 3$, $15 \mapsto 4$, $3 \mapsto 5$, $2 \mapsto 6$, $8 \mapsto 7$, $6 \mapsto 8$, $12 \mapsto 9$, $14 \mapsto 10$, $13 \mapsto 11$, $4 \mapsto 12$, $5 \mapsto 13$, $7 \mapsto 14$, $11 \mapsto 15$, $16 \mapsto 16$. The stretches of the twenty-seven edges are $13{:}\,4$, $1\,10{:}\,1$, $23{:}\,1$, $29{:}\,3$, $2\,12{:}\,3$, $2\,13{:}\,5$, $3\,10{:}\,3$, $3\,12{:}\,4$, $3\,14{:}\,5$, $3\,15{:}\,1$, $48{:}\,5$, $4\,16{:}\,4$, $56{:}\,5$, $57{:}\,1$, $69{:}\,5$, $6\,14{:}\,2$, $6\,15{:}\,4$, $7\,12{:}\,5$, $7\,16{:}\,2$, $89{:}\,4$, $8\,10{:}\,5$, $8\,13{:}\,4$, $9\,15{:}\,1$, $11\,13{:}\,4$, $11\,14{:}\,5$, $12\,15{:}\,5$, $13\,16{:}\,5$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. Breadth-first numberings from any start vertex have width $7$ or more, and the numbering of Step 4 is the only one of width $5$ apart from its reverse, which is why the usual heuristics stop at $6$ or $7$.

Answer: $5$.

## Rubric

- c1 (5 pts, final answer): Gives $5$.
- c2 (2 pts): Exhibits an explicit numbering of the sixteen vertices of width $5$ (every edge stretched by at most $5$).
- c3 (2 pts): Proves that no numbering of width $4$ exists by a valid argument, for instance the prefix argument (the first $k$ vertices of a numbering of width $4$ have at most four outside neighbours, and no set of six vertices satisfies this) or an exhaustive case analysis.
- c4 (1 pts): States the degree bound $\lceil 6/2 \rceil = 3$ or the diameter bound $\lceil 15/4 \rceil = 4$ and recognises that neither is tight.

Common wrong answers: 6, 4, 7

## References box

The general theory of the bandwidth problem, including the degree, diameter and density lower bounds: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the written lower-bound proof (the prefix argument: the first $k$ vertices of a numbering of width $4$ have at most four outside neighbours, and the chain of such sets dies at six vertices; all $57$ sets are listed), two independent exact computations of the bandwidth (backtracking over numberings and a dynamic programme over sets of placed vertices), the explicit numbering of width $5$ with the stretch of every edge, the check that no density bound reaches $5$, and the widths of all Cuthill-McKee numberings. The program is embedded with its output.

## Verify field

Section 2 of verification_notes.txt is the written lower-bound proof (the first k vertices of a numbering of width 4 have at most four outside neighbours; the chain of such sets is listed in full and dies at six vertices). Section 3 gives two independent exact computations, section 4 the explicit numbering of width 5 with every edge stretch, section 5 the check that no degree, diameter or density bound reaches 5. Section 7 embeds the program with its output.

## How to submit

Revise the task06 entry on Summit field by field with the texts above: replace the image, the question text, the solution, the rubric, the common wrong answers, the references text and the reference file (remove verification_notes.txt and upload this reference.txt under that name).

## Screen

Screened 2026-10-16 (figure plus stem only, no code, no web). First pass: Opus cut off at the 64k output token ceiling with no answer, the budget spent in thinking; Sonnet cut off the same way. Second Opus run (same prompt, plus one sentence that an answer with a short justification beats no answer): correct, 5, in 25 minutes and 103k tokens. It read all 27 edges correctly, found the unique width-5 numbering, and proved the lower bound by a halving argument (with width 4 the first four and the last four positions have disjoint closed neighbourhoods, so they form a K4,4 in the graph of pairs at distance 3 or more, and that graph has no K4). Two attempts at a staged re-screen were refused by the model's safeguards and are not counted. Tally: Opus 1/2 (one cut-off), Sonnet 0/1 (cut-off).