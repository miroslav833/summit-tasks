# task05 v3: revision of SUM-MVB7DTW7 with the reviewer's Graph A (13 vertices)

Domain: Mathematics. Subdomain: Graph theory: graph layout problems (bandwidth of a graph)

## Question

The figure shows a graph $G$ with $13$ vertices, labelled $1$ to $13$, and $22$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 13\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer.

## Answer

5

## Solution

Step 1: Read the graph off the figure.
The edges are $13$, $18$, $1\,13$, $24$, $26$, $2\,10$, $2\,12$, $36$, $37$, $39$, $45$, $47$, $48$, $59$, $7\,10$, $7\,12$, $8\,10$, $8\,11$, $9\,13$, $10\,11$, $11\,13$, $12\,13$. The degrees are $4$ for the vertices $1, 2, 3, 4, 7, 8, 13$, $3$ for $9, 10, 11, 12$ and $2$ for $5, 6$; the maximum degree is $4$ and the diameter is $3$.

Step 2: The cheap bounds all stop at $4$.
A vertex of degree $4$ forces a stretch of at least $\lceil 4/2 \rceil = 2$; the diameter bound gives $\lceil 12/3 \rceil = 4$; and the density bound, $\lceil (k-1)/d \rceil$ for a connected subgraph with $k$ vertices and diameter $d$, never exceeds $4$ here: the eleven vertices $1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12$ induce a subgraph of diameter $3$, which gives $\lceil 10/3 \rceil = 4$, and no connected induced subgraph does better (all of them are checked in the verification notes). So these arguments prove only that the bandwidth is at least $4$.

Step 3: There is no numbering of width $4$.
Build a numbering position by position. A vertex may be placed at position $i$ only if all its already placed neighbours sit at positions $i-4$ or later, and after each placement every placed vertex $u$ at position $p$ must still have at least as many free positions in $(i, p+4]$ as it has unplaced neighbours, otherwise one of its edges will be stretched beyond $4$. These two rules are exact: a numbering of width $4$ exists if and only if the construction reaches position $13$. Carried out for every choice at every step, the construction dies in every branch; the complete tree has $1\,612$ nodes, and the verification notes print every branch down to depth $3$ with the rule that kills it, together with the full program. An independent check with a different formulation (a dynamic programme over the set of placed vertices and the last four placed) also finds no numbering of width $4$. Hence the bandwidth is at least $5$.

Step 4: A numbering of width $5$.
Give the vertices the positions $1 \mapsto 1$, $11 \mapsto 2$, $8 \mapsto 3$, $7 \mapsto 4$, $13 \mapsto 5$, $3 \mapsto 6$, $10 \mapsto 7$, $4 \mapsto 8$, $12 \mapsto 9$, $9 \mapsto 10$, $6 \mapsto 11$, $2 \mapsto 12$, $5 \mapsto 13$. The stretches of the twenty-two edges are $13{:}\,5$, $18{:}\,2$, $1\,13{:}\,4$, $24{:}\,4$, $26{:}\,1$, $2\,10{:}\,5$, $2\,12{:}\,3$, $36{:}\,5$, $37{:}\,2$, $39{:}\,4$, $45{:}\,5$, $47{:}\,4$, $48{:}\,5$, $59{:}\,3$, $7\,10{:}\,3$, $7\,12{:}\,5$, $8\,10{:}\,4$, $8\,11{:}\,1$, $9\,13{:}\,5$, $10\,11{:}\,5$, $11\,13{:}\,3$, $12\,13{:}\,4$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. There are $176$ numberings of width $5$, with nine different pairs of end vertices, so nothing about the optimal numberings is forced by a short argument; the breadth-first numberings from any start vertex have width $6$ or more.

Answer: $5$.

## Rubric

- c1 (5 pts, final answer): Gives $5$.
- c2 (2 pts): Exhibits an explicit numbering of the thirteen vertices of width $5$ (every edge stretched by at most $5$).
- c3 (2 pts): Proves that no numbering of width $4$ exists by a complete argument (an exhaustive placement search with correct pruning rules, or an equivalent case analysis that covers every possibility).
- c4 (1 pts): States a valid lower bound of $4$ (the diameter bound $\lceil 12/3 \rceil = 4$ or a density bound on a connected subgraph) and recognises that it is not tight.

Common wrong answers: 4, 6, 3

## References box

The density lower bound for the bandwidth (a connected subgraph with $k$ vertices and diameter $d$ forces width at least $\lceil (k-1)/d \rceil$) and the general theory of the bandwidth problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains two independent exact computations of the bandwidth (backtracking over numberings, and a dynamic programme over sets of placed vertices), the diameter computation for the certificate subgraph, the explicit numbering of width $4$ with the stretch of every edge, and the widths of all Cuthill-McKee numberings; the program is embedded with its output.

## Verify field

Section 2 of verification_notes.txt gives the two independent exact computations showing no numbering of width 4 exists (the pruned placement search with its tree printed to depth 3, and a dynamic programme) and the check that every cheap lower bound stops at 4; section 3 gives the explicit width-5 numbering with every edge stretch; section 6 embeds the program verify_key.py with its full output.

## Screen

(filled in after the screen)