# task06: bandwidth of a 14-vertex graph

Domain: Mathematics. Subdomain: Graph theory: graph layout problems (bandwidth of a graph)

## Question

The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $27$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 14\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

What is the bandwidth of $G$? Give a single integer.

## Answer

5

## Solution

Step 1: Read the graph off the figure.
The edges are $12$, $14$, $16$, $18$, $1\,11$, $1\,14$, $28$, $37$, $38$, $3\,10$, $3\,12$, $3\,13$, $4\,10$, $4\,11$, $4\,13$, $4\,14$, $59$, $5\,12$, $69$, $6\,11$, $78$, $7\,11$, $9\,13$, $9\,14$, $11\,13$, $11\,14$, $12\,14$. The degrees are $6$ (vertices $1$ and $11$), $5$ (vertices $3$, $4$ and $14$), $4$ (vertices $8$, $9$ and $13$), $3$ (vertices $6$, $7$ and $12$) and $2$ (vertices $2$, $5$ and $10$). The diameter of $G$ is $4$.

Step 2: The easy bounds give $3$ and $4$.
A vertex of degree $6$ forces some incident edge to be stretched by at least $\lceil 6/2 \rceil = 3$, and the diameter bound gives $\lceil (14-1)/4 \rceil = 4$. Both are short of the answer.

Step 3: An induced subgraph of diameter $2$ gives $5$.
If $H$ is a connected subgraph with $k$ vertices and diameter $d$, then in any numbering the lowest and highest numbered vertices of $H$ differ by at least $k-1$ and are joined inside $H$ by a path of at most $d$ edges, so some edge of that path is stretched by at least $\lceil (k-1)/d \rceil$. Take $H$ to be the subgraph induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$. Every two of its ten vertices are adjacent or have a common neighbour inside $H$: the non-adjacent pairs and a common neighbour are $\{1,3\}{:}\,8$, $\{1,7\}{:}\,8$, $\{1,10\}{:}\,4$, $\{1,12\}{:}\,14$, $\{1,13\}{:}\,4$, $\{3,4\}{:}\,10$, $\{3,11\}{:}\,7$, $\{3,14\}{:}\,12$, $\{4,7\}{:}\,11$, $\{4,8\}{:}\,1$, $\{4,12\}{:}\,14$, $\{7,10\}{:}\,3$, $\{7,12\}{:}\,3$, $\{7,13\}{:}\,3$, $\{7,14\}{:}\,11$, $\{8,10\}{:}\,3$, $\{8,11\}{:}\,1$, $\{8,12\}{:}\,3$, $\{8,13\}{:}\,3$, $\{8,14\}{:}\,1$, $\{10,11\}{:}\,4$, $\{10,12\}{:}\,3$, $\{10,13\}{:}\,3$, $\{10,14\}{:}\,4$, $\{11,12\}{:}\,14$, $\{12,13\}{:}\,3$, $\{13,14\}{:}\,4$. So $H$ has diameter $2$ and the bound is $\lceil 9/2 \rceil = 5$.

Step 4: A numbering of width $5$.
Give the vertices the positions $2 \mapsto 1$, $7 \mapsto 2$, $8 \mapsto 3$, $1 \mapsto 4$, $11 \mapsto 5$, $4 \mapsto 6$, $3 \mapsto 7$, $6 \mapsto 8$, $14 \mapsto 9$, $13 \mapsto 10$, $10 \mapsto 11$, $12 \mapsto 12$, $9 \mapsto 13$, $5 \mapsto 14$. The stretches of the twenty-seven edges are $12{:}\,3$, $14{:}\,2$, $16{:}\,4$, $18{:}\,1$, $1\,11{:}\,1$, $1\,14{:}\,5$, $28{:}\,2$, $37{:}\,5$, $38{:}\,4$, $3\,10{:}\,4$, $3\,12{:}\,5$, $3\,13{:}\,3$, $4\,10{:}\,5$, $4\,11{:}\,1$, $4\,13{:}\,4$, $4\,14{:}\,3$, $59{:}\,1$, $5\,12{:}\,2$, $69{:}\,5$, $6\,11{:}\,3$, $78{:}\,1$, $7\,11{:}\,3$, $9\,13{:}\,3$, $9\,14{:}\,4$, $11\,13{:}\,5$, $11\,14{:}\,4$, $12\,14{:}\,3$. The largest is $5$.

Step 5: Conclusion.
The bandwidth is at least $5$ by Step 3 and at most $5$ by Step 4, so it equals $5$. (Breadth-first numberings from any start vertex have width $6$ or more; the numbering of Step 4 places the two vertices of degree $6$ at positions $4$ and $5$ and spreads their neighbours on both sides.)

Answer: $5$.

## Rubric

- c1 (5 pts, final answer): Gives $5$.
- c2 (2 pts): Exhibits an explicit numbering of the fourteen vertices of width $5$ (every edge stretched by at most $5$).
- c3 (2 pts): Proves the lower bound $5$ by a valid argument, for instance the density bound $\lceil (k-1)/d \rceil$ applied to a connected subgraph with $k = 10$ vertices and diameter $d = 2$ such as the one induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$, or an exhaustive argument that no numbering of width $4$ exists.
- c4 (1 pts): States the degree bound $\lceil \Delta/2 \rceil = 3$ or the diameter bound $\lceil 13/4 \rceil = 4$ and recognises that it is not tight.

Common wrong answers: 4, 6, 7

## References box

The density lower bound for the bandwidth (a connected subgraph with $k$ vertices and diameter $d$ forces width at least $\lceil (k-1)/d \rceil$) and the general theory of the bandwidth problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth, which is why the exact value needs a certificate on each side: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains two independent exact computations of the bandwidth (backtracking over numberings, and a dynamic programme over sets of placed vertices), the diameter computation for the certificate subgraph, the explicit numbering of width $5$ with the stretch of every edge, and the widths of all Cuthill-McKee numberings; the program is embedded with its output.

## Verify field

Sections 2 to 4 of verification_notes.txt give the certificate subgraph (ten vertices, diameter 2, with a common neighbour listed for every non-adjacent pair), the explicit width-5 numbering with every edge stretch, and two independent exact computations showing no numbering of width 4 exists; section 6 embeds the program with its output.

## Screen

Screened 2026-10-16 (figure plus stem only, no code, no web). Opus 1/1 correct in 8 min and 77k tokens: found the width-5 numbering, then a window argument around the clique 1, 4, 11, 14 with a short case split for the lower bound. Sonnet 1/1 correct in 37 min, but by luck: it misread four edges and gave no proof of the lower bound. Verdict: a bigger instance did not help; Opus found a different short lower-bound argument. Not submitted. The counting version is in v2-count/.