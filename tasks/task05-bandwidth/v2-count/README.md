# task05 v2: number of optimal numberings (bandwidth) of a 12-vertex graph

Revision of task05 after Summit returned it (Model A 3/3 fast, short lower-bound arguments). Same figure; the question now asks for the number of numberings attaining the bandwidth.

## Question

The figure shows a graph $G$ with $12$ vertices, labelled $1$ to $12$, and $20$ edges. A numbering of $G$ is a bijection $f$ from the vertex set to $\{1, 2, \dots, 12\}$, and its width is $\max |f(u) - f(v)|$ over all edges $uv$ of $G$. The bandwidth of $G$ is the minimum width over all numberings.

How many numberings of $G$ have width equal to the bandwidth of $G$? A numbering and its reverse (the numbering $v \mapsto 13 - f(v)$) are counted as two different numberings. Give a single integer.

## Answer

6 (also accepted: $6$, six)

## Solution

Step 1: Read the graph off the figure.
The edges are $12$, $13$, $14$, $16$, $1\,11$, $26$, $28$, $2\,10$, $34$, $35$, $49$, $4\,10$, $4\,11$, $69$, $58$, $8\,12$, $79$, $9\,12$, $7\,11$ and $10\,11$. The degrees are $5$ (vertices $1$ and $4$), $4$ (vertices $2$, $9$ and $11$), $3$ (vertices $3$, $6$, $8$ and $10$) and $2$ (vertices $5$, $7$ and $12$).

Step 2: The bandwidth is $4$.
Lower bound: if $H$ is a connected subgraph with $k$ vertices and diameter $d$, every numbering stretches some edge of $H$ by at least $\lceil (k-1)/d \rceil$, because the lowest and highest numbered vertices of $H$ differ by at least $k-1$ and are joined inside $H$ by at most $d$ edges. The subgraph induced on $\{1, 2, 3, 4, 6, 9, 10, 11\}$ has eight vertices and diameter $2$ (every two of them are adjacent or have a common neighbour among $1$, $4$, $6$ and $2$), so the width is at least $\lceil 7/2 \rceil = 4$. Upper bound: the numbering $5, 8, 12, 6, 3, 2, 9, 1, 4, 10, 7, 11$ (positions $1$ to $12$) has width $4$.

Step 3: What every numbering of width $4$ must look like.
Write $p(v)$ for the position of $v$. Call $H$ the eight-vertex subgraph of Step 2. Its lowest and highest vertices are at least $7$ apart and joined by a path of at most two edges of stretch at most $4$, so they are exactly $7$ or $8$ apart, and the eight vertices of $H$ fill a window of $8$ or $9$ consecutive positions. The four vertices $5$, $7$, $8$, $12$ outside $H$ therefore occupy the positions outside that window, at most one of them inside it. Vertex $11$ has neighbours $1$, $4$, $7$, $10$; vertex $7$ has neighbours $9$ and $11$; vertex $5$ has neighbours $3$ and $8$; vertex $12$ has neighbours $8$ and $9$; vertex $8$ has neighbours $2$, $5$, $12$. Since $7$, $5$, $12$ and $8$ sit at the ends and each must be within $4$ of its neighbours, $7$ forces $9$ and $11$ to lie within $4$ of an end, which puts $11$ at the end itself on one side (it is in $H$ and its $H$-neighbours $1$, $4$, $10$ must still be reachable), while $5$, $8$, $12$ occupy the other end with $3$ and $9$ just inside. Working through the positions of $1$ and $4$ (adjacent, both of degree $5$, so they sit next to each other in the middle of the window with their ten neighbour slots spread on both sides) leaves exactly three arrangements up to reversal.

Step 4: The complete list.
Reading positions $1$ to $12$:
$$5, 8, 12, 6, 3, 2, 9, 1, 4, 10, 7, 11 \qquad 5, 12, 8, 6, 3, 9, 2, 1, 4, 7, 10, 11 \qquad 8, 5, 12, 6, 2, 3, 9, 1, 10, 4, 7, 11$$
and their three reverses. Each has width $4$ (the eight edges $16$, $1\,11$, $28$, $2\,10$, $34$, $35$, $79$ and $9\,12$ are stretched by exactly $4$ in all six, every other edge by less). That there are no others is the content of Step 3 together with the finite check of the remaining placements; the verification notes carry the full search tree, every dead branch with the reason it dies, and a second, independent count by a dynamic programme over sets of placed vertices. Both give six.

Step 5: Conclusion.
The bandwidth is $4$ and exactly $6$ numberings attain it, $3$ up to reversal. (For comparison, $7\,826$ numberings have width at most $5$.)

Answer: $6$.

## Rubric

- c1 (5 pts, final answer): Gives $6$.
- c2 (2 pts): Establishes that the bandwidth is $4$: a valid lower-bound argument (for instance the eight-vertex induced subgraph of diameter $2$ on $\{1, 2, 3, 4, 6, 9, 10, 11\}$) and an explicit numbering of width $4$.
- c3 (2 pts): Lists the three optimal numberings up to reversal, $5\,8\,12\,6\,3\,2\,9\,1\,4\,10\,7\,11$, $5\,12\,8\,6\,3\,9\,2\,1\,4\,7\,10\,11$ and $8\,5\,12\,6\,2\,3\,9\,1\,10\,4\,7\,11$ (or their reverses), each checked to have width $4$.
- c4 (1 pts): Shows that no other numbering of width $4$ exists, by a case analysis of the positions of the end vertices and of the adjacent degree-$5$ vertices $1$ and $4$, or by an equivalent exhaustive argument.

Common wrong answers: 3, 2, 12, 4

## References box

The density lower bound for the bandwidth and the general theory of the problem: P. Z. Chinn, J. Chvatalova, A. K. Dewdney and N. E. Gibbs, The bandwidth problem for graphs and matrices, a survey, Journal of Graph Theory 6 (1982), 223-254. NP-completeness of bandwidth: C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976), 263-270. The uploaded file verification_notes.txt contains the proof that the bandwidth is $4$, the complete enumeration of the numberings of width $4$ by backtracking (six, listed, with the top of the search tree printed and the reason every dead branch dies), an independent count of six by a dynamic programme over sets of placed vertices, and the structural facts shared by all six numberings; the program is embedded with its output.

## Verify field

Sections 2 to 5 of verification_notes.txt give the proof that the bandwidth is 4, the complete list of the six numberings of width 4 with the top of the search tree and the reason every dead branch dies, an independent count by a dynamic programme, and the structural facts shared by all six; section 6 embeds the program with its output.

## How to submit

Either revise the returned task05 entry field by field (question text, answer, solution, rubric, common wrong answers, references text, reference file) with the texts above, or import the zip as a new question if the platform allows it.

## Screen

(filled in after the screen)