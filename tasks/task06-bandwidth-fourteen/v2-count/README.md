# task06 v2: number of optimal numberings (bandwidth) of a 14-vertex graph

Counting version of task06. Summit returned task05 and suggested asking for the number of optimal numberings instead. The task06 graph has 248 of them, far too many for any hand route, so two edges were added (67 and 6-10, 29 edges in all). The bandwidth stays 5, the easy bounds stay 3 and 4, the diameter stays 4, and exactly six numberings (three up to reversal) attain width 5. New figure, same drawing style.

Domain: Mathematics. Subdomain: Graph theory: graph layout problems (bandwidth of a graph and its optimal numberings)

## Question

The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $29$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 14\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

How many numberings of $G$ have width equal to the bandwidth of $G$? A numbering and its reverse (the numbering $v \mapsto 15 - f(v)$) are counted as two different numberings. Give a single integer.

## Answer

6 (also accepted: $6$, six)

## Solution

Step 1: Read the graph off the figure.
The edges are $12$, $14$, $16$, $18$, $1\,11$, $1\,14$, $28$, $37$, $38$, $3\,10$, $3\,12$, $3\,13$, $4\,10$, $4\,11$, $4\,13$, $4\,14$, $59$, $5\,12$, $67$, $69$, $6\,10$, $6\,11$, $78$, $7\,11$, $9\,13$, $9\,14$, $11\,13$, $11\,14$ and $12\,14$. The degrees are $6$ (vertices $1$ and $11$), $5$ (vertices $3$, $4$, $6$ and $14$), $4$ (vertices $7$, $8$, $9$ and $13$), $3$ (vertices $10$ and $12$) and $2$ (vertices $2$ and $5$). The diameter of $G$ is $4$.

Step 2: The bandwidth is $5$.
Lower bound. Take a connected subgraph $H$ with $k$ vertices and diameter $d$. In any numbering the lowest and the highest vertex of $H$ are at least $k-1$ apart, and a path of at most $d$ edges inside $H$ joins them, so one of those edges is stretched by at least $\lceil (k-1)/d \rceil$. The subgraph induced on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$ has ten vertices and diameter $2$. Any two of them are adjacent or share a neighbour inside the subgraph ($1$ and $3$ share $8$, $3$ and $4$ share $10$, $7$ and $14$ share $11$, $12$ and $13$ share $3$, and so on for the other pairs). This gives width at least $\lceil 9/2 \rceil = 5$. The degree bound $\lceil 6/2 \rceil = 3$ and the diameter bound $\lceil 13/4 \rceil = 4$ are weaker. Upper bound. The numbering $2, 8, 7, 1, 11, 4, 3, 6, 14, 13, 10, 12, 9, 5$ (positions $1$ to $14$) has width $5$. So the bandwidth is $5$.

Step 3: What a numbering of width $5$ must look like.
Write $p(v)$ for the position of $v$. Suppose $v$ is in position $1$. Each neighbour of $v$ is then in a position at most $6$, and each vertex at distance $2$ from $v$ in a position at most $11$, so the whole ball of radius $2$ around $v$ has to fit into eleven positions. Count these balls. Around $2$ the ball has $9$ vertices and around $5$ it has $7$. Around every other vertex it has at least $12$ ($12$ around $8$, $9$, $10$ and $12$, $13$ around $1$, $4$, $6$, $7$, $11$ and $13$, $14$ around $3$ and $14$). So the ends of the numbering are $2$ and $5$, and after a reversal we can take $p(2) = 1$ and $p(5) = 14$. The neighbours of $2$ are $1$ and $8$. Put $1$ in position $2$ and its other five neighbours fill positions $3$ to $7$; their further neighbours $3$, $7$, $9$, $10$, $12$, $13$ then have to sit in position $12$ or lower, and that is thirteen vertices in twelve positions. So $p(8) = 2$, and $1$ is somewhere in positions $3$ to $6$. Now the other end. The vertex in position $13$ has its radius-$2$ ball inside positions $3$ to $14$, twelve positions, and $5$ is in there as well. This rules out every vertex except $9$. The balls around $8$ and $10$ have $12$ vertices and do not contain $5$, and for $12$ the vertex $6$ joins the count, because $6$ is adjacent to $9$ and $9$ is within five positions of $5$. So $p(9) = 13$, and $12$ is in one of positions $9$ to $12$. The two vertices of degree $6$, $1$ and $11$, need room on both sides, so they sit in the middle. The same holds for $3$ and $6$, which have neighbours near both ends ($3$ is adjacent to $8$ and $12$, $6$ to $7$ and $9$). Checking the placements that keep every edge within $5$ gives $p(1) \in \{4, 5\}$, $p(12) = 12$, $p(3) = 7$, $p(6) = 8$, and three arrangements in all.

Step 4: The complete list.
Reading positions $1$ to $14$:
$$2, 8, 7, 1, 11, 4, 3, 6, 14, 13, 10, 12, 9, 5 \qquad 2, 8, 7, 10, 1, 11, 3, 6, 4, 14, 13, 12, 9, 5 \qquad 2, 8, 10, 7, 1, 4, 3, 6, 11, 14, 13, 12, 9, 5$$
and their three reverses. Each has width $5$. In the first two the edges $1\,14$, $38$, $3\,12$, $4\,10$, $67$, $69$ and $11\,13$ are stretched by exactly $5$, in the third the edges $1\,14$, $38$, $3\,12$, $4\,13$, $69$, $6\,10$ and $7\,11$. No other numbering works, by Step 3 and the finite check of what is left. The verification notes carry the search tree with the reason each dead branch dies, and a second count by a dynamic programme over sets of placed vertices. Both give six.

Step 5: Conclusion.
The bandwidth is $5$ and exactly $6$ numberings attain it, $3$ up to reversal. For comparison, $23\,662$ numberings have width at most $6$.

Answer: $6$.

## Rubric

- c1 (5 pts, final answer): Gives $6$.
- c2 (2 pts): Establishes that the bandwidth is $5$: a valid lower-bound argument (for instance the ten-vertex induced subgraph of diameter $2$ on $\{1, 3, 4, 7, 8, 10, 11, 12, 13, 14\}$) and an explicit numbering of width $5$.
- c3 (2 pts): Lists the three optimal numberings up to reversal, $2\,8\,7\,1\,11\,4\,3\,6\,14\,13\,10\,12\,9\,5$, $2\,8\,7\,10\,1\,11\,3\,6\,4\,14\,13\,12\,9\,5$ and $2\,8\,10\,7\,1\,4\,3\,6\,11\,14\,13\,12\,9\,5$ (or their reverses), each checked to have width $5$.
- c4 (1 pts): Shows that no other numbering of width $5$ exists, by a case analysis of the end vertices (they must be $2$ and $5$) and of the positions of the degree-$6$ vertices $1$ and $11$, or by an exhaustive argument.

Common wrong answers: 2, 4, 8, 3, 12

## References box

The density lower bound for the bandwidth and the general theory of the problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the proof that the bandwidth is $5$, the complete enumeration of the numberings of width $5$ by backtracking (six, listed, with the top of the search tree printed and the reason every dead branch dies), an independent count of six by a dynamic programme over sets of placed vertices, and the structural facts shared by all six numberings. The program is embedded with its output.

## Verify field

Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 5, the complete list of the six numberings of width 5 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six; section 6 embeds the program with its output.

## How to submit

Import the zip as a new question (the figure is new, so this is not a field-by-field revision of task06).

## Screen

Screened 2026-10-16 (figure plus stem only, no code, no web). Opus: correct, 6, after 64 minutes and 112k tokens. It proved the ends must be 2 and 5 by the distance-2 ball count, derived 9 and 12 next to 5, fixed 3 and 8, and split on the one free vertex among positions 4 to 7 to get the three classes. It read 30 edges (a phantom 6-13) and flagged the discrepancy; the answer did not depend on it. Sonnet: no answer, cut off at the 64k output token ceiling. Tally Opus 1/1, Sonnet 0/1.