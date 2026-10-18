# task09 v11: rooted pebbling number of a 14-vertex graph, value only (revision 3 of SUM-MVBG0GO3)

Domain: Mathematics. Subdomain: Graph theory: graph pebbling (rooted pebbling number)

## Question

The figure shows a graph $G$ with $14$ vertices, labelled $1$ to $14$, and $20$ edges, and the vertex with the double circle is called $r$. A configuration of pebbles on $G$ puts a non-negative integer number of pebbles on each vertex. In one "pebbling move" two pebbles are taken off a vertex, then one of them is put on a neighbour of that vertex and the other one is lost. We say that $r$ is reachable from a configuration when there is a sequence of pebbling moves after which $r$ has at least one pebble. The rooted pebbling number $\pi(G, r)$ is the smallest integer $k$ such that $r$ is reachable from each configuration with $k$ pebbles in total.

Find $\pi(G, r)$ and give it as a single integer. Only the value is asked for, and a written proof that every configuration with that many pebbles reaches $r$ is not needed.

## Answer

27

Also accepted: $27$, $\pi(G, r) = 27$, pebbling number 27

## Image necessity

The graph and the target vertex are given only in the figure. The text does not list the twenty edges, and the answer depends on the exact edge set and on which vertex has the double circle, because the failing configurations put their piles on vertices at distance 3 and 4 from the target, and the two edges which join the left part to the rest of the graph decide how many pebbles get lost.

## Solution

Step 1. Graph from the figure.
There are $20$ edges in the figure, $12$, $13$, $25$, $28$, $34$, $36$, $3\,10$, $4\,10$, $4\,11$, $58$, $59$, $68$, $6\,10$, $79$, $7\,12$, $8\,13$, $9\,12$, $10\,11$, $12\,14$ and $13\,14$. Target $r$ is vertex $1$ and it has only two neighbours, $2$ and $3$, where vertex $2$ is also joined to $5$ and $8$ and vertex $3$ is also joined to $4$, $6$ and $10$. Breadth first search from $1$ gives distance $1$ for $2$ and $3$, distance $2$ for $4$, $5$, $6$, $8$ and $10$, distance $3$ for $9$, $11$ and $13$, and distance $4$ for $7$, $12$ and $14$, so the eccentricity of $1$ is $4$. There are two parts of the graph which decide the answer. On the left there is the part $L = \{7, 9, 12, 13, 14\}$, and it is joined to the rest of the graph only by the two edges $5\,9$ and $8\,13$. On the right there is the triangle $4\,10\,11$, where vertex $11$ has degree $2$ and sits at distance $3$ from $1$, and we call this triangle the pocket.

Step 2. Easy lower bounds.
When fifteen pebbles are on vertex $7$ and there are no other pebbles, at most seven pebbles get to distance $3$, then at most three to distance $2$ and one to a neighbour of $1$, so $\pi(G, 1) \ge 2^{4} = 16$. One pebble on each vertex other than $1$ gives $13$ pebbles and no move is possible from it, so $\pi(G, 1) \ge 14$. Both bounds are far from the true value. The computation in Step 4 also shows that a failing configuration with one large pile and single pebbles has at most $22$ pebbles, and a failing configuration with at most two piles has at most $25$ pebbles, for example fifteen on $7$, seven on $11$ and one pebble on each of $12$, $13$ and $14$.

Step 3. A configuration of $26$ pebbles from which $1$ is not reachable.
Take the configuration $C$ with fifteen pebbles on $7$, seven pebbles on $11$, three pebbles on $14$ and one pebble on $13$, which is $26$ pebbles in total. A pebble can be moved onto $1$ only from $2$ or from $3$ when that vertex holds two pebbles, and both start empty, so $1$ is reachable from $C$ only if two pebbles arrive at $2$, or two pebbles arrive at $3$, at some time during the game.

The pocket can not do this alone. With its seven pebbles on $11$ and nothing else on the graph, at most one pebble ever arrives at $3$, because each pebble which comes to $4$ or $10$ costs two pebbles on $11$ and each pebble which goes on to $3$ costs two more, and a pebble which goes back to $11$ also loses half. The left part can not do it alone either. With fifteen on $7$, three on $14$ and one on $13$ and nothing else, at most one pebble ever arrives at $2$, and the edge from $8$ to $6$ is used at most once. Along the direct route $7$, $9$, $5$, $2$ the pile of fifteen gives seven pebbles on $9$, then three on $5$ and then one on $2$, and at each of these vertices one pebble stays behind because the piles are odd, while the small pile of three on $14$ with the single pebble on $13$ gives only one pebble on $8$ or on $12$. The only place where the two parts meet is vertex $6$, which is joined to $8$ on the left side and to $3$ and $10$ on the right side. One pebble from the left on $6$ and one pebble from the pocket on $6$ give one move from $6$ to $3$, and after it the pocket has nothing left for a second pebble on $3$, so in the whole game at most one pebble arrives at $2$ and at most one arrives at $3$.

These facts were checked by computer. Breadth first search from $C$ lists all $187\,805$ configurations which can be reached from $C$ by pebbling moves, none of them has a pebble on $1$, and none has two pebbles on $2$ or on $3$. A dynamic programme over the same configurations gives the largest number of moves along each edge over all move sequences, and it confirms the numbers above, for $C$ and for the pocket and the left part alone. The program and its output are in the reference file. So $\pi(G, 1) \ge 27$.

Step 4. Each configuration of $27$ pebbles reaches $1$.
Adding a pebble to a configuration never makes $1$ unreachable. For $k \ge 0$ let $U_k$ be the set of configurations of $k$ pebbles with no pebble on $1$ from which $1$ is not reachable. Each member of $U_k$ is a member of $U_{k-1}$ with one more pebble, and a candidate is in $U_k$ exactly when no move from it lands on $1$ and each move from it goes into $U_{k-1}$, so the sets can be built one after the other starting from $U_0$. Their sizes are $1, 13, 89, 424, 1564, 4714, 11984, 26227, 50076, 84113, 124960, 165021, 195106, 208549, 203602, 183222, 153277, 119824, 87410, 58994, 36112, 19351, 8710, 3193, 925, 191, 20, 0$ for $k = 0, 1, \dots, 27$. The set $U_{27}$ is empty, so $\pi(G, 1) \le 27$.

The $20$ members of $U_{26}$ all have seven pebbles on $11$ and nineteen pebbles in $L$, and each of them has at least three piles. Besides $C$ there are, for example, thirteen on $7$ with five on $14$ and one on $12$, nine on $7$ with five on $12$ and five on $14$, seven on each of $7$ and $12$ with five on $14$, and fifteen on $14$ with three on $7$ and one on $9$. The recursion was written two times independently, with the same layer sizes, and a direct search over move sequences confirms that each of the $20$ configurations fails and that each configuration made from one of them by adding a pebble reaches $1$. In addition $60\,000$ random configurations of $25$, $26$ and $27$ pebbles get the same verdict from both methods.

Step 5. Answer.
From Step 3 we have $\pi(G, 1) \ge 27$ and from Step 4 we have $\pi(G, 1) \le 27$, so $\pi(G, r) = 27$.

Answer: $27$.

## Rubric

- c1 (5 pts, final answer): Gives $27$ as the final answer.
- c2 (2 pts): Gives a configuration of $26$ pebbles from which $r$ is not reachable, for example fifteen pebbles on $7$, seven on $11$, three on $14$ and one on $13$, and gives a valid reason why $r$ can not be reached from it.
- c3 (2 pts): Explains why the seven pebbles on $11$ and the nineteen pebbles on the left part can not work together: at most one pebble crosses from $8$ to $6$, so neither $2$ nor $3$ ever holds two pebbles.
- c4 (1 pts): States the bounds $\pi(G, r) \ge 2^{4} = 16$ from the eccentricity of $r$ and $\pi(G, r) \ge n = 14$, and says that neither of them is tight.

Common wrong answers: 26, 23, 16, 25, 28, 14

## References box

Graph pebbling was introduced by F. R. K. Chung, Pebbling in hypercubes, SIAM Journal on Discrete Mathematics 2 (1989), 467-472, and a survey is G. Hurlbert, A survey of graph pebbling, Congressus Numerantium 139 (1999), 41-64. The reduction to the first time a neighbour of the target holds two pebbles, and the fact that wasteful move sequences can be left out, come from the No-Cycle Lemma of K. Milans and B. Clark, The complexity of graph pebbling, SIAM Journal on Discrete Mathematics 20 (2006), 769-798. For bounds on graphs of small diameter see T. A. Clarke, R. A. Hochberg and G. H. Hurlbert, Pebbling in diameter two graphs and products of paths, Journal of Graph Theory 25 (1997), 119-128, and B. Bukh, Maximum pebbling number of graphs of diameter three, Journal of Graph Theory 52 (2006), 353-357. In the uploaded file verification_notes.txt there are the two independent exact computations of the rooted pebbling number (layer recursion over unreachable configurations, written two times, and direct search over move sequences for all maximal failing configurations, their extensions and 60,000 random configurations), the list of the 187,805 configurations which can be reached from the twenty-six-pebble configuration of Step 3, the move counts for that configuration and for its two parts alone, and the program with its output.

## Verify field

In verification_notes.txt, sections 1 to 3 have the graph, the trivial bounds and the twenty-six-pebble configuration (fifteen pebbles on 7, seven on 11, three on 14, one on 13, target 1), with the list of the 187,805 configurations reachable from it, none of them with a pebble on 1, and the move counts which show at most one pebble ever arrives at 2 and at most one at 3. Section 4 has the two independent exact computations which show that each configuration of 27 pebbles reaches 1 (layer recursion written two times, and direct search over move sequences for all 20 maximal failing configurations, their one-pebble extensions and 60,000 random configurations), and the pile bounds. Section 5 has the program verify_key.py with its full output.

## Screen

v11 (same figure and key as v10; stem adds one sentence: only the value is asked, no written proof of the upper bound is needed). Reason: Summit returned v10 as unfair, Model A 2/5 correct and 3 attempts out of room twice, because each run tried to prove by hand that all 27-pebble configurations reach r. Screen on this wording, figure plus stem, no code: Opus 2/3 (27 twice with the configuration fifteen on 7, three on 14, one on 13, seven on 11; one run 26 with a 25-pebble configuration), Sonnet 0/1 (26), no cut-offs, 3 to 6 minutes and 55k to 61k tokens per run. Two wordings with a computer-checked fact about the left side in the stem were screened and dropped: with the thresholds for the left side (20 reach r, 19 gather two on 8) Opus 3/3 and Sonnet 1/1 in about 90 s; with only the far-part threshold (20 pebbles on 7, 9, 12, 13, 14 reach r) Opus 3/3 and Sonnet 1/1. Any threshold fact gives the answer by adding seven on 11. Earlier screen of v10 wording: Opus 1/3, Sonnet 0/1.