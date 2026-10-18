# task08: number of Hamiltonian cycles of a drawn 28-vertex cubic graph

Mathematics, subdomain: Graph theory: enumeration of Hamiltonian cycles in a cubic graph. Earlier contents of this folder (fractional chromatic number, crack growth, test matrices, covering arrays, M/G/1 queue) are archived under work/.

## Question

The figure shows a simple undirected graph on $28$ vertices, labelled $A$ to $Z$, $a$ and $b$. The edges are the straight segments drawn between the circles. Where two segments cross, the crossing point is not a vertex and the two edges do not meet.

A Hamiltonian cycle is a cycle that passes through every vertex exactly once. Two Hamiltonian cycles count as the same if they use the same set of edges, so the starting vertex and the direction of travel do not matter.

How many Hamiltonian cycles does the graph have? Give a single integer.

## Answer

52

## Solution

Step 1: Read the graph.
The figure has $42$ edges: $AG, AJ, AS, BK, BS, BV, CH, CL, CY, DI, DN, DW, EL, EP, EZ, FS, FX, FZ, GT, Gb, HJ, Ha, IM, Ib, JV, KQ, KU, LR, MO, MX, NT, NV, OQ, OZ, PU, PX, QY, RT, Ra, Ub, WY, Wa$. Every vertex has degree $3$, so the graph is cubic ($28 \cdot 3 / 2 = 42$). It has no triangles and no $4$-cycles (girth $5$), it is not planar and it has no symmetry other than the identity, so the count has to be done by a search.

Step 2: Reduce to one choice per vertex.
A Hamiltonian cycle uses exactly two of the three edges at every vertex, so the unused edges form a perfect matching, and a perfect matching gives a Hamiltonian cycle exactly when the remaining $28$ edges form one cycle rather than several. Two propagation rules drive a hand search: if an edge is left out, the other two edges at both of its ends are used; if two edges at a vertex are used, the third is left out. A branch dies when a vertex keeps fewer than two usable edges or when the used edges close a cycle shorter than $28$.

Step 3: The case split.
Split on the edge left out at $D$ (its neighbours are $I$, $N$, $W$), and inside each case on the edge left out at the next vertex.
- $DI$ left out ($DN$, $DW$ used): split at $N$. Leaving out $NT$ gives $14$ cycles, leaving out $NV$ gives $8$; total $22$.
- $DN$ left out ($DI$, $DW$ used): split at $I$. Leaving out $IM$ gives $7$, leaving out $Ib$ gives $7$; total $14$.
- $DW$ left out ($DI$, $DN$ used): split at $I$. Leaving out $IM$ gives $9$, leaving out $Ib$ gives $7$; total $16$.
Hence the graph has $22 + 14 + 16 = 52$ Hamiltonian cycles. For example $A\,G\,T\,N\,D\,I\,b\,U\,K\,B\,V\,J\,H\,C\,L\,R\,a\,W\,Y\,Q\,O\,M\,X\,P\,E\,Z\,F\,S$ (back to $A$) is one of them; the verification notes list all $52$.

Step 4: Checks.
(i) In a cubic graph every edge lies on an even number of Hamiltonian cycles (Smith's theorem, Thomason 1978). The counts through the edges at $D$ are $52 - 22 = 30$ for $DI$, $52 - 14 = 38$ for $DN$ and $52 - 16 = 36$ for $DW$, all even, and they add up to $104 = 2 \cdot 52$ because each cycle uses two of the three edges. (ii) The count was confirmed by two independent programs: a depth-first search for cycles through $A$, and an enumeration of all $98$ perfect matchings of which exactly $52$ leave a single $28$-cycle.

Step 5: The traps.
Counting each cycle once per direction gives $104$. The hand search is long, and losing cycles in a branch gives $48$, $50$ or $51$; losing two cycles can leave every parity even, so the parity check does not catch it.

Answer: $52$.

## Rubric

- c1 (5 pts, final answer): Gives $52$ as the final answer.
- c2 (1 pts): Reads the graph correctly: $28$ vertices, $42$ edges, every vertex of degree $3$ (an edge list or adjacency list matching the figure).
- c3 (3 pts): Organises the count by which edge is left out at a vertex (equivalently, by perfect matchings whose complement is a single cycle) and reports case totals that add up to $52$, for instance $22$, $14$ and $16$ for the edges $DI$, $DN$, $DW$ left out at $D$.
- c4 (1 pts): Counts each cycle once, not once per direction or starting vertex.

Common wrong answers: 50, 48, 104, 51

## References box

Counting Hamiltonian cycles is #P-complete in general, so no formula is expected and the count is a finite search: L. G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8 (1979), 410-421. The parity check used in the solution (every edge of a cubic graph lies on an even number of Hamiltonian cycles, Smith's theorem): A. G. Thomason, Hamiltonian cycles and uniquely edge colourable graphs, Annals of Discrete Mathematics 3 (1978), 259-268. The uploaded file verification_notes.txt gives the adjacency list, counts the cycles by a depth-first search and by perfect matchings (both 52), gives the case split of the solution, checks the parity of every edge and lists all 52 cycles; the program is embedded with its output.

## Verify field

Section 2 of verification_notes.txt counts the Hamiltonian cycles by a depth-first search from A (52 distinct edge sets). Section 3 counts them a second way, as the perfect matchings whose complement is one 28-cycle (98 perfect matchings, 52 good). Section 4 gives the case split of the solution (DI, DN, DW left out: 22, 14, 16). Section 5 checks that every edge lies on an even number of the cycles. Section 6 lists all 52 cycles. The program verify_key.py is embedded with its output.

## Image necessity

The graph exists only in the figure: the question gives no vertex or edge, and the answer is a property of that particular edge set, so it cannot be found without reading all 42 edges from the drawing.

## Screen

SUMMIT-MATCHING SCREEN (tools/summit_screen.py, Opus 5.5 at --effort max, 5 attempts, figure plus stem, 2026-10-18): 4/5 correct (52 in 10, 15, 16 and 30 minutes, 81k to 246k reported output tokens), 1 cut-off at the 128k output limit after 63 minutes. In band (1 to 4 of 5), one cut-off is below the unfair threshold of two. The max-effort runs counted by cutting the graph into two sides joined by six edges and pairing the crossings, with parity checks per edge.

Cheap subagent screen (figure plus stem, no tools), 2026-10-18. Family history in tasks/task13-hamiltonian-cycle-count/work/screen.md.

This graph (28 vertices, 42 edges, girth 5, not planar, trivial automorphism group, 14 crossings, key 52):
- Opus 0/3: 48 (DW 16, DN 12, DI 20), 50 (16, 12, 22), 51 (16, 14, 21). Every run read all 42 edges correctly and used the right method (edge left out at D, forced-edge propagation); the misses are cycles lost in the branches. 230 to 285 s, no cut-off.
- Sonnet 0/1: 50 (16, 14, 20), 240 s.

Size ladder (same family, non-planar, girth 5, trivial automorphism group):
- 18 vertices, key 21: Opus 2/2, Sonnet 1/1.
- 22 vertices, key 25: Opus 3/3, Sonnet 1/1.
- 24 vertices, key 38: Opus 3/3, Sonnet 1/1.
- 26 vertices, key 40: Opus 2/3 (40, 39, 40), Sonnet 1/1.
- 28 vertices, key 52: Opus 0/3, Sonnet 0/1 (this package).
Planar versions (16 and 20 vertices, fullerenes C26 and C28) were solved by face 2-colouring and symmetry and are not used.

