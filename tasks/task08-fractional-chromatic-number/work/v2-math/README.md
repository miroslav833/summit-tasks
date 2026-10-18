# task08 (revision): fractional chromatic number of a 20-vertex planar 4-regular graph

Revision of Summit item SUM-MVBCQZWW (the 12-vertex version came back too easy: the weaker model solved it twice out of three). The 12-vertex package is kept in work/v1/.

Domain: Mathematics. Subdomain: Graph theory: fractional graph colouring (fractional chromatic number and linear programming duality)

## Question

The figure shows a planar graph $G$ with $20$ vertices, labelled $1$ to $20$, and $40$ edges. Every vertex has degree $4$. An independent set of $G$ is a set of vertices no two of which are joined by an edge. A fractional colouring of $G$ gives each independent set $I$ a weight $x_I \ge 0$ in such a way that, for every vertex $v$, the weights of the independent sets that contain $v$ add up to at least $1$. The weight of the fractional colouring is $\sum_I x_I$, and the fractional chromatic number $\chi_f(G)$ is the smallest weight of a fractional colouring of $G$.

Find $\chi_f(G)$. Give the exact value as a fraction in lowest terms.

## Answer

35/11

## Solution

Step 1: Read the graph off the figure.
The edges are $1\,2$, $1\,3$, $1\,5$, $1\,6$, $2\,4$, $2\,6$, $2\,9$, $3\,4$, $3\,11$, $3\,15$, $4\,17$, $4\,20$, $5\,6$, $5\,7$, $5\,8$, $6\,10$, $7\,8$, $7\,11$, $7\,12$, $8\,12$, $8\,18$, $9\,10$, $9\,16$, $9\,17$, $10\,16$, $10\,18$, $11\,12$, $11\,13$, $12\,13$, $13\,14$, $13\,18$, $14\,15$, $14\,18$, $14\,19$, $15\,19$, $15\,20$, $16\,17$, $16\,19$, $17\,20$, $19\,20$. Every vertex has degree $4$. The triangles are $1\,2\,6$, $1\,5\,6$, $4\,17\,20$, $5\,7\,8$, $7\,8\,12$, $7\,11\,12$, $9\,10\,16$, $9\,16\,17$, $11\,12\,13$, $13\,14\,18$, $14\,15\,19$ and $15\,19\,20$, and there is no $K_4$, so the clique number is $\omega(G) = 3$. The graph has $2455$ non-empty independent sets, $212$ of them maximal (they are listed in the verification notes). The largest have seven vertices, so the independence number is $\alpha(G) = 7$, and the nine independent sets of size $7$ are $\{2,3,5,10,12,14,17\}$, $\{2,3,5,10,12,14,20\}$, $\{2,3,5,10,12,17,19\}$, $\{2,3,5,10,13,17,19\}$, $\{2,3,5,12,14,16,20\}$, $\{2,3,5,12,16,18,20\}$, $\{2,3,5,12,17,18,19\}$, $\{2,3,7,10,13,17,19\}$, $\{2,3,8,10,13,17,19\}$. Each of them contains the vertices $2$ and $3$ and exactly one of $17$ and $20$.

Step 2: The bounds that come first, and why they do not settle the question.
A fractional colouring $x$ satisfies $\sum_{I \ni v} x_I \ge 1$ for every vertex $v$. Summing over the three vertices of a triangle, and using that an independent set contains at most one of them, gives $\sum_I x_I \ge 3 = \omega(G)$. Summing over all twenty vertices gives $\sum_I |I|\, x_I \ge 20$, and since $|I| \le 7$ this is $\sum_I x_I \ge 20/7 = n/\alpha(G)$. For a vertex-transitive graph the bound $n/\alpha$ is exact, but $G$ is only regular: its automorphism group is trivial (vertex $3$ lies in no triangle and vertex $7$ in three, for instance), so the identity $\chi_f(G) = n/\alpha(G)$ is not available. The same summation over the nineteen vertices other than $2$ gives more, because every independent set of $G - 2$ has at most six vertices (the nine sets of size $7$ all contain $2$): $\chi_f(G) \ge \chi_f(G - 2) \ge 19/6$, and the same holds for $G - 3$. From above, the colour classes $\{1,4,7,9,13,15\}$, $\{2,3,5,10,12,14,17\}$, $\{6,8,11,16,20\}$, $\{18,19\}$ form a proper $4$-colouring, which is a fractional colouring of weight $4$. So far $19/6 \le \chi_f(G) \le 4$.

Step 3: Lower bound $35/11$ from a fractional clique.
Let $L = \{2, 3, 4, 17, 20\}$. Give each vertex of $L$ the weight $w_v = 1/11$ and each of the other fifteen vertices the weight $w_v = 2/11$. The total is $5/11 + 30/11 = 35/11$. For an independent set $I$ the weight is $w(I) = \sum_{v \in I} w_v = (2|I| - |I \cap L|)/11$, and the claim is that $w(I) \le 1$ for every independent set. If $|I| \le 5$ then $w(I) \le 10/11$. If $|I| = 6$ then $w(I) \le 1$ exactly when $I$ meets $L$, and every independent set of six vertices does meet $L$: the fifteen vertices outside $L$ induce a subgraph with independence number $5$ (the enumeration in the verification notes lists all $179$ independent sets of size $6$, each containing a vertex of $L$; $72$ of them contain exactly one and have weight exactly $1$). If $|I| = 7$ then $I$ is one of the nine sets of Step 1, each of which contains $2$, $3$ and one of $17$, $20$, so $|I \cap L| = 3$ and $w(I) = (14 - 3)/11 = 1$. Now let $x$ be any fractional colouring. Then
$$\sum_I x_I \;\ge\; \sum_I x_I\, w(I) \;=\; \sum_v w_v \sum_{I \ni v} x_I \;\ge\; \sum_v w_v \;=\; \frac{35}{11}.$$
So $\chi_f(G) \ge 35/11$, which is strictly more than the bound $19/6$ of Step 2.

Step 4: Upper bound $35/11$ from an explicit fractional colouring.
Take the seventeen independent sets $A$ = $\{1,7,10,13,15,17\}$ with weight $\tfrac{5}{11}$; $B$ = $\{1,8,10,13,17,19\}$ with weight $\tfrac{2}{11}$; $C$ = $\{1,8,10,11,14,20\}$ with weight $\tfrac{2}{11}$; $D$ = $\{1,4,9,11,15,18\}$ with weight $\tfrac{2}{11}$; $E$ = $\{2,3,5,12,17,18,19\}$ with weight $\tfrac{2}{11}$; $F$ = $\{2,3,5,12,16,18,20\}$ with weight $\tfrac{2}{11}$; $G$ = $\{2,3,5,12,14,16,20\}$ with weight $\tfrac{4}{11}$; $H$ = $\{2,3,7,10,13,17,19\}$ with weight $\tfrac{2}{11}$; $I$ = $\{2,5,12,15,16,18\}$ with weight $\tfrac{1}{11}$; $J$ = $\{3,6,7,9,18,19\}$ with weight $\tfrac{1}{11}$; $K$ = $\{4,5,9,12,18,19\}$ with weight $\tfrac{2}{11}$; $L$ = $\{6,8,9,11,14,20\}$ with weight $\tfrac{2}{11}$; $M$ = $\{6,8,11,14,16,20\}$ with weight $\tfrac{1}{11}$; $N$ = $\{4,6,8,9,11,19\}$ with weight $\tfrac{2}{11}$; $O$ = $\{4,6,8,9,11,14\}$ with weight $\tfrac{2}{11}$; $P$ = $\{4,6,7,15,16,18\}$ with weight $\tfrac{1}{11}$; $Q$ = $\{4,6,7,13,15,16\}$ with weight $\tfrac{2}{11}$. Each set is independent (no two of its vertices appear together in the edge list of Step 1), and the weights add up to $(5 + 2 + 2 + 2 + 2 + 2 + 4 + 2 + 1 + 1 + 2 + 2 + 1 + 2 + 2 + 1 + 2)/11 = 35/11$. Every vertex is covered with total weight exactly $1$; the sets containing each vertex are $1$: $A, B, C, D$; $2$: $E, F, G, H, I$; $3$: $E, F, G, H, J$; $4$: $D, K, N, O, P, Q$; $5$: $E, F, G, I, K$; $6$: $J, L, M, N, O, P, Q$; $7$: $A, H, J, P, Q$; $8$: $B, C, L, M, N, O$; $9$: $D, J, K, L, N, O$; $10$: $A, B, C, H$; $11$: $C, D, L, M, N, O$; $12$: $E, F, G, I, K$; $13$: $A, B, H, Q$; $14$: $C, G, L, M, O$; $15$: $A, D, I, P, Q$; $16$: $F, G, I, M, P, Q$; $17$: $A, B, E, H$; $18$: $D, E, F, I, J, K, P$; $19$: $B, E, H, J, K, N$; $20$: $C, F, G, L, M$, and in each case the listed weights sum to $11/11$. Multiplying all weights by $11$ turns the list into $35$ independent sets (set $A$ five times, set $G$ four times, the sets with weight $2/11$ twice, the sets with weight $1/11$ once) in which every vertex appears exactly $11$ times: a $35{:}11$-colouring of $G$. Hence $\chi_f(G) \le 35/11$.

Step 5: Conclusion.
Steps 3 and 4 give $\chi_f(G) = 35/11$. None of the bounds of Step 2 is attained: $20/7$, $3$ and $19/6$ are all smaller, and $4$ is larger. A $2$-fold colouring needs $7$ colours (there is no $6{:}2$-colouring, by the search in the verification notes), so stopping at a $2$-fold colouring gives $7/2$; the first $k$-fold colouring whose ratio equals $\chi_f(G)$ is the $35{:}11$-colouring of Step 4.

Answer: $35/11$.

## Rubric

- c1 (5 pts, final answer): Gives $35/11$ (or an exactly equivalent form).
- c2 (2 pts): Exhibits a fractional colouring of $G$ of total weight $35/11$: a list of independent sets with non-negative weights covering every vertex with total at least $1$ (for instance a $35{:}11$-colouring), with weights summing to $35/11$.
- c3 (2 pts): Proves the lower bound $\chi_f(G) \ge 35/11$ by a valid argument, for instance a vertex weighting of total $35/11$ under which every independent set weighs at most $1$ (such as $1/11$ on vertices $2$, $3$, $4$, $17$, $20$ and $2/11$ on the other fifteen vertices), or an exact solution of the linear programme and its dual.
- c4 (1 pts): Determines the independence number $\alpha(G) = 7$ and the chromatic number $\chi(G) = 4$, so that $20/7 \le \chi_f(G) \le 4$.

Common wrong answers: 20/7, 3, 19/6, 4, 7/2

## References box

Fractional colourings, fractional cliques and the linear programming duality between them (every fractional colouring weighs at least as much as every fractional clique, with equality at the optimum): L. Lovasz, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13 (1975), 383-390. The $k$-fold colourings whose ratios $k/d$ attain the fractional chromatic number: S. Stahl, $n$-tuple colorings and associated graphs, Journal of Combinatorial Theory Series B 20 (1976), 185-203. The uploaded file verification_notes.txt enumerates every independent set of the drawn graph (2455 non-empty, 212 maximal, nine of size 7), checks the fractional clique of weight $35/11$ against all of them and the fractional colouring of weight $35/11$ vertex by vertex, solves the linear programme exactly by a rational simplex and numerically by a second solver, computes the best induced-subgraph ratio ($19/6$) over all induced subgraphs, and shows that no $6{:}2$-colouring exists; the program is embedded with its output.

## Verify field

Sections 3 and 4 of verification_notes.txt give the two certificates: the vertex weighting of total 35/11 (1/11 on vertices 2, 3, 4, 17, 20 and 2/11 on the other fifteen vertices) with the weight of every maximal independent set listed and the two facts behind it (every independent set of six vertices meets {2, 3, 4, 17, 20}; each of the nine independent sets of seven vertices contains three of them), and the seventeen weighted independent sets of total 35/11 that cover every vertex exactly once. Section 5 solves the linear programme exactly by a rational simplex and numerically by HiGHS, both giving 35/11. Section 6 computes the best induced-subgraph ratio 19/6 over all induced subgraphs. Section 7 embeds the program verify_key.py with its full output.

## Screen

Revision (20 vertices, key 35/11). Opus 0/1: the run hit the 64k output-token ceiling without an answer (cut-off; its reply began with reading the figure and never reached a final line). Sonnet 0/1 (answered 19/6, 61 min, 135k tokens): read all 40 edges correctly, found the twelve triangles, alpha = 7 and chi = 4, then the vertex-deleted bound 19/6 (weight 0 on vertex 3, 1/6 on the other nineteen) and declared it tight.

Original 12-vertex version (key 13/4), kept in work/v1: Opus 1/1 correct (10.5 min, 64k tokens); Sonnet 0/1 (answered 3 after misreading a crossing). Summit verdict on it: too easy, failed at the weaker-model probe (Sonnet 2/3 correct).

